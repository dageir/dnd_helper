from typing import Union

from sqlalchemy import UUID, update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.character.models import SGameCharacterAdd, Stats
from db.models import GameCharactersOrm


class CharacterDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_character(self, body: SGameCharacterAdd):

        stats_dict = body.stats.__dict__
        equipment = body.equipment
        new_eq = []
        abilities = body.abilities
        new_abilities = []

        for key in stats_dict:
            stats_dict[key] = stats_dict[key].__dict__

        for eq in equipment:
            new_eq.append(eq.__dict__)

        for ability in abilities:
            current_ability = ability.__dict__
            current_ability['cube'] = current_ability['cube'].value
            current_ability['scale'] = current_ability['scale'].value
            new_abilities.append(current_ability)

        new_char = GameCharactersOrm(
            name=body.name,
            image=body.image,
            race=body.race,
            class_=body.class_,
            description=body.description,
            armor_class=body.armor_class,
            max_health=body.max_health,
            now_health=body.now_health,
            equipment=new_eq,
            stats=stats_dict,
            abilities=new_abilities,
            is_bot=body.is_bot
        )

        self.db_session.add(new_char)
        await self.db_session.flush()
        return new_char

    async def get_all_characters(self):
        query = select('*').select_from(GameCharactersOrm)
        res = await self.db_session.execute(query)
        chars = res.fetchall()
        return chars