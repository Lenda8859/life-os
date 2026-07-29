"""Тесты фундамента базы данных."""

from pathlib import Path

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError

from life_os.database.connection import session_scope
from life_os.database.init_db import init_database
from life_os.database.models import Goal, GoalHorizon, LifeArea


@pytest.fixture
def database_url(tmp_path: Path) -> str:
    """Вернуть адрес отдельной базы внутри временной папки pytest."""
    return f"sqlite:///{(tmp_path / 'test_life_os.db').as_posix()}"


def test_init_database_creates_first_tables(database_url: str) -> None:
    """Инициализация должна создать первые таблицы проекта."""
    engine = init_database(database_url)

    try:
        table_names = set(inspect(engine).get_table_names())
        assert table_names == {"alembic_version", "goals", "life_areas"}
    finally:
        engine.dispose()


def test_goal_is_saved_with_life_area(database_url: str) -> None:
    """Цель должна сохраняться со ссылкой на существующую сферу."""
    engine = init_database(database_url)

    try:
        with session_scope(engine) as session:
            area = LifeArea(
                name="Обучение",
                description="Python, SQL и разработка",
                priority=5,
                current_score=4,
                desired_score=9,
            )
            area.goals.append(
                Goal(
                    title="Изучить основы SQLAlchemy",
                    horizon=GoalHorizon.MONTH,
                )
            )
            session.add(area)

        with session_scope(engine) as session:
            saved_goal = session.scalar(select(Goal))
            assert saved_goal is not None
            assert saved_goal.life_area.name == "Обучение"
            assert saved_goal.progress_percent == 0
    finally:
        engine.dispose()


def test_invalid_life_area_score_is_rejected(database_url: str) -> None:
    """SQLite должна отклонить оценку вне диапазона от 1 до 10."""
    engine = init_database(database_url)

    try:
        with pytest.raises(IntegrityError):
            with session_scope(engine) as session:
                session.add(
                    LifeArea(
                        name="Некорректная сфера",
                        current_score=11,
                        desired_score=10,
                    )
                )
    finally:
        engine.dispose()
