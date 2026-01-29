# undojournal.py
# Журнал событий для отмены/повтора изменений в виджетах проекта.

import copy
from collections import namedtuple


def _deep_copy_value(value):
    """Возвращает глубокую копию значения для хранения в журнале."""
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return copy.deepcopy(value)
    return value


# Запись журнала: тип, вкладка, контекст, идентификатор виджета, старое/новое значение.
# form: dict_name (str), key (str), widget_type (str)
# table_cell: table_id (str), row (int), col (int)
# diagram_type: нет доп. полей
# table_row_add: table_id (str), row_data (dict)
# table_row_delete: table_id (str), row_data (dict), row_index (int)
# table_row_reorder: table_id (str), old_order (list), new_order (list)
# table_row_add_pair: node_data (dict), connection_data (dict) - атомарная операция для узла+соединения
JournalEntry = namedtuple(
    "JournalEntry",
    ["entry_type", "tab_index", "context", "old_value", "new_value"]
    + ["dict_name", "key", "widget_type", "table_id", "row", "col", "row_data", "row_index", "node_data", "connection_data"],
    defaults=[None, None, None, None, None, None, None, None, None, None],
)


def _make_form_entry(tab_index, context, dict_name, key, widget_type, old_value, new_value):
    return JournalEntry(
        entry_type="form",
        tab_index=tab_index,
        context=context,
        old_value=_deep_copy_value(old_value),
        new_value=_deep_copy_value(new_value),
        dict_name=dict_name,
        key=key,
        widget_type=widget_type,
    )


def _make_table_cell_entry(tab_index, context, table_id, row, col, old_value, new_value):
    return JournalEntry(
        entry_type="table_cell",
        tab_index=tab_index,
        context=context,
        old_value=_deep_copy_value(old_value),
        new_value=_deep_copy_value(new_value),
        table_id=table_id,
        row=row,
        col=col,
    )


def _make_diagram_type_entry(tab_index, old_value, new_value):
    return JournalEntry(
        entry_type="diagram_type",
        tab_index=tab_index,
        context=None,
        old_value=_deep_copy_value(old_value),
        new_value=_deep_copy_value(new_value),
    )


def _make_table_row_add_entry(tab_index, context, table_id, row_data):
    """Создает запись о добавлении строки в таблицу"""
    return JournalEntry(
        entry_type="table_row_add",
        tab_index=tab_index,
        context=context,
        old_value=None,
        new_value=None,
        table_id=table_id,
        row_data=_deep_copy_value(row_data),
    )


def _make_table_row_delete_entry(tab_index, context, table_id, row_data, row_index):
    """Создает запись об удалении строки из таблицы"""
    return JournalEntry(
        entry_type="table_row_delete",
        tab_index=tab_index,
        context=context,
        old_value=None,
        new_value=None,
        table_id=table_id,
        row_data=_deep_copy_value(row_data),
        row_index=row_index,
    )


def _make_table_row_reorder_entry(tab_index, context, table_id, old_order, new_order):
    """Создает запись об изменении порядка строк в таблице"""
    return JournalEntry(
        entry_type="table_row_reorder",
        tab_index=tab_index,
        context=context,
        old_value=_deep_copy_value(old_order),
        new_value=_deep_copy_value(new_order),
        table_id=table_id,
    )


def _make_table_row_add_pair_entry(tab_index, context, node_data, connection_data):
    """Создает запись о добавлении пары узел+соединение (атомарная операция)"""
    return JournalEntry(
        entry_type="table_row_add_pair",
        tab_index=tab_index,
        context=context,
        old_value=None,
        new_value=None,
        node_data=_deep_copy_value(node_data),
        connection_data=_deep_copy_value(connection_data),
    )


class UndoJournal:
    """Журнал изменений в виджетах с поддержкой отмены (Undo) и повтора (Redo)."""

    def __init__(self, max_size=100):
        self.undo_stack = []
        self.redo_stack = []
        self.max_size = max_size

    def record_form_change(
        self, tab_index, context, dict_name, key, widget_type, old_value, new_value
    ):
        entry = _make_form_entry(
            tab_index, context, dict_name, key, widget_type, old_value, new_value
        )
        self._push_undo(entry)

    def record_table_cell_change(
        self, tab_index, context, table_id, row, col, old_value, new_value
    ):
        entry = _make_table_cell_entry(
            tab_index, context, table_id, row, col, old_value, new_value
        )
        self._push_undo(entry)

    def record_diagram_type_change(self, tab_index, old_value, new_value):
        entry = _make_diagram_type_entry(tab_index, old_value, new_value)
        self._push_undo(entry)

    def record_table_row_add(self, tab_index, context, table_id, row_data):
        """Записывает добавление строки в таблицу"""
        entry = _make_table_row_add_entry(tab_index, context, table_id, row_data)
        self._push_undo(entry)

    def record_table_row_delete(self, tab_index, context, table_id, row_data, row_index):
        """Записывает удаление строки из таблицы"""
        entry = _make_table_row_delete_entry(
            tab_index, context, table_id, row_data, row_index
        )
        self._push_undo(entry)

    def record_table_row_reorder(self, tab_index, context, table_id, old_order, new_order):
        """Записывает изменение порядка строк в таблице"""
        entry = _make_table_row_reorder_entry(
            tab_index, context, table_id, old_order, new_order
        )
        self._push_undo(entry)

    def record_table_row_add_pair(self, tab_index, context, node_data, connection_data):
        """Записывает добавление пары узел+соединение как атомарную операцию"""
        entry = _make_table_row_add_pair_entry(
            tab_index, context, node_data, connection_data
        )
        self._push_undo(entry)

    def _push_undo(self, entry):
        self.redo_stack.clear()
        self.undo_stack.append(entry)
        while len(self.undo_stack) > self.max_size:
            self.undo_stack.pop(0)

    def can_undo(self):
        return len(self.undo_stack) > 0

    def can_redo(self):
        return len(self.redo_stack) > 0

    def pop_undo(self):
        if not self.undo_stack:
            return None
        return self.undo_stack.pop()

    def push_redo(self, entry):
        self.redo_stack.append(entry)

    def pop_redo(self):
        if not self.redo_stack:
            return None
        return self.redo_stack.pop()

    def push_undo(self, entry):
        self.undo_stack.append(entry)

    def clear(self):
        """Очищает оба журнала (undo и redo)."""
        self.undo_stack.clear()
        self.redo_stack.clear()
