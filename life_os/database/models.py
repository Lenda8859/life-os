"""Первые SQLAlchemy-модели Life OS."""

from datetime import date
from enum import StrEnum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from life_os.database.base import Base, TimestampMixin


class GoalHorizon(StrEnum):
    """Допустимый горизонт планирования цели."""

    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    THREE_YEARS = "three_years"


class GoalStatus(StrEnum):
    """Допустимые состояния цели."""

    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LifeArea(TimestampMixin, Base):
    """Жизненная сфера пользователя."""

    __tablename__ = "life_areas"
    __table_args__ = (
        CheckConstraint(
            "priority BETWEEN 1 AND 5",
            name="ck_life_areas_priority",
        ),
        CheckConstraint(
            "current_score BETWEEN 1 AND 10",
            name="ck_life_areas_current_score",
        ),
        CheckConstraint(
            "desired_score BETWEEN 1 AND 10",
            name="ck_life_areas_desired_score",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    current_score: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    desired_score: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    goals: Mapped[list["Goal"]] = relationship(
        back_populates="life_area",
        cascade="save-update, merge",
    )


class Goal(TimestampMixin, Base):
    """Цель, связанная с жизненной сферой."""

    __tablename__ = "goals"
    __table_args__ = (
        CheckConstraint(
            "priority BETWEEN 1 AND 5",
            name="ck_goals_priority",
        ),
        CheckConstraint(
            "progress_percent BETWEEN 0 AND 100",
            name="ck_goals_progress_percent",
        ),
        CheckConstraint(
            "target_date IS NULL OR start_date IS NULL "
            "OR target_date >= start_date",
            name="ck_goals_date_order",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    life_area_id: Mapped[int] = mapped_column(
        ForeignKey("life_areas.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[date | None] = mapped_column(Date)
    target_date: Mapped[date | None] = mapped_column(Date)
    horizon: Mapped[GoalHorizon] = mapped_column(
        Enum(
            GoalHorizon,
            native_enum=False,
            create_constraint=True,
            name="goal_horizon",
            values_callable=lambda enum_class: [item.value for item in enum_class],
        ),
        nullable=False,
    )
    priority: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    status: Mapped[GoalStatus] = mapped_column(
        Enum(
            GoalStatus,
            native_enum=False,
            create_constraint=True,
            name="goal_status",
            values_callable=lambda enum_class: [item.value for item in enum_class],
        ),
        default=GoalStatus.PLANNED,
        nullable=False,
    )
    progress_percent: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    achievement_criteria: Mapped[str | None] = mapped_column(Text)
    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    life_area: Mapped[LifeArea] = relationship(back_populates="goals")
