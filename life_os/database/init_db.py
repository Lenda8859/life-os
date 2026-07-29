"""Команда инициализации локальной базы Life OS."""

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine

from life_os.config import DATABASE_PATH, DATABASE_URL, PROJECT_ROOT
from life_os.database.connection import (
    create_database_engine,
    ensure_sqlite_directory,
)


def init_database(database_url: str = DATABASE_URL) -> Engine:
    """Применить все миграции и вернуть engine готовой базы."""
    ensure_sqlite_directory(database_url)
    alembic_config = Config(str(PROJECT_ROOT / "alembic.ini"))
    alembic_config.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(alembic_config, "head")

    engine = create_database_engine(database_url)
    return engine


def main() -> None:
    """Инициализировать пользовательскую базу из командной строки."""
    engine = init_database()
    engine.dispose()
    print(f"База Life OS подготовлена: {DATABASE_PATH}")


if __name__ == "__main__":
    main()
