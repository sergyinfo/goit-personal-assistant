"""
A module for the NoteHistoryEntry class
"""
from datetime import datetime

class NoteHistoryEntry:
    """
    Represents a note history entry
    """
    def __init__(self, previous_text: str, new_text: str, timestamp: datetime) -> None:
        self.previous_text: str = previous_text
        self.new_text: str = new_text
        self.timestamp: datetime = timestamp

    def to_dict(self):
        """
        Returns a dictionary representation of the note history entry
        """
        return {
            "previous_text": self.previous_text,
            "new_text": self.new_text,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a note history entry object from a dictionary
        """
        return cls(
            data['previous_text'],
            data['new_text'],
            datetime.fromisoformat(data['timestamp'])
        )

    def __str__(self) -> str:
        return (f"NoteHistoryEntry(previous_text={self.previous_text!r}, new_text={self.new_text!r}, "
                f"timestamp={self.timestamp})")

    def __repr__(self) -> str:
        return self.__str__()
