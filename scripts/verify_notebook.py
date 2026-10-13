"""Execute notebook cells in a fresh Python process; keep execution logs local."""
import json
import time
import traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    notebook=json.loads((ROOT/'notebooks/kaggle_submission.ipynb').read_text(encoding='utf-8'))
    namespace={'__name__':'__main__'};executed=0;start=time.time()
    try:
        for i,cell in enumerate(notebook['cells']):
            if cell['cell_type']=='code':
                source=''.join(cell['source']);print(f'Executing notebook cell {i}',flush=True)
                exec(compile(source,f'notebook-cell-{i}','exec'),namespace)
                executed+=1
        reports=['outputs/results/model_comparison.json','outputs/research/ol/model_comparison.json','outputs/research/ol/movement_report.json','outputs/research/ol/outcome_report.json','outputs/research/ol/sensitivity.json']
        for filename in reports:
            assert json.loads((ROOT/filename).read_text()) == json.loads((namespace['WORK']/filename).read_text()), filename
        report={'matching_analysis_reports':len(reports),'status':'passed','executed_code_cells':executed,'elapsed_seconds':round(time.time()-start,2),'environment':'Local Python; fresh reproduction directory; official five CSVs','kaggle_runtime_verified':False}
    except Exception:
        report={'status':'failed','executed_code_cells':executed,'error':traceback.format_exc()}
        raise
    finally:
        dest=ROOT/'outputs/verification';dest.mkdir(parents=True,exist_ok=True)
        (dest/'notebook-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
