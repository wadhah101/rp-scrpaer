from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML()
yaml.width = 4096

DEFAULT_MATCHES_PATH = Path("data/embeddings/llm-matches.yaml")

IMPORT_TAG = "#import-from-rp"
RP_DAY_ID_PATTERN = re.compile(r"rp-day-id:(\d+)")


@dataclass
class ExerciseMatch:
    rp_id: str
    rp_name: str
    hevy_best_match_id: str
    hevy_best_match_name: str


def _load_matches(path: Path) -> list[ExerciseMatch]:
    data = yaml.load(path)
    return [ExerciseMatch(**item) for item in data]
