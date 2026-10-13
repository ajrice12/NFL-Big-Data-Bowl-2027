"""Generate a self-contained, output-free Kaggle notebook from maintained modules."""
import hashlib
import json
from pathlib import Path
from src.load_data import ROOT

def main():
    modules=['src/__init__.py','src/load_data.py','src/clean_tracking.py','src/combine_metrics.py','src/nfl_outcomes.py','src/train_models.py','src/validate_results.py','src/ol_movement.py','src/ol_outcomes.py','src/ol_models.py','src/ol_sensitivity.py','scripts/__init__.py','scripts/build_presentation.py','scripts/research_checks.py','visualizations/__init__.py','visualizations/research_figures.py']
    sources={name:(ROOT/name).read_text(encoding='utf-8-sig') for name in modules}
    hashes={name:hashlib.sha256(text.encode()).hexdigest() for name,text in sources.items()}
    cells=[]
    def cell(kind,text):
        item={'cell_type':kind,'metadata':{},'source':text.splitlines(keepends=True)}
        if kind=='code':item.update(execution_count=None,outputs=[])
        cells.append(item)
    cell('markdown','# The 3-Second Problem\n\nA self-contained reproduction of two **separate** exploratory experiments: OL mirror recovery versus rookie pressure rate, and WR/TE movement versus rookie receiving separation. Attach the official NFL Big Data Bowl 2027 dataset. No repository download, Internet access, or raw-data output is required.\n\nThe notebook embeds maintained Python modules, writes them to the working directory, and runs training-only preprocessing with temporal holdouts. Tracking is not a validated scouting signal. Outputs and figures contain local research information: review competition sharing rules before publishing generated artifacts.\n')
    cell('code','from pathlib import Path\nimport os, sys, json, subprocess, hashlib\nIN_KAGGLE = Path("/kaggle/input").exists()\nWORK = Path("/kaggle/working/three_second_research") if IN_KAGGLE else Path.cwd() / "notebook_reproduction"\nWORK.mkdir(parents=True, exist_ok=True)\nprint("Reproduction root:", WORK)\n')
    cell('code','SOURCES = '+repr(sources)+'\nSOURCE_HASHES = '+repr(hashes)+'\nfor name, text in SOURCES.items():\n    assert hashlib.sha256(text.encode()).hexdigest() == SOURCE_HASHES[name]\n    target = WORK / name\n    target.parent.mkdir(parents=True, exist_ok=True)\n    target.write_text(text, encoding="utf-8")\nsys.path.insert(0, str(WORK))\n')
    cell('code','# Locate the official dataset root; fail on ambiguity rather than mix sources.\nif IN_KAGGLE:\n    candidates = [p.parent for p in Path("/kaggle/input").rglob("combine_tracking.csv") if (p.parent / "player_play.csv").exists()]\nelse:\n    candidates = [p for p in [Path.cwd()/"data/raw", Path.cwd().parent/"data/raw"] if (p/"combine_tracking.csv").exists()]\nassert len(candidates) == 1, f"Expected one official dataset root, found {candidates}"\nSOURCE = candidates[0]\n# Only five tables are needed; the 22.7M game-tracking rows are not required.\nrequired = ["players", "games", "combine_results", "combine_tracking", "player_play"]\nfrom src.load_data import convert_csv, PROCESSED\nPROCESSED.mkdir(parents=True, exist_ok=True)\nmanifest = {}\nfor name in required:\n    csv = SOURCE / f"{name}.csv"\n    assert csv.exists(), csv\n    rows = convert_csv(csv, PROCESSED / f"{name}.parquet")\n    manifest[csv.name] = {"rows": rows, "source_bytes": csv.stat().st_size}\n    print(name, rows)\n(PROCESSED/"ingestion_manifest.json").write_text(json.dumps(manifest))\n')
    cell('markdown','## Prespecified pipeline\n\nThe default OL recovery target is 20% of within-attempt p90–p10 projected excursion. Missing recoveries remain censored. Only earlier cohorts train the models. Alternate 15% and 25% targets assess sensitivity and do not select a winner. Short dropbacks do not establish protection at three seconds.\n')
    cell('code','def run(module):\n    result = subprocess.run([sys.executable, "-m", module], cwd=WORK, text=True, capture_output=True)\n    print(result.stdout[-7000:])\n    if result.returncode:\n        raise RuntimeError(result.stderr)\nfor module in ["src.clean_tracking", "src.combine_metrics", "src.nfl_outcomes", "src.validate_results", "src.train_models", "src.ol_movement", "src.ol_outcomes", "src.ol_models", "src.ol_sensitivity"]:\n    print("RUN", module)\n    run(module)\n')
    cell('code','receiver = json.loads((WORK/"outputs/results/model_comparison.json").read_text())\nol = json.loads((WORK/"outputs/research/ol/model_comparison.json").read_text())\nfor label, report in [("WR/TE separation", receiver), ("OL pressure rate", ol)]:\n    print(label, json.dumps(report, indent=2)[:6500])\nassert ol["held_out_draft_year"] == 2025\nassert ol["train_players"] == 37 and ol["test_players"] == 17\nassert abs(receiver["models"]["traditional"]["mae"] - 0.24906361836797772) < 1e-7\nassert abs(ol["models"]["traditional"]["mae"] - 0.023368755233743682) < 1e-7\n# Numeric comparisons can need minor tolerance changes across dependency versions.\n')
    cell('code','import pandas as pd\nobs = pd.read_parquet(WORK/"data/processed/ol/opportunities.parquet")\nclassification = obs.event_by_3.astype(int)+obs.observed_clean_at_3.astype(int)+obs.censored_before_3.astype(int)\nassert classification[obs.timing_valid].eq(1).all()\nassert classification[~obs.timing_valid].eq(0).all()\nassert obs.season.eq(obs.draft_year).all() and obs.season_type.eq("REG").all()\nassert not obs.duplicated(["game_id","play_id","nfl_id"]).any()\nprint("Independent opportunity and timing checks passed.")\n')
    cell('code','# Local export supports scientific plotting; it contains restricted trajectories.\n# Do not include research.json or processed/raw files in a public notebook output.\nrun("scripts.build_presentation")\nrun("visualizations.research_figures")\nfrom IPython.display import display, Image\nfor name in ["ol_predictions", "lre_worked_example", "lre_sensitivity", "nfl_observation_boundary", "receiver_predictions"]:\n    display(Image(filename=str(WORK/"outputs/figures"/f"{name}.png")))\n')
    cell('markdown','## Interpretation\n\nCandidate LRE fails to establish incremental predictive value. The 2025 player-MAE difference is slightly negative and its bootstrap interval crosses zero; the opportunity Brier difference is tiny in the opposite direction. Both OL models lose to the pooled-training-rate benchmark on player MAE. The receiver tracking model performs substantially worse than its traditional baseline.\n\nLimitations include small player cohorts, one mirror attempt per athlete, a geometric lateral proxy, unverified field semantics, conditional deployment, unmodeled scheme/quarterback context, informative release censoring, fixed regularization, and uncertainty conditional on fitted models. These results do not justify ranking prospects.\n')
    cell('code','''# Remove reconstructable research outputs from Kaggle's public output bundle.
# Keep rendered notebook figures and aggregate model reports only.
if IN_KAGGLE:
    import shutil
    for folder in [WORK/"data", WORK/"outputs/presentation"]:
        if folder.exists():
            assert folder.resolve().is_relative_to(WORK.resolve())
            shutil.rmtree(folder)
    for filename in (WORK/"outputs").rglob("predictions_*.csv"):
        filename.unlink()
    receiver_predictions = WORK/"outputs/results/held_out_predictions.csv"
    receiver_predictions.unlink(missing_ok=True)
    print("Removed local trajectory export, processed data, and per-player prediction CSVs.")
''')
    notebook={'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.11'}},'nbformat':4,'nbformat_minor':5}
    for i,c in enumerate(cells):c['id']=f'research-{i:02d}'
    dest=ROOT/'notebooks/kaggle_submission.ipynb';dest.write_text(json.dumps(notebook,indent=1,ensure_ascii=False),encoding='utf-8');print(f'Generated {len(cells)} self-contained notebook cells.')
if __name__=='__main__':main()
