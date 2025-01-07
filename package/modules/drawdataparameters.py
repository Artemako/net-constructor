
class DrawData:

    def __init__(self, object_target):
        self.__object_target = object_target
        #
        self.__self_data = self.__object_target.get_data()

    def get_sd(self, key) -> str:
        return str(self.__self_data.get(key, {}).get("value", ""))


class DrawParameters:
    def __init__(
        self,
        object_diagramm,
        object_target,
        object_before=None,
        object_after=None
    ):
        self.__object_diagramm = object_diagramm
        self.__object_self = object_target
        self.__object_before = object_before
        self.__object_after = object_after

        self.__self_parameters = {}
        self.__before_parameters = {}
        self.__after_parameters = {}

        new_dict_diagramm_parameters = self._get_dict(
            self.__object_diagramm.get_parameters(),
            self.__object_diagramm.get_config_parameters(),
        )
        self.__self_parameters = {
            **new_dict_diagramm_parameters,
            **self._get_dict(
                self.__object_self.get_parameters(),
                self.__object_self.get_config_parameters(),
            ),
        }

        if self.__object_before:
            self.__before_parameters = {
                **new_dict_diagramm_parameters,
                **self._get_dict(
                    self.__object_before.get_parameters(),
                    self.__object_before.get_config_parameters(),
                ),
            }
        if self.__object_after:
            self.__after_parameters = {
                **new_dict_diagramm_parameters,
                **self._get_dict(
                    self.__object_after.get_parameters(),
                    self.__object_after.get_config_parameters(),
                ),
            }

    def _get_dict(self, parameters, config_parameters) -> dict:
        new_dict = {}
        for key, dict_value in config_parameters.items():
            new_dict[key] = dict_value.get("value", 0)
        for key in config_parameters.keys():
            value = parameters.get(key, {}).get("value", None)
            if value is not None:
                new_dict[key] = value
        return new_dict

    def get_sp(self, key):
        return self.__self_parameters.get(key, 0)

    def get_bp(self, key):
        return self.__before_parameters.get(key, 0)

    def get_ap(self, key):
        return self.__after_parameters.get(key, 0)
    
