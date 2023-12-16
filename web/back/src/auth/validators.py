import hashlib
import hmac
import time

from src.auth import TelegramAuth, TelegramDataError, TelegramDataIsOutdated


def validate_telegram_data(telegram_bot_token: str, data: TelegramAuth) -> dict:
    """
    Checking the authorization telegram data according to the information.
    Official telegram doc: https://core.telegram.org/widgets/login

    Example of incoming data for validation:
        https://localhost/login?
        id=245942576&
        first_name=Pavel&
        last_name=Glukhov&
        username=Gluuk&
        photo_url=https%3A%2F%2Ft.me%2Fi%2Fuserpic%2F320%2F0hxupwk8k7ZrvTyRMSEk83gQax0UFTGkhZzN-NPKIAk.jpg&
        auth_date=1688449915&hash=9f1a28d6e929af7e314b634df2a8dbb78460ef409368ac58c809c48dd9a4d367&
        hash=9f1a28d6e929af7e314b634df2a8dbb78460ef409368ac58c809c48dd9a4d367

    :param telegram_bot_token:
    :param data:
    :return:
    """
    data = data.model_dump()
    received_hash = data.pop("hash", None)
    auth_date = data.get("auth_date")

    if _verify_telegram_session_outdate(auth_date):
        raise TelegramDataIsOutdated("Telegram authentication session is expired.")

    generated_hash = _generate_hash(data, telegram_bot_token)

    if generated_hash != received_hash:
        raise TelegramDataError("Request data is incorrect")

    return data


def _verify_telegram_session_outdate(auth_date: str) -> bool:
    seconds_in_day = 60 * 60 * 24
    unix_time_now = time.monotonic()
    unix_time_auth_date = int(auth_date)
    timedelta = unix_time_now - unix_time_auth_date

    if timedelta > seconds_in_day:
        return True
    return False


def _generate_hash(data: dict, token: str) -> str:
    data_check_string = [
        "{}={}".format(k, v) for k, v in data.items() if k != "hash" and v is not None
    ]
    data_check_string = "\n".join(sorted(data_check_string))

    secret_key = hashlib.sha256(token.encode()).digest()
    generated_hash = hmac.new(
        secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()
    return generated_hash
