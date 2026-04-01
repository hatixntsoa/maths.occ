"""
Persistent storage layer – reads/writes data.json.

Schema:
{
    "hand":    [ <card>, ... ],          # current 12-card hand on table
    "deck":    [ <card>, ... ],          # remaining undealt cards
    "score":   int,                      # sets found this session
    "history": [ { "cards": [...], "timestamp": "..." }, ... ]
}
"""

import json
import os
from datetime import datetime, timezone

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data.json")


def _default_state() -> dict:
    return {"hand": [], "deck": [], "score": 0, "history": []}


def load(path: str = DEFAULT_PATH) -> dict:
    path = os.path.abspath(path)
    if not os.path.exists(path):
        return _default_state()
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        # back-fill missing keys
        for k, v in _default_state().items():
            data.setdefault(k, v)
        return data
    except (json.JSONDecodeError, OSError):
        return _default_state()


def save(state: dict, path: str = DEFAULT_PATH) -> None:
    path = os.path.abspath(path)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2)


def record_set(state: dict, cards: list[dict]) -> dict:
    """Append a found SET to history and increment score."""
    state["score"] = state.get("score", 0) + 1
    state.setdefault("history", []).append({
        "cards": cards,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    return state
