import json
from pprint import pprint

from fastapi import UploadFile

from api.character.models import Equipment, Stats, Force, Intelligence, Charisma, StatValue, Agility, Wisdom, \
    SGameCharacterAdd


def parse_description(data: dict) -> str:
    all_text_list = []
    for content in data['data']['content']:
        if 'content' in content:
            for text in content['content']:
                all_text_list.append(text['text'])
            all_text_list.append('\n \n')
    all_text = ''.join(all_text_list)
    return all_text

def parse_equipment(data: dict) -> list[Equipment]:
    res = data['resources']
    equipments = []
    for eq in res.keys():
        cur_eq = res[eq]
        equipments.append(Equipment(
            name=cur_eq['name'],
            max=cur_eq['max'],
            current=cur_eq['current']
        ))
    return equipments

def gen_bonus(value: int, prof: int) -> int:
    modification = prof * 2
    if value >= 10:
        return ((value - 10) // 2) + modification
    return (-((11 - value) // 2)) + modification


def check_prof(data: dict, name_skill: str) -> int:
    if 'isProf' not in data[name_skill]:
        return 0
    return data[name_skill]['isProf']

def parse_stats(data: dict) -> Stats:
    stats_dict = data['stats']
    skills_dict = data['skills']
    force_dict = stats_dict['str']
    force_value = force_dict['score']
    force = Force(value=force_value,
                  athletics=gen_bonus(force_value, check_prof(skills_dict, 'athletics')))
    body_type = StatValue(value=stats_dict['con']['score'])
    int_dict = stats_dict['int']
    int_value = int_dict['score']
    int = Intelligence(value=int_value,
                       history=gen_bonus(int_value, check_prof(skills_dict, 'history')),
                       magic=gen_bonus(int_value, check_prof(skills_dict, 'arcana')),
                       nature=gen_bonus(int_value, check_prof(skills_dict, 'nature')),
                       investigation=gen_bonus(int_value, check_prof(skills_dict, 'investigation')),
                       religion=gen_bonus(int_value, check_prof(skills_dict, 'religion'))
                       )
    char_dict = stats_dict['cha']
    char_value = char_dict['score']
    char = Charisma(value=char_value,
                    performance=gen_bonus(char_value, check_prof(skills_dict, 'performance')),
                    intimidation=gen_bonus(char_value, check_prof(skills_dict, 'intimidation')),
                    fraud=gen_bonus(char_value, check_prof(skills_dict, 'deception')),
                    conviction=gen_bonus(char_value, check_prof(skills_dict, 'persuasion'))
                    )
    agil_dict = stats_dict['dex']
    agil_value = agil_dict['score']
    agil = Agility(value=agil_value,
                   acrobatics=gen_bonus(agil_value, check_prof(skills_dict, 'acrobatics')),
                   sleight_of_hand=gen_bonus(agil_value, check_prof(skills_dict, 'sleight of hand')),
                   stealth=gen_bonus(agil_value, check_prof(skills_dict, 'stealth'))
                   )
    wis_dict = stats_dict['wis']
    wis_value = wis_dict['score']
    wis = Wisdom(value=wis_value,
                 perception=gen_bonus(wis_value, check_prof(skills_dict, 'perception')),
                 survival=gen_bonus(wis_value, check_prof(skills_dict, 'survival')),
                 medicine=gen_bonus(wis_value, check_prof(skills_dict, 'medicine')),
                 insight=gen_bonus(wis_value, check_prof(skills_dict, 'insight')),
                 animal_care=gen_bonus(wis_value, check_prof(skills_dict, 'animal handling')),
                 )
    all_stats = Stats(force=force,
                      body_type=body_type,
                      intelligence=int,
                      charisma=char,
                      agility=agil,
                      wisdom=wis)
    return all_stats

def _create_character_by_file(file: UploadFile, is_bot: bool):
    my_file = file.file.read()
    data = json.loads(my_file)
    need_data = json.loads(data['data'])
    name = need_data['name']['value']
    race = need_data['info']['race']['value']
    class_ = need_data['info']['charClass']['value']
    description = parse_description(need_data['text']['background']['value'])
    armor_class = int(need_data['vitality']['ac']['value'])
    max_health = int(need_data['vitality']['hp-max']['value'])
    now_health = int(need_data['vitality']['hp-current']['value'])
    equipment = parse_equipment(need_data)
    stats = parse_stats(need_data)
    abilities = []

    char = SGameCharacterAdd(
        name=name,
        image='',
        race=race,
        class_=class_,
        description=description,
        armor_class=armor_class,
        max_health=max_health,
        now_health=now_health,
        equipment=equipment,
        stats=stats,
        abilities=abilities,
        is_bot=is_bot
    )

    return char
