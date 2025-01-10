class NumberFormatter:

    def __init__(self):
        self.__precision_number = 0
        self.__precision_separator = 1
    
    def set_precision_number(self, precision_number):
        self.__precision_number = precision_number

    def set_precision_separator(self, precision_separator):
        self.__precision_separator = precision_separator

    def get(self, number_input):
        try:
            number_float = float(number_input)
        except ValueError:
            return ""

        format_string = f"{{:.{self.__precision_number}f}}"
        formatted_number = format_string.format(number_float)       
        separator = '.' if self.__precision_separator == 1 else ','
        formatted_number = formatted_number.replace('.', separator) if separator == ',' else formatted_number
        return formatted_number


# # Пример использования:
# formatter = NumberFormatter()
# formatter.set_precision_number(2)
# formatter.set_precision_separator(0)
# print(formatter.get("1234.56"))
# print(formatter.get(str(125.6789)))

