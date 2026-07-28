"""Первый тест минимального каркаса."""

from streamlit.testing.v1 import AppTest

from life_os import __version__
from life_os.config import APP_NAME, APP_SUBTITLE
from life_os.navigation import get_navigation_labels


def test_application_metadata() -> None:
    """Основные сведения о приложении должны быть определены."""
    assert APP_NAME == "Life OS"
    assert APP_SUBTITLE == "Моя новая жизнь"
    assert __version__ == "0.1.0"


def test_navigation_contains_expected_sections() -> None:
    """Меню должно содержать все запланированные разделы без повторений."""
    labels = get_navigation_labels()

    assert labels[0] == "Главная"
    assert "Цели" in labels
    assert "Итоги недели" in labels
    assert len(labels) == 10
    assert len(labels) == len(set(labels))


def test_user_can_open_goals_section() -> None:
    """Выбор пункта меню должен переключать содержимое страницы."""
    app = AppTest.from_file("app.py").run()

    assert not app.exception
    assert len(app.radio) == 1

    app.radio[0].set_value("Цели").run()

    assert not app.exception
    assert app.radio[0].value == "Цели"
    assert any("Цели" in element.value for element in app.markdown)
