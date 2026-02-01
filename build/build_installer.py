#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт сборки установщика полной версии (Inno Setup).
Запускать после Nuitka, когда папка main.dist.full\\main.dist\\ уже заполнена:
  python build/build_installer.py
  python build/build_installer.py --iscc "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
"""

import argparse
import os
import subprocess
import sys

# Имя exe полной версии (должно совпадать с Nuitka --output-filename)
FULL_EXE_NAME = "Конструктор схем ВОЛП.exe"
# Относительно корня проекта
DIST_REL_PATH = os.path.join("main.dist.full", "main.dist", FULL_EXE_NAME)
INSTALLER_SCRIPT = os.path.join("build", "installer_full.iss")
OUTPUT_DIR = "output"
OUTPUT_BASENAME = "Конструктор схем ВОЛП Setup.exe"


def main() -> int:
    """Проверяет наличие сборки и запускает iscc."""
    parser = argparse.ArgumentParser(
        description="Собрать установщик полной версии (Inno Setup)"
    )
    parser.add_argument(
        "--iscc",
        default="iscc",
        metavar="PATH",
        help="Путь к ISCC.exe (по умолчанию: iscc из PATH)",
    )
    args = parser.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    exe_path = os.path.join(root, DIST_REL_PATH)
    script_path = os.path.join(root, INSTALLER_SCRIPT)

    if not os.path.isfile(exe_path):
        print(
            "Ошибка: не найден exe полной версии. Сначала выполните:\n"
            "  python build/build_variant.py --full\n"
            "  python -m nuitka ... (см. build/BUILD_NUITKA.md)\n"
            "Ожидаемый путь: {}".format(exe_path),
            file=sys.stderr,
        )
        return 1

    if not os.path.isfile(script_path):
        print(
            "Ошибка: не найден скрипт установщика: {}".format(script_path),
            file=sys.stderr,
        )
        return 1

    cmd = [args.iscc, INSTALLER_SCRIPT]
    try:
        subprocess.run(cmd, cwd=root, check=True)
    except FileNotFoundError:
        print(
            "Ошибка: не найден iscc. Установите Inno Setup и добавьте в PATH,\n"
            "либо укажите путь: --iscc \"C:\\...\\ISCC.exe\"",
            file=sys.stderr,
        )
        return 1
    except subprocess.CalledProcessError as e:
        print("Ошибка сборки установщика (код {}).".format(e.returncode), file=sys.stderr)
        return e.returncode

    installer_path = os.path.join(root, OUTPUT_DIR, OUTPUT_BASENAME)
    if os.path.isfile(installer_path):
        print("Установщик создан: {}".format(os.path.normpath(installer_path)))
    else:
        print("Сборка завершена. Проверьте каталог: {}".format(os.path.join(root, OUTPUT_DIR)))

    return 0


if __name__ == "__main__":
    sys.exit(main())
