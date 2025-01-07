from PySide6.QtCore import Qt

class Constants:
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
            "TexturePattern": Qt.TexturePattern
        }
