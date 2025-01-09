import package.app as app
import os
import sys


def main():
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()

# TODO Замена типа диаграммы

# TODO Сохранить КАК

# TODO bool для 0 м (по левому правому краю)
# TODO Если прямоугольник то изменить центр текста для Секции