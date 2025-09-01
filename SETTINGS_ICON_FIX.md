# Исправление проблемы с иконкой настроек

## Описание проблемы
При попытке использовать иконку `settings.svg` для действия "Настройки" возникала ошибка:
```
qt.svg: Cannot open file ':/white-icons/resources/white-icons/settings.svg', because: No such file or directory
qt.svg: Cannot open file ':/black-icons/resources/black-icons/settings.svg', because: No such file or directory
```

## Причина проблемы
Иконка `settings.svg` существовала в файловой системе в папках:
- `resources/black-icons/settings.svg`
- `resources/white-icons/settings.svg`

Но не была зарегистрирована в файле ресурсов `resources.qrc`, поэтому Qt не мог её найти.

## Решение

### 1. Добавление иконок в файл ресурсов
**Файл:** `resources.qrc`

Добавлены строки:
```xml
<!-- В секции white-icons -->
<file>resources/white-icons/settings.svg</file>

<!-- В секции black-icons -->
<file>resources/black-icons/settings.svg</file>
```

### 2. Пересборка файла ресурсов
Выполнена команда:
```bash
pyside6-rcc resources.qrc -o resources_rc.py
```

### 3. Обновление контроллера иконок
**Файл:** `package/controllers/icons.py`

Изменена строка:
```python
# Было:
(mw.ui.action_settings, f":/{icon_set}/resources/{icon_set}/show-properties.svg"),

# Стало:
(mw.ui.action_settings, f":/{icon_set}/resources/{icon_set}/settings.svg"),
```

### 4. Обновление UI файла
**Файл:** `package/ui/mainwindow_ui.py`

Изменена строка:
```python
# Было:
self.action_settings = QAction(QIcon(":/white-icons/resources/white-icons/show-properties.svg"), "Настройки", MainWindow)

# Стало:
self.action_settings = QAction(QIcon(":/white-icons/resources/white-icons/settings.svg"), "Настройки", MainWindow)
```

## Результат
Теперь иконка `settings.svg` корректно отображается для действия "Настройки" и меняется при смене темы:
- **Тёмная тема**: белая иконка `settings.svg`
- **Светлая тема**: чёрная иконка `settings.svg`

## Важное замечание
При добавлении новых иконок в проект всегда нужно:
1. Поместить файлы иконок в соответствующие папки (`black-icons` и `white-icons`)
2. Добавить их в файл `resources.qrc`
3. Пересобрать ресурсы командой `pyside6-rcc resources.qrc -o resources_rc.py`
