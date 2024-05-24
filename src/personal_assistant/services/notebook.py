from datetime import datetime
from typing import Dict, List, Optional

from personal_assistant.enums import EntityType
from personal_assistant.models import Note
from personal_assistant.services import StorageService, TagManagerService

class Notebook:
    def __init__(self, storage_service: StorageService) -> None:
        self.storage_service: StorageService = storage_service
        self.notes: Dict[str, Note] = {}
        self.tag_manager: TagManagerService = TagManagerService()

    def add_note(self, note: Note) -> None:
        self.notes[note.note_id] = note

    def remove_note (self, note_id: str) -> None:
        if note_id in self.notes:
            note = self.notes.pop(note_id)
            for tag in note.get_tags():
                self.tag_manager.remove_tag(tag, EntityType.NOTE, note_id)

    def update_note_text(self, note_id: str, new_text: str) -> None:
        if note_id in self.notes:
            self.notes[note_id].update_text(new_text)

    def find_note_by_id(self, note_id: str) -> Optional[Note]:
        return self.notes.get(note_id)
    
    def find_note_by_content(self, content: str) -> List[Note]:
        return [note for note in self.notes.values() if content in note.text]

    def find_notes_by_tag(self, tag: str) -> List[Note]:
        note_ids = self.tag_manager.search_by_tag(tag).get(EntityType.NOTE, [])
        return [self.notes[note_id] for note_id in note_ids if note_id in self.notes]

    def save(self) -> None:
        data = {note_id: note.__dict__ for note_id, note in self.notes.items()}
        self.storage_service.save_data(data, "notes_data")

    def load(self) -> None:
        data: Dict[str, Note] = self.storage_service.load_data("notes_data")
        for note_id, note_data in data.items():
            note = Note(
                text=note_data['text'],
                
                tags=note_data['tags'],
                note_id=note_data['note_id']
            )
            note.created_at = datetime.fromisoformat(note_data['created_at'])
            note.updated_at = datetime.fromisoformat(note_data['updated_at'])
            note.is_archived = note_data['is_archived']
            self.notes[note_id] = note

    def __enter__(self) -> 'Notebook':
        self.load()
        return self

    def __exit__(self, *args) -> None:
        self.save()
