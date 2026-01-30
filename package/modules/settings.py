"""Настройки приложения через QSettings: тема, проекты, параметры, журнал отмены."""

import datetime
import os

from PySide6.QtCore import QSettings


class SettingsManagerObjectsManager:
    """Хранит ссылки на объекты, нужные Settings (логгер, пути)."""

    def __init__(self, osbm) -> None:
        self.obj_logg = osbm.obj_logg if hasattr(osbm, 'obj_logg') else None
        self.obj_dirpath = osbm.obj_dirpath if hasattr(osbm, 'obj_dirpath') else None


class Settings:
    """Доступ к настройкам приложения (QSettings): тема, проекты, параметры, журнал."""

    def __init__(self) -> None:
        self.__theme_display_names = {
            "dark": "Тёмная",
            "light": "Светлая"
        }
        self.__theme_keys_by_display = {v: k for k, v in self.__theme_display_names.items()}

    def setting_osbm(self, osbm):
        """Сохраняем метод setting_osbm как в оригинальном SettingsDatabase"""
        self.__osbm = SettingsManagerObjectsManager(osbm)
        self.__settings = QSettings("Constant", "Net-constructor")
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger("Settings setting_osbm() completed")

    def initialize_default_settings(self):
        """Инициализация настроек по умолчанию"""
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger("Settings initialize_default_settings()")

        # Устанавливаем значения по умолчанию, если они еще не существуют
        if not self.__settings.contains("theme"):
            self.__settings.setValue("theme", "dark")

        if not self.__settings.contains("project_current_name"):
            self.__settings.setValue("project_current_name", "")

        # иниц. список проектов, если его нет
        if not self.__settings.contains("projects"):
            self.__settings.setValue("projects", [])

        # настройка отображения параметров
        if not self.__settings.contains("show_parameters"):
            self.__settings.setValue("show_parameters", False)

        # лимит журнала отмены/повтора (1–1000, по умолчанию 100)
        if not self.__settings.contains("journal_limit"):
            self.__settings.setValue("journal_limit", 100)



    # region Методы для работы с темой

    def get_theme(self) -> str:
        """Возвращает внутренний ключ темы (dark/light)"""
        result = self.__settings.value("theme", "dark")
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings get_theme(): {result}")
        return result

    def get_theme_display_name(self) -> str:
        """Возвращает русское название текущей темы"""
        theme_key = self.get_theme()
        return self.__theme_display_names.get(theme_key, "Тёмная")

    def set_theme_by_display_name(self, display_name: str):
        """Устанавливает тему по русскому названию, сохраняет английский ключ"""
        theme_key = self.__theme_keys_by_display.get(display_name, "dark")
        self.set_theme(theme_key)

    def set_theme(self, theme: str):
        """Сохраняет тему как 'dark' или 'light'"""
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings set_theme(): {theme}")
        self.__settings.setValue("theme", theme)

    # endregion

    # region Методы для работы с настройками

    def get_project_current_name(self) -> str:
        """Получить имя текущего проекта"""
        result = self.__settings.value("project_current_name", "")
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings get_project_current_name(): {result}")
        return result

    def set_project_current_name(self, project_name: str):
        """Установить имя текущего проекта"""
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings set_project_current_name(): {project_name}")
        self.__settings.setValue("project_current_name", project_name)

    def get_show_parameters(self) -> bool:
        """Получить настройку отображения параметров"""
        result = self.__settings.value("show_parameters", False, type=bool)
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings get_show_parameters(): {result}")
        return result

    def set_show_parameters(self, show: bool):
        """Установить настройку отображения параметров"""
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings set_show_parameters(): {show}")
        self.__settings.setValue("show_parameters", show)

    def get_journal_limit(self) -> int:
        """Получить лимит журнала (1–1000, по умолчанию 100)"""
        result = self.__settings.value("journal_limit", 100)
        if result is None:
            result = 100
        try:
            result = int(result)
        except (TypeError, ValueError):
            result = 100
        result = max(1, min(1000, result))
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings get_journal_limit(): {result}")
        return result

    def set_journal_limit(self, limit: int):
        """Установить лимит журнала (1–1000)"""
        limit = max(1, min(1000, limit))
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings set_journal_limit(): {limit}")
        self.__settings.setValue("journal_limit", limit)

    # endregion

    # region Методы для работы с проектами

    def add_or_update_project(self, project_dir: str = None):
        """Основной метод для добавления/обновления проекта"""
        if project_dir is None and self.__osbm.obj_dirpath:
            project_dir = self.__osbm.obj_dirpath.get_dir_app()

        if not project_dir:
            return

        projects = self.get_projects()
        project_name = os.path.basename(project_dir)
        current_datetime = datetime.datetime.now().replace(microsecond=0).isoformat()

        # Ищем существующий проект
        existing_project = None
        for i, project in enumerate(projects):
            if project.get("directory_project") == project_dir:
                existing_project = i
                break

        project_data = {
            "name_project": project_name,
            "directory_project": project_dir,
            "date_create_project": current_datetime
            if existing_project is None
            else projects[existing_project]["date_create_project"],
            "date_last_open_project": current_datetime,
        }

        if existing_project is not None:
            # Обновляем существующий проект
            projects[existing_project] = project_data
        else:
            # Добавляем новый проект
            projects.append(project_data)

        # Сохраняем обновленный список
        self.__settings.setValue("projects", projects)
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings add_or_update_project(): {project_name}")

    def get_projects(self) -> list:
        """Получить список всех проектов"""
        projects = self.__settings.value("projects", [])
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings get_projects(): {len(projects)} projects")
        return projects

    def get_last_projects(self, limit: int = 5) -> list:
        """Получить последние проекты"""
        projects = self.get_projects()
        # Сортируем по дате последнего открытия
        sorted_projects = sorted(
            projects, key=lambda x: x.get("date_last_open_project", ""), reverse=True
        )
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings get_last_projects(): {len(sorted_projects[:limit])} projects")
        return sorted_projects[:limit]

    def delete_project(self, project_dir: str):
        """Удалить проект из списка"""
        projects = self.get_projects()
        projects = [p for p in projects if p.get("directory_project") != project_dir]
        self.__settings.setValue("projects", projects)
        if self.__osbm.obj_logg:
            self.__osbm.obj_logg.debug_logger(f"Settings delete_project(): {project_dir}")

    # endregion

    def sync(self):
        """Синхронизировать настройки"""
        self.__settings.sync()
