"""
Tag model.
"""
from typing import Dict, Set
from personal_assistant.enums.entity_type import EntityType

class Tag:
    """
    A class to represent a tag
    """
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.associations: Dict[EntityType, Set[str]] = {
            EntityType.CONTACT: set(),
            EntityType.NOTE: set(),
        }

    def associate_with(self, obj_type: EntityType, obj_id: str) -> None:
        """
        Associate the tag with an object
        """
        self.associations[obj_type].add(obj_id)

    def dissociate_from(self, obj_type: EntityType, obj_id: str) -> None:
        """
        Dissociate the tag from an object
        """
        self.associations[obj_type].discard(obj_id)

    def __str__(self) -> str:
        return f"Tag(name={self.name}, associations={self.associations})"

    def __repr__(self) -> str:
        return self.__str__()
