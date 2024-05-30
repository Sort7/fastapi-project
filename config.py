from pydantic_settings import BaseSettings

class Settinds(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fa"


settings = Settinds()

# from pathlib import Path
#
# from sqlalchemy import create_engine
#
#
# BASE_DIR = Path(__file__).parent
# db_file_path = BASE_DIR / "blog.db"
# # DB_URL = f"sqlate:///db_file_path"
# DB_URL = "postgresql+pg8000://user:example@localhost:5432/blog"
# DB_ECHO = True
#
# engine = create_engine(
#     url = DB_URL,
#     echo = DB_ECHO
# )