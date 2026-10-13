"""High-resolution research figures from the verified local export; no remote assets."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.load_data import ROOT
CYAN='#067c87';GRAY='#747b83';AMBER='#b77820'

def save(fig,name):
    dest=ROOT/'outputs/figures';dest.mkdir(parents=True,exist_ok=True)
    fig.savefig(dest/f'{name}.png',dpi=240,bbox_inches='tight')
    fig.savefig(dest/f'{name}.svg',bbox_inches='tight');plt.close(fig)

def main():
    d=json.loads((ROOT/'outputs/presentation/research.json').read_text())
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})
    for receiver in [False,True]:
        rows=d['receiver_predictions'] if receiver else d['ol_predictions'];actual='mean_separation' if receiver else 'pressure_rate';enh='prediction_traditional_plus_tracking' if receiver else 'prediction_tracking'
        fig,ax=plt.subplots(figsize=(6.7,5.1));x=np.array([r[actual] for r in rows]);b=np.array([r['prediction_traditional'] for r in rows]);e=np.array([r[enh] for r in rows]);ax.vlines(x,np.minimum(b,e),np.maximum(b,e),color='#cccccc',lw=1);ax.scatter(x,b,color=GRAY,label='Traditional',s=24);ax.scatter(x,e,color=CYAN,label='Tracking enhanced',s=24);lim=max(x.max(),b.max(),e.max())*1.07;ax.plot([0,lim],[0,lim],color='#aaaaaa',ls='--',label='Identity');ax.set(xlim=(0,lim),ylim=(0,lim),xlabel='Observed mean separation (source units)' if receiver else 'Observed player pressure rate',ylabel='Predicted outcome',title=f'{"Receiver" if receiver else "Offensive-line"} experiment / 2025 temporal holdout (n={len(rows)})');ax.legend(frameon=False);fig.text(.12,-.01,'Separate hypotheses. Player-level errors; observational outcomes.',fontsize=9,color=GRAY);save(fig,'receiver_predictions' if receiver else 'ol_predictions')
    fig,axes=plt.subplots(1,2,figsize=(10.4,4.2));o=d['outcomes'];keys=['pressure_events_by_3','observed_clean_at_3','censored_before_3','timing_inconsistent_or_missing'];axes[0].barh(['Pressure by 3 s','Clean through 3 s','Censored before 3 s','Timing excluded'],[o[k] for k in keys],color=[AMBER,CYAN,GRAY,'#bdbdbd']);axes[0].invert_yaxis();axes[0].set(xlabel='Proxy opportunities',title='Disjoint timing classifications');axes[1].bar(range(4),[x['pressure_rate']*100 for x in d['duration_bins']],color=CYAN);axes[1].set_xticks(range(4),[x['label'] for x in d['duration_bins']],rotation=20,ha='right');axes[1].set(ylabel='Any-pressure rate (%)',title='Conditional on observed dropback duration');fig.suptitle('Short pressure-free dropbacks do not establish three-second resilience');fig.tight_layout();fig.text(.1,-.08,'Descriptive, not causal. Release censoring, role and deployment remain unresolved.',fontsize=9,color=GRAY);save(fig,'nfl_observation_boundary')
    fig,ax=plt.subplots(figsize=(7,4.2));s=d['sensitivity'];y=np.arange(len(s));value=np.array([r['mae_improvement'] for r in s]);lo=np.array([r['interval'][0] for r in s]);hi=np.array([r['interval'][1] for r in s]);ax.errorbar(value*100,y,xerr=np.vstack([value-lo,hi-value])*100,fmt='o',color=CYAN,capsize=4);ax.axvline(0,color=GRAY,ls='--');ax.set_yticks(y,[f"{r['excursion_fraction']:.0%} excursion target" for r in s]);ax.set(xlabel='Traditional MAE − tracking MAE (percentage points)',title='OL metric sensitivity / paired test-player bootstrap 95% intervals');fig.text(.12,-.03,'2025 test n=17. No target was selected using these held-out results.',fontsize=9,color=GRAY);save(fig,'lre_sensitivity')
    t=next(t for t in d['trajectories'] if t['nfl_id']==d['cases'][0]['nfl_id'] and t['reversals']);f=np.array([[np.nan if v is None else v for v in r] for r in t['frames']],dtype=float);fig,axes=plt.subplots(2,1,figsize=(8,5.5),sharex=True);axes[0].plot(f[:,0],f[:,5],color=CYAN,label='Projected displacement');axes[1].plot(f[:,0],f[:,6],color=CYAN,label='Finite-difference velocity');
    for i,r in enumerate(t['reversals']):
        for ax in axes:ax.axvline(r['time'],color=AMBER,ls=':',lw=1)
        axes[0].scatter(r['time'],f[r['index'],5],marker='D',color=AMBER,zorder=3)
        if r['completed']:axes[0].plot([r['time'],f[r['recovery_index'],0]],[f[r['index'],5]]*2,color=AMBER,lw=3);axes[0].annotate(f"R{i+1}: {r['delay']:.2f}s",(r['time'],f[r['index'],5]),xytext=(4,9),textcoords='offset points',fontsize=8)
    axes[0].set(ylabel='Projected position (source units)',title=f"Candidate recovery / {t['name']} / mirror attempt");axes[0].margins(y=.25);axes[1].set(xlabel='Elapsed time (s)',ylabel='Axis velocity (source units/s)');axes[1].axhline(0,color=GRAY,lw=.8);fig.tight_layout();fig.text(.1,-.03,'Dominant-axis proxy; no body orientation. Target = 20% of p90–p10 excursion.',fontsize=9,color=GRAY);save(fig,'lre_worked_example')
    print('Wrote five scientific figures in PNG and SVG.')
if __name__=='__main__':main()
