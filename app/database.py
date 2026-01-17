from sqlmodel import SQLModel, create_engine, Session
import logging

logger = logging.getLogger(__name__)


DATABASE_URL = "sqlite:///./articles.db"


engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def init_db():
    logger.info("Initializing database...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database initialized successfully.")


def get_session():
    with Session(engine) as session:
        yield session
