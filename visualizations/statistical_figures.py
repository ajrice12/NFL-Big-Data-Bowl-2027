"""Plot held-out player errors from the baseline and tracking models."""
import matplotlib.pyplot as plt
import pandas as pd
from src.load_data import ROOT


def main():
    data = pd.read_csv(ROOT / "outputs" / "results" / "held_out_predictions.csv")
    baseline = (data.mean_separation - data.prediction_traditional).abs()
    tracking = (data.mean_separation - data.prediction_traditional_plus_tracking).abs()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(baseline, tracking, color="#0072B2", alpha=0.7)
    limit = max(baseline.max(), tracking.max()) * 1.05
    ax.plot([0, limit], [0, limit], color="0.4", linestyle="--")
    ax.set(xlabel="Traditional model absolute error", ylabel="Tracking model absolute error",
           title="Rookie receiver separation: held-out player errors", xlim=(0, limit), ylim=(0, limit))
    fig.tight_layout()
    destination = ROOT / "outputs" / "figures"
    destination.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination / "held_out_errors.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
