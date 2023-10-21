import requests
import json
from bs4 import BeautifulSoup
from record import Record
from params import Params


class Scrapper:

    url = Params.get('url')
    new_records = {}
    old_records = {}

    def load(self):
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

        with open(Params.get('test_filename'), encoding="utf8") as file:
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
        jsons = {}
        for key, record in self.new_records.items():
            try:
                jsons[key] = record.get_json()
            except Exception as error:
                print(f'Error with record. Item id = {record.item_id} , {record.full_name}')
                print('Exception ', error)
        with open(Params.get('folder_path')+Params.get('history_filename'), "w") as final:
            json.dump(jsons, final, indent=2)

    def print(self, one_line=True):
        for id, record in self.new_records.items():
            record.print_info(one_line)

    def print_old(self, one_line=True):
        for id, record in self.old_records.items():
            record.print_info(one_line)

    def compare(self): #Returns array with all differences
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

    def compare_text(self):

        changed, diff = self.compare()
        text = 'News from automodel\n'
        for message in diff["messages"]:
            text += message + "\n"


        if not changed:
            return changed, text

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

        return changed, text
