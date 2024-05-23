
"""
This is the Address class for the personal assistant application. It parses the address string arguments, 
validates the data from the user, and returns the address.
"""
import re
from typing import Optional 
class Address:
    def __init__(self, address_str: str) -> None:
        self.street: Optional[str] = None
        self.house_number: Optional[str] = None
        self.apartment_number: Optional[str] = None
        self.city: Optional[str] = None
        self.state: Optional[str] = None
        self.postal_code: Optional[str] = None
        self.country: Optional[str] = None
        self.parse_address(address_str)
        self.validate()

    def parse_address(self, address_str):
        parts = address_str.split(',')
        if len(parts) > 0:
            self.street = parts[0].strip()
        if len(parts) > 1:
            potential_house_number = parts[1].strip()
            if re.match(r'^\d[\d\w]*$', potential_house_number):
                self.house_number = potential_house_number
            else:
                raise ValueError("Недійсний номер будинку: має починатися з цифри та містити лише цифри та літери.")
        if len(parts) > 2:
            potential_apartment_number = parts[2].strip()
            if re.match(r'^[\d\w]+$', potential_apartment_number):
                self.apartment_number = potential_apartment_number
            else:
                raise ValueError("Невірний номер квартири: має містити лише цифри та літери.")

        if len(parts) > 3:
            self.city = parts[3].strip()
        if len(parts) > 4:
            self.state = parts[4].strip()
        if len(parts) > 5:
            potential_postal_code = parts[5].strip()
            if re.match(r'^\d+$', potential_postal_code):
                self.postal_code = potential_postal_code
            else:
                 raise ValueError("Недійсний поштовий індекс: має містити лише цифри.")
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
        return ", ".join(filter(None, parts))