import os
import zipfile
from datetime import datetime
import calendar

def run_shell():
    """Эмулятор оболочки с поддержкой команд ls, exit, tac, cal, cd, chmod."""
    current_directory = '/'

    with zipfile.ZipFile('doc1.zip', 'r') as myzip:
        while True:
            command = input(f'{current_directory}$ ')
            parts = command.split()

            if len(parts) == 0:
                continue

            cmd = parts[0]
            args = parts[1:]

            if cmd == 'ls':
                # Показать файлы в текущей директории
                list_files(myzip, current_directory)

            elif cmd == 'exit':
                break

            elif cmd == 'tac':
                if len(args) == 0:
                    print("tac: missing file operand")
                else:
                    file_path = os.path.join(current_directory.lstrip('/'), args[0])
                    tac_file(myzip, file_path)

            elif cmd == 'cal':
                now = datetime.now()
                print(calendar.month(now.year, now.month))

            elif cmd == 'cd':
                if len(args) == 0:
                    print("cd: missing argument")
                else:
                    new_dir = args[0]
                    current_directory = change_directory(myzip, current_directory, new_dir)

            elif cmd == 'chmod':
                if len(args) < 2:
                    print("chmod: missing operand")
                else:
                    chmod_file(args[0], args[1])

            else:
                print(f"{cmd}: command not found")

def list_files(myzip, current_directory):
    """Вывод списка файлов и папок в текущей директории."""
    current_directory = current_directory.lstrip('/')
    for name in myzip.namelist():
        if name.startswith(current_directory):
            relative_path = os.path.relpath(name, current_directory)
            if '/' not in relative_path:
                print(relative_path)

def tac_file(myzip, file_path):
    """Вывод содержимого файла в обратном порядке."""
    try:
        content = myzip.read(file_path).decode().splitlines()
        for line in reversed(content):
            print(line)
    except KeyError:
        print(f"tac: {file_path}: No such file")

def change_directory(myzip, current_directory, new_dir):
    """Смена директории."""
    if new_dir == "..":
        return os.path.dirname(current_directory.rstrip('/'))
    else:
        potential_dir = os.path.join(current_directory, new_dir).lstrip('/')
        # Проверяем, что новая директория существует
        if any(name.startswith(potential_dir + '/') for name in myzip.namelist()):
            return os.path.normpath('/' + potential_dir)
        else:
            print(f"cd: {new_dir}: No such directory")
            return current_directory

def chmod_file(mode, file_name):
    """Симуляция изменения прав доступа к файлу."""
    print(f"Simulating chmod {mode} on {file_name} (permissions are not actually changed)")


if __name__ == "__main__":
    run_shell()