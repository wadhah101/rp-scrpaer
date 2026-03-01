import json
import logging

import polars as pl

from embeddings.schemas import (
    MuscleGroupMapping,
    hevy_schema,
    muscleGroupMappingSchema,
    rp_schema,
)

logger = logging.getLogger(__name__)


def load_rp_exercises(path: str) -> pl.DataFrame:
    logger.info("Loading rp exercises from %s", path)
    df = pl.read_json(path, schema=rp_schema)
    df = df.select(pl.all().name.prefix("rp_"))
    logger.debug(
        "Loaded %d rp exercises, columns: %s, mem: %.2f MB",
        len(df),
        df.columns,
        df.estimated_size() / 1024 / 1024,
    )
    return df


def load_hevy_exercises(path: str) -> pl.DataFrame:
    logger.info("Loading hevy exercises from %s", path)
    df = pl.read_json(path, schema=hevy_schema)
    df = df.select(pl.all().name.prefix("hevy_"))
    logger.debug(
        "Loaded %d hevy exercises, columns: %s, mem: %.2f MB",
        len(df),
        df.columns,
        df.estimated_size() / 1024 / 1024,
    )
    return df


def load_muscle_group_mappings(path: str) -> pl.DataFrame:
    logger.info("Loading muscle group mappings from %s", path)
    with open(path) as f:
        mappings = json.load(f)

    normalized: list[MuscleGroupMapping] = [
        {
            "rp_muscleGroupId": k,
            "hevy_primary": (
                v["hevy_primary"]
                if isinstance(v["hevy_primary"], list)
                else [v["hevy_primary"]]
            ),
            "rp_muscleGroup": v["name"],
        }
        for k, v in mappings.items()
    ]

    df = pl.DataFrame(normalized, schema=muscleGroupMappingSchema)
    logger.debug("Normalized %d muscle group mappings", len(normalized))
    return df


def _clean_rich_text(expr: pl.Expr) -> pl.Expr:
    return (
        expr.str.to_lowercase()
        .str.strip_chars()
        .str.strip_chars(",")
        .str.replace_all(r"[()]", "")
    )


def _rp_rich_text(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        _clean_rich_text(
            pl.format(
                "{}, {}, {}",
                pl.col("rp_name"),
                pl.col("rp_exerciseType"),
                pl.col("hevy_primary").list.join(", "),
            )
        ).alias("rich_text_representation")
    )


def _hevy_rich_text(df: pl.DataFrame) -> pl.DataFrame:
    return df.with_columns(
        _clean_rich_text(
            pl.format(
                "{}, {}, {}",
                pl.col("hevy_title"),
                pl.col("hevy_primary_muscle_group"),
                pl.col("hevy_secondary_muscle_groups").list.join(", "),
            )
        ).alias("rich_text_representation")
    )


def prepare_rp_exercises(
    rp_df: pl.DataFrame, mappings_df: pl.DataFrame
) -> pl.DataFrame:
    logger.debug("Joining rp exercises with muscle group mappings")
    df = rp_df.join(mappings_df, on="rp_muscleGroupId", how="right")
    logger.debug(
        "After join: %d rp exercises, %d columns",
        len(df),
        len(df.columns),
    )

    logger.debug("Building rich text representations for rp exercises")
    return _rp_rich_text(df)


def prepare_hevy_exercises(hevy_df: pl.DataFrame) -> pl.DataFrame:
    logger.debug("Building rich text representations for hevy exercises")
    return _hevy_rich_text(hevy_df)
