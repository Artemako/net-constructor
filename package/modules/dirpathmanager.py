"""Централизованное управление путями приложения (директория приложения)."""

from typing import Optional


class DirPathManager:
    """Хранит и возвращает базовый путь к директории приложения."""

    def __init__(self) -> None:
        self.__dir_app: Optional[str] = None

    def set_dir_app(self, dir_app: str) -> None:
        """Устанавливает директорию приложения."""
        self.__dir_app = dir_app

    def get_dir_app(self) -> Optional[str]:
        """Возвращает директорию приложения."""
        return self.__dir_app
