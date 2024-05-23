"""
This is the Birthday class for the personal assistant application. 
It parses the converts input data into datetime.date object and validates the data, 
get_next_birthday method returns the next birthday of the contact, 
get_age mathod returns the age of the contact, __str__ method returns a time 
representation of a datetime.date object in "day.month.year" format.
"""

from datetime import datetime, date
from typing import Optional

class Birthday:
    """
    Birthday class to parse and validate birthday fields.
    """
    def __init__(self, date_input):
        if isinstance(date_input, str):
            self.date = datetime.strptime(date_input, "%d.%m.%Y").date()
        elif isinstance(date_input, date):
            self.date = date_input
        else:
            raise ValueError("Дата народження має бути строкою у форматі ДД.ММ.РРРР чи об'єкт datetime.date")
        self.validate()

    def validate(self):
        """
        Validate the birthday field.
        """
        if self.date > date.today():
            raise ValueError("Дата народження не може бути у майбутньому.")

    def get_next_birthday(self, today: Optional[date] = None) -> date:
        """
        Return the next birthday date.
        """
        if today is None:
            today = date.today()

        year = today.year if today <= date(today.year, self.date.month, self.date.day) else today.year + 1

        try:
            next_birthday = date(year, self.date.month, self.date.day)
        except ValueError:  # 29 лютого у не-високосний рік
            if self.date.month == 2 and self.date.day == 29:
                next_birthday = date(year, 3, 1)  # Переносимо на 1 березня
            else:
                raise

        return next_birthday

    def get_age(self, today=None):
        """
        Return the age of the contact.
        """
        if today is None:
            today = date.today()
        age = today.year - self.date.year
        if (today.month, today.day) < (self.date.month, self.date.day):
            age -= 1
        return age

    def __str__(self):
        return self.date.strftime("%d.%m.%Y")
