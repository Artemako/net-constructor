# Сборка exe с Nuitka (demo и full)

Перед запуском Nuitka обязательно выполните скрипт варианта сборки: он генерирует `package/modules/_build_config.py`, от которого зависит режим (demo/full) в exe.

Имена exe должны совпадать с заголовком приложения: полная версия — «Конструктор схем ВОЛП», демо — «Конструктор схем ВОЛП (демо)» (константы в `package.constants`).

Сборка без `--onefile`: создаётся **папка** с exe, DLL и прочими модулями, плюс в неё переносятся `configs` и `resources` для запуска программы.

Флаг `--plugin-enable=pyside6` обязателен: без него Nuitka не подтянет Qt-плагины (platforms, styles и т.д.), и при запуске exe появится ошибка «no Qt platform plugin could be initialized».

При проблемах с кодировкой имён exe в PowerShell перед сборкой выполните `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` или запускайте Nuitka из cmd с `chcp 65001`.

## Демо-версия

```powershell
python build_variant.py --demo
python -m nuitka --standalone --windows-console-mode=disable --plugin-enable=pyside6 --output-dir=main.dist.demo --output-filename="Конструктор схем ВОЛП (демо).exe" --include-package=package --include-package-data=package --include-data-dir=configs=configs --include-data-dir=resources=resources main.pyw
```

В папке `main.dist.demo` будут: `Конструктор схем ВОЛП (демо).exe`, все нужные DLL/модули, а также каталоги `configs` и `resources`.

## Полная версия

```powershell
python build_variant.py --full
python -m nuitka --standalone --windows-console-mode=disable --plugin-enable=pyside6 --output-dir=main.dist.full --output-filename="Конструктор схем ВОЛП.exe" --include-package=package --include-package-data=package --include-data-dir=configs=configs --include-data-dir=resources=resources main.pyw
```

В папке `main.dist.full` будут: `Конструктор схем ВОЛП.exe`, все нужные DLL/модули, а также каталоги `configs` и `resources`.

## Запуск из исходников (без exe)

- Демо: `python main.pyw --demo`
- Полная: `python main.pyw --full`

Если не указать `--demo`/`--full`, режим берётся из переменной окружения `NET_CONSTRUCTOR_MODE` (значения `demo` или `full`). При отсутствии `_build_config.py` и переменной окружения по умолчанию используется режим `demo`.
