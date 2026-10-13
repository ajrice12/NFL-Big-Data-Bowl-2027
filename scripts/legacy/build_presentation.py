import json
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

root = Path.cwd()
processed = root / 'data/processed'
destination = Path(r'C:\Users\shann_o\.codex\visualizations\2026\10\12\01a1327c-2a89-76b0-8274-7156f4482ccc\nfl-data-presentation.html')
players = pd.read_parquet(processed / 'players.parquet')
attempts = pd.read_parquet(processed / 'combine_attempt_metrics.parquet').merge(
    players[['nfl_id', 'display_name', 'nfl_position']], on='nfl_id', validate='many_to_one')
tracking = pd.read_parquet(processed / 'combine_tracking_clean.parquet')
trajectories = []

def add(frame, label, detail):
    frame = frame.sort_values('time').copy()
    frame['time'] = pd.to_datetime(frame.time)
    elapsed = (frame.time - frame.time.iloc[0]).dt.total_seconds()
    frames = pd.DataFrame({'t': elapsed, 'x': frame.x, 'y': frame.y, 's': frame.s}).dropna()
    if len(frames) < 2:
        return
    trajectories.append({'label': label, 'detail': detail, 'frames': frames.round(3).values.tolist()})

for drill in ['COMEBACK_ROUTE_RIGHT', 'GAUNTLET_DRILL', 'FORTY_YARD_DASH', 'SHORT_SHUTTLE']:
    eligible = attempts.loc[attempts.drill_name.eq(drill) & attempts.nfl_position.isin(['WR','TE'])
                            & attempts.duration.between(2, 25)]
    eligible = eligible.sort_values(['draft_year', 'display_name', 'attempt'], ascending=[False,True,True])
    for row in eligible.drop_duplicates('nfl_id').head(3).itertuples():
        selected = tracking.loc[tracking.nfl_id.eq(row.nfl_id) & tracking.event_id.eq(row.event_id)
                                & tracking.drill_name.eq(row.drill_name) & tracking.attempt.eq(row.attempt)]
        label = f'{row.display_name} ({row.nfl_position}, {int(row.draft_year)}) · {drill.replace("_", " ").title()}'
        detail = f'Combine · attempt {int(row.attempt)} · NFL ID {int(row.nfl_id)} · {len(selected)} recorded frames'
        add(selected, label, detail)

sample = pq.ParquetFile(processed / 'game_tracking_2025.parquet').read_row_group(0).to_pandas()
sample = sample.dropna(subset=['nfl_id', 'x', 'y', 's'])
sizes = sample.groupby(['game_id', 'play_id', 'nfl_id']).size()
chosen = sizes.loc[sizes.between(20,500)].index[0]
frame = sample.loc[sample.game_id.eq(chosen[0]) & sample.play_id.eq(chosen[1]) & sample.nfl_id.eq(chosen[2])]
name = players.loc[players.nfl_id.eq(chosen[2]), 'display_name']
name = str(name.iloc[0]) if len(name) else f'Player {int(chosen[2])}'
add(frame, f'{name} · NFL game tracking (2025 sample)',
    f'NFL game {int(chosen[0])} · play {int(chosen[1])} · single-player sample; no teammates or ball shown')

manifest = json.loads((processed/'ingestion_manifest.json').read_text())
tables = {}
for name in manifest:
    sample = pd.read_csv(root/'data/raw'/name,nrows=5)
    total = len(sample.columns)
    sample = sample.iloc[:,:8]
    tables[name] = {'columns':list(sample.columns),'totalColumns':total,
                    'rows':json.loads(sample.to_json(orient='values'))}
payload = {'trajectories':trajectories,'manifest':manifest,'tables':tables,
           'results':json.loads((root/'outputs/results/model_comparison.json').read_text())}
html = destination.read_text(encoding='utf-8')
html = html.replace('__PRESENTATION_DATA__',json.dumps(payload,allow_nan=False).replace('<','\\u003c'))
assert '__PRESENTATION_DATA__' not in html
assert len(html.encode('utf-8')) < 1_000_000
destination.write_text(html,encoding='utf-8')
print(f'{len(trajectories)} actual trajectories; {sum(len(t["frames"]) for t in trajectories)} frames; {len(tables)} tables; {len(html.encode())} bytes')
