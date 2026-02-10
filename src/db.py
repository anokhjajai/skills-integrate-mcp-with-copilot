from sqlmodel import Session, create_engine, SQLModel
from typing import Generator

DATABASE_URL = "sqlite:///./data.db"

# For SQLite, disable same-thread check for FastAPI dev server
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
