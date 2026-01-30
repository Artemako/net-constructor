"""Диалог управления списком названий секторов: редактирование, сброс, сохранение."""

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


class SectorNamesDialog(QDialog):
    """Диалог для управления списком названий секторов."""

    def __init__(self, obsm, parent=None) -> None:
        super().__init__(parent)
        self.__obsm = obsm
        self.__configs = obsm.obj_configs
        self.__current_sector_names = []
        self.__original_sector_names = [] 
        
        self.setWindowTitle("Управление списком названий секторов")
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
        
        # Группа редактирования списка названий секторов
        edit_group = QGroupBox("Список названий секторов")
        edit_layout = QVBoxLayout()
        edit_layout.setContentsMargins(10, 10, 10, 10)
        edit_layout.setSpacing(10)
        
        # Текстовое поле для редактирования
        self.sector_names_text = QTextEdit()
        self.sector_names_text.setPlaceholderText("Введите названия секторов, каждый с новой строки")
        self.sector_names_text.setMinimumHeight(200)
        self.sector_names_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        edit_layout.addWidget(self.sector_names_text)
        
        edit_group.setLayout(edit_layout)
        main_layout.addWidget(edit_group)
        
        # Группа управления
        control_group = QGroupBox("Управление списком")
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(10, 10, 10, 10)
        control_layout.setSpacing(10)
        
        self.add_sector_name_btn = QPushButton("Добавить название")
        self.clear_sector_names_btn = QPushButton("Очистить")
        self.restore_default_btn = QPushButton("По умолчанию")
        
        # Добавляем подсказки
        self.add_sector_name_btn.setToolTip("Добавить новое название сектора в список")
        self.clear_sector_names_btn.setToolTip("Очистить весь список названий секторов")
        self.restore_default_btn.setToolTip("Восстановить список названий секторов по умолчанию")
        
        control_layout.addWidget(self.add_sector_name_btn)
        control_layout.addWidget(self.clear_sector_names_btn)
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
            
        self.add_sector_name_btn.clicked.connect(self.add_sector_name)
        self.clear_sector_names_btn.clicked.connect(self.clear_sector_names)
        self.restore_default_btn.clicked.connect(self.restore_default_sector_names)
        self.sector_names_text.textChanged.connect(self.on_sector_names_changed)
        
    def load_data(self):
        """Загрузка данных"""
        self.__current_sector_names = self.__configs.get_list_by_type("sector_names")
        
        # Загружаем исходные данные по умолчанию
        default_sector_names = ["По опорам", "В грунте", "По зданию"]
        self.__original_sector_names = default_sector_names.copy()
        
        self.sector_names_text.setPlainText("\n".join(self.__current_sector_names))
        
    def on_sector_names_changed(self):
        """Обработчик изменения списка названий секторов"""
        text = self.sector_names_text.toPlainText()
        self.__current_sector_names = [line.strip() for line in text.split('\n') if line.strip()]
        
    def add_sector_name(self):
        """Добавляет новое название сектора"""
       
        # Создаем собственный диалог для ввода
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить название сектора")
        dialog.setModal(True)
        dialog.resize(300, 100)
        
        layout = QVBoxLayout(dialog)
        
        # Поле ввода
        label = QLabel("Введите название сектора:")
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
            sector_name = input_field.text().strip()
            if sector_name:
                current_text = self.sector_names_text.toPlainText()
                if current_text:
                    current_text += "\n"
                current_text += sector_name
                self.sector_names_text.setPlainText(current_text)
            
    def clear_sector_names(self):
        """Очищает список названий секторов"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText("Вы уверены, что хотите очистить список названий секторов?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # Заменяем текст кнопок на русский
        msg_box.button(QMessageBox.Yes).setText("Да")
        msg_box.button(QMessageBox.No).setText("Нет")
        
        reply = msg_box.exec()
        
        if reply == QMessageBox.Yes:
            self.sector_names_text.clear()
            
    def restore_default_sector_names(self):
        """Восстанавливает список названий секторов по умолчанию"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText("Восстановить список названий секторов по умолчанию? Текущий список будет заменен.")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        # Заменяем текст кнопок на русский
        msg_box.button(QMessageBox.Yes).setText("Да")
        msg_box.button(QMessageBox.No).setText("Нет")
        
        reply = msg_box.exec()
        
        if reply == QMessageBox.Yes:
            # Восстанавливаем список по умолчанию
            if self.__original_sector_names:
                self.sector_names_text.setPlainText("\n".join(self.__original_sector_names))
            else:
                self.sector_names_text.clear()
            
    def accept(self):
        """Обработчик нажатия OK"""
        # Сохраняем изменения
        self.__configs.update_list_by_type("sector_names", self.__current_sector_names)
        self.__configs.save_lists(self.__obsm.obj_dirpath.get_dir_app())
        super().accept()
