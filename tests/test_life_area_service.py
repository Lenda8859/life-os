"""Тесты бизнес-логики жизненных сфер."""

from pathlib import Path

import pytest
from sqlalchemy import Engine

from life_os.database.connection import session_scope
from life_os.database.init_db import init_database
from life_os.services.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from life_os.services.life_area_service import (
    archive_life_area,
    create_life_area,
    get_life_area,
    list_life_areas,
    update_life_area,
)


@pytest.fixture
def engine(tmp_path: Path) -> Engine:
    """Создать отдельную мигрированную базу для каждого теста."""
    database_url = f"sqlite:///{(tmp_path / 'service_test.db').as_posix()}"
    database_engine = init_database(database_url)
    yield database_engine
    database_engine.dispose()


def test_create_life_area_normalizes_values(engine: Engine) -> None:
    """Создание должно убрать лишние пробелы и сохранить данные."""
    with session_scope(engine) as session:
        life_area = create_life_area(
            session,
            name="  Карьера   и доход  ",
            description="  Профессиональное развитие  ",
            priority=5,
            current_score=4,
            desired_score=9,
        )
        life_area_id = life_area.id

    with session_scope(engine) as session:
        saved_area = get_life_area(session, life_area_id)
        assert saved_area.name == "Карьера и доход"
        assert saved_area.description == "Профессиональное развитие"
        assert saved_area.priority == 5


def test_update_life_area(engine: Engine) -> None:
    """Редактирование должно заменить пользовательские поля."""
    with session_scope(engine) as session:
        life_area = create_life_area(session, name="Здоровье")
        life_area_id = life_area.id

    with session_scope(engine) as session:
        updated_area = update_life_area(
            session,
            life_area_id,
            name="Здоровье и энергия",
            description="Сон, движение и самочувствие",
            priority=5,
            current_score=6,
            desired_score=9,
        )
        assert updated_area.name == "Здоровье и энергия"
        assert updated_area.current_score == 6


def test_archive_hides_life_area_from_default_list(engine: Engine) -> None:
    """Архивная сфера должна скрываться, но оставаться в базе."""
    with session_scope(engine) as session:
        active_area = create_life_area(session, name="Обучение", priority=5)
        archived_area = create_life_area(session, name="Отдых", priority=2)
        archive_life_area(session, archived_area.id)
        active_area_id = active_area.id
        archived_area_id = archived_area.id

    with session_scope(engine) as session:
        visible_ids = {area.id for area in list_life_areas(session)}
        all_ids = {
            area.id for area in list_life_areas(session, include_archived=True)
        }
        assert visible_ids == {active_area_id}
        assert all_ids == {active_area_id, archived_area_id}


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("name", "   ", "не может быть пустым"),
        ("priority", 6, "от 1 до 5"),
        ("current_score", 0, "от 1 до 10"),
        ("desired_score", 11, "от 1 до 10"),
    ),
)
def test_create_rejects_invalid_values(
    engine: Engine,
    field: str,
    value: str | int,
    message: str,
) -> None:
    """Сервис должен отклонить некорректные данные до записи."""
    values: dict[str, str | int] = {
        "name": "Финансы",
        "priority": 3,
        "current_score": 5,
        "desired_score": 10,
    }
    values[field] = value

    with session_scope(engine) as session:
        with pytest.raises(ValidationError, match=message):
            create_life_area(session, **values)  # type: ignore[arg-type]


def test_duplicate_name_is_rejected_case_insensitively(engine: Engine) -> None:
    """Названия с отличающимся регистром не должны дублироваться."""
    with session_scope(engine) as session:
        create_life_area(session, name="Финансы")

    with session_scope(engine) as session:
        with pytest.raises(ConflictError, match="уже существует"):
            create_life_area(session, name="финансы")


def test_missing_life_area_raises_clear_error(engine: Engine) -> None:
    """Неизвестный идентификатор должен давать сервисную ошибку."""
    with session_scope(engine) as session:
        with pytest.raises(NotFoundError, match="id=999"):
            get_life_area(session, 999)
