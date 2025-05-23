import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
if os.getcwd() != script_dir:
    os.chdir(script_dir)

file_name = "example_file.txt"
with open(file_name, 'w') as f:
    f.write("Тест.\n")
    f.write("Строка 2.\n")
    f.write("Строка 3.\n")

if os.path.exists(file_name):
    file_stats = os.stat(file_name)
    print(f"Размер файла: {file_stats.st_size} байт")
    print(f"Дата последнего изменения: {time.ctime(file_stats.st_mtime)}")
    print(f"Дата последнего доступа: {time.ctime(file_stats.st_atime)}")
else:
    exit(1)

print(f"Текущий пользователь: {os.getenv('USER')}")
print(f"Права доступа к файлу: {oct(file_stats.st_mode)[-3:]}")
try:
    os.chmod(file_name, 0o777)
    updated_stats = os.stat(file_name)
    print(f"Новые права доступа: {oct(updated_stats.st_mode)[-3:]}")
except Exception as e:
    print(f"Ошибка: {e}")