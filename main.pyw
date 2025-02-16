import package.app as app
import os
import sys


def main():
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    app.App(current_directory)


if __name__ == "__main__":
    main()


# TODO По кабелю, по волокну - надписи для первой вершины

# TODO to_left_and_to_right_arrow_length
# не отображается виджет
# TypeError: 'PySide6.QtWidgets.QSpinBox.setValue' called with wrong argument types:
#   PySide6.QtWidgets.QSpinBox.setValue(str)
# Supported signatures:
#   PySide6.QtWidgets.QSpinBox.setValue(int)