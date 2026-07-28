"""Боковая навигация приложения."""

from collections.abc import Callable
from dataclasses import dataclass

import streamlit as st

from life_os.config import APP_SUBTITLE


@dataclass(frozen=True)
class NavigationItem:
    """Описание пункта бокового меню."""

    label: str
    icon: str
    description: str


NAVIGATION_ITEMS = (
    NavigationItem("Главная", "⌂", "Краткая сводка дня"),
    NavigationItem("Жизненные сферы", "◉", "Баланс основных направлений жизни"),
    NavigationItem("Цели", "◇", "Долгосрочные и ближайшие цели"),
    NavigationItem("Задачи", "✓", "Планы на сегодня и неделю"),
    NavigationItem("Привычки", "↻", "Регулярные действия и серии"),
    NavigationItem("Финансы", "₽", "Доходы, расходы и баланс"),
    NavigationItem("Обучение", "⌘", "Темы и учебные занятия"),
    NavigationItem("Здоровье", "♡", "Энергия, сон и настроение"),
    NavigationItem("Дневник", "✎", "Мысли, итоги и достижения"),
    NavigationItem("Итоги недели", "▦", "Обзор прогресса за неделю"),
)


def get_navigation_labels() -> tuple[str, ...]:
    """Вернуть подписи пунктов меню в порядке отображения."""
    return tuple(item.label for item in NAVIGATION_ITEMS)


def render_navigation() -> str:
    """Показать боковое меню и вернуть выбранный раздел."""
    labels = get_navigation_labels()
    icons = {item.label: item.icon for item in NAVIGATION_ITEMS}

    with st.sidebar:
        st.markdown(
            '<p class="brand">life<span>OS</span></p>',
            unsafe_allow_html=True,
        )
        st.caption(APP_SUBTITLE)
        st.markdown(
            '<p class="menu-title">МОЁ ПРОСТРАНСТВО</p>',
            unsafe_allow_html=True,
        )

        selected_page = st.radio(
            "Основные разделы",
            labels,
            format_func=lambda label: f"{icons[label]}  {label}",
            label_visibility="collapsed",
        )

        st.markdown(
            """
            <div class="sidebar-footer">
                <span class="status-dot"></span>
                Данные хранятся локально
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected_page


def render_selected_page(
    selected_page: str,
    dashboard_renderer: Callable[[], None],
) -> None:
    """Показать выбранную страницу или экран будущего модуля."""
    if selected_page == "Главная":
        dashboard_renderer()
        return

    item = next(
        item for item in NAVIGATION_ITEMS if item.label == selected_page
    )
    render_module_preview(item)


def render_module_preview(item: NavigationItem) -> None:
    """Показать спокойную заглушку для ещё не реализованного модуля."""
    st.markdown(
        f"""
        <section class="page-heading">
            <div>
                <p class="eyebrow">РАЗДЕЛ LIFE OS</p>
                <h1>{item.label}</h1>
                <p>{item.description}</p>
            </div>
            <div class="page-icon">{item.icon}</div>
        </section>
        <section class="empty-state">
            <span class="tag">СКОРО</span>
            <h2>Раздел подготовлен к разработке</h2>
            <p>
                Сейчас здесь нет форм и фиктивных данных. Функциональность
                появится на своём этапе после проектирования базы и тестов.
            </p>
            <div class="empty-state-line"></div>
            <small>Вернитесь на главную страницу через меню слева.</small>
        </section>
        """,
        unsafe_allow_html=True,
    )
