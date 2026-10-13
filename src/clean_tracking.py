"""Clean Combine trajectories without filling gaps or assuming coordinate units."""
import json
import numpy as np
import pandas as pd
from src.load_data import PROCESSED, ROOT

KEYS = ['draft_year', 'nfl_id', 'event_id', 'drill_name', 'attempt']

def clean_tracking(frame, return_report=False):
    report={'source_rows':len(frame)}
    frame=frame.loc[frame.entity_type.eq('PLAYER')].copy()
    report['player_rows']=len(frame)
    frame['time']=pd.to_datetime(frame.time,errors='coerce')
    before=len(frame)
    frame=frame.dropna(subset=KEYS+['time','x','y','s'])
    finite=np.isfinite(frame[['x','y','s']].to_numpy(dtype=float)).all(axis=1)
    frame=frame.loc[finite & frame.s.ge(0)]
    report['invalid_or_missing_rows_removed']=before-len(frame)
    for key in ['nfl_id','draft_year','attempt']:
        values=frame[key].to_numpy(dtype=float)
        if not np.isfinite(values).all() or not np.equal(values,np.floor(values)).all():
            raise ValueError(f'{key} must contain finite integer-valued identifiers')
    duplicate=frame.duplicated(KEYS+['time'],keep=False)
    if duplicate.any():
        conflicts=frame.loc[duplicate].groupby(KEYS+['time'],observed=True)[['x','y','s']].nunique().gt(1).any(axis=1)
        report['conflicting_duplicate_timestamps']=int(conflicts.sum())
    else:report['conflicting_duplicate_timestamps']=0
    before=len(frame)
    # Retain original first-row policy and report conflicts rather than silently average.
    frame=frame.drop_duplicates(KEYS+['time']).sort_values(KEYS+['time'])
    report['duplicate_rows_removed']=before-len(frame)
    frame['dt']=frame.groupby(KEYS,observed=True).time.diff().dt.total_seconds()
    valid=frame.dt.between(.05,.15)
    frame['signed_acceleration']=(frame.groupby(KEYS,observed=True).s.diff()/frame.dt).where(valid)
    report['clean_frames']=len(frame)
    report['invalid_derivative_intervals']=int((frame.dt.notna()&~valid).sum())
    frame=frame.reset_index(drop=True)
    return (frame,report) if return_report else frame

def main():
    frame,report=clean_tracking(pd.read_parquet(PROCESSED/'combine_tracking.parquet'),return_report=True)
    frame.to_parquet(PROCESSED/'combine_tracking_clean.parquet',index=False)
    destination=ROOT/'outputs/research';destination.mkdir(parents=True,exist_ok=True)
    (destination/'tracking_quality.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
