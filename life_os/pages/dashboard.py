"""Стартовая страница Life OS."""

from datetime import date
from pathlib import Path

import streamlit as st

from life_os.config import APP_DESCRIPTION, APP_NAME, APP_SUBTITLE

STYLES_PATH = Path(__file__).resolve().parents[1] / "assets" / "styles.css"


def load_styles() -> None:
    """Подключить локальные стили стартовой страницы."""
    try:
        styles = STYLES_PATH.read_text(encoding="utf-8")
    except OSError:
        return
    st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)


def render_sidebar() -> None:
    """Показать навигацию-заглушку первой итерации."""
    with st.sidebar:
        st.markdown('<p class="brand">life<span>OS</span></p>', unsafe_allow_html=True)
        st.caption(APP_SUBTITLE)
        st.markdown("---")
        st.markdown("●  Главная")
        st.markdown("○  Жизненные сферы")
        st.markdown("○  Цели")
        st.markdown("○  Задачи")
        st.markdown("○  Привычки")
        st.markdown("○  Финансы")
        st.markdown("○  Обучение")
        st.markdown("○  Здоровье")
        st.markdown("○  Дневник")
        st.markdown("○  Итоги недели")
        st.markdown('<div class="sidebar-note">Первая итерация</div>', unsafe_allow_html=True)


def render_dashboard() -> None:
    """Отобразить минимальную главную страницу без подключения базы данных."""
    load_styles()
    render_sidebar()

    today = date.today().strftime("%d.%m.%Y")
    st.markdown(
        f"""
        <section class="hero">
            <div>
                <p class="eyebrow">{today}</p>
                <h1>{APP_NAME} <span>— {APP_SUBTITLE}</span></h1>
                <p>{APP_DESCRIPTION}</p>
            </div>
            <div class="hero-mark">✦</div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Сегодня в фокусе")
    columns = st.columns(4)
    cards = (
        ("Задачи", "—", "Появятся на этапе задач", "pink"),
        ("Привычки", "—", "Появятся на этапе привычек", "blue"),
        ("Энергия", "—", "Появится в дневнике здоровья", "yellow"),
        ("Баланс", "— ₽", "Появится на этапе финансов", "green"),
    )
    for column, (title, value, caption, color) in zip(columns, cards, strict=True):
        with column:
            st.markdown(
                f"""
                <article class="metric-card {color}">
                    <p>{title}</p>
                    <strong>{value}</strong>
                    <small>{caption}</small>
                </article>
                """,
                unsafe_allow_html=True,
            )

    left, right = st.columns((3, 2))
    with left:
        st.markdown(
            """
            <section class="content-card">
                <span class="tag">НАЧАЛО</span>
                <h3>Ваше пространство готово</h3>
                <p>
                    Сейчас работает стартовая страница. На следующих этапах
                    здесь появятся реальные цели, задачи и показатели.
                </p>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
            <section class="content-card dark">
                <span class="tag">СЛЕДУЮЩИЙ ШАГ</span>
                <h3>Основа данных</h3>
                <p>После проверки каркаса мы отдельно спроектируем и подключим базу.</p>
            </section>
            """,
            unsafe_allow_html=True,
        )
