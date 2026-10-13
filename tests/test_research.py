"""Meaningful edge cases for reversal, censoring, and temporal validation."""
import unittest
import numpy as np
import pandas as pd
from src.ol_movement import measure_attempt
from src.ol_outcomes import construct_outcomes
from src.ol_models import fit_comparison
from src.clean_tracking import clean_tracking


class ResearchMethods(unittest.TestCase):
    def track(self,x,t=None):
        t=np.arange(len(x))*.1 if t is None else np.asarray(t)
        return pd.DataFrame({'x':x,'y':np.zeros(len(x)),'s':np.ones(len(x)),
                             'time':pd.Timestamp('2025-01-01')+pd.to_timedelta(t,unit='s')})

    def test_stationary_not_zero_recovery(self):
        summary,_=measure_attempt(self.track(np.zeros(20)))
        self.assertEqual(summary['reversals'],0)
        self.assertTrue(np.isnan(summary['recovery_delay']))

    def test_true_reversal_and_recovery(self):
        frame=self.track(np.r_[np.arange(15)*.1,1.4-np.arange(1,16)*.1])
        summary,details=measure_attempt(frame)
        self.assertEqual(summary['reversals'],1)
        self.assertEqual(summary['completed'],1)
        reversal=details['reversals'][0]
        self.assertEqual(reversal['index'],14)
        self.assertGreater(reversal['delay'],0)
        self.assertLessEqual(reversal['delay'],.5)

    def test_gap_does_not_create_reversal(self):
        x=np.r_[np.arange(15)*.1,1.4-np.arange(1,16)*.1]
        t=np.arange(30)*.1;t[15:]+=2
        summary,_=measure_attempt(self.track(x,t))
        self.assertEqual(summary['gaps'],1)
        self.assertEqual(summary['reversals'],0)

    def test_recovery_invariant_to_translation(self):
        a=self.track(np.r_[np.arange(15)*.1,1.4-np.arange(1,16)*.1])
        b=a.copy();b.x+=250;b.y-=30
        self.assertAlmostEqual(measure_attempt(a)[0]['recovery_delay'],measure_attempt(b)[0]['recovery_delay'])

    def test_censoring_and_missing_times(self):
        plays=pd.DataFrame({'game_id':[1]*5,'play_id':range(5),'nfl_id':[10]*5,
             'play_nullified_by_penalty':['N']*5,'lined_up_position':['T']*5,
             'pressure_allowed':['FALSE','FALSE','TRUE','TRUE','TRUE'],
             'time_to_pressure_allowed':[np.nan,np.nan,2.,np.nan,4.],
             'dropback_duration':[2.,4.,2.5,4.,3.], 'pass_rushers_encountered':[1]*5,'pass_result':['C']*5})
        games=pd.DataFrame({'game_id':[1],'season':[2025],'season_type':['REG']})
        players=pd.DataFrame({'nfl_id':[10],'draft_year':[2025],'nfl_position':['T']})
        obs,_,report=construct_outcomes(plays,games,players)
        self.assertEqual(report['censored_before_3'],1)
        self.assertEqual(report['observed_clean_at_3'],1)
        self.assertEqual(report['pressure_events_by_3'],1)
        self.assertEqual(report['timing_inconsistent_or_missing'],2)
        self.assertFalse(obs.loc[0,'observed_clean_at_3'])

    def test_cleaning_reports_conflicts_and_nonfinite(self):
        frame=self.track([0.,1.,2.,3.])
        frame['entity_type']='PLAYER';frame['nfl_id']=10;frame['draft_year']=2025
        frame['event_id']='event';frame['drill_name']='mirror';frame['attempt']=1
        frame.loc[1,'time']=frame.loc[0,'time']
        frame.loc[3,'x']=np.inf
        clean,report=clean_tracking(frame,return_report=True)
        self.assertEqual(len(clean),2)
        self.assertEqual(report['conflicting_duplicate_timestamps'],1)
        self.assertEqual(report['invalid_or_missing_rows_removed'],1)
        self.assertTrue(np.isfinite(clean.x).all())

    def test_fractional_player_identifier_rejected(self):
        frame=self.track(np.arange(12))
        frame['entity_type']='PLAYER';frame['nfl_id']=10.5;frame['draft_year']=2025
        frame['event_id']='event';frame['drill_name']='mirror';frame['attempt']=1
        with self.assertRaises(ValueError):clean_tracking(frame)
    def test_temporal_holdout_minimum(self):
        self.assertEqual(fit_comparison(pd.DataFrame({'draft_year':[2025]}),2025),(None,None))


if __name__=='__main__':unittest.main()
