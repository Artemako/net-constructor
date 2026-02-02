# Настройка окружения разработчика

## Требования

- **Python 3.8** (рекомендуется 3.8.10).
- ОС: Windows 10/11 (приложение ориентировано на Windows).

## Шаги

1. Клонируйте репозиторий и перейдите в корень проекта.

2. Создайте виртуальное окружение и активируйте его:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   В cmd:

   ```cmd
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

3. Установите зависимости приложения:

   ```bash
   pip install -r requirements.txt
   ```

4. Запуск из исходников:

   - Демо: `python main.pyw --demo`
   - Полная версия: `python main.pyw --full`

   Если не указать `--demo`/`--full`, режим берётся из переменной окружения `NET_CONSTRUCTOR_MODE` (значения `demo` или `full`). При отсутствии сгенерированного `package/modules/_build_config.py` и переменной окружения по умолчанию используется режим `demo`.

5. Опционально: открыть файл проекта при старте:

   ```bash
   python main.pyw --demo путь/к/файлу.nce
   ```

6. **Редактирование UI главного окна**: исходник формы главного окна — `package/ui/mainwindow.ui`. После изменений в Qt Designer регенерируйте Python-модуль из корня проекта:

   ```bash
   pyside6-uic package/ui/mainwindow.ui -o package/ui/mainwindow_ui.py
   ```

   Ручные правки в `mainwindow_ui.py` по возможности не делайте; логика и обработчики — в `package/components/mainwindow.py`.

Каталог `configs/` должен находиться рядом с запускаемым скриптом (в корне проекта при разработке). Ресурсы (иконки, шрифты) подключаются через `resources_rc.py`.
