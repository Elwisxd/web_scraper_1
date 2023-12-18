from scrapper import Scrapper
from mail import Email
from params import Params
import os

def main():
    Params.set_base_folder()
    s = Scrapper()
    s.load()
    s.load_from_json(os.path.join(Params.get('folder_path'),Params.get('history_filename')))
    changed, diff_json = s.compare()
    s.save_to_json()
    if changed:
        message = s.compare_text(diff_json)
        e = Email(message.encode('ascii', errors='ignore'))
        e.send_email()
        s.save_history(diff_json)

if __name__ == '__main__':
    main()




