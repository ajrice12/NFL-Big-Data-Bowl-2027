"""Exploratory dominant-axis reversal and recovery measurements for OL mirror drills."""
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from src.load_data import PROCESSED, ROOT
from src.clean_tracking import KEYS

MIRROR_NAMES = {'PASS_PRO-MIRROR_DRILL', 'PASS_PRO_MIRROR_DRILL'}


def measure_attempt(frame, fraction=0.2):
    frame = frame.sort_values('time').reset_index(drop=True).copy()
    times = pd.to_datetime(frame.time)
    t = (times - times.iloc[0]).dt.total_seconds().to_numpy(dtype=float)
    xy = frame[['x', 'y']].to_numpy(dtype=float)
    if len(xy) < 10 or not np.isfinite(xy).all():
        raise ValueError('An attempt requires at least ten finite coordinate frames.')
    centered = xy - np.mean(xy, axis=0)
    _, singular, vectors = np.linalg.svd(centered, full_matrices=False)
    axis = vectors[0]
    if axis[np.argmax(np.abs(axis))] < 0:
        axis = -axis
    lateral = centered @ axis
    dt = np.r_[np.nan, np.diff(t)]
    valid = np.isfinite(dt) & (dt >= .05) & (dt <= .15)
    segment = np.cumsum(~valid)
    velocity = np.full(len(t), np.nan)
    velocity[valid] = np.diff(lateral, prepend=lateral[0])[valid] / dt[valid]
    acceleration = np.full(len(t), np.nan)
    speed = frame.s.to_numpy(dtype=float)
    acceleration[valid] = np.diff(speed, prepend=speed[0])[valid] / dt[valid]
    smoothed = pd.Series(velocity).groupby(segment).transform(lambda x: x.rolling(3, center=True, min_periods=2).median()).to_numpy()
    threshold = .1 * np.nanquantile(np.abs(velocity), .9) if np.isfinite(velocity).any() else np.inf
    excursion = float(np.quantile(lateral, .9) - np.quantile(lateral, .1))
    target = fraction * excursion
    reversals = []
    if target > 1e-6:
        for seg in np.unique(segment):
            indices = np.flatnonzero(segment == seg)
            signs = np.sign(smoothed[indices])
            signs[~np.isfinite(smoothed[indices]) | (np.abs(smoothed[indices]) < threshold)] = 0
            runs = []
            start = 0
            for j in range(1, len(indices) + 1):
                if j == len(indices) or signs[j] != signs[start]:
                    if signs[start] != 0 and j - start >= 3:
                        runs.append((int(indices[start]), int(indices[j-1]), int(signs[start])))
                    start = j
            for previous, following in zip(runs, runs[1:]):
                if previous[2] == following[2]:
                    continue
                a, b = previous[1], following[0]
                local = lateral[a:b+1]
                extremum = int(a + (np.argmax(local) if previous[2] > 0 else np.argmin(local)))
                if reversals and reversals[-1]['index'] == extremum:
                    continue
                reversals.append({'index': extremum, 'time': float(t[extremum]), 'direction': following[2], 'segment': int(seg)})
        for j, reversal in enumerate(reversals):
            idx = reversal['index']
            same = np.flatnonzero(segment == reversal['segment'])
            end = int(same[-1])
            if j+1 < len(reversals) and reversals[j+1]['segment'] == reversal['segment']:
                end = reversals[j+1]['index']
            candidates = np.arange(idx+1, end+1)
            completed = candidates[(lateral[candidates] - lateral[idx]) * reversal['direction'] >= target]
            hit = int(completed[0]) if len(completed) else None
            reversal.update(completed=hit is not None, recovery_index=hit,
                            delay=float(t[hit]-t[idx]) if hit is not None else None,
                            observed_until=float(t[end]-t[idx]), target_displacement=target)
    completed = [r['delay'] for r in reversals if r['completed']]
    variance = float(singular[0]**2 / np.sum(singular**2)) if np.sum(singular**2) > 0 else 0.
    summary = {'reversals': len(reversals), 'completed': len(completed),
               'recovery_delay': float(np.median(completed)) if completed else np.nan,
               'completion_fraction': len(completed)/len(reversals) if reversals else np.nan,
               'axis_variance_fraction': variance, 'target_displacement': target,
               'axis_x': float(axis[0]), 'axis_y': float(axis[1]),
               'frames': len(t), 'gaps': int(np.sum(~valid[1:])),
               'duration': float(t[-1]), 'peak_speed': float(np.max(speed))}
    details = {'t': t, 'xy': xy, 's': speed, 'acceleration': acceleration,
               'lateral': lateral, 'lateral_velocity': velocity, 'segment': segment,
               'reversals': reversals}
    return summary, details


def main():
    source = pd.read_parquet(PROCESSED/'combine_tracking_clean.parquet')
    players = pd.read_parquet(PROCESSED/'players.parquet')
    ids = players.loc[players.nfl_position.isin(['C','G','T']), 'nfl_id']
    source = source.loc[source.nfl_id.isin(ids) & source.drill_name.isin(MIRROR_NAMES)].copy()
    source.drill_name = 'PASS_PRO_MIRROR_DRILL'
    summaries, events = [], []
    for key, group in source.groupby(KEYS, observed=True):
        identity = dict(zip(KEYS, key))
        summary, detail = measure_attempt(group)
        summaries.append(identity | summary)
        events.extend(identity | r for r in detail['reversals'])
    attempts = pd.DataFrame(summaries)
    event_frame = pd.DataFrame(events)
    destination = PROCESSED/'ol'
    destination.mkdir(exist_ok=True)
    attempts.to_parquet(destination/'mirror_attempts.parquet', index=False)
    event_frame.to_parquet(destination/'reversals.parquet', index=False)
    # Median attempts prevents players with more frames from dominating.
    features = attempts.groupby(['nfl_id','draft_year'], observed=True).agg(
        lre_delay=('recovery_delay','median'), lre_completion=('completion_fraction','mean'),
        mirror_peak_speed=('peak_speed','median'), mirror_attempts=('frames','size'),
        detected_reversals=('reversals','sum'), completed_reversals=('completed','sum'),
        axis_variance_fraction=('axis_variance_fraction','median')).reset_index()
    features.to_parquet(destination/'movement_features.parquet', index=False)
    repeated = int((features.mirror_attempts > 1).sum())
    agreement = []
    for _, group in event_frame.loc[event_frame.completed].groupby(['nfl_id','draft_year'], observed=True):
        values = group.delay.to_numpy(dtype=float)
        if len(values) >= 4:
            agreement.append([np.median(values[::2]),np.median(values[1::2])])
    correlation = float(spearmanr(np.asarray(agreement)[:,0],np.asarray(agreement)[:,1]).statistic) if len(agreement)>3 else None
    report = {'mirror_players':len(features),'mirror_attempts':len(attempts),'mirror_frames':int(attempts.frames.sum()),
              'detected_reversals':len(event_frame),'completed_reversals':int(event_frame.completed.sum()),
              'players_with_delay':int(features.lre_delay.notna().sum()),'players_with_repeated_attempts':repeated,
              'within_attempt_odd_even_players':len(agreement),'within_attempt_odd_even_spearman':correlation,
              'repeatability_status':'Independent repeated-attempt reliability unavailable' if repeated==0 else 'Repeated attempts available; reliability not yet established',
              'candidate_definition':'Median observed recovery time to 20% of robust dominant-axis excursion; incomplete events retained separately.'}
    out = ROOT/'outputs/research/ol';out.mkdir(parents=True,exist_ok=True)
    (out/'movement_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
