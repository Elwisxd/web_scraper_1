

class Record:

    # raw html
    # item id
    # full name
    # price
    # old_price
    # manufacturer

    def __init__(self, data, data_format):
        self.item_id = ''
        self.full_name = ''
        self.price = ''
        self.price_old = ''
        self.manufacturer = ''
        self.item_link = ''

        if data_format == 'html':
            self.load_from_html(data)
        elif data_format == 'json':
            self.load_from_json(data)

    def get_item_id(self):
        if self.item_id:
            return self.item_id
        return ''

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return ''

    def get_price(self):
        if self.price:
            return self.price
        return ''

    def get_price_old(self):
        if self.price_old:
            return self.price_old
        return ''

    def get_item_link(self):
        if self.item_link:
            return self.item_link
        return ''

    def get_manufacturer(self):
        if self.manufacturer:
            return self.manufacturer
        return ''

    def load_from_html(self, html):
        self.item_id = html.get("data-cat-item-id")
        self.full_name = html.find("div", class_="cat-thumb-title")
        self.price = html.find("span", class_="moze-price")
        self.price_old = html.find("s", class_="moze-secondary")
        self.item_link = html.find("a").get("href")
        self.manufacturer = ''

        if self.full_name:
            self.full_name = self.full_name.get_text().strip()

        if self.price:
            self.price = self.price.get_text().strip()
            if self.price[1:].isnumeric():
                self.price = self.price[1:]

        if self.price_old:
            self.price_old = self.price_old.get_text().strip()
            if self.price_old[1:].isnumeric():
                self.price_old = self.price_old[1:]

        if self.item_link:
            self.manufacturer = self.get_manufacturer_string(self.item_link)

    def load_from_json(self, json):
        self.item_id = json['item_id']
        self.full_name = json['full_name']
        self.price = json['price']
        self.price_old = json['price_old']
        self.manufacturer = json['manufacturer']

    def get_json(self):
        return {
            'item_id': self.get_item_id(),
            'full_name': self.get_full_name(),
            'price': self.get_price(),
            'price_old': self.get_price_old(),
            'manufacturer': self.get_manufacturer()
        }

    def print_info(self, one_line=True):
        if one_line:
            print(self.get_item_id() + " | " + self.get_manufacturer() + " | " + self.get_full_name())
        else:
            print(self.get_item_id())
            print(f'   {self.get_full_name()}')
            print(f'   {self.get_price()}')
            print(f'   {self.get_price_old()}')
            print(f'   {self.get_manufacturer()}')
            print()

    @staticmethod
    def get_manufacturer_string(url):
        start = url.find('/item/') + 6
        manufacturer = url[start:url.find('/', start)]
        if 'untitled' in manufacturer:
            manufacturer = manufacturer[:8]

        manufacturer = manufacturer.replace('-', ' ')
        return manufacturer

    @staticmethod
    def get_diff_dict(field_name, old_value, new_value):
        return {
            'field': field_name,
            'old_value': old_value,
            'new_value': new_value
        }

    @staticmethod
    def compare(old, new):

        # {
        #     'field': 'field1',
        #     'old_value': '',
        #     'new_ value'
        # }

        response = {'full_name': new.full_name, 'messages': [], 'diff': []}
        if not old.item_id == new.item_id:
            response['messages'].append(f'Item IDs dont match - old record ID ({old.item_id}), new record ID ({new.item_id})')
            return response

        if not old.get_price() == new.get_price():
            response['diff'].append(Record.get_diff_dict('price', old.price, new.price))

        if not old.get_price_old() == new.get_price_old():
            response['diff'].append(Record.get_diff_dict('price_old', old.price_old, new.price_old))

        return response

    @staticmethod
    def get_comparision(old, new):
        response = Record.compare(old, new)
        comp_str = ''
        try:
            if len(response['diff']) == 0:
                return ''
            comp_str += ' _____________________________________________\n'
            comp_str += ' |'+response['full_name']+"\n"
            for message in response['messages']:
                comp_str += f' - {message}'
            for diff in response['diff']:
                comp_str +=' |Changed '+diff['field']+"\n"
                comp_str +=' | old : '+diff['old_value']+"\n"
                comp_str +=' | new : '+diff['new_value']+"\n"
            comp_str += ' |_____________________________________________\n'

        except Exception as error:
            comp_str += f'Error occured: {error} \n'
        return comp_str

    @staticmethod
    def print_comparision(old, new):
        result = Record.get_comparision(old, new)

        if result:
            print(result)

    def get_info_string(self):
        response = ' _______________________________________________________\n'
        #response += f'Item ID   : {self.get_item_id()}\n'
        response += f' | Name      : {self.get_full_name()}\n'
        response += f' | Price     : {self.get_price()}\n'
        response += f' | Old price : {self.get_price_old()}\n'
        response += f' | Brand     : {self. get_manufacturer()}\n'
        response += ' _______________________________________________________\n\n'
        return response
