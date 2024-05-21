import uuid

from datetime import datetime
from typing import List, Optional

from personal_assistant.enums import *
from personal_assistant.models import NoteHistoryEntry, TagManager

class Note:
    def __init__(self, text: str, tags: Optional[List[str]] = None, note_id: Optional[str] = None, default_tags: Optional[List[str]] = None) -> None:
        self.note_id: str = note_id or str(uuid.uuid4())
        self.text: str = text
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()
        self.tags: List[str] = tags or []
        self.tag_manager: TagManager = TagManager()
        self.is_archived: bool = False
        self.note_history: List[NoteHistoryEntry] = []
        
        if default_tags:
            self.tags.extend(default_tags)
        
        for tag in self.tags:
            self.tag_manager.add_tag(tag, EntityType.NOTE, self.note_id)
    
    def update_text(self, new_text: str) -> None:
        history_entry = NoteHistoryEntry(previous_text=self.text, new_text=new_text, timestamp=datetime.now())
        self.note_history.append(history_entry)
        self.text = new_text
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)
            # TODO: self.tag_manager.add_tag(tag, EntityType.NOTE, self.note_id)
    
    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)
            # TODO self.tag_manager.remove_tag(tag, EntityType.NOTE, self.note_id)
    
    def get_tags(self) -> List[str]:
        return self.tags
    
    def search_keyword(self, keyword: str) -> bool:
        return keyword in self.text
    
    def archive(self) -> None:
        self.is_archived = True
    
    def restore(self) -> None:
        self.is_archived = False
    
    def get_history(self) -> List[NoteHistoryEntry]:
        return self.note_history
    
    def __str__(self) -> str:
        return (f"Note(id={self.note_id}, text={self.text}, created_at={self.created_at}, "
                f"updated_at={self.updated_at}, tags={self.tags}, is_archived={self.is_archived})")
    
    def __repr__(self) -> str:
        return (f"Note(note_id={self.note_id!r}, text={self.text!r}, created_at={self.created_at!r}, "
                f"updated_at={self.updated_at!r}, tags={self.tags!r}, is_archived={self.is_archived!r})")
    
    def __hash__(self) -> int:
        return hash((self.note_id, self.text, self.created_at, self.updated_at, tuple(self.tags), self.is_archived))
    
    def __len__(self) -> int:
        return len(self.text)
    
    def __contains__(self, tag: str) -> bool:
        return tag in self.tags
    
    def __iter__(self):
        return iter(self.tags)
