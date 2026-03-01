import json
import logging
from pprint import pprint  # noqa

import polars as pl

from embeddings.schemas import (
    MuscleGroupMapping,
    hevy_schema,
    muscleGroupMappingSchema,
    rp_schema,
)

logger = logging.getLogger(__name__)

logger.info("Loading rp exercises from data/rp/exercises.json")
rp_exercises: pl.DataFrame = pl.read_json("data/rp/exercises.json", schema=rp_schema)
rp_exercises = rp_exercises.select(pl.all().name.prefix("rp_"))
logger.debug(
    "Loaded %d rp exercises, columns: %s, mem: %.2f MB",
    len(rp_exercises),
    rp_exercises.columns,
    rp_exercises.estimated_size() / 1024 / 1024,
)

logger.info("Loading hevy exercises from data/hevy/exercises.json")
hevy_exercises = pl.read_json("data/hevy/exercises.json", schema=hevy_schema)
hevy_exercises = hevy_exercises.select(pl.all().name.prefix("hevy_"))
logger.debug(
    "Loaded %d hevy exercises, columns: %s, mem: %.2f MB",
    len(hevy_exercises),
    hevy_exercises.columns,
    hevy_exercises.estimated_size() / 1024 / 1024,
)

logger.info("Loading muscle group mappings from data/muscle_group_mapping.json")
mappings = json.load(open("data/muscle_group_mapping.json"))


normalized_mapping: list[MuscleGroupMapping] = [
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

normalized_mapping_df = pl.DataFrame(
    normalized_mapping, schema=muscleGroupMappingSchema
)

logger.debug("Normalized %d muscle group mappings", len(normalized_mapping))

logger.debug("Joining rp exercises with muscle group mappings")
rp_exercises = rp_exercises.join(
    normalized_mapping_df,
    on="rp_muscleGroupId",
    how="right",
)
logger.debug(
    "After join: %d rp exercises, %d columns",
    len(rp_exercises),
    len(rp_exercises.columns),
)

# rp: add rich text representation for embeddings
logger.debug("Building rich text representations for rp exercises")
rp_exercises = rp_exercises.with_columns(
    pl.format(
        "{}, {}, {}",
        pl.col("rp_name"),
        pl.col("rp_exerciseType"),
        pl.col("hevy_primary").list.join(", "),
    )
    .str.to_lowercase()
    .str.strip_chars()
    .str.strip_chars(",")
    .str.replace_all(r"[()]", "")
    .alias("rich_text_representation")
)

# hevy: add rich text representation for embeddings
logger.debug("Building rich text representations for hevy exercises")
hevy_exercises = hevy_exercises.with_columns(
    pl.format(
        "{}, {}, {}",
        pl.col("hevy_title"),
        pl.col("hevy_primary_muscle_group"),
        pl.col("hevy_secondary_muscle_groups").list.join(", "),
    )
    .str.to_lowercase()
    .str.strip_chars()
    .str.strip_chars(",")
    .str.replace_all(r"[()]", "")
    .alias("rich_text_representation")
)

logger.info(
    "DataFrames ready:%d rp exercises (%d cols, %.2f MB), "
    "%d hevy exercises (%d cols, %.2f MB)",
    len(rp_exercises),
    len(rp_exercises.columns),
    rp_exercises.estimated_size() / 1024 / 1024,
    len(hevy_exercises),
    len(hevy_exercises.columns),
    hevy_exercises.estimated_size() / 1024 / 1024,
)
