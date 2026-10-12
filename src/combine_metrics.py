"""Summarize attempts, then use medians across repeated attempts per drill."""
import pandas as pd
from src.clean_tracking import KEYS
from src.load_data import PROCESSED


def build_metrics(frame):
    attempts = frame.groupby(KEYS, observed=True).agg(
        peak_speed=("s", "max"), mean_speed=("s", "mean"),
        accel_p90=("signed_acceleration", lambda x: x.quantile(0.9)),
        brake_p10=("signed_acceleration", lambda x: x.quantile(0.1)),
        frames=("time", "size"), start=("time", "min"), end=("time", "max"),
    ).reset_index()
    attempts["duration"] = (attempts.end - attempts.start).dt.total_seconds()
    attempts = attempts.loc[attempts.frames.ge(10) & attempts.duration.gt(0)]
    traits = ["peak_speed", "mean_speed", "accel_p90", "brake_p10", "duration"]
    metrics = attempts.groupby(["draft_year", "nfl_id", "drill_name"], observed=True)[traits].median()
    wide = metrics.unstack("drill_name")
    wide.columns = [f"sensor__{drill}__{trait}" for trait, drill in wide.columns]
    return attempts, wide.reset_index()


def main():
    attempts, wide = build_metrics(pd.read_parquet(PROCESSED / "combine_tracking_clean.parquet"))
    attempts.to_parquet(PROCESSED / "combine_attempt_metrics.parquet", index=False)
    wide.to_parquet(PROCESSED / "combine_metrics.parquet", index=False)
    print(f"Saved {len(attempts):,} attempts across {len(wide):,} players")


if __name__ == "__main__":
    main()
