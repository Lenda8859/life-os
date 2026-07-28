"""Загрузка визуальных ресурсов Life OS."""

from pathlib import Path

import streamlit as st

STYLES_PATH = Path(__file__).resolve().parent / "styles.css"


def load_styles() -> None:
    """Подключить локальную таблицу стилей."""
    try:
        styles = STYLES_PATH.read_text(encoding="utf-8")
    except OSError as error:
        st.warning(f"Не удалось загрузить оформление: {error}")
        return
    st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)
