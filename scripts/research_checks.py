"""Verify outputs, join invariants, cohort ordering, and preserved receiver scores."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from src.load_data import ROOT,PROCESSED


def main():
    messages=[]
    def check(ok,label):
        if not ok:raise AssertionError(label)
        messages.append(label)
    current=json.loads((ROOT/'outputs/results/model_comparison.json').read_text())
    saved=json.loads((ROOT/'outputs/checkpoints/pre-overhaul/results/model_comparison.json').read_text()) if (ROOT/'outputs/checkpoints/pre-overhaul/results/model_comparison.json').exists() else {'mae_improvement':-0.2947473905667486}
    check(np.isclose(current['mae_improvement'],saved['mae_improvement']),'Original receiver MAE comparison reproduced')
    events=pd.read_parquet(PROCESSED/'ol/reversals.parquet')
    check(events.loc[events.completed,'delay'].gt(0).all(),'Completed recoveries have positive observed delay')
    check(events.loc[~events.completed,'delay'].isna().all(),'Incomplete recoveries remain censored')
    obs=pd.read_parquet(PROCESSED/'ol/opportunities.parquet')
    check(not obs.duplicated(['game_id','play_id','nfl_id']).any(),'OL opportunities have unique player-play keys')
    check(obs.season.eq(obs.draft_year).all() & obs.season_type.eq('REG').all(),'OL outcomes are rookie regular season only')
    check(obs.lined_up_position.isin(['C','G','T']).all() & obs.pass_rushers_encountered.ge(1).all(),'Proxy opportunity role and rusher rules hold')
    count=obs.event_by_3.astype(int)+obs.observed_clean_at_3.astype(int)+obs.censored_before_3.astype(int)
    check(count.loc[obs.timing_valid].eq(1).all(),'Every valid timing row belongs to exactly one three-second risk set')
    check(count.loc[~obs.timing_valid].eq(0).all(),'Invalid timing rows excluded from all time-based categories')
    report=json.loads((ROOT/'outputs/research/ol/model_comparison.json').read_text())
    cohort=pd.read_parquet(PROCESSED/'ol/model_cohort.parquet')
    check(cohort.loc[cohort.draft_year.lt(report['held_out_draft_year'])].nfl_id.nunique()==report['train_players'],'Training players precede held-out draft cohort')
    check(cohort.loc[cohort.draft_year.eq(report['held_out_draft_year'])].nfl_id.nunique()==report['test_players'],'Held-out players match report')
    output=ROOT/'outputs/verification';output.mkdir(parents=True,exist_ok=True)
    (output/'research_checks.json').write_text(json.dumps({'passed':len(messages),'checks':messages},indent=2),encoding='utf-8')
    print('\n'.join('PASS '+m for m in messages))


if __name__=='__main__':main()
