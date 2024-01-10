def _format_time(date_time: str | None) -> str | None:
    if date_time is None:
        return None
    if date_time[-1] == "Z":
        return date_time
    return date_time + "Z"


def _format_unix_time(seconds: int | None) -> int | None:
    if seconds is None:
        return seconds
    return int(str(seconds)[:10])  # Какая-то ydb дичь, оно высирает нули справа
