import package.app as app
import os
import sys


def main():
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()


# TODO Переместить вершину

# TODO Добавить вершину не только в конец

# TODO Стрелки пропали

# TODO DELTA X, Y вершин и для названия соединения