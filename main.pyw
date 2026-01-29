import package.app as app
import os
import sys


def main():
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()

# ЛЮБОЕ ИЗМЕНЕНИЕ В ВИДЖЕТЕ СОХРАНЯТЬ, НО НЕ ОБНОВЛЯТЬ РЕЗУЛЬТАТ
# ЖУРНАЛ СОБЫТИЙ С ВОЗМОЖНОСТЬЮ ОТКАТА
# is_demo - сразу открыт постановочный файл без возможности сохранения его + ограничение по времени в 60 минут
# НАДПИСИ SAMPLE ПОВЕРХ

# undojournal в obsm