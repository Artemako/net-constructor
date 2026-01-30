import json

def process_json(data):
    # Проверяем, является ли data словарем
    if isinstance(data, dict):
        for key, value in data.items():
            # Если ключ - "value" и значение - число, увеличиваем его в 4 раза
            if key == "value" and isinstance(value, (int, float)):
                data[key] = value * 2
            # Рекурсивно обрабатываем вложенные словари или списки
            elif isinstance(value, (dict, list)):
                process_json(value)
    # Проверяем, является ли data списком
    elif isinstance(data, list):
        for item in data:
            # Рекурсивно обрабатываем каждый элемент списка
            process_json(item)

# Чтение JSON из файла
# input_file = "configs/config_connections.json"
# input_file = "configs/config_global.json"
input_file = "configs/config_nodes.json"
with open(input_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Обработка JSON
process_json(json_data)

# Запись результата в файл
output_file = "result.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=4, ensure_ascii=False)

print(f"Обработка завершена. Результат сохранён в файл {output_file}")