"""Build rookie regular-season receiver outcomes with explicit opportunity counts."""
import pandas as pd
from src.load_data import PROCESSED


def build_outcomes(plays, games, players):
    games = games.loc[games.season_type.eq("REG"), ["game_id", "season"]]
    plays = plays.merge(games, on="game_id", validate="many_to_one")
    plays = plays.merge(players[["nfl_id", "draft_year", "nfl_position"]], on="nfl_id", validate="many_to_one")
    plays = plays.loc[plays.season.eq(plays.draft_year) & plays.nfl_position.isin(["WR", "TE"])]
    plays = plays.loc[plays.play_nullified_by_penalty.eq("N")]
    plays = plays.drop_duplicates(["game_id", "play_id", "nfl_id"])
    # Route labels distinguish receiving opportunities; separation is measured
    # at pass-forward and is only summarized when the supplied value exists.
    routes = plays.loc[plays.route_ran.notna() & plays.route_ran.ne("")].copy()
    return routes.groupby(["nfl_id", "draft_year"], observed=True).agg(
        route_plays=("play_id", "size"),
        separation_observations=("separation_at_pass_forward", "count"),
        mean_separation=("separation_at_pass_forward", "mean"),
    ).reset_index()


def main():
    outcomes = build_outcomes(*(pd.read_parquet(PROCESSED / f"{name}.parquet")
                                for name in ["player_play", "games", "players"]))
    outcomes.to_parquet(PROCESSED / "nfl_outcomes.parquet", index=False)
    print(f"Saved {len(outcomes):,} rookie WR/TE outcomes")


if __name__ == "__main__":
    main()
