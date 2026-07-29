"""Постоянные настройки стартовой версии Life OS."""

from pathlib import Path

APP_NAME = "Life OS"
APP_SUBTITLE = "Моя новая жизнь"
APP_DESCRIPTION = (
    "Спокойное пространство для целей, привычек и осознанных изменений."
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "life_os.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"
