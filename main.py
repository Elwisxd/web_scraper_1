from scrapper import Scrapper
from mail import Email
from params import Params

def main():
    s = Scrapper()
    s.load()
    s.load_from_json(Params.get('folder_path')+Params.get('history_filename'))
    changed, message = s.compare_text()
    print(message)
    s.save_to_json()
    if changed:
        e = Email(message.encode('ascii', errors='ignore'))
        e.send_email()


if __name__ == '__main__':
    main()




