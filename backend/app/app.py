from fastapi import FastAPI
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

from app.models.user_model import User
from app.models.todo_model import Todo
from app.api.api_v1.router import router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url= f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def app_init():
    """
        initialize crucial application services
    """

    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).crud_jwt_fastapi_mongodb_do_davi

    await init_beanie(
        database = db_client,
        document_models = [
            #importa e carrega a model de usuario
            User,
            Todo
        ]
    )

app.include_router(router, prefix = settings.API_V1_STR)




@app.get('/')
async def hello():
    return {"message": "HELLO WORLD"}