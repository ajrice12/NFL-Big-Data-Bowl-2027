"""Export local-only research evidence for the modular presentation. Never deploy this export."""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from src.load_data import ROOT,PROCESSED
from src.clean_tracking import KEYS
from src.ol_movement import measure_attempt,MIRROR_NAMES


def safe(value):
    if isinstance(value,dict):return {str(k):safe(v) for k,v in value.items()}
    if isinstance(value,(list,tuple,np.ndarray)):return [safe(v) for v in value]
    if isinstance(value,(np.integer,)):return int(value)
    if isinstance(value,(float,np.floating)):return round(float(value),6) if np.isfinite(value) else None
    if value is pd.NA or value is pd.NaT:return None
    if isinstance(value,(np.bool_,)):return bool(value)
    return value


def main():
    players=pd.read_parquet(PROCESSED/'players.parquet')
    cohort=pd.read_parquet(PROCESSED/'ol/model_cohort.parquet').merge(players[['nfl_id','display_name']],on='nfl_id',validate='one_to_one')
    position=cohort.nfl_position.value_counts().index[0]
    candidates=cohort.loc[cohort.nfl_position.eq(position)].sort_values('nfl_id')
    cases=[];selected=set()
    for percentile in [.25,.5,.75]:
        target=candidates.lre_delay.quantile(percentile)
        choice=candidates.loc[~candidates.nfl_id.isin(selected)].assign(distance=lambda d:(d.lre_delay-target).abs()).sort_values(['distance','nfl_id']).iloc[0]
        selected.add(choice.nfl_id)
        row=choice[['nfl_id','display_name','nfl_position','draft_year','lre_delay','lre_completion','opportunities','pressure_rate','long_opportunities','long_pressure_rate']].to_dict()
        row['selection_percentile']=percentile;cases.append(row)
    out=ROOT/'outputs/research/ol'
    (out/'case_selection.json').write_text(json.dumps(safe({'procedure':'Most common eligible OL position; nearest 25th/50th/75th recovery-delay quantile; ties by NFL ID; outcomes not used.','position':position,'cases':cases}),indent=2))
    source=pd.read_parquet(PROCESSED/'combine_tracking_clean.parquet')
    ol=players.loc[players.nfl_position.isin(['C','G','T'])]
    drills=MIRROR_NAMES|{'PASS_RUSH_DROP','FIVE_YARD_WAVE_DRILL_SLIDE_AND_SHUFFLE'}
    source=source.loc[source.nfl_id.isin(ol.nfl_id)&source.drill_name.isin(drills)].copy()
    source.loc[source.drill_name.isin(MIRROR_NAMES),'drill_name']='PASS_PRO_MIRROR_DRILL'
    metadata=players.set_index('nfl_id').to_dict(orient='index')
    trajectories=[];worked=[]
    for key,group in source.groupby(KEYS,observed=True):
        group=group.sort_values('time')
        summary,detail=measure_attempt(group)
        player=metadata[key[1]]
        record={'id':f'{int(key[1])}-{key[2]}-{int(key[4])}','nfl_id':int(key[1]),'year':int(key[0]),
                'name':player['display_name'],'position':player['nfl_position'],'drill':key[3],'attempt':int(key[4]),
                'event_id':key[2],'summary':summary,
                'frames':np.column_stack([detail['t'],detail['xy'],detail['s'],detail['acceleration'],detail['lateral'],detail['lateral_velocity'],detail['segment']]),
                'reversals':detail['reversals'] if key[3]=='PASS_PRO_MIRROR_DRILL' else []}
        trajectories.append(record)
        if key[1] in selected and key[3]=='PASS_PRO_MIRROR_DRILL':
            variants=[]
            for fraction in [.15,.2,.25]:
                measured,variant=measure_attempt(group,fraction)
                variants.append({'fraction':fraction,'summary':measured,'reversals':variant['reversals']})
            worked.append({'nfl_id':int(key[1]),'variants':variants})
    # Stable order puts documented case-study athletes first, then player ID.
    trajectories.sort(key=lambda t:(t['nfl_id'] not in selected,t['nfl_id'],t['drill'],t['attempt']))
    manifest=json.loads((PROCESSED/'ingestion_manifest.json').read_text())
    samples={}
    for name in manifest:
        raw=ROOT/'data/raw'/name
        sample=pd.read_csv(raw,nrows=5) if raw.exists() else next(pq.ParquetFile(PROCESSED/(Path(name).stem+'.parquet')).iter_batches(batch_size=5)).to_pandas()
        cols=list(sample.columns[:8])
        if 'tracking' in name:
            cols=[c for c in ['nfl_id','time','drill_name','play_id','x','y','s','a'] if c in sample.columns]
        samples[name]={'columns':cols,'rows':json.loads(sample[cols].to_json(orient='values')),'column_count':len(sample.columns)}
    ol_report=json.loads((out/'model_comparison.json').read_text())
    prediction_file=out/f'predictions_{ol_report["held_out_draft_year"]}.csv'
    predictions=pd.read_csv(prediction_file).merge(players[['nfl_id','display_name']],on='nfl_id').to_dict(orient='records')
    receiver_predictions=pd.read_csv(ROOT/'outputs/results/held_out_predictions.csv').merge(players[['nfl_id','display_name']],on='nfl_id').to_dict(orient='records')
    obs=pd.read_parquet(PROCESSED/'ol/opportunities.parquet')
    duration_bins=[]
    for left,right,label in [(0,2,'Under 2 s'),(2,3,'2–3 s'),(3,4,'3–4 s'),(4,100,'4 s or longer')]:
        g=obs.loc[obs.dropback_duration.ge(left)&obs.dropback_duration.lt(right)]
        duration_bins.append({'label':label,'opportunities':len(g),'pressure_rate':float(g.pressure.mean())})
    files=[out/'model_comparison.json',ROOT/'outputs/results/model_comparison.json',out/'movement_report.json',out/'outcome_report.json']
    payload={'schema_version':1,'local_only':True,'raw_data_warning':'Contains restricted local trajectory examples. Do not commit or deploy.',
             'manifest':manifest,'counts':{'prospects':len(players),'combine_attempts':len(pd.read_parquet(PROCESSED/'combine_attempt_metrics.parquet')),
             'combine_clean_frames':len(pd.read_parquet(PROCESSED/'combine_tracking_clean.parquet'))},
             'ol':ol_report,'receiver':json.loads((ROOT/'outputs/results/model_comparison.json').read_text()),
             'movement':json.loads((out/'movement_report.json').read_text()),'outcomes':json.loads((out/'outcome_report.json').read_text()),
             'sensitivity':json.loads((out/'sensitivity.json').read_text()),'cases':cases,'worked_examples':worked,
             'trajectories':trajectories,'samples':samples,'ol_predictions':predictions,'receiver_predictions':receiver_predictions,
             'duration_bins':duration_bins,
             'provenance':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
    destination=ROOT/'outputs/presentation';destination.mkdir(parents=True,exist_ok=True)
    (destination/'research.json').write_text(json.dumps(safe(payload),separators=(',',':'),allow_nan=False),encoding='utf-8')
    # Compact browser entry point: frames are fetched only for selected attempts.
    outcomes=pd.read_parquet(PROCESSED/'ol/outcomes.parquet').set_index('nfl_id').to_dict(orient='index')
    attempts_dir=destination/'attempts';attempts_dir.mkdir(exist_ok=True)
    catalog=[]
    for trajectory in trajectories:
        filename=hashlib.sha256(trajectory['id'].encode()).hexdigest()[:20]+'.json'
        trajectory['nfl']=outcomes.get(trajectory['nfl_id'])
        (attempts_dir/filename).write_text(json.dumps(safe(trajectory),separators=(',',':'),allow_nan=False),encoding='utf-8')
        item={k:v for k,v in trajectory.items() if k not in ['frames','reversals']}
        item['file']='attempts/'+filename;item['frame_count']=len(trajectory['frames'])
        catalog.append(item)
    briefing={k:v for k,v in payload.items() if k not in ['trajectories','samples','worked_examples']}
    briefing['schema_version']=2
    briefing['featured_attempts']=[next(t for t in catalog if t['nfl_id']==c['nfl_id'] and t['drill']=='PASS_PRO_MIRROR_DRILL') for c in cases]
    briefing['model_opportunities']=ol_report['train_opportunities']+ol_report['test_opportunities']
    for filename,value in [('briefing.json',briefing),('catalog.json',catalog),('appendix.json',{'samples':samples,'worked_examples':worked})]:
        (destination/filename).write_text(json.dumps(safe(value),separators=(',',':'),allow_nan=False),encoding='utf-8')
    print(f'Exported {len(trajectories)} local attempts; compact briefing plus on-demand trajectory files.')


if __name__=='__main__':main()
