import json


class Params:

    @staticmethod
    def get(name):
        with open("params.json", "r") as file:
            jsonData = json.load(file)

        if jsonData[name]:
            return jsonData[name]
        return ""
