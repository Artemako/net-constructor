import package.app as app
import os
import sys


def main():
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()

# TODO Замена типа диаграммы

# TODO Переделпть "is_global" на два отдельных параметра


# TODO Стрелки переноса wrap
# TODO  Типы для виджетов
# TODO Вершина Со стрелкой влево вверх