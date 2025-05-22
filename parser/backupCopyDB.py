
# D:\PythonProject\WebParsing\parser\backupCopyDB.py

import os
import shutil
from datetime import datetime

def main():
    print(f"{' Резервное копирование базы данных ':^50}")
    print(f"{' Режим: работа с кодом Python ':^50}\n")

    stop = input('Для продолжения нажмите любую клавишу,\nдля остановки нажмите "Q": ')
    if stop.upper() in ("Q", "Й"):
        return

    database_backup()

def database_backup():
    # Папка для резервных копий (относительно parser/)
    path_backup_folder = os.path.join(os.path.dirname(__file__), 'backup_folder')
    if not os.path.exists(path_backup_folder):
        os.makedirs(path_backup_folder)

    # Путь к исходной базе данных (относительно parser/)
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3'))
    if not os.path.exists(db_path):
        print(f"Файл базы данных не найден: {db_path}")
        return

    # Имя резервной копии с таймштампом
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(path_backup_folder, f'db_backup_{timestamp}.sqlite3')

    try:
        shutil.copy(db_path, backup_file)
        print(f'Создана резервная копия: {backup_file}')
    except Exception as e:
        print(f'Ошибка при создании резервной копии: {e}')

if __name__ == "__main__":
    main()
