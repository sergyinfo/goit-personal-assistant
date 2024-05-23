import re

class PhoneNumber:
    def __init__(self, number: str):
        self.number = self.clean_number(number)
        self.validate()

    def clean_number(self, number: str) -> str:
        # Очищує номер від усіх символів, крім цифр.
        cleaned = re.sub(r'\D', '', number)
        return cleaned

    def validate(self):
        # Перевіряє, чи відповідає очищений номер формату виключно з цифр та має відповідну довжину (9-12 цифр).
        # 380501234567 = 12 цифр, без 38 = 10 цифр, іноземні номери без двозначного коду = 9 цифр
        if not self.number.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if not (9 <= len(self.number) <= 12):
            raise ValueError("Phone number must contain between 9 and 12 digits, including the country code.")

    def __eq__(self, other):
        # Порівняння двох екземплярів PhoneNumber. Можна використати для перевірки, чи існує вже такий номер в контактах
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
            
    def __str__(self):
        return self.format_number()
