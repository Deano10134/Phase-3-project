"""Utility algorithms (placeholders)."""


def simple_priority_sort(tasks):
    """Return tasks sorted by a simple priority attribute if present."""
    try:
        return sorted(tasks, key=lambda t: getattr(t, "priority", 0), reverse=True)
    except Exception:
        return list(tasks)
