import csv
from scrapper import Scrapper
from params import Params
import os


with open("data.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["No", "Name", "Manufacturer", "Price", "Price old"])
    s = Scrapper()
    s.load_from_json(os.path.join(Params.get('folder_path'),Params.get('history_filename')))
    index = 0
    for key, record in s.old_records.items():
        index += 1
        writer.writerow([index, record.get_full_name(), record.get_manufacturer(), record.get_price().replace('.', ','), record.get_price_old().replace('.', ',')])

