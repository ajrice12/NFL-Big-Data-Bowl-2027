"""Animate one explicitly selected Combine attempt."""
import argparse
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd
from src.load_data import PROCESSED, ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event-id", required=True)
    parser.add_argument("--nfl-id", type=int, required=True)
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args()
    data = pd.read_parquet(PROCESSED / "combine_tracking_clean.parquet",
                           filters=[("event_id", "=", args.event_id), ("nfl_id", "=", args.nfl_id), ("attempt", "=", args.attempt)])
    data = data.sort_values("time")
    if data.empty or data.drill_name.nunique() != 1:
        raise SystemExit("Selection must contain exactly one drill trajectory.")
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(data.x, data.y, color="0.85")
    point, = ax.plot([], [], "o", color="#0072B2")
    ax.set(xlabel="x (source units)", ylabel="y (source units)", title=str(data.drill_name.iloc[0]))
    ax.set_aspect("equal", adjustable="datalim")
    def update(index):
        point.set_data([data.x.iloc[index]], [data.y.iloc[index]])
        return point,
    animation = FuncAnimation(fig, update, frames=len(data), interval=100)
    destination = ROOT / "outputs" / "animations"
    destination.mkdir(parents=True, exist_ok=True)
    animation.save(destination / f"player_{args.nfl_id}_attempt_{args.attempt}.gif", writer=PillowWriter(fps=10))
    plt.close(fig)


if __name__ == "__main__":
    main()
