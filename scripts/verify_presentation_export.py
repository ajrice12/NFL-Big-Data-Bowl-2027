"""Verify the compact app export against actual processed frames and model reports."""
import json
import numpy as np
import pandas as pd
from src.load_data import ROOT,PROCESSED
from scripts.build_presentation import safe

def main():
    dest=ROOT/'outputs/presentation'
    briefing=json.loads((dest/'briefing.json').read_text())
    catalog=json.loads((dest/'catalog.json').read_text())
    source=pd.read_parquet(PROCESSED/'combine_tracking_clean.parquet')
    source.loc[source.drill_name.eq('PASS_PRO-MIRROR_DRILL'),'drill_name']='PASS_PRO_MIRROR_DRILL'
    groups={key:g.sort_values('time') for key,g in source.groupby(['nfl_id','event_id','drill_name','attempt'],observed=True)}
    checks=[]
    reports={'ol':'outputs/research/ol/model_comparison.json','receiver':'outputs/results/model_comparison.json',
             'movement':'outputs/research/ol/movement_report.json','outcomes':'outputs/research/ol/outcome_report.json',
             'sensitivity':'outputs/research/ol/sensitivity.json'}
    for key,filename in reports.items():
        assert briefing[key]==safe(json.loads((ROOT/filename).read_text())),key
        checks.append(f'{key} evidence exactly matches rounded source report')
    assert 'trajectories' not in briefing and 'samples' not in briefing
    assert briefing['model_opportunities']==briefing['ol']['train_opportunities']+briefing['ol']['test_opportunities']
    assert len({t['id'] for t in catalog})==len(catalog)
    for meta in catalog:
        t=json.loads((dest/meta['file']).read_text())
        assert t['id']==meta['id'] and t['name']==meta['name'] and t['nfl_id']==meta['nfl_id']
        g=groups[(t['nfl_id'],t['event_id'],t['drill'],t['attempt'])]
        frames=np.asarray(t['frames'],dtype=float)
        assert len(frames)==len(g)==meta['frame_count']
        assert np.allclose(frames[:,1:4],g[['x','y','s']].to_numpy(dtype=float),atol=.00000051,rtol=0)
        times=(g.time-g.time.iloc[0]).dt.total_seconds().to_numpy()
        assert np.allclose(frames[:,0],times,atol=.00000051,rtol=0)
    checks.extend(['No full trajectory or sample bundle in startup briefing','Model opportunity total matches training plus test exposures',
                   'Unique catalog attempt IDs',f'All {len(catalog)} attempts match source name, ID, drill, attempt, timestamp, x, y and speed'])
    report={'status':'passed','checks':checks,'trajectory_files':len(catalog),'briefing_bytes':(dest/'briefing.json').stat().st_size}
    out=ROOT/'outputs/verification/redesign';out.mkdir(parents=True,exist_ok=True)
    (out/'export-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
