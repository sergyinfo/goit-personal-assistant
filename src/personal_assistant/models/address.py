class Address:
    def __init__(self, address_str):
        self.street = None
        self.house_number = None
        self.apartment_number = None
        self.city = None
        self.state = None
        self.postal_code = None
        self.country = None
        self.parse_address(address_str)
        self.validate()

    def parse_address(self, address_str):
        parts = address_str.split(',')
        if len(parts) > 0:
            self.street = parts[0].strip()
        if len(parts) > 1:
            self.house_number = parts[1].strip()
        if len(parts) > 2:
            self.apartment_number = parts[2].strip()
        if len(parts) > 3:
            self.city = parts[3].strip()
        if len(parts) > 4:
            self.state = parts[4].strip()
        if len(parts) > 5:
            self.postal_code = parts[5].strip()
        if len(parts) > 6:
            self.country = parts[6].strip()

    def validate(self):
        if not self.street or not self.house_number:
            raise ValueError(f"Вулиця та номер будинку є обов'язковими полями адреси. {Address.get_input_format()}")

    @staticmethod
    def get_input_format():
        return "Введіть адресу в форматі: вулиця, номер будинку, [номер квартири,] [місто,] [штат,] [поштовий індекс,] [країна]."

    def __str__(self):
        parts = [self.street, self.house_number, self.apartment_number, self.city, self.state, self.postal_code, self.country]
        address_string = ", ".join(filter(lambda x: x is not None, parts))
        return address_string


"""
#приклад використання

if __name__ == "__main__":

    input_address = input(Address.get_input_format() + "\n")
    try:
        address = Address(input_address)
        print("Адреса успішно введена:")
        print(address)
    except ValueError as e:
        print("Помилка валідації адреси:")
        print(e)

"""

