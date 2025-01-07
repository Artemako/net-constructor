
class DrawText:

    def __init__(self):
        self.__painter = None
    
    def draw_multiline_text_by_hc_vb(self, painter_text, text, center_x, bottom_y):
        self.__painter = painter_text()
        """По центру по горизонтали и по низу по вертикали"""
        lines = text.split("\n")
        # Вычисляем начальную y-координату для рисования так, чтобы нижний край совпадал с bottom_y
        start_y = bottom_y
        # Рисуем каждую строку текста
        text_y = start_y
        for line in reversed(lines):
            text_width = self.__painter.fontMetrics().horizontalAdvance(line)
            # Центрируем каждую строку относительно center_x
            text_x = center_x - text_width // 2
            self.__painter.drawText(text_x, text_y, line)
            text_y -= self.__painter.fontMetrics().height()

    def draw_multiline_text_by_hc_vt(self, painter_text, text, center_x, top_y):
        """По центру по горизонтали и по верху по вертикали"""
        self.__painter = painter_text()
        lines = text.split("\n")
        # Вычисляем начальную y-координату для рисования так, чтобы верхний край совпадал с top_y
        start_y = top_y + self.__painter.fontMetrics().height() * 0.618
        # Рисуем каждую строку текста
        text_y = start_y
        for line in lines:
            text_width = self.__painter.fontMetrics().horizontalAdvance(line)
            # Центрируем каждую строку относительно center_x
            text_x = center_x - text_width // 2
            self.__painter.drawText(text_x, text_y, line)
            text_y += self.__painter.fontMetrics().height()

    # def draw_lefted_by_left_single_line_text(self, text, left_x, y):
    #     """Отображает однострочный текст, выровненный по левому краю, начиная с заданной координаты x."""
    #     # Рисуем текст с начальной x-координаты, оставляя текст выровненным по левому краю
    #     self.painter.drawText(left_x, y, text)

    def draw_singleline_text_by_hl_vb(self, painter_text, text, left_x, bottom_y):
        self.__painter = painter_text()
        text_y = bottom_y
        self.__painter.drawText(left_x, text_y, text)

    def draw_singleline_text_by_hl_vt(self, painter_text, text, left_x, top_y):
        self.__painter = painter_text()
        text_y = top_y + self.__painter.fontMetrics().height() * 0.618
        self.__painter.drawText(left_x, text_y, text)

    # def draw_righted_by_right_single_line_text(self, text, right_x, y):
    #     """Отображает однострочный текст, выровненный по правому краю, начиная с заданной координаты x."""
    #     # Вычисляем ширину текста
    #     text_width = self.painter.fontMetrics().horizontalAdvance(text)
    #     # Рассчитываем начальную x-координату для выравнивания по правому краю
    #     text_x = right_x - text_width
    #     # Рисуем текст смещенный, чтобы правая граница текста совпадала с right_x
    #     self.painter.drawText(text_x, y, text)
        
    def draw_singleline_text_by_hr_vb(self, painter_text, text, right_x, y):
        self.__painter = painter_text()
        # Вычисляем ширину текста
        text_width = self.__painter.fontMetrics().horizontalAdvance(text)
        # Рассчитываем начальную x-координату для выравнивания по правому краю
        text_x = right_x - text_width
        text_y = y
        # Рисуем текст смещенный, чтобы правая граница текста совпадала с right_x
        self.__painter.drawText(text_x, text_y, text)

    def draw_singleline_text_by_hr_vt(self, painter_text, text, right_x, y):
        self.__painter = painter_text()
        # Вычисляем ширину текста
        text_width = self.__painter.fontMetrics().horizontalAdvance(text)
        # Рассчитываем начальную x-координату для выравнивания по правому краю
        text_x = right_x - text_width
        text_y = y + self.__painter.fontMetrics().height() * 0.618 
        # Рисуем текст смещенный, чтобы правая граница текста совпадала с right_x
        self.__painter.drawText(text_x, text_y, text)