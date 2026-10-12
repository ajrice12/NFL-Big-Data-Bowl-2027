"""Fail on duplicate keys, invalid speeds, or contaminated outcome cohorts."""
import pandas as pd
from src.load_data import PROCESSED, ROOT


def main():
    messages = []
    def require(condition, message):
        if not condition:
            raise ValueError(message)
        messages.append(message)
    for table in ["players", "combine_results", "combine_metrics", "nfl_outcomes"]:
        frame = pd.read_parquet(PROCESSED / f"{table}.parquet")
        keys = ["nfl_id"] if table == "players" else ["nfl_id", "draft_year"]
        require(not frame.empty, f"{table}: nonempty")
        require(not frame[keys].isna().any().any(), f"{table}: complete keys")
        require(not frame.duplicated(keys).any(), f"{table}: unique keys")
    tracking = pd.read_parquet(PROCESSED / "combine_tracking_clean.parquet")
    require(tracking.s.ge(0).all(), "tracking: nonnegative speed")
    require(tracking.time.notna().all(), "tracking: valid timestamps")
    outcomes = pd.read_parquet(PROCESSED / "nfl_outcomes.parquet")
    require(outcomes.separation_observations.le(outcomes.route_plays).all(), "outcomes: valid denominators")
    output = ROOT / "outputs" / "results" / "validation.txt"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join("PASS " + m for m in messages) + "\n", encoding="utf-8")
    print(output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
