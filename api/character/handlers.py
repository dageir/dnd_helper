from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from api.character.models import SGameCharacterAdd, SGameCharacterGet, Avatar
from api.character.tools.longstory import _create_character_by_file
from config import DB_PASSWORD
from db.dals import CharacterDAL
from db.session import get_db


character_router = APIRouter()

#TODO вынести переменную path_to_static в ENV (возможно депрекейтнуть эту ручку)
async def _upload_avatar(file):
    try:
        content = file.file.read()

        path_to_static = f'../../OpenServer/domains/dndHelper.com/front/static/{file.filename}'
        with open(path_to_static, 'wb') as f:
            f.write(content)
    except Exception as err:
        return {"message": f"There was an error uploading the file ({err})"}
    finally:
        file.file.close()
        return {"message": f"Successfully uploaded {file.filename}"}

async def _create_character(body:SGameCharacterAdd,
                            session: AsyncSession):
    async with session.begin():
        char_dal = CharacterDAL(session)
        char = await char_dal.create_character(body)
        return char


async def _get_all_characters(session: AsyncSession):
    char_dal = CharacterDAL(session)
    chars = await char_dal.get_all_characters()
    return chars

async def create_character_by_file(file: UploadFile, is_bot: bool):
    return _create_character_by_file(file, is_bot)


@character_router.post('/test')
async def create_character():
    return {'status': 'It`s work!'}


@character_router.post('/create', response_model=SGameCharacterGet)
async def create_character(body: SGameCharacterAdd,
                           db: AsyncSession = Depends(get_db)):
    return await _create_character(body, db)


@character_router.get('/get_all', response_model=list[SGameCharacterGet])
async def get_all_characters(db: AsyncSession = Depends(get_db)):
    return await _get_all_characters(db)


@character_router.post('/upload_from_longstoryshort', response_model=SGameCharacterGet)
async def upload_longstory_file(file: UploadFile = File(...),
                                is_bot: bool = True,
                                db: AsyncSession = Depends(get_db)):
    return await create_character_by_file(file, is_bot)


@character_router.post('/upload_avatar')
async def upload_avatar(file: UploadFile = File(...)):
    return await _upload_avatar(file)

# @character_router.post('/upload_avatar')
# async def upload_avatar(body):
#     return await _upload_avatar(body)
