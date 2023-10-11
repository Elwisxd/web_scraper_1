from scrapper import Scrapper
from mail import Email
from params import Params

def main():
    s = Scrapper()
    s.load()
    s.load_from_json(Params.get('folder_path')+Params.get('history_filename'))
    message = s.compare()
    s.save_to_json()
    if message:
        e = Email(message)
        e.send_email()


if __name__ == '__main__':
    main()




