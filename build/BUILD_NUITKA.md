# Сборка exe с Nuitka (demo и full)

Перед запуском Nuitka обязательно выполните скрипт варианта сборки: он генерирует `package/modules/_build_config.py`, от которого зависит режим (demo/full) в exe.

Имена exe должны совпадать с заголовком приложения: полная версия — «Конструктор схем ВОЛП», демо — «Конструктор схем ВОЛП (демо)» (константы в `package.constants`).

Сборка без `--onefile`: создаётся **папка** с exe, DLL и прочими модулями, плюс в неё переносится каталог `configs` для запуска программы. Ресурсы приложения (иконки, шрифты и т.д.) уже встроены в exe через `resources_rc.py`. Для отображения иконки exe в проводнике Windows нужен файл `resources/app-icon.ico` (см. флаг `--windows-icon-from-ico`).

Флаг `--plugin-enable=pyside6` обязателен: без него Nuitka не подтянет Qt-плагины (platforms, styles и т.д.), и при запуске exe появится ошибка «no Qt platform plugin could be initialized».

При проблемах с кодировкой имён exe в PowerShell перед сборкой выполните `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` или запускайте Nuitka из cmd с `chcp 65001`.

## Демо-версия

```powershell
python build/build_variant.py --demo
python -m nuitka --standalone --windows-console-mode=disable --plugin-enable=pyside6 --output-dir=main.dist.demo --output-filename="Конструктор схем ВОЛП (демо).exe" --include-package=package --include-package-data=package --include-data-dir=configs=configs --windows-icon-from-ico=resources/app-icon.ico main.pyw
```

В папке `main.dist.demo` будут: `Конструктор схем ВОЛП (демо).exe`, все нужные DLL/модули и каталог `configs`.

## Полная версия

```powershell
python build/build_variant.py --full
python -m nuitka --standalone --windows-console-mode=disable --plugin-enable=pyside6 --output-dir=main.dist.full --output-filename="Конструктор схем ВОЛП.exe" --include-package=package --include-package-data=package --include-data-dir=configs=configs --windows-icon-from-ico=resources/app-icon.ico main.pyw
```

В папке `main.dist.full` будут: `Конструктор схем ВОЛП.exe`, все нужные DLL/модули и каталог `configs`.

## Установщик полной версии

После сборки полной версии (Nuitka) можно создать один exe-установщик с помощью [Inno Setup](https://jrsoftware.org/isinfo.php).

**Требования:** установленный Inno Setup (в PATH должен быть `iscc.exe`, либо путь задаётся вручную).

**Сборка установщика** (из корня проекта):

```powershell
python build/build_installer.py
```

Если `iscc` не в PATH:

```powershell
python build/build_installer.py --iscc "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```

Скрипт проверяет наличие `main.dist.full\main.dist\Конструктор схем ВОЛП.exe` и запускает `iscc build/installer_full.iss`. Итоговый установщик создаётся в папке `output\` и называется `Конструктор схем ВОЛП Setup.exe`.

Ручной запуск Inno Setup (без скрипта):

```powershell
iscc build/installer_full.iss
```

Настройки установщика (иконка, ярлыки, опциональная ассоциация .nce) заданы в `build/installer_full.iss`.

## Запуск из исходников (без exe)

- Демо: `python main.pyw --demo`
- Полная: `python main.pyw --full`

Если не указать `--demo`/`--full`, режим берётся из переменной окружения `NET_CONSTRUCTOR_MODE` (значения `demo` или `full`). При отсутствии `_build_config.py` и переменной окружения по умолчанию используется режим `demo`.
