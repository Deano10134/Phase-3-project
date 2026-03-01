"""General helper utilities for the package."""
from datetime import datetime


def iso(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.isoformat()

