

class DirPathManager:

    def __init__(self):
        self.__dir_app = None

    def set_dir_app(self, dir_app):
        self.__dir_app = dir_app

    def get_dir_app(self):
        return self.__dir_app