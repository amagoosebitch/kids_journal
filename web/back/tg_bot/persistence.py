import pickle
from io import BytesIO

import boto3
from botocore.exceptions import ClientError
from telegram.ext import PicklePersistence
from telegram.ext._picklepersistence import _BotPickler, _BotUnpickler

session = boto3.session.Session()
s3 = session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")


class S3PicklePersistence(PicklePersistence):
    def _dump_singlefile(self) -> None:
        data = {
            "conversations": self.conversations,
            "user_data": self.user_data,
            "chat_data": self.chat_data,
            "bot_data": self.bot_data,
            "callback_data": self.callback_data,
        }
        print(f"saving state {data}")
        self._byte_file = BytesIO()
        _BotPickler(self.bot, self._byte_file, protocol=pickle.HIGHEST_PROTOCOL).dump(
            data
        )

    def _load_singlefile(self) -> None:
        try:
            get_obj_response = s3.get_object(
                Bucket="dobry-mir-tg-bot-b1gf54qrjkrq75uriq7l", Key="persistence"
            )
            data = _BotUnpickler(
                self.bot, BytesIO(get_obj_response["Body"].read())
            ).load()
            print(f'loading state {data}')
            self.user_data = data["user_data"]
            self.chat_data = data["chat_data"]
            # For backwards compatibility with files not containing bot data
            self.bot_data = data.get("bot_data", self.context_types.bot_data())
            self.callback_data = data.get("callback_data", {})
            self.conversations = data["conversations"]
        except (ClientError, KeyError, ConnectionRefusedError) as e:
            print(e)
            print("error occured, init with empty fields")
            self.conversations = {}
            self.user_data = {}
            self.chat_data = {}
            self.bot_data = self.context_types.bot_data()
            self.callback_data = None

    async def flush(self) -> None:
        await super().flush()

        self._byte_file.seek(0)
        s3.put_object(
            Bucket="dobry-mir-tg-bot-b1gf54qrjkrq75uriq7l",
            Key="persistence",
            Body=self._byte_file,
        )
