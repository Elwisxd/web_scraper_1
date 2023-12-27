import requests
import json
from bs4 import BeautifulSoup
from record import Record
from params import Params
import os
import datetime


class Scrapper:

    """Class scrapper is class for old and new information comparing"""

    url = Params.get('url')
    new_records = {}
    old_records = {}

    def load(self):
        """
        Loads information from url in new_records list
        """
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div", class_="cat-thumb")

        for result in results:
            r = Record(result, 'html')
            try:
                self.new_records[r.item_id] = r
            except Exception as error:
                print(f'Error with record. Item id = {r.item_id} , {r.full_name} | error : {error}')

    def load_from_file(self):
        """
        Loads information from html file in new_records list
        """
        with open(os.path.join(Params.get('folder_path'), Params.get('test_filename')), encoding="utf8") as file:
            soup = BeautifulSoup(file, "html.parser")
            results = soup.find_all("div", class_="cat-thumb")

            for result in results:
                r = Record(result, 'html')
                try:
                    self.new_records[r.item_id] = r
                except Exception as error:
                    print(f'Error with record. Item id = {r.item_id} , {r.full_name}')
                    print('Exception ', error)

    def load_from_json(self, file_name):
        """
        Loads information from json file in old_records list
        Parameters:
            file_name (str) - name of file containing json formatted information
        """
        f = open(file_name)
        data = json.load(f)
        for d in data.values():
            record = Record(d, "json")
            try:
                self.old_records[record.item_id] = record
            except Exception as error:
                print(f'Error with record. Item id = {record.item_id} , {record.full_name}')
                print('Exception ', error)

    def save_to_json(self):
        """
        Saves information from new_records list to json file
        """
        jsons = {}
        for key, record in self.new_records.items():
            try:
                jsons[key] = record.get_json()
            except Exception as error:
                print(f'Error with record. Item id = {record.item_id} , {record.full_name}')
                print('Exception ', error)
        with open(os.path.join(Params.get('folder_path'),Params.get('history_filename')), "w") as final:
            json.dump(jsons, final, indent=2)

    def print(self, one_line=True):
        """
        Prints all records from new_records list
        Parameters:
            one_line (bool) - if record needs to be displayed in one line
        """
        for id, record in self.new_records.items():
            record.print_info(one_line)

    def print_old(self, one_line=True):
        """
        Prints all records from old_records list
            one_line (bool) - if record needs to be displayed in one line
        """
        for id, record in self.old_records.items():
            record.print_info(one_line)

    def compare(self):
        """
        Compares all differences between old_records list and new_records list.
        Returns:
            changed (bool) - determines if something has changed
            differences (dictionary) - all differences between new and old records
        """
        changed = False
        differences = {
            "messages": [],
            "added": [],
            "discounted": [],
            "restocked": [],
            "sold_out": [],
            "markup": []
        }

        if len(self.old_records) == 0:
            differences["messages"].append('List \'old_records\' empty, nothing to compare')
            return changed, differences
        if len(self.new_records) == 0:
            differences["messages"].append('List \'new_records\'empty, nothing to compare')
            return changed, differences

        new_keys = set(self.new_records.keys())
        old_keys = set(self.old_records.keys())

        added = new_keys.difference(old_keys)

        if len(added) > 0:
            changed = True

        for key in added:
            differences["added"].append(self.new_records[key].get_info_dict())

        for key in new_keys.intersection(old_keys):
            diff_types, difference = Record.compare(self.old_records[key], self.new_records[key])
            if not diff_types:
                continue
            changed = True
            for diff_type in diff_types:
                differences[diff_type].append(difference)

        return changed, differences

    def compare_text(self, diff):
        """
        Method generates string from difference dictionary.
        Parameters:
            diff (dictionary) - difference dictionary produced by 'compare' method.
        Returns:
            (str) - all differences formatted as string
        """
        text = 'News from automodel\n'
        for message in diff["messages"]:
            text += message + "\n"

        text += "==== NEW        (" + str(len(diff["added"])) + ") =====\n"
        text += "==== DISCOUNTED (" + str(len(diff["discounted"])) + ") =====\n"
        text += "==== RESTOCKED  (" + str(len(diff["restocked"])) + ") =====\n"
        text += "==== SOLD OUT   (" + str(len(diff["sold_out"])) + ") =====\n"
        text += "==== MARK UP    (" + str(len(diff["markup"])) + ") =====\n"

        text += "\n\n"

        text += "=========== NEW (" + str(len(diff["added"])) + ") ============\n"
        for added in diff["added"]:
            text += Record.get_added_string_from_dict(added)

        text += "==== DISCOUNTED (" + str(len(diff["discounted"])) + ") ============\n"
        for discounted in diff["discounted"]:
            text += Record.get_changed_string_from_dict(discounted)

        text += "===== RESTOCKED (" + str(len(diff["restocked"])) + ") ============\n"
        for restocked in diff["restocked"]:
            text += Record.get_changed_string_from_dict(restocked)

        text += "====== SOLD OUT (" + str(len(diff["sold_out"])) + ") ============\n"
        for sold_out in diff["sold_out"]:
            text += Record.get_changed_string_from_dict(sold_out)

        text += "======== MARKUP (" + str(len(diff["markup"])) + ") ============\n"
        for markup in diff["markup"]:
            text += Record.get_changed_string_from_dict(markup)

        return text

    def save_history(self, diff_json):
        """
        Saves history to json file.
        Parameters:
            diff_json (dictionary) - difference dictionary produced by 'compare' method.
        Returns:
            (bool) - determines if file saving was successful
        """
        history_folder_path = os.path.join(Params.get('folder_path'), Params.get('history_folder_name'))

        if not os.path.isdir(history_folder_path):
            try:
                os.mkdir(history_folder_path)
            except Exception as e:
                print('Error occurred : '+str(e))

        if not os.path.isdir(history_folder_path) :
            print("Path doesnt exist")
            return False

        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d_%H%M%S") + ".txt"

        with open(os.path.join(history_folder_path, filename), "x") as file:
            json.dump(diff_json, file, indent=2)

        return True
