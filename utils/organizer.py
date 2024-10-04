import os
import json


class Organizer:
    def __init__(self, path):
        self.path = path
        self.data = {}
        self.organize()
        self.data_saver()

    def organize(self) -> None:
        for folder in os.listdir(self.path):
           for file in os.listdir(f"{self.path}/{folder}"):
                if file.endswith(".json"):
                    info = self.json_file_loader(f"{self.path}/{folder}/{file}")
                    name = self.user_name_getter(info)
                    messages = self.messages_getter(info)
                    self.data.update({name: messages})

    @staticmethod
    def json_file_loader(path) -> dict:
        with open(path, "r") as file:
            return json.load(file)

    @staticmethod
    def user_name_getter(info: dict) -> str:
        name = info.get("participants")[0].get("name")
        return name

    @staticmethod
    def messages_getter(info: dict) -> list:
        messages = info.get("messages")
        return messages

    def data_saver(self) -> None:
        with open("formatted_data.json", "w") as file:
            json.dump(self.data, file, indent=4)
