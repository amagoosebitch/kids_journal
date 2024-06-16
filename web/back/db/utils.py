def _format_time(date_time: str | None) -> str | None:
    if date_time is None:
        return None
    if date_time[-1] == "Z":
        return date_time
    return date_time + "Z"


def _format_date_time(date_time: str | None) -> str | None:
    if date_time is None:
        return "null"
    if len(date_time.split("T")) <= 1 or len(date_time) <= 10:
        date_time = date_time.split("T")[0]
        return f'CAST("{date_time}" as Date)'
    date_time = date_time.split(".")[0]
    if "+" in date_time:
        ind = date_time.find("+")
        date_time = date_time[:ind] + date_time[ind + 6 :]
    if date_time[-1] == "Z":
        return f'CAST("{date_time}" as Datetime)'
    return f'CAST("{date_time}Z" as Datetime)'


def _format_date_time_to_date(date_time: str | None) -> str | None:
    if date_time is None:
        return None
    date_time = date_time.split("T")[0]
    return f'CAST("{date_time}" as Date)'


def _format_unix_time(seconds: int | None) -> int | None:
    if seconds is None:
        return seconds
    return int(str(seconds)[:10])  # Какая-то ydb дичь, оно высирает нули справа
