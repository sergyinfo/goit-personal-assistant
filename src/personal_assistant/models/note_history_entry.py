from datetime import datetime

class NoteHistoryEntry:
    def __init__(self, previous_text: str, new_text: str, timestamp: datetime) -> None:
        self.previous_text: str = previous_text
        self.new_text: str = new_text
        self.timestamp: datetime = timestamp
    
    def __str__(self) -> str:
        return (f"NoteHistoryEntry(previous_text={self.previous_text!r}, new_text={self.new_text!r}, "
                f"timestamp={self.timestamp})")
    
    def __repr__(self) -> str:
        return self.__str__()
