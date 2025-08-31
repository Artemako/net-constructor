# Руководство по смене PNG иконок для тем

## Обзор

В проекте реализована система автоматической смены PNG иконок в зависимости от выбранной темы, аналогично тому, как это сделано в папке `auto-exec-doc`.

## Структура ресурсов

### PNG файлы для тем

- `resources/png/` - стандартные PNG иконки (используются по умолчанию)
- `resources/black-png/` - PNG иконки для темной темы
- `resources/white-png/` - PNG иконки для светлой темы

### Доступные иконки

В каждой папке содержатся следующие PNG файлы:
- `branch-closed.png` - иконка закрытой ветки дерева
- `branch-open.png` - иконка открытой ветки дерева
- `checkbox-check.png` - иконка отмеченного чекбокса
- `checkbox-check-disabled.png` - иконка отключенного отмеченного чекбокса
- `combobox-down.png` - иконка стрелки вниз для комбобокса
- `scrollbar-*.png` - иконки для скроллбаров (вверх, вниз, влево, вправо, hover, disabled)
- `sort-asc.png` - иконка сортировки по возрастанию
- `sort-desc.png` - иконка сортировки по убыванию
- `spinner-up.png` - иконка спиннера вверх
- `spinner-down.png` - иконка спиннера вниз
- `sub-menu-arrow.png` - иконка стрелки подменю
- `sub-menu-arrow-hover.png` - иконка стрелки подменю при наведении

## Использование

### В коде

```python
from package.controllers.style import Style

# Создание контроллера стилей
style_controller = Style()

# Установка темы
style_controller.set_style_for_mw_by_name(window, "dark")  # темная тема
style_controller.set_style_for_mw_by_name(window, "light") # светлая тема

# Переключение темы
new_theme = style_controller.toggle_theme()

# Применение темы ко всем окнам
style_controller.apply_theme_to_all_windows("light")

# Получение префикса для PNG ресурсов
png_prefix = style_controller.get_png_prefix("light")  # вернет "white-png"
```

### В главном приложении

Система уже интегрирована в главное приложение:

1. **Инициализация**: Контроллер стилей создается в `ObjectsManager`
2. **Применение темы**: Тема применяется при запуске приложения
3. **Смена темы**: Доступна через меню (View -> Dark Theme / Light Theme)

### В QSS стилях

В QSS стилях используются пути к PNG файлам:

```css
/* Для темной темы автоматически заменяется на black-png */
QTreeView::branch:closed:has-children {
    image: url(:/png/resources/png/branch-closed.png);
}

/* Для светлой темы автоматически заменяется на white-png */
QTreeView::branch:closed:has-children {
    image: url(:/white-png/resources/white-png/branch-closed.png);
}
```

## Автоматическая замена путей

Система автоматически заменяет пути к PNG файлам в зависимости от темы:

- `:/png/resources/png/` → `:/black-png/resources/black-png/` (для темной темы)
- `:/png/resources/png/` → `:/white-png/resources/white-png/` (для светлой темы)

## Добавление новых PNG иконок

1. Добавьте PNG файл в папки `resources/black-png/` и `resources/white-png/`
2. Обновите файл `resources.qrc`, добавив новые файлы в соответствующие секции
3. Перекомпилируйте ресурсы: `pyside6-rcc resources.qrc -o resources_rc.py`

## Тестирование

Для тестирования системы смены тем используйте файл `test_theme_switch.py`:

```bash
python test_theme_switch.py
```

Этот скрипт создает тестовое окно с кнопками для переключения тем и показывает текущий PNG префикс.

## Совместимость

Система полностью совместима с существующим кодом и не требует изменений в других частях приложения. Все существующие вызовы `setStyleSheet()` продолжат работать как прежде.
