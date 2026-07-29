"""Подключение к SQLite и управление транзакциями."""

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from sqlite3 import Connection as SQLiteConnection

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from life_os.config import DATABASE_URL


def create_database_engine(
    database_url: str = DATABASE_URL,
    *,
    echo: bool = False,
) -> Engine:
    """Создать SQLAlchemy engine и включить внешние ключи SQLite."""
    engine = create_engine(database_url, echo=echo)

    if database_url.startswith("sqlite"):
        event.listen(engine, "connect", _enable_sqlite_foreign_keys)

    return engine


def ensure_sqlite_directory(database_url: str = DATABASE_URL) -> None:
    """Создать каталог для файловой SQLite-базы, если он отсутствует."""
    prefix = "sqlite:///"
    if not database_url.startswith(prefix) or database_url == "sqlite:///:memory:":
        return

    database_path = Path(database_url.removeprefix(prefix))
    database_path.parent.mkdir(parents=True, exist_ok=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Создать фабрику независимых сессий для указанного engine."""
    return sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def session_scope(
    engine: Engine,
) -> Generator[Session, None, None]:
    """Выполнить операции в транзакции с commit или rollback."""
    session_factory = create_session_factory(engine)
    session = session_factory()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _enable_sqlite_foreign_keys(
    dbapi_connection: SQLiteConnection,
    _connection_record: object,
) -> None:
    """Включить проверку внешних ключей для соединения SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
