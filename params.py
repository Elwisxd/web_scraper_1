import json
import os

class Params:

    """
    Class for getting values from params.json file.
    """
    @staticmethod
    def get(name):
        """
        Method for getting param from params.json file by key name.
        Parameters:
            name (str) - name of parameter
        Returns:
            (str) - parameter value or empty string
        """
        with open("params.json", "r") as file:
            jsonData = json.load(file)

        if jsonData[name]:
            return jsonData[name]
        return ""
