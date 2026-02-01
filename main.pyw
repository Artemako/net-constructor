"""Точка входа приложения "Конструктор схем ВОЛП"."""

import os
import sys
from typing import Optional


def _parse_mode_args() -> None:
    """Разбирает --demo/--full до импорта приложения и задаёт NET_CONSTRUCTOR_MODE."""
    for arg in sys.argv[1:]:
        if arg == "--demo":
            os.environ["NET_CONSTRUCTOR_MODE"] = "demo"
            return
        if arg == "--full":
            os.environ["NET_CONSTRUCTOR_MODE"] = "full"
            return


def _get_file_to_open_from_argv() -> Optional[str]:
    """Из аргументов командной строки возвращает путь к .nce для открытия при старте (или None)."""
    for arg in sys.argv[1:]:
        if arg in ("--demo", "--full"):
            continue
        path = arg.strip().strip('"').strip("'")
        if path.lower().endswith(".nce") and os.path.isfile(path):
            return os.path.abspath(path)
    return None


def main() -> None:
    """Запуск приложения."""
    _parse_mode_args()
    file_to_open = _get_file_to_open_from_argv()
    import package.app as app
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory, file_to_open=file_to_open)


if __name__ == "__main__":
    main()



# 