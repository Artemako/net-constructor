"""Диалог управления списком кабелей: редактирование, сброс, сохранение."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class CableListsDialog(QDialog):
    """Диалог для управления списком кабелей."""

    def __init__(self, obsm, parent=None) -> None:
        super().__init__(parent)
        self.__obsm = obsm
        self.__configs = obsm.obj_configs
        self.__current_cables = []
        self.__original_cables = []  # Сохраняем исходный список для восстановления
        
        self.setWindowTitle("Управление списком кабелей")
        self.setModal(True)
        self.resize(600, 500)
        
        self.setup_ui()
        self.setup_connections()
        self.load_data()
        
    def setup_ui(self) -> None:
        """Настройка интерфейса диалога."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Группа редактирования списка кабелей
        edit_group = QGroupBox("Список кабелей")
        edit_layout = QVBoxLayout()
        edit_layout.setContentsMargins(10, 10, 10, 10)
        edit_layout.setSpacing(10)
        
        # Текстовое поле для редактирования
        self.cables_text = QTextEdit()
        self.cables_text.setPlaceholderText("Введите кабели, каждый с новой строки")
        self.cables_text.setMinimumHeight(200)
        self.cables_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        edit_layout.addWidget(self.cables_text)
        
        edit_group.setLayout(edit_layout)
        main_layout.addWidget(edit_group)
        
        # Группа управления
        control_group = QGroupBox("Управление списком")
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(10, 10, 10, 10)
        control_layout.setSpacing(10)
        
        self.add_cable_btn = QPushButton("Добавить кабель")
        self.clear_cables_btn = QPushButton("Очистить")
        self.restore_default_btn = QPushButton("По умолчанию")
        
        # Добавляем подсказки
        self.add_cable_btn.setToolTip("Добавить новый кабель в список")
        self.clear_cables_btn.setToolTip("Очистить весь список кабелей")
        self.restore_default_btn.setToolTip("Восстановить список кабелей по умолчанию")
        
        control_layout.addWidget(self.add_cable_btn)
        control_layout.addWidget(self.clear_cables_btn)
        control_layout.addWidget(self.restore_default_btn)
        control_layout.addStretch()
        
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)
        
        # Кнопки диалога
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        buttons_layout.setSpacing(10)
        
        buttons_layout.addStretch()
        
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        # Устанавливаем русские названия для кнопок
        button_box.button(QDialogButtonBox.Ok).setText("Сохранить")
        button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        
        buttons_layout.addWidget(button_box)
        
        main_layout.addLayout(buttons_layout)
        
        # Устанавливаем политику изменения размера
        self.setMinimumSize(500, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def setup_connections(self):
        """Настройка связей между элементами"""
        button_box = self.findChild(QDialogButtonBox)
        if button_box:
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)
            
        self.add_cable_btn.clicked.connect(self.add_cable)
        self.clear_cables_btn.clicked.connect(self.clear_cables)
        self.restore_default_btn.clicked.connect(self.restore_default_cables)
        self.cables_text.textChanged.connect(self.on_cables_changed)
        
    def load_data(self):
        """Загрузка данных"""
        self.__current_cables = self.__configs.get_list_by_type("cable_types")
        
        # Загружаем исходные данные по умолчанию
        default_cables = ["Марка ВОК 1", "Марка ВОК 2", "Марка ВОК 3"]
        self.__original_cables = default_cables.copy()
        
        self.cables_text.setPlainText("\n".join(self.__current_cables))
        
    def on_cables_changed(self):
        """Обработчик изменения списка кабелей"""
        text = self.cables_text.toPlainText()
        self.__current_cables = [line.strip() for line in text.split('\n') if line.strip()]
        
    def add_cable(self):
        """Добавляет новый кабель"""
       
        # Создаем собственный диалог для ввода
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить кабель")
        dialog.setModal(True)
        dialog.resize(300, 100)
        
        layout = QVBoxLayout(dialog)
        
        # Поле ввода
        label = QLabel("Введите название кабеля:")
        layout.addWidget(label)
        
        input_field = QLineEdit()
        layout.addWidget(input_field)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Добавить")
        cancel_button = QPushButton("Отмена")
        
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)
        
        # Подключаем сигналы
        add_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        input_field.returnPressed.connect(dialog.accept)
        
        # Устанавливаем фокус на поле ввода
        input_field.setFocus()
        
        # Показываем диалог
        if dialog.exec() == QDialog.Accepted:
            cable_name = input_field.text().strip()
            if cable_name:
                current_text = self.cables_text.toPlainText()
                if current_text:
                    current_text += "\n"
                current_text += cable_name
                self.cables_text.setPlainText(current_text)
            
    def clear_cables(self):
        """Очищает список кабелей"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText("Вы уверены, что хотите очистить список кабелей?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # Заменяем текст кнопок на русский
        msg_box.button(QMessageBox.Yes).setText("Да")
        msg_box.button(QMessageBox.No).setText("Нет")
        
        reply = msg_box.exec()
        
        if reply == QMessageBox.Yes:
            self.cables_text.clear()
            
    def restore_default_cables(self):
        """Восстанавливает список кабелей по умолчанию"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText("Восстановить список кабелей по умолчанию? Текущий список будет заменен.")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # Заменяем текст кнопок на русский
        msg_box.button(QMessageBox.Yes).setText("Да")
        msg_box.button(QMessageBox.No).setText("Нет")
        
        reply = msg_box.exec()
        
        if reply == QMessageBox.Yes:
            # Восстанавливаем список по умолчанию
            if self.__original_cables:
                self.cables_text.setPlainText("\n".join(self.__original_cables))
            else:
                self.cables_text.clear()
            
    def accept(self):
        """Обработчик нажатия OK"""
        # Сохраняем изменения
        self.__configs.update_list_by_type("cable_types", self.__current_cables)
        self.__configs.save_lists(self.__obsm.obj_dirpath.get_dir_app())
        super().accept()
