"""Explicit pressure opportunity and censoring rules, kept separate from receivers."""
import json
import numpy as np
import pandas as pd
from src.load_data import PROCESSED, ROOT


def flag(series):
    return series.astype('string').str.upper().map({'TRUE':1.,'FALSE':0.,'1':1.,'0':0.,'1.0':1.,'0.0':0.})


def construct_outcomes(plays,games,players):
    ol=players.loc[players.nfl_position.isin(['C','G','T']),['nfl_id','draft_year','nfl_position']]
    merged=plays.merge(games[['game_id','season','season_type']],on='game_id',validate='many_to_one').merge(ol,on='nfl_id',validate='many_to_one')
    rookie=merged.loc[merged.season_type.eq('REG') & merged.season.eq(merged.draft_year) & merged.play_nullified_by_penalty.eq('N')].copy()
    if rookie.duplicated(['game_id','play_id','nfl_id']).any():
        raise ValueError('Duplicate OL player-play rows require resolution.')
    rookie['pressure']=flag(rookie.pressure_allowed)
    eligible=(rookie.lined_up_position.isin(['C','G','T']) & rookie.pressure.notna()
              & rookie.dropback_duration.gt(0) & rookie.pass_rushers_encountered.ge(1)
              & rookie.pass_result.notna())
    obs=rookie.loc[eligible].copy()
    event_time=pd.to_numeric(obs.time_to_pressure_allowed,errors='coerce').astype(float)
    obs['timing_valid']=(obs.pressure.eq(0) | (event_time.ge(0) & event_time.le(obs.dropback_duration))).fillna(False)
    obs['exit_time']=np.where(obs.pressure.eq(1),event_time,obs.dropback_duration)
    obs['event_by_3']=obs.timing_valid & obs.pressure.eq(1) & event_time.le(3)
    obs['observed_clean_at_3']=obs.timing_valid & ~obs.event_by_3 & obs.exit_time.ge(3)
    obs['censored_before_3']=obs.timing_valid & ~obs.event_by_3 & obs.exit_time.lt(3)
    def summarize(g):
        long=g.loc[g.dropback_duration.ge(3)]
        return pd.Series({'opportunities':len(g),'pressures':int(g.pressure.sum()),'pressure_rate':g.pressure.mean(),
                          'long_opportunities':len(long),'long_pressures':int(long.pressure.sum()),
                          'long_pressure_rate':long.pressure.mean(),'timing_observations':int(g.timing_valid.sum()),
                          'events_by_3':int(g.event_by_3.sum()),'observed_clean_at_3':int(g.observed_clean_at_3.sum()),
                          'censored_before_3':int(g.censored_before_3.sum()),'mean_dropback_duration':g.dropback_duration.mean(),
                          'mean_rushers':g.pass_rushers_encountered.mean(),
                          'mean_pressure_time':g.loc[g.pressure.eq(1)&g.timing_valid,'exit_time'].mean()})
    summaries=obs.groupby(['nfl_id','draft_year','nfl_position'],observed=True).apply(summarize,include_groups=False).reset_index()
    report={'ol_prospects':len(ol),'rookie_regular_season_player_plays':len(rookie),
            'proxy_protection_opportunities':len(obs),'players_with_opportunities':int(obs.nfl_id.nunique()),
            'pressure_events':int(obs.pressure.sum()),'timing_inconsistent_or_missing':int((~obs.timing_valid).sum()),
            'dropbacks_at_least_3_seconds':int(obs.dropback_duration.ge(3).sum()),
            'censored_before_3':int(obs.censored_before_3.sum()),'observed_clean_at_3':int(obs.observed_clean_at_3.sum()),
            'pressure_events_by_3':int(obs.event_by_3.sum()),
            'survival_status':'Descriptive risk sets only. Release/end-of-dropback may be informative censoring; a validated survival prediction model is deferred.'}
    return obs,summaries,report


def main():
    obs,summaries,report=construct_outcomes(*(pd.read_parquet(PROCESSED/f'{name}.parquet') for name in ['player_play','games','players']))
    dest=PROCESSED/'ol';dest.mkdir(exist_ok=True)
    obs.to_parquet(dest/'opportunities.parquet',index=False)
    summaries.to_parquet(dest/'outcomes.parquet',index=False)
    out=ROOT/'outputs/research/ol';out.mkdir(parents=True,exist_ok=True)
    (out/'outcome_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
