"""Copy official CSVs and convert to Parquet in bounded-memory batches."""
import argparse
import json
import shutil
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"


def convert_csv(source, destination, chunksize=100_000):
    # Infer numeric fields explicitly; fixed types prevent all-null chunks from
    # changing the Arrow schema midway through large files.
    header = pd.read_csv(source, nrows=0).columns
    string_fields = {
        "time", "event", "entity_type", "event_id", "drill_type", "drill_name",
        "display_name", "combine_position", "nfl_position", "birth_date",
        "college_name", "college_conference", "game_key", "season_type",
        "home_team_abbr", "visitor_team_abbr", "team_abbr", "lined_up_position",
        "play_description", "possession_team", "yardline_side", "game_clock",
        "play_direction", "offense_formation", "receiver_alignment", "pass_result",
        "play_nullified_by_penalty", "team_coverage_man_zone", "team_coverage_type",
        "route_ran", "coverage_assignment", "coverage_assignment_at_snap",
    }
    bool_fields = {
        "in_motion_at_ball_snap", "target", "fumble", "fumble_lost", "pressure_allowed",
        "quick_pressure", "unblocked_pressure", "blitzing", "caused_forced_fumble",
        "recovered_fumble", "tackle_for_loss",
    }
    # Preserve mixed TRUE/FALSE and 0/1 flag encodings as strings.
    types = {c: "string" if c in string_fields | bool_fields else "Float64" for c in header}
    rows = 0
    temporary = destination.with_suffix(".parquet.tmp")
    try:
        writer = None
        try:
            for chunk in pd.read_csv(source, dtype=types, chunksize=chunksize):
                table = pa.Table.from_pandas(chunk, preserve_index=False)
                if writer is None:
                    writer = pq.ParquetWriter(temporary, table.schema, compression="zstd")
                writer.write_table(table)
                rows += len(chunk)
        finally:
            if writer is not None:
                writer.close()
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Folder containing official CSVs; copies into data/raw")
    parser.add_argument("--tables", nargs="+", help="CSV stems to convert; default: all")
    args = parser.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    if args.source:
        for source in args.source.glob("*.csv"):
            target = RAW / source.name
            if source.resolve() != target.resolve() and not target.exists():
                shutil.copy2(source, target)
    files = sorted(RAW.glob("*.csv"))
    if args.tables:
        files = [RAW / f"{name}.csv" for name in args.tables]
    if not files:
        raise SystemExit("No CSVs found. Supply --source or populate data/raw.")
    manifest_path = PROCESSED / "ingestion_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    for source in files:
        rows = convert_csv(source, PROCESSED / f"{source.stem}.parquet")
        manifest[source.name] = {"rows": rows, "source_bytes": source.stat().st_size}
        print(f"{source.name}: {rows:,} rows", flush=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
