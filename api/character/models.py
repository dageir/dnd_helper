import uuid
from enum import Enum

from fastapi import UploadFile, File
from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        crm_mode = True

class StatValue(TunedModel):
    value: int

class Force(StatValue):
    athletics: int

class Intelligence(StatValue):
    history: int
    magic: int
    nature: int
    investigation: int
    religion: int

class Charisma(StatValue):
    performance: int
    intimidation: int
    fraud: int
    conviction: int

class Agility(StatValue):
    acrobatics: int
    sleight_of_hand: int
    stealth: int

class Wisdom(StatValue):
    perception: int
    survival: int
    medicine: int
    insight: int
    animal_care: int

class Stats(TunedModel):
    force: Force
    body_type: StatValue
    intelligence: Intelligence
    charisma: Charisma
    agility: Agility
    wisdom: Wisdom

class Equipment(TunedModel):
    name: str
    max: int
    current: int

class Scale(Enum):
    FORSE = 'СИЛА'
    BODY_TYPE = 'ТЕЛОСЛОЖЕНИЕ'
    INTELLIGENCE = 'ИНТЕЛЛЕКТ'
    CHARISMA = 'ХАРИЗМА'
    AGILITY = 'ЛОВКОСТЬ'
    WISDOM = 'МУДРОСТЬ'

class Cube(Enum):
    NO_CUBE = ''
    CUBE_K2 = '1K2'
    CUBE_K4 = '1K4'
    CUBE_K6 = '1K6'
    CUBE_K8 = '1K8'
    CUBE_K10 = '1K10'
    CUBE_K12 = '1K12'
    CUBE_K20 = '1K20'
    CUBE_K100 = '1K100'


class Ability(TunedModel):
    name: str
    description: str
    cube: Cube
    scale: Scale


class SGameCharacterAdd(TunedModel):
    name: str
    image: str
    race: str
    class_: str
    description: str = None
    armor_class: int
    max_health: int
    now_health: int
    equipment: list[Equipment]
    stats: Stats | dict
    abilities: list[Ability]
    is_bot: bool

class SGameCharacterGet(SGameCharacterAdd):
    id: uuid.UUID

class Avatar(TunedModel):
    file: UploadFile
    file_name: str
