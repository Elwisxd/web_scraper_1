from helper import Helper

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
            self.full_name = self.full_name.encode('ascii', 'ignore').decode('ascii')

        if self.price:
            self.price = self.price.get_text().strip()
            self.price = self.price.encode('ascii', 'ignore').decode('ascii')
            if self.price[1:].isnumeric():
                self.price = self.price[1:]

        if self.price_old:
            self.price_old = self.price_old.get_text().strip()
            self.price_old = self.price_old.encode('ascii', 'ignore').decode('ascii')
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
            'old': old_value,
            'new': new_value
        }

    @staticmethod
    def compare(old, new):

        types = []
        response = {'full_name': new.get_full_name(), 'manufacturer': new.get_manufacturer(), 'messages': [], 'differences': []}

        try:

            if not old.item_id == new.item_id:
                response['messages'].append(f'Item IDs dont match - old record ID ({old.item_id}), new record ID ({new.item_id})')
                return types, response

            if old.get_price() == new.get_price():
                return types, response

            if (not Helper.isfloat(new.get_price())) and Helper.isfloat(old.get_price()):
                response['differences'].append(Record.get_diff_dict('price', old.price, new.price))
                types.append('sold_out')

            if (not Helper.isfloat(old.get_price())) and Helper.isfloat(new.get_price()):
                response['differences'].append(Record.get_diff_dict('price', old.price, new.price))
                types.append('restocked')

            if Helper.isfloat(old.get_price()) and Helper.isfloat(new.get_price()):
                if float(old.get_price()) > float(new.get_price()):
                    response['differences'].append(Record.get_diff_dict('price', old.price, new.price))
                    types.append('discounted')
                else:
                    response['differences'].append(Record.get_diff_dict('price', old.price, new.price))
                    types.append('markup')


            return types, response
        except Exception as error:
            response["messages"].append("Error occured")
            return response

    def get_info_string(self):
        response = ' _______________________________________________________\n'
        #response += f'Item ID   : {self.get_item_id()}\n'
        response += f' | Name      : {self.get_full_name()}\n'
        response += f' | Price     : {self.get_price()}\n'
        response += f' | Old price : {self.get_price_old()}\n'
        response += f' | Brand     : {self. get_manufacturer()}\n'
        response += ' _______________________________________________________\n\n'
        return response

    def get_info_dict(self):
        response = {}
        response["full_name"] = self.get_full_name()
        response["manufacturer"] = self.get_manufacturer()
        response["price"] = self.get_price()
        response["price_old"] = self.get_price_old()
        return response

    @staticmethod
    def get_added_string_from_dict(diff):
        text = " ______________________\n"
        text += " | name   : " + diff["full_name"]+"\n"
        text += " | manuf. : " + diff["manufacturer"]+"\n"
        text += " | price     : " + diff["price"]+"\n"
        text += " | price old : " + diff["price_old"]+"\n"
        text += " |_____________________\n"
        return text

    @staticmethod
    def get_changed_string_from_dict(diff):
        text = " ______________________\n"
        text += " | name   : " + diff["full_name"]+"\n"
        text += " | manuf. : " + diff["manufacturer"]+"\n"
        for message in diff["messages"]:
            text += " |m : " + message + "\n"
        for difference in diff["differences"]:
            text += " | field : " + difference["field"] + "\n"
            text += " | old   : " + difference["old"] + "\n"
            text += " | new   : " + difference["new"] + "\n"
        text += " |_____________________\n"
        return text
