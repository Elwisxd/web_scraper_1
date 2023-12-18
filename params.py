import json
import os

class Params:

    @staticmethod
    def get(name):
        with open("params.json", "r") as file:
            jsonData = json.load(file)

        if jsonData[name]:
            return jsonData[name]
        return ""

    @staticmethod
    def set_base_folder():
        data = ""
        with open('params.json', "r") as file:
            data = json.load(file)

        data['folder_path'] = os.getcwd()
        with open('params.json', "w") as file:
            json.dump(data, file, indent=1)
