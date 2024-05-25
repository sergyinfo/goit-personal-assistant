from typing import Dict, List
from collections import defaultdict
from personal_assistant.enums.entity_type import EntityType
from personal_assistant.models.tag import Tag

class TagManagerService:
    """
    A class that represents a tag manager service, which is responsible for managing tags.
    """
    _instance: 'TagManagerService' = None

    def __new__(cls) -> 'TagManagerService': # check for Singleton
        if cls._instance is None:
            cls._instance = super(TagManagerService, cls).__new__(cls)
            cls._instance.tags = defaultdict(Tag)
        return cls._instance

    def add_tag(self, tag_name: str, obj_type: EntityType, obj_id: str) -> None:
        """
        Adds tag and associates it with an object.
        """
        if tag_name not in self.tags:
            self.tags[tag_name] = Tag(name=tag_name)
        tag = self.tags[tag_name]
        tag.associate_with(obj_type, obj_id)

    def remove_tag(self, tag_name: str, obj_type: EntityType, obj_id: str) -> None:
        """
        Removes tag and dissociates it from an object.
        """
        if tag_name in self.tags:
            tag = self.tags[tag_name]
            tag.dissociate_from(obj_type, obj_id)
            if not tag.associations:
                del self.tags[tag_name]

    def search_by_tag(self, tag_name: str):
        """
        Searches for objects associated with a tag.
        """
        if tag_name in self.tags:
            return self.tags[tag_name].get_associations()
        return {}

    def __str__(self) -> str:
        return f"TagManagerService(tags={dict(self.tags)})"

    def __repr__(self) -> str:
        return self.__str__()
