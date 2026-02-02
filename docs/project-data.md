# Данные проекта

Описывается хранение и изменение данных проекта: структура в памяти, загрузка/сохранение файла .nce и бизнес-операции изменения данных.

Код: [package.modules.project](api/modules.md#package.modules.project) — класс `Project`.

## Хранение

Единственный источник правды — словарь **`__data`** в памяти (атрибут класса `Project`).

Файл проекта с расширением **.nce** — сериализация этого словаря: JSON, кодировка UTF-8, с отступами (`json.dump(..., indent=4, ensure_ascii=False)`).

Структура `__data`:

| Ключ | Назначение |
|------|------------|
| `diagram_type_id` | Идентификатор типа диаграммы (из config_global.json, ключ `diagrams`). |
| `diagram_name` | Человекочитаемое имя типа диаграммы. |
| `diagram_parameters` | Параметры отображения диаграммы (отступы, расстояние между рядами, центрирование и т.д.). |
| `control_sectors_config` | Конфиг полей секторов управления (структура по config_global). |
| `nodes` | Массив узлов. Каждый узел: `id`, `order`, `node_id`, `data`, `parameters`, `is_wrap`. |
| `connections` | Массив соединений. Каждое соединение: `id`, `order`, `connection_id`, `data`, `parameters`, `control_sectors`. |
| `archived_parameters` | Архив параметров по типам диаграмм при смене типа: для каждого `type_id` хранятся `nodes`, `connections`, `diagram_parameters`. |

Узлы и соединения содержат идентификаторы типов (`node_id`, `connection_id`) и данные полей, описанных в [config_nodes.json](configs.md#config_nodesjson) и [config_connections.json](configs.md#config_connectionsjson).

## Загрузка и сохранение

- **open_project(file_path):** чтение JSON из файла в `__data`; путь сохраняется в `__file_name`.
- **create_new_project(diagram_data, control_sectors_config, file_path):** инициализация `__data` (пустые `nodes`, `connections`, `archived_parameters`); запись на диск через `_write_project()`.
- **create_demo_project(diagram_data, control_sectors_config):** то же без пути к файлу (`__file_name = None`); на диск не записывается.
- **save_as_project(file_path):** обновление `__file_name` и запись через `_write_project()`.
- **_write_project():** если `__file_name` задан, запись `__data` в файл (`json.dump`). Вызывается после каждого изменения данных, которое должно попасть в файл (кроме демо-проекта без сохранения).

## Изменение данных (бизнес-операции)

### Смена типа диаграммы

**change_type_diagram(new_diagram, config_nodes, config_connections):**

1. Текущие параметры узлов, соединений и `diagram_parameters` сохраняются в `archived_parameters[current_type_id]`.
2. Типы узлов и соединений переводится в новый тип по маппингу [package.constants.DiagramToDiagram](api/constants.md) (`_update_diagram_nodes`, `_update_diagram_connections`).
3. Если для нового типа есть архив в `archived_parameters`, параметры узлов, соединений и `diagram_parameters` восстанавливаются из архива; иначе используются параметры по умолчанию из `new_diagram`.
4. Обновляются `diagram_type_id`, `diagram_name`; вызывается `_write_project()`.

### Элементы (узлы и соединения)

- **add_pair(key_dict_node_and_key_dict_connection):** добавление пары узел + соединение. Сначала добавляется узел (`_add_node`), затем соединение (`_add_connection`). Для нового соединения создаются три контрольных сектора по умолчанию (`_add_default_control_sectors`). Вызывается `_write_project()`.
- **delete_pair(node, connection):** удаление пары из массивов `nodes` и `connections`; порядок оставшихся элементов пересчитывается (`order`). Вызывается `_write_project()`.
- **restore_pair(node_data, connection_data):** восстановление пары в конце списков (для отмены удаления / повтора добавления). Вызывается `_write_project()`.

### Контрольные секторы

- **add_control_sector(obj, name, physical_length, length, penultimate):** добавление сектора к соединению с `connection["id"] == obj["id"]`. Новый сектор получает уникальный `id`, порядок в списке `control_sectors` пересчитывается. Вызывается `_write_project()`.
- **delete_control_sector(obj, selected_cs):** удаление сектора из `control_sectors` соединения; порядок пересчитывается. Вызывается `_write_project()`.
- **set_new_order_control_sectors(obj, new_order_control_sectors):** замена списка `control_sectors` у соединения на новый порядок; у каждого сектора обновляется `order`. Вызывается `_write_project()`.

### Редактирование полей

**save_project(obj, is_node, is_general_tab, is_editor_tab, config_nodes, config_connections, diagram_type_id, diagram_name, new_diagram_parameters, new_data, new_parameters):**

- **is_general_tab:** обновляются `diagram_type_id`, `diagram_name` и ключи в `diagram_parameters` из `new_diagram_parameters`.
- **is_editor_tab:** для выбранного узла или соединения (по `obj["id"]`) обновляются `data` и `parameters` из `new_data` и `new_parameters`. При отсутствии ключа в `node["data"]` или `node["parameters"]` он создаётся (`_check_empty_data_key`, `_check_empty_parameters_key`). Для полей типа type_object и objects при необходимости синхронизируются значения с другими объектами того же типа (`_check_type_object_key`, `_check_objects_key`).

После изменений вызывается `_write_project()`.

### Порядок элементов

- **set_new_order_nodes(new_order_nodes):** замена `__data["nodes"]` на переупорядоченный список; у каждого узла обновляется `order`.
- **set_new_order_connections(new_order_connections):** замена `__data["connections"]` на переупорядоченный список; у каждого соединения обновляется `order`.

### Прочее

- **wrap_node(node):** переключение флага `is_wrap` у узла с заданным `id`. Вызывается `_write_project()`.

## Схема потока

```mermaid
flowchart LR
  UI["Операции UI"]
  Project["Project"]
  Data["__data"]
  Write["_write_project"]
  File[".nce файл"]
  UI --> Project
  Project --> Data
  Data --> Write
  Write --> File
```

Операции UI вызывают методы `Project`. Методы изменяют `__data`. При необходимости сохранения вызывается `_write_project()`, который записывает `__data` в файл .nce.
