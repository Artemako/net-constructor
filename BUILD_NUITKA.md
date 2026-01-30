# Сборка exe с Nuitka (demo и full)

Перед запуском Nuitka обязательно выполните скрипт варианта сборки: он генерирует `package/modules/_build_config.py`, от которого зависит режим (demo/full) в exe.

Сборка без `--onefile`: создаётся **папка** с exe, DLL и прочими модулями, плюс в неё переносятся `configs` и `resources` для запуска программы.

Флаг `--plugin-enable=pyside6` обязателен: без него Nuitka не подтянет Qt-плагины (platforms, styles и т.д.), и при запуске exe появится ошибка «no Qt platform plugin could be initialized».

## Демо-версия

```powershell
python build_variant.py --demo
python -m nuitka --standalone --windows-console-mode=disable --plugin-enable=pyside6 --output-dir=main.dist.demo --output-filename=main_demo.exe --include-package=package --include-package-data=package --include-data-dir=configs=configs --include-data-dir=resources=resources main.pyw
```

В папке `main.dist.demo` будут: `main_demo.exe`, все нужные DLL/модули, а также каталоги `configs` и `resources`.

## Полная версия

```powershell
python build_variant.py --full
python -m nuitka --standalone --windows-console-mode=disable --plugin-enable=pyside6 --output-dir=main.dist.full --output-filename=main_full.exe --include-package=package --include-package-data=package --include-data-dir=configs=configs --include-data-dir=resources=resources main.pyw
```

В папке `main.dist.full` будут: `main_full.exe`, все нужные DLL/модули, а также каталоги `configs` и `resources`.

## Запуск из исходников (без exe)

- Демо: `python main.pyw --demo`
- Полная: `python main.pyw --full`

Если не указать `--demo`/`--full`, режим берётся из переменной окружения `NET_CONSTRUCTOR_MODE` (значения `demo` или `full`). При отсутствии `_build_config.py` и переменной окружения по умолчанию используется режим `demo`.
