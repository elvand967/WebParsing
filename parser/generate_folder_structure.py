# D:\PythonProject\WebParsing\parser\generate_folder_structure.py
'''
скрипт создаст файл realtek.txt с деревом каталогов и файлов, исключая '.idea'; '.venv' и '.git'
'''

import os


def print_tree(path, exclusions, prefix="", is_last=True, output_lines=None):
    if output_lines is None:
        output_lines = []

    name = os.path.basename(path)
    if name == "":
        # Корневая папка (например, D:\PythonProject\WebParsing)
        output_lines.append(path.upper())
    else:
        connector = "\\---" if is_last else "+---"
        output_lines.append(f"{prefix}{connector}{name}")

    # Обновляем префикс для вложенных элементов
    if is_last:
        new_prefix = prefix + "    "
    else:
        new_prefix = prefix + "|   "

    try:
        entries = [e for e in os.listdir(path) if e not in exclusions]
    except PermissionError:
        # Если нет доступа к папке, пропускаем
        return output_lines

    # Сортируем: сначала папки, потом файлы, для удобства чтения
    dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
    files = [e for e in entries if os.path.isfile(os.path.join(path, e))]

    # Выводим файлы
    for i, file in enumerate(files):
        is_last_file = (i == len(files) - 1) and (len(dirs) == 0)
        file_connector = "\\---" if is_last_file else "+---"
        output_lines.append(f"{new_prefix}{file_connector}{file}")

    # Рекурсивно выводим папки
    for i, directory in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1)
        print_tree(os.path.join(path, directory), exclusions, new_prefix, is_last_dir, output_lines)

    return output_lines

def generate_tree_report(base_path, exclusions, output_file):
    lines = print_tree(base_path, exclusions)
    # Записываем в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    base_path = r"D:\PythonProject\WebParsing"
    exclusions = ['.idea', '.venv', '.git']
    output_file = "realtek.txt"
    generate_tree_report(base_path, exclusions, output_file)



# def generate_folder_structure(path, exclusions, output_file):
#     with open(output_file, 'w', encoding='utf-8') as f:
#         for root, dirs, files in os.walk(path):
#             # Удаляем из обхода исключаемые директории
#             dirs[:] = [d for d in dirs if d not in exclusions]
#             level = root.replace(path, '').count(os.sep)
#             indent = ' ' * 4 * level
#             f.write(f"{indent}{os.path.basename(root)}/\n")
#             subindent = ' ' * 4 * (level + 1)
#             for file in files:
#                 f.write(f"{subindent}{file}\n")
#
# if __name__ == "__main__":
#     base_path = r"D:\PythonProject\WebParsing"
#     exclusions = ['.idea', '.venv', '.git']
#     output_file = "realtek.txt"
#     generate_folder_structure(base_path, exclusions, output_file)