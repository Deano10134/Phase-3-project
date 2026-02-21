"""Formatting helpers."""


def human_duration(hours: float) -> str:
    """Return a human readable duration for hours."""
    h = int(hours)
    m = int((hours - h) * 60)
    parts = []
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}m")
    return " ".join(parts) if parts else "0m"
