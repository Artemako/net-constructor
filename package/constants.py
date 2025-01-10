from PySide6.QtCore import Qt


class FillStyles:
    def __init__(self):
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
    
    def keys(self):
        return self.__fill_styles.keys()

    def get(self, fill_pattern_name, default):
        return self.__fill_styles.get(fill_pattern_name, default)
    
class TextAlignments:
    def __init__(self):
        self.__text_alignments = {
            "LeftAlign": Qt.AlignLeft,
            "CenterAlign": Qt.AlignCenter,
            "RightAlign": Qt.AlignRight
        }
    
    def keys(self):
        return self.__text_alignments.keys()

    def get(self, text_alignment_name, default):
        return self.__text_alignments.get(text_alignment_name, default)



# class DiagrammToDiagramm:
    # def __init__(self):
    #     self.__nodes_mapping = {
    #         ("0", "50"): {"0": "50", "1": "51"},
    #         ("50", "0"): {"50": "0", "51": "1"},
    #         ("0", "100"): {"0": "100", "1": "101"},
    #         ("100", "0"): {"100": "0", "101": "1"},
    #         ("50", "100"): {"50": "100", "51": "101"},
    #         ("100", "50"): {"100": "50", "101": "51", "102": None},
    #     }
    #     self.__connections_mapping = {
    #         ("0", "50"): {"0": "50"},
    #         ("50", "0"): {"50": "0"},
    #         ("0", "100"): {"0": "100"},
    #         ("100", "0"): {"100": "0"},
    #         ("50", "100"): {"50": "100"},
    #         ("100", "50"): {"100": "50"}
    #     }
    #     # TODO 

    # def get_new_type_id(self, old_diagramm_type_id, new_diagramm_type_id, object_type_id, is_node=False):
    #     mapping = self.__nodes_mapping if is_node else self.__connections_mapping
    #     return mapping.get((old_diagramm_type_id, new_diagramm_type_id), {}).get(object_type_id, None)

class DiagrammToDiagramm:
    def __init__(self):
        self.__nodes_mapping = {
            "0": {
                "50": "0",
                "51": "1",
                "100": "0",
                "101": "1"
            },
            "50": {
                "0": "50",
                "1": "51",
                "100": "50",
                "101": "51",
                "102": None
            },
            "100": {
                "0": "100",
                "1": "101",
                "50": "100",
                "51": "101"
            },
        }
        self.__connections_mapping = {
            "0": {
                "50": "0",
                "100": "0"
            },
            "50": {
                "0": "50",
                "100": "50"
            },
            "100": {
                "0": "100",
                "50": "100"
            },
        }

    def get_new_type_id(self, new_diagramm_type_id, object_type_id, is_node=False):
        mapping = self.__nodes_mapping if is_node else self.__connections_mapping
        return mapping.get(new_diagramm_type_id, {}).get(object_type_id, None)
