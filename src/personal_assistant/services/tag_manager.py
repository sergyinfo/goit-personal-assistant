from typing import Dict, List
from collections import defaultdict
from personal_assistant.enums.entity_type import EntityType
from personal_assistant.models.tag import Tag

class TagManagerService:
    _instance: 'TagManagerService' = None

    def __new__(cls) -> 'TagManagerService': # check for Singleton
        if cls._instance is None:
            cls._instance = super(TagManagerService, cls).__new__(cls)
            cls._instance.tags = defaultdict(Tag)
        return cls._instance

    def add_tag(self, tag_name: str, obj_type: EntityType, obj_id: str) -> None:
        tag: Tag = self.tags[tag_name]
        tag.name = tag_name
        tag.associate_with(obj_type, obj_id)

    def remove_tag(self, tag_name: str, obj_type: EntityType, obj_id: str) -> None:
        if tag_name in self.tags:
            tag: Tag = self.tags[tag_name]
            tag.dissociate_from(obj_type, obj_id)
            if not any(tag.associations.values()):
                del self.tags[tag_name]

    def search_by_tag(self, tag_name: str) -> Dict[EntityType, List[str]]:
        if tag_name in self.tags:
            tag = self.tags[tag_name]
            return {obj_type: list(ids) for obj_type, ids in tag.associations.items()}
        return {}

    def __str__(self) -> str:
        return f"TagManagerService(tags={dict(self.tags)})"

    def __repr__(self) -> str:
        return self.__str__()
