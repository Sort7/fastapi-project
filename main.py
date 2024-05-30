from fastapi import FastAPI
import uvicorn

app = FastAPI()

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
    uvicorn.run("main:app", reload=True) # Вызываем uvicorn.run (запуск сервера) указав
    # в кавычках путь к приложению "main:app", а через команду reload=True - задаем
    # автоматический перезапуск приложения