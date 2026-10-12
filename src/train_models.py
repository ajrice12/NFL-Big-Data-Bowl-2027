"""Compare traditional tests with sensor features using held-out draft cohorts."""
import json
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from src.load_data import PROCESSED, ROOT

BASELINE = ["combine_height", "combine_weight", "ten_yd_split", "forty", "vertical",
            "broad_jump", "three_cone", "short_shuttle"]


def main():
    tables = {name: pd.read_parquet(PROCESSED / f"{name}.parquet")
              for name in ["nfl_outcomes", "combine_results", "combine_metrics"]}
    data = tables["nfl_outcomes"]
    for name in ["combine_results", "combine_metrics"]:
        data = data.merge(tables[name], on=["nfl_id", "draft_year"], validate="one_to_one")
    data = data.loc[data.separation_observations.ge(20) & data.mean_separation.notna()].copy()
    data["position_TE"] = data.combine_position.eq("TE").astype(int)
    cohorts = sorted(data.draft_year.unique())
    if len(cohorts) < 2:
        raise SystemExit("Need at least two draft cohorts with 20 separation observations per player.")
    train, test = data.loc[data.draft_year.lt(cohorts[-1])], data.loc[data.draft_year.eq(cohorts[-1])]
    if len(train) < 10 or len(test) < 2:
        raise SystemExit("Insufficient players for a meaningful cohort holdout.")
    baseline = BASELINE + ["position_TE"]
    # Feature availability is selected on training players only.
    sensors = [c for c in data if c.startswith("sensor__") and train[c].notna().mean() >= 0.5]
    if not sensors:
        raise SystemExit("No sensor features meet training availability threshold.")
    results, predictions = {}, test[["nfl_id", "draft_year", "mean_separation"]].copy()
    for name, columns in {"traditional": baseline, "traditional_plus_tracking": baseline + sensors}.items():
        model = make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                              StandardScaler(), Ridge(alpha=10.0))
        model.fit(train[columns], train.mean_separation)
        pred = model.predict(test[columns])
        predictions[f"prediction_{name}"] = pred
        results[name] = {"mae": float(mean_absolute_error(test.mean_separation, pred)),
                         "r2": float(r2_score(test.mean_separation, pred)), "features": columns}
    predictions["prediction_train_mean"] = float(train.mean_separation.mean())
    results["train_mean"] = {"mae": float(mean_absolute_error(test.mean_separation, predictions.prediction_train_mean))}
    rng = np.random.default_rng(2027)
    improvement = (np.abs(test.mean_separation.to_numpy() - predictions.prediction_traditional.to_numpy())
                   - np.abs(test.mean_separation.to_numpy() - predictions.prediction_traditional_plus_tracking.to_numpy()))
    boot = rng.choice(improvement, size=(2000, len(improvement)), replace=True).mean(axis=1)
    report = {"train_players": len(train), "test_players": len(test), "held_out_draft_year": int(cohorts[-1]),
              "models": results, "mae_improvement": float(improvement.mean()),
              "mae_improvement_bootstrap_95pct": np.quantile(boot, [0.025, 0.975]).tolist(),
              "limitations": "Exploratory fixed-alpha model; one cohort holdout; observational outcome; no causal claims. Bootstrap describes test-player uncertainty only."}
    destination = ROOT / "outputs" / "results"
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "model_comparison.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    predictions.to_csv(destination / "held_out_predictions.csv", index=False)
    print(json.dumps({k: v for k, v in report.items() if k != "models"}, indent=2))


if __name__ == "__main__":
    main()
