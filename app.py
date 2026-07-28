"""Точка входа в локальное приложение Life OS."""

from life_os.assets import load_styles
from life_os.navigation import render_navigation, render_selected_page
from life_os.pages.dashboard import render_dashboard


def main() -> None:
    """Настроить Streamlit и показать стартовую страницу."""
    import streamlit as st

    st.set_page_config(
        page_title="Life OS — Моя новая жизнь",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    load_styles()
    selected_page = render_navigation()
    render_selected_page(selected_page, dashboard_renderer=render_dashboard)


if __name__ == "__main__":
    main()
