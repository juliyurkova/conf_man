import calendar
from datetime import datetime

from zipfile import ZipFile

with ZipFile('files.zip', 'a') as myzip:
    while True:
        command = input('$ ')
        if command == 'ls':
            for name in myzip.namelist():
                print(name)
        elif command == "exit":
            break
        elif command.startswith('tac '):
            path = command.split()[1]
            content = myzip.read(path).decode()
            print(reversed(content))
        elif command=='cal':
            now = datetime.now()
            print(calendar.month(now.year, now.month))
