"""
A module for the PhoneNumber class
"""
import re

class PhoneNumber:
    """
    A class to represent a phone number
    """
    def __init__(self, number: str):
        self.number = self.clean_number(number)
        self.validate()

    def clean_number(self, number: str) -> str:
        """
        Clean the number from all characters except digits
        """
        cleaned = re.sub(r'\D', '', number)
        return cleaned

    def validate(self):
        """
        Validate the phone number to contain only digits and have the appropriate length
        380501234567 = 12 digits, without 38 = 10 digits, 
        foreign numbers without a two-digit code = 9 digits
        """
        if not self.number.isdigit():
            raise ValueError("Номер телефону повинен містити лише цифри.")
        if not (9 <= len(self.number) <= 12):
            raise ValueError("Номер телефону повинен містити від 9 до 12 цифр, включаючи код країни.")

    def __eq__(self, other):
        if isinstance(other, PhoneNumber):
            return self.number == other.number
        return False    

    def format_number(self) -> str:
        # Повертає форматований номер телефону.
        if len(self.number) == 10:
            return f"+38 ({self.number[:3]}) {self.number[3:6]} {self.number[6:8]} {self.number[8:]}"
        elif len(self.number) == 12:
            return f"+{self.number[:2]} ({self.number[2:5]}) {self.number[5:8]} {self.number[8:10]} {self.number[10:]}"
        else:
            return f"+{self.number[:2]} {self.number[2:5]} {self.number[5:8]} {self.number[8:]}"

    def to_dict(self):
        """
        Convert the phone number to a dictionary
        """
        return self.number

    @classmethod
    def from_dict(cls, data):
        """
        Create a new PhoneNumber object from a dictionary
        """
        return cls(number=data)

    def __str__(self):
        return self.format_number()
