"""Первый тест минимального каркаса."""

from life_os import __version__
from life_os.config import APP_NAME, APP_SUBTITLE


def test_application_metadata() -> None:
    """Основные сведения о приложении должны быть определены."""
    assert APP_NAME == "Life OS"
    assert APP_SUBTITLE == "Моя новая жизнь"
    assert __version__ == "0.1.0"
