"""Операции с жизненными сферами."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from life_os.database.models import LifeArea
from life_os.services.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)

MIN_PRIORITY = 1
MAX_PRIORITY = 5
MIN_SCORE = 1
MAX_SCORE = 10
MAX_NAME_LENGTH = 120


def create_life_area(
    session: Session,
    *,
    name: str,
    description: str | None = None,
    priority: int = 3,
    current_score: int = 5,
    desired_score: int = 10,
) -> LifeArea:
    """Проверить данные, создать сферу и добавить её в сессию."""
    normalized_name = _normalize_name(name)
    _validate_values(priority, current_score, desired_score)
    _ensure_unique_name(session, normalized_name)

    life_area = LifeArea(
        name=normalized_name,
        description=_normalize_description(description),
        priority=priority,
        current_score=current_score,
        desired_score=desired_score,
    )
    session.add(life_area)
    session.flush()
    return life_area


def get_life_area(session: Session, life_area_id: int) -> LifeArea:
    """Вернуть сферу по идентификатору или сообщить об отсутствии."""
    life_area = session.get(LifeArea, life_area_id)
    if life_area is None:
        raise NotFoundError(f"Жизненная сфера с id={life_area_id} не найдена.")
    return life_area


def list_life_areas(
    session: Session,
    *,
    include_archived: bool = False,
) -> list[LifeArea]:
    """Вернуть сферы по приоритету, скрыв архивные по умолчанию."""
    statement = select(LifeArea)
    if not include_archived:
        statement = statement.where(LifeArea.is_archived.is_(False))
    statement = statement.order_by(LifeArea.priority.desc(), LifeArea.name)
    return list(session.scalars(statement))


def update_life_area(
    session: Session,
    life_area_id: int,
    *,
    name: str,
    description: str | None,
    priority: int,
    current_score: int,
    desired_score: int,
) -> LifeArea:
    """Проверить и заменить редактируемые поля жизненной сферы."""
    life_area = get_life_area(session, life_area_id)
    normalized_name = _normalize_name(name)
    _validate_values(priority, current_score, desired_score)
    _ensure_unique_name(
        session,
        normalized_name,
        excluded_life_area_id=life_area_id,
    )

    life_area.name = normalized_name
    life_area.description = _normalize_description(description)
    life_area.priority = priority
    life_area.current_score = current_score
    life_area.desired_score = desired_score
    session.flush()
    return life_area


def archive_life_area(session: Session, life_area_id: int) -> LifeArea:
    """Скрыть жизненную сферу без удаления её данных."""
    life_area = get_life_area(session, life_area_id)
    life_area.is_archived = True
    session.flush()
    return life_area


def _normalize_name(name: str) -> str:
    """Убрать лишние пробелы и проверить название."""
    normalized_name = " ".join(name.split())
    if not normalized_name:
        raise ValidationError("Название жизненной сферы не может быть пустым.")
    if len(normalized_name) > MAX_NAME_LENGTH:
        raise ValidationError(
            f"Название не должно быть длиннее {MAX_NAME_LENGTH} символов."
        )
    return normalized_name


def _normalize_description(description: str | None) -> str | None:
    """Преобразовать пустое описание в None."""
    if description is None:
        return None
    normalized_description = description.strip()
    return normalized_description or None


def _validate_values(
    priority: int,
    current_score: int,
    desired_score: int,
) -> None:
    """Проверить числовые границы до обращения к SQLite."""
    _validate_range("Приоритет", priority, MIN_PRIORITY, MAX_PRIORITY)
    _validate_range("Текущая оценка", current_score, MIN_SCORE, MAX_SCORE)
    _validate_range("Желаемая оценка", desired_score, MIN_SCORE, MAX_SCORE)


def _validate_range(label: str, value: int, minimum: int, maximum: int) -> None:
    """Проверить целое число на принадлежность диапазону."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{label} должна быть целым числом.")
    if not minimum <= value <= maximum:
        raise ValidationError(
            f"{label} должна быть от {minimum} до {maximum}."
        )


def _ensure_unique_name(
    session: Session,
    name: str,
    *,
    excluded_life_area_id: int | None = None,
) -> None:
    """Не допустить одинаковые названия с разным регистром."""
    statement = select(LifeArea.id, LifeArea.name)
    if excluded_life_area_id is not None:
        statement = statement.where(LifeArea.id != excluded_life_area_id)

    normalized_name = name.casefold()
    existing_areas = session.execute(statement)
    if any(
        existing_name.casefold() == normalized_name
        for _, existing_name in existing_areas
    ):
        raise ConflictError(f"Жизненная сфера «{name}» уже существует.")
