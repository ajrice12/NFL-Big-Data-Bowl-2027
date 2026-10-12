"""Compare named players within a selected drill."""
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from src.load_data import PROCESSED, ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drill", required=True)
    parser.add_argument("--players", nargs="+", type=int, required=True)
    args = parser.parse_args()
    data = pd.read_parquet(PROCESSED / "combine_attempt_metrics.parquet")
    data = data.loc[data.drill_name.eq(args.drill) & data.nfl_id.isin(args.players)]
    if data.empty:
        raise SystemExit("No matching attempts.")
    data = data.groupby("nfl_id", as_index=False).peak_speed.median()
    names = pd.read_parquet(PROCESSED / "players.parquet")[["nfl_id", "display_name"]]
    data = data.merge(names, validate="one_to_one").sort_values("peak_speed")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(data.display_name, data.peak_speed, color="#0072B2")
    ax.set(xlabel="Median attempt peak speed (source units)", title=args.drill)
    fig.tight_layout()
    destination = ROOT / "outputs" / "figures"
    destination.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination / "player_comparison.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
