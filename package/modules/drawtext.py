"""Отрисовка текста: перенос строк, выравнивание, подписи на диаграмме."""


class DrawText:
    def __init__(self):
        self.__painter = None

    def _wrap_text_to_width(self, text, max_width=None):
        if max_width is None or max_width <= 0:
            return text.split("\n")

        wrapped_lines = []
        for original_line in text.split("\n"):
            if not original_line.strip():
                wrapped_lines.append(original_line)
                continue

            words = original_line.split()
            current_line = []
            current_line_width = 0

            for word in words:
                word_width = self.__painter.fontMetrics().horizontalAdvance(word)

                # Если слово не помещается в текущую строку
                if current_line and (current_line_width + word_width) > max_width:
                    # Если слово слишком длинное для пустой строки - разбиваем посимвольно
                    if word_width > max_width:
                        # Добавляем текущую строку, если она не пустая
                        if current_line:
                            wrapped_lines.append(" ".join(current_line))
                            current_line = []
                            current_line_width = 0

                        # Разбиваем слово посимвольно
                        chars = list(word)
                        current_word_part = []
                        current_part_width = 0

                        for char in chars:
                            char_width = self.__painter.fontMetrics().horizontalAdvance(
                                char
                            )
                            if current_part_width + char_width > max_width:
                                wrapped_lines.append("".join(current_word_part))
                                current_word_part = [char]
                                current_part_width = char_width
                            else:
                                current_word_part.append(char)
                                current_part_width += char_width

                        if current_word_part:
                            wrapped_lines.append("".join(current_word_part))
                    else:
                        # Переносим слово на следующую строку
                        wrapped_lines.append(" ".join(current_line))
                        current_line = [word]
                        current_line_width = word_width
                else:
                    # Добавляем слово в текущую строку
                    current_line.append(word)
                    current_line_width += (
                        word_width + self.__painter.fontMetrics().horizontalAdvance(" ")
                    )  # добавляем пробел

            # Добавляем оставшиеся слова
            if current_line:
                wrapped_lines.append(" ".join(current_line))

        return wrapped_lines

    def draw_multiline_text_by_hl_vb(
        self, painter_text, text, left_x, bottom_y, max_width=None
    ):
        """По левому краю по горизонтали и по низу по вертикали"""
        self.__painter = painter_text()
        lines = self._wrap_text_to_width(text, max_width)
        # Вычисляем начальную y-координату для рисования так, чтобы нижний край совпадал с bottom_y
        text_y = bottom_y
        # Рисуем каждую строку текста
        for line in reversed(lines):
            self.__painter.drawText(left_x, text_y, line)
            text_y -= self.__painter.fontMetrics().height()

    def draw_multiline_text_by_hr_vb(
        self, painter_text, text, right_x, bottom_y, max_width=None
    ):
        """По правому краю по горизонтали и по низу по вертикали"""
        self.__painter = painter_text()
        lines = self._wrap_text_to_width(text, max_width)
        # Вычисляем начальную y-координату для рисования так, чтобы нижний край совпадал с bottom_y
        text_y = bottom_y
        # Рисуем каждую строку текста
        for line in reversed(lines):
            text_width = self.__painter.fontMetrics().horizontalAdvance(line)
            text_x = right_x - text_width  # выравнивание по правому краю
            self.__painter.drawText(text_x, text_y, line)
            text_y -= self.__painter.fontMetrics().height()

    def draw_multiline_text_by_hc_vb(
        self, painter_text, text, center_x, bottom_y, max_width=None
    ):
        self.__painter = painter_text()
        """По центру по горизонтали и по низу по вертикали"""
        lines = self._wrap_text_to_width(text, max_width)
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

    def draw_multiline_text_by_hc_vt(
        self, painter_text, text, center_x, top_y, max_width=None
    ):
        """По центру по горизонтали и по верху по вертикали"""
        self.__painter = painter_text()
        lines = self._wrap_text_to_width(text, max_width)
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

    def draw_multiline_text_by_hc_vc(
        self, painter_text, text, center_x, center_y, max_width=None
    ):
        """По центру по горизонтали и по центру по вертикали"""
        self.__painter = painter_text()
        lines = self._wrap_text_to_width(text, max_width)
        total_text_height = len(lines) * self.__painter.fontMetrics().height()
        # * 0.618
        start_y = (
            center_y
            - (total_text_height // 2)
            + (self.__painter.fontMetrics().height() // 2)
        ) + self.__painter.fontMetrics().height() * 0.618 // 2
        # Рисуем каждую строку текста
        text_y = start_y
        for line in lines:
            text_width = self.__painter.fontMetrics().horizontalAdvance(line)
            # Центрируем каждую строку относительно center_x
            text_x = center_x - text_width // 2
            self.__painter.drawText(text_x, text_y, line)
            text_y += self.__painter.fontMetrics().height()

    def draw_singleline_text_rotated_by_hc_vt(
        self, painter_text, text, center_x, top_y
    ):
        self.__painter = painter_text()
        self.__painter.save()
        self.__painter.translate(center_x, top_y)
        self.__painter.rotate(-90)
        self.draw_singleline_text_by_hr_vc(painter_text, text, 0, 0)
        self.__painter.restore()

    def draw_singleline_text_by_hr_vc(self, painter_text, text, right_x, center_y):
        self.__painter = painter_text()
        text_width = self.__painter.fontMetrics().horizontalAdvance(text)
        text_height = self.__painter.fontMetrics().height() * 0.618
        text_x = right_x - text_width
        text_y = center_y + text_height // 2
        self.__painter.drawText(text_x, text_y, text)

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
