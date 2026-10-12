"""Clean Combine trajectories without filling gaps or assuming coordinate units."""
import pandas as pd
from src.load_data import PROCESSED

KEYS = ["draft_year", "nfl_id", "event_id", "drill_name", "attempt"]


def clean_tracking(frame):
    frame = frame.loc[frame.entity_type.eq("PLAYER")].copy()
    frame["time"] = pd.to_datetime(frame.time, errors="coerce")
    frame = frame.dropna(subset=KEYS + ["time", "x", "y", "s"])
    frame = frame.loc[frame.s.ge(0)].drop_duplicates(KEYS + ["time"])
    frame = frame.sort_values(KEYS + ["time"])
    frame["dt"] = frame.groupby(KEYS, observed=True).time.diff().dt.total_seconds()
    # Signed acceleration from speed avoids interpreting vendor a as signed.
    valid = frame.dt.between(0.05, 0.15)
    frame["signed_acceleration"] = (
        frame.groupby(KEYS, observed=True).s.diff() / frame.dt
    ).where(valid)
    return frame.reset_index(drop=True)


def main():
    frame = clean_tracking(pd.read_parquet(PROCESSED / "combine_tracking.parquet"))
    frame.to_parquet(PROCESSED / "combine_tracking_clean.parquet", index=False)
    print(f"Saved {len(frame):,} cleaned PLAYER frames")


if __name__ == "__main__":
    main()
