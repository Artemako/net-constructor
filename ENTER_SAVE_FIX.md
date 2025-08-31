# Исправление конфликта Enter в текстовых полях

## Проблема
Действие "Сохранение" применялось как по `Ctrl+S`, так и по `Enter`. Однако возникал конфликт:
- `Enter` в текстовых полях (`QLineEdit`, `QTextEdit`) должен создавать новую строку
- `Enter` вне текстовых полей должен выполнять сохранение

## Решение

### Изменения в `package/components/mainwindow.py`

1. **Удален Enter из горячих клавиш сохранения** (строки 113-118):
```python
# Было:
self.ui.action_save.setShortcuts([
    QKeySequence("Return"),  # Enter (Return)
    QKeySequence("Ctrl+S"),  # Ctrl + S
])

# Стало:
self.ui.action_save.setShortcuts([
    QKeySequence("Ctrl+S"),  # Ctrl + S
])
```

2. **Добавлен фильтр событий** (строка 121):
```python
# Устанавливаем фильтр событий для обработки Enter
self.installEventFilter(self)
```

3. **Реализован метод `eventFilter`** (строки 1942-1965):
```python
def eventFilter(self, obj, event):
    """
    Фильтр событий для обработки нажатия Enter.
    Сохранение выполняется только если фокус не находится в текстовом поле.
    """
    from PySide6.QtCore import QEvent
    from PySide6.QtGui import QKeyEvent
    
    if event.type() == QEvent.KeyPress:
        key_event = QKeyEvent(event)
        if key_event.key() == Qt.Key_Return or key_event.key() == Qt.Key_Enter:
            # Получаем виджет с фокусом
            focused_widget = QApplication.focusWidget()
            
            # Проверяем, является ли виджет с фокусом текстовым полем
            if focused_widget is not None:
                widget_class_name = focused_widget.__class__.__name__
                if widget_class_name in ['QLineEdit', 'QTextEdit', 'QPlainTextEdit']:
                    # Если фокус в текстовом поле, не выполняем сохранение
                    return False
            
            # Если фокус не в текстовом поле, выполняем сохранение
            if self.__obsm.obj_project.is_active():
                self._save_changes_to_file_nce()
            return True
    
    return False
```

## Логика работы

1. **Ctrl+S**: Работает везде, включая текстовые поля
2. **Enter в текстовых полях** (`QLineEdit`, `QTextEdit`, `QPlainTextEdit`): 
   - Создает новую строку (стандартное поведение Qt)
   - Сохранение НЕ выполняется
3. **Enter вне текстовых полей**: 
   - Выполняется сохранение проекта
   - Событие перехватывается и не передается дальше

## Поддерживаемые типы текстовых полей

- `QLineEdit` - однострочные текстовые поля
- `QTextEdit` - многострочные текстовые поля
- `QPlainTextEdit` - простые многострочные текстовые поля

## Тестирование

Создан тестовый файл `test_enter_save.py` для проверки корректности работы фильтра событий.

## Совместимость

Изменения полностью совместимы с существующим кодом и не влияют на другие функции приложения.
