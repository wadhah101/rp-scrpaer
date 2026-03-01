from typing import TypedDict

import polars as pl

rp_schema = {
    "id": pl.UInt32,
    "name": pl.String,
    "muscleGroupId": pl.UInt32,
    "exerciseType": pl.String,
}


hevy_schema = {
    "id": pl.String,
    "title": pl.String,
    "type": pl.String,
    "primary_muscle_group": pl.String,
    "secondary_muscle_groups": pl.List(pl.String),
}


class Subtypes(TypedDict, total=False):
    incline: str
    horizontal: str
    vertical: str
    compound: str
    raise_: str  # 'raise' is a keyword in some contexts, used raise_ or keep as 'raise'
    heavy_axial: str
    non_heavy_axial: str


SubtypeDict = dict[str, str]


class MuscleGroupMapping(TypedDict):
    hevy_primary: list[str]
    name: str
    rp_muscleGroupId: str
    muscle_name: str
    subtypes: SubtypeDict | None
    note: str | None


# The resulting type for your data
MuscleGroupsData = list[MuscleGroupMapping]


muscleGroupMappingSchema = {
    "hevy_primary": pl.List(
        pl.String
    ),  # Guess data of which hevy primary muscle groups map to which rp muscle group
    "rp_muscleGroupId": pl.UInt32,  # join column
    "rp_muscleGroup": pl.String,  # Guessed data
}
