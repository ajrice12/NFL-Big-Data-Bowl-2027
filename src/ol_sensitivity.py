"""Probe the provisional recovery-distance choice without selecting a winner."""
import json
import pandas as pd
from src.load_data import ROOT,PROCESSED
from src.clean_tracking import KEYS
from src.ol_movement import measure_attempt,MIRROR_NAMES
from src.ol_models import fit_comparison


def main():
    frame=pd.read_parquet(PROCESSED/'combine_tracking_clean.parquet')
    cohort=pd.read_parquet(PROCESSED/'ol/model_cohort.parquet')
    frame=frame.loc[frame.nfl_id.isin(cohort.nfl_id)&frame.drill_name.isin(MIRROR_NAMES)].copy()
    frame.drill_name='PASS_PRO_MIRROR_DRILL'
    reports=[]
    for fraction in [.15,.2,.25]:
        values=[]
        for key,group in frame.groupby(KEYS,observed=True):
            measured,_=measure_attempt(group,fraction)
            values.append({'nfl_id':key[1],'draft_year':key[0],'lre_delay':measured['recovery_delay'],'lre_completion':measured['completion_fraction']})
        replacement=pd.DataFrame(values).groupby(['nfl_id','draft_year'],as_index=False).median()
        data=cohort.drop(columns=['lre_delay','lre_completion']).merge(replacement,on=['nfl_id','draft_year'],validate='one_to_one')
        data=data.loc[data.lre_delay.notna()]
        result,_=fit_comparison(data,data.draft_year.max())
        reports.append({'excursion_fraction':fraction,'eligible_players':len(data),
                        'median_recovery_delay':float(data.lre_delay.median()),
                        'mae_improvement':result['mae_improvement'],
                        'interval':result['mae_improvement_bootstrap_95pct']})
    (ROOT/'outputs/research/ol/sensitivity.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
    print(json.dumps(reports,indent=2))


if __name__=='__main__':main()
