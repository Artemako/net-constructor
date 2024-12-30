
class DrawText:

    def __init__(self, painter):
        self.painter = painter
    
    def draw_centered_by_bottom_multiline_text(self, text, center_x, bottom_y):
        lines = text.split("\n")
        # Вычисляем общую высоту текста
        total_text_height = self.painter.fontMetrics().height() * len(lines)
        # Вычисляем начальную y-координату для рисования так, чтобы нижний край совпадал с bottom_y
        start_y = bottom_y - total_text_height
        # Рисуем каждую строку текста
        text_y = start_y
        for line in lines:
            text_width = self.painter.fontMetrics().horizontalAdvance(line)
            # Центрируем каждую строку относительно center_x
            text_x = center_x - text_width // 2
            self.painter.drawText(text_x, text_y, line)
            text_y += self.painter.fontMetrics().height()

    def draw_lefted_by_left_single_line_text(self, text, left_x, y):
        """Отображает однострочный текст, выровненный по левому краю, начиная с заданной координаты x."""
        # Рисуем текст с начальной x-координаты, оставляя текст выровненным по левому краю
        self.painter.drawText(left_x, y, text)

    def draw_righted_by_right_single_line_text(self, text, right_x, y):
        """Отображает однострочный текст, выровненный по правому краю, начиная с заданной координаты x."""
        # Вычисляем ширину текста
        text_width = self.painter.fontMetrics().horizontalAdvance(text)
        # Рассчитываем начальную x-координату для выравнивания по правому краю
        text_x = right_x - text_width
        # Рисуем текст смещенный, чтобы правая граница текста совпадала с right_x
        self.painter.drawText(text_x, y, text)
        

