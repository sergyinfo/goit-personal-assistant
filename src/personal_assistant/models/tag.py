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

    def to_dict(self) -> Dict:
        """
        Return the tag as a dictionary
        """
        return {
            "name": self.name,
            "associations": {obj_type.value: list(ids) for obj_type, ids in self.associations.items()},
        }
    
    @classmethod
    def from_dict(cls, tag_dict: Dict) -> 'Tag':
        """
        Create a tag from a dictionary
        """
        tag = cls(tag_dict["name"])
        for obj_type, ids in tag_dict["associations"].items():
            tag.associations[EntityType(obj_type)] = set(ids)
        return tag

    def __str__(self) -> str:
        return f"Tag(name={self.name}, associations={self.associations})"

    def __repr__(self) -> str:
        return self.__str__()
