from datetime import UTC, datetime


def clock_now() -> datetime:
    return datetime.now(UTC)
