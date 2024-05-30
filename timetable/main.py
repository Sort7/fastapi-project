from fastapi import FastAPI
import uvicorn

from api import router as api_pouter
from core.config import settings


app = FastAPI()
app.include_router(api_pouter, prefix=settings.api.prefix)

@app.get("/")
def hello():
    return {"massage": "hello world",}


@app.get("/itens")
def list_items():
    return ["Iens1", "Itens2"]


@app.get("/itens/{items_id}")
def list_items(items_id: int):
    return {"Iens":{ "id": items_id}}


if __name__ == '__main__':
    uvicorn.run(
        "main:app", # Вызываем uvicorn.run (запуск сервера) указав в кавычках путь к приложению "main:app",
        host = settings.run.host,
        port = settings.run.port,
        reload=True # через команду reload=True - задаем автоматический перезапуск приложения
    )