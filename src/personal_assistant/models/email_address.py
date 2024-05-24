"""
A module for the EmailAddress class
"""
import re

class EmailAddress:
    """
    A class to represent an email address
    """
    EMAIL_PATTERN = re.compile(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", re.IGNORECASE)

    def __init__(self, email):
        self.email = email
        self.validate()

    def validate(self):
        """
        Validate the email address
        """
        if not self.EMAIL_PATTERN.match(self.email):
            raise ValueError(f"Email address {self.email} is invalid")
        
    def to_dict(self):
        """
        Convert the email address to a dictionary
        """
        return self.email
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a new EmailAddress object from a dictionary
        """
        return cls(email=data)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.email.lower() == other.email.lower()
        return False

    def __str__(self):
        return self.email
