from pydantic import BaseModel
from typing import List

class AbilityScores(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

class DnDCharacter(BaseModel):
    name: str
    race: str
    character_class: str
    level: int
    abilities: AbilityScores
    skills: List[str]
    spells: List[str]
    equipment: List[str]