"""Player-level temporal holdouts for the exploratory OL pressure-rate hypothesis."""
import json
import numpy as np
import pandas as pd
from scipy.special import expit,logit
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from src.load_data import PROCESSED, ROOT
from src.train_models import BASELINE


def fit_comparison(data,year,seed=2027):
    train=data.loc[data.draft_year.lt(year)].copy();test=data.loc[data.draft_year.eq(year)].copy()
    if len(train)<10 or len(test)<5:return None,None
    base=BASELINE+['role_C','role_T']
    columns={'traditional':base,'tracking':base+['lre_delay','lre_completion']}
    target=logit((train.pressures+.5)/(train.opportunities+1))
    rows=test[['nfl_id','draft_year','nfl_position','opportunities','pressures','pressure_rate','long_opportunities','long_pressure_rate','lre_delay','lre_completion']].copy()
    models={};effects={}
    for name,features in columns.items():
        pipeline=make_pipeline(SimpleImputer(strategy='median',add_indicator=True,keep_empty_features=True),StandardScaler(),Ridge(alpha=10.))
        pipeline.fit(train[features],target)
        prediction=expit(pipeline.predict(test[features]))
        rows['prediction_'+name]=prediction
        n=test.opportunities.to_numpy(dtype=float);events=test.pressures.to_numpy(dtype=float)
        models[name]={'mae':float(np.mean(np.abs(prediction-test.pressure_rate))),
                      'opportunity_brier':float(np.sum(n*prediction**2-2*prediction*events+events)/n.sum()),'features':features}
        effects[name]=dict(zip(features,pipeline[-1].coef_[:len(features)].astype(float).tolist()))
    null=float(train.pressures.sum()/train.opportunities.sum())
    rows['prediction_train_rate']=null
    improvement=(np.abs(rows.prediction_traditional-rows.pressure_rate)-np.abs(rows.prediction_tracking-rows.pressure_rate)).to_numpy(dtype=float)
    rng=np.random.default_rng(seed);boot=rng.choice(improvement,size=(2000,len(improvement))).mean(axis=1)
    report={'experiment':'offensive_line_pressure_rate','held_out_draft_year':int(year),'train_players':len(train),'test_players':len(test),
            'train_opportunities':int(train.opportunities.sum()),'test_opportunities':int(test.opportunities.sum()),
            'models':models,'train_rate_benchmark_mae':float(np.mean(np.abs(null-test.pressure_rate))),
            'mae_improvement':float(improvement.mean()),'mae_improvement_bootstrap_95pct':np.quantile(boot,[.025,.975]).tolist(),
            'standardized_logit_coefficients':effects,'status':'Exploratory temporal holdout; LRE not validated',
            'limitations':['Small player sample. Fixed regularization. Conditional deployment and opportunity selection.',
                           'Bootstrap samples held-out players and does not include model refitting or game clustering.',
                           'Completed-event median can be selective. Lateral axis is a geometric proxy.',
                           'Predicts any-pressure rate, not causal three-second protection or a survival hazard.']}
    return report,rows


def main():
    outcomes=pd.read_parquet(PROCESSED/'ol/outcomes.parquet')
    features=pd.read_parquet(PROCESSED/'ol/movement_features.parquet')
    combine=pd.read_parquet(PROCESSED/'combine_results.parquet')
    data=outcomes.merge(features,on=['nfl_id','draft_year'],validate='one_to_one').merge(combine,on=['nfl_id','draft_year'],validate='one_to_one')
    data=data.loc[data.opportunities.ge(50)&data.lre_delay.notna()&data.detected_reversals.ge(2)].copy()
    data['role_C']=data.nfl_position.eq('C').astype(int);data['role_T']=data.nfl_position.eq('T').astype(int)
    out=ROOT/'outputs/research/ol';out.mkdir(parents=True,exist_ok=True)
    data.to_parquet(PROCESSED/'ol/model_cohort.parquet',index=False)
    reports=[]
    for year in sorted(data.draft_year.unique())[1:]:
        report,rows=fit_comparison(data,year)
        if report:
            reports.append(report);rows.to_csv(out/f'predictions_{int(year)}.csv',index=False)
    if not reports:
        (out/'model_comparison.json').write_text(json.dumps({'status':'Analysis incomplete','reason':'Insufficient eligible temporal cohort sizes','eligible_players':len(data)},indent=2))
        return
    report=reports[-1];report['temporal_splits']=reports[:-1]
    report['eligible_players']=len(data)
    (out/'model_comparison.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['standardized_logit_coefficients','temporal_splits','models']},indent=2))


if __name__=='__main__':main()
