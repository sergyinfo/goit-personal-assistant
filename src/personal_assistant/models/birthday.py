from datetime import datetime, date, timedelta

class Birthday:
    def __init__(self, date_input):
        if isinstance(date_input, str):
            self.date = datetime.strptime(date_input, "%d.%m.%Y").date()
        elif isinstance(date_input, date):
            self.date = date_input
        else:
            raise ValueError("Дата народження має бути строкою у форматі ДД.ММ.РРРР чи об'єкт datetime.date")
        self.validate()

    def validate(self):
        if self.date > date.today():
            raise ValueError("Дата народження не може бути у майбутньому.")

    def get_next_birthday(self, today=None):
        if today is None:
            today = date.today()
        next_birthday = self.date.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return next_birthday

    def get_age(self, today=None):
        if today is None:
            today = date.today()
        age = today.year - self.date.year
        if (today.month, today.day) < (self.date.month, self.date.day):
            age -= 1
        return age

    def __str__(self):
        return self.date.strftime("%d.%m.%Y")
    
"""
# Приклад використання
if __name__ == "__main__":
    input_date = input("Введіть дату народження в форматі 'ДД.ММ.РРРР': ")
    try:
        birthday = Birthday(input_date)
        print("Дата народження:", birthday)
        print("Наступний день народження:", birthday.get_next_birthday())
        print("Вік:", birthday.get_age())
    except ValueError as e:
        print("Помилка валідації дати народження:")
        print(e)

"""
