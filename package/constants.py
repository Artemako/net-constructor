"""Константы и маппинги стилей Qt: заливка, выравнивание текста, линии, диаграммы."""

from PySide6.QtCore import Qt

# Название приложения (заголовок окна и имена exe при сборке)
APP_TITLE = "Конструктор схем ВОЛП"
APP_TITLE_DEMO = "Конструктор схем ВОЛП (демо)"


class FillStyles:
    """Маппинг имён стилей заливки на Qt.BrushStyle."""

    def __init__(self) -> None:
        self.__fill_styles = {
            "NoBrush": Qt.NoBrush,
            "SolidPattern": Qt.SolidPattern,
            "Dense1Pattern": Qt.Dense1Pattern,
            "Dense2Pattern": Qt.Dense2Pattern,
            "Dense3Pattern": Qt.Dense3Pattern,
            "Dense4Pattern": Qt.Dense4Pattern,
            "Dense5Pattern": Qt.Dense5Pattern,
            "Dense6Pattern": Qt.Dense6Pattern,
            "Dense7Pattern": Qt.Dense7Pattern,
            "HorPattern": Qt.HorPattern,
            "VerPattern": Qt.VerPattern,
            "CrossPattern": Qt.CrossPattern,
            "BDiagPattern": Qt.BDiagPattern,
            "FDiagPattern": Qt.FDiagPattern,
            "DiagCrossPattern": Qt.DiagCrossPattern,
            "LinearGradientPattern": Qt.LinearGradientPattern,
            "RadialGradientPattern": Qt.RadialGradientPattern,
            "ConicalGradientPattern": Qt.ConicalGradientPattern,
            "TexturePattern": Qt.TexturePattern,
        }
    
    def keys(self) -> list:
        """Возвращает список имён стилей заливки."""
        return list(self.__fill_styles.keys())

    def get(self, fill_pattern_name: str, default):
        """Возвращает Qt-стиль заливки по имени или default."""
        return self.__fill_styles.get(fill_pattern_name, default)


class TextAlignments:
    """Маппинг имён выравнивания текста на Qt.AlignmentFlag."""

    def __init__(self) -> None:
        self.__text_alignments = {
            "LeftAlign": Qt.AlignLeft,
            "CenterAlign": Qt.AlignCenter,
            "RightAlign": Qt.AlignRight
        }
    
    def keys(self) -> list:
        """Возвращает список имён выравнивания."""
        return list(self.__text_alignments.keys())

    def get(self, text_alignment_name: str, default):
        """Возвращает Qt-выравнивание по имени или default."""
        return self.__text_alignments.get(text_alignment_name, default)


class LineStyles:
    """Маппинг имён стилей линий на Qt.PenStyle."""

    def __init__(self) -> None:
        self.__line_styles = {
            # "NoPen": Qt.NoPen,
            "SolidLine": Qt.SolidLine,
            "DashLine": Qt.DashLine,
            "DotLine": Qt.DotLine,
            "DashDotLine": Qt.DashDotLine,
            "DashDotDotLine": Qt.DashDotDotLine,
            # "CustomDashLine": Qt.CustomDashLine,
        }
    
    def keys(self) -> list:
        """Возвращает список имён стилей линий."""
        return list(self.__line_styles.keys())

    def get(self, line_style_name: str, default):
        """Возвращает Qt-стиль линии по имени или default."""
        return self.__line_styles.get(line_style_name, default)


class DiagramToDiagram:
    """Маппинг типов узлов и соединений между типами диаграмм."""

    def __init__(self) -> None:
        self.__nodes_mapping = {
            "0": {
                "50": "0",
                "51": "1",
                "100": "0",
                "101": "1",
                "150": "0",
                "151": "1"
            },
            "50": {
                "0": "50",
                "1": "51",
                "100": "50",
                "101": "51",
                "150": "50",
                "151": "51"
            },
            "100": {
                "0": "100",
                "1": "101",
                "50": "100",
                "51": "101",
                "150": "100",
                "151": "101"
            },
            "150" : {
                "0": "150",
                "1": "151",
                "50": "150",
                "51": "151",
                "100": "150",
                "101": "151"
            }
        }
        self.__connections_mapping = {
            "0": {
                "50": "0",
                "100": "0",
                "150": "0"
            },
            "50": {
                "0": "50",
                "100": "50",
                "150": "50"
            },
            "100": {
                "0": "100",
                "50": "100",
                "150": "100"
            }, 
            "150": {
                "0": "150",
                "50": "150",
                "100": "150"
            }   
        }

    def get_new_type_id(
        self, new_diagram_type_id: str, object_type_id: str, is_node: bool = False
    ):
        """Возвращает id типа в новой диаграмме по id в текущей (узел или соединение)."""
        mapping = self.__nodes_mapping if is_node else self.__connections_mapping
        return mapping.get(new_diagram_type_id, {}).get(object_type_id)
