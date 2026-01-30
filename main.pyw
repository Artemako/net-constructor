"""Точка входа приложения Net Constructor."""

import os
import sys


def _parse_mode_args() -> None:
    """Разбирает --demo/--full до импорта приложения и задаёт NET_CONSTRUCTOR_MODE."""
    for arg in sys.argv[1:]:
        if arg == "--demo":
            os.environ["NET_CONSTRUCTOR_MODE"] = "demo"
            return
        if arg == "--full":
            os.environ["NET_CONSTRUCTOR_MODE"] = "full"
            return


def main() -> None:
    """Запуск приложения."""
    _parse_mode_args()
    import package.app as app
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()
