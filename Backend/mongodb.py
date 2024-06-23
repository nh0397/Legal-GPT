from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from typing import Union

class MongoDB:

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def connect(self) -> Union[MongoClient, None]:
        if not self.password:
            print("Please set env variable for password!")
            return

        escaped_username = quote_plus(self.username)
        escaped_password = quote_plus(self.password)

        uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.5hufumz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        client = MongoClient(uri, server_api=ServerApi("1"))

        try:
            client.admin.command("ping")
            print("Successfully connected to MongoDB!")
            return client
        except Exception as e:
            print(e)

        return None
