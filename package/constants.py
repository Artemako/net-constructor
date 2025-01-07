from PySide6.QtCore import Qt


class FillStyles:
    def __init__(self):
        self.fill_styles = {
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
    
    def keys(self):
        return self.fill_styles.keys()

    def get(self, fill_pattern_name, default):
        return self.fill_styles.get(fill_pattern_name, default)

class DiagrammToDiagramm:
    def __init__(self):
        self.diagramm_to_diagramm = {
            "0": {
                "50": {"nodes": {"0": "50", "1": "51"}, "connections": {"0": "50"}},
                "100": {},
                "150": {},
            },
            "50": {"100": {}, "150": {}},
            "100": {"150": {}},
        }

    # TODO Проверка возможности перехода
