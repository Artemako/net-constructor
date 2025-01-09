
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

    def draw_singleline_text_by_hl_vb(self, painter_text, text, left_x, bottom_y):
        self.__painter = painter_text()
        text_y = bottom_y
        self.__painter.drawText(left_x, text_y, text)

    def draw_singleline_text_by_hl_vt(self, painter_text, text, left_x, top_y):
        self.__painter = painter_text()
        text_y = top_y + self.__painter.fontMetrics().height() * 0.618
        self.__painter.drawText(left_x, text_y, text)
        
    def draw_singleline_text_by_hr_vb(self, painter_text, text, right_x, bottom_y):
        self.__painter = painter_text()
        # Вычисляем ширину текста
        text_width = self.__painter.fontMetrics().horizontalAdvance(text)
        # Рассчитываем начальную x-координату для выравнивания по правому краю
        text_x = right_x - text_width
        text_y = bottom_y
        # Рисуем текст смещенный, чтобы правая граница текста совпадала с right_x
        self.__painter.drawText(text_x, text_y, text)

    def draw_singleline_text_by_hr_vt(self, painter_text, text, right_x, top_y):
        self.__painter = painter_text()
        # Вычисляем ширину текста
        text_width = self.__painter.fontMetrics().horizontalAdvance(text)
        # Рассчитываем начальную x-координату для выравнивания по правому краю
        text_x = right_x - text_width
        text_y = top_y + self.__painter.fontMetrics().height() * 0.618 
        # Рисуем текст смещенный, чтобы правая граница текста совпадала с right_x
        self.__painter.drawText(text_x, text_y, text)

    
    def draw_rotated_text_90(self, painter_text, text, center_x, top_y):
        self.__painter = painter_text()
        # Сохраняем состояние контекста рисования
        self.__painter.save()
        # Перемещаем систему координат к точке, где нужно нарисовать текст
        self.__painter.translate(center_x, top_y)
        # Поворачиваем контекст на 90 градусов по часовой стрелке
        self.__painter.rotate(90)
        # Рисуем текст
        text_width = self.__painter.fontMetrics().horizontalAdvance(text)
        text_height = self.__painter.fontMetrics().height()
        # Смещаем на половину ширины, чтобы текст был центрирован
        self.__painter.drawText(-text_height // 2, text_width // 2, text)
        # Восстанавливаем состояние контекста рисования
        self.__painter.restore()

# "is_left_node_caption": {
#     "value": true,
#     "name": "Расположение нижних подписей вершин у левого/правого края",
#     "order": ...,
#     "type": "bool"
# },