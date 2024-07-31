from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from api.character.handlers import character_router
from db.models import create_tables, delete_tables

from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База создана')
    yield
    print('Выключение')

app = FastAPI(title='dnd_master_helper', lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:63342",
    "http://dndhelper.com",
    "https://dndhelper.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_api_router = APIRouter()

main_api_router.include_router(character_router, prefix='/char', tags=['char'])

app.include_router(main_api_router)
