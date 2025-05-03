import os
import shutil

def main():
    # 1) Скопирует файл с предыдущего задания
    original_file = 'example_file.txt'
    copied_file = 'copied_file.txt'
    
    if os.path.exists(original_file):
        shutil.copy2(original_file, copied_file)
        print(f"Файл {original_file} скопирован как {copied_file}")
    else:
        print(f"Файл {original_file} не найден, создаем новый")
        with open(original_file, 'w') as f:
            f.write("Пример содержимого файла\n")
        shutil.copy2(original_file, copied_file)

    # 2) Переименует файл. Создайте несколько вложенных директорий и переместите копию файла в одну из них
    renamed_file = 'renamed_file.txt'
    os.rename(copied_file, renamed_file)
    
    nested_dirs = os.path.join('src', 'secsem','lab3','dir1', 'dir2', 'dir3')
    os.makedirs(nested_dirs, exist_ok=True)
    
    destination_path = os.path.join(nested_dirs, renamed_file)
    shutil.move(renamed_file, destination_path)
    print(f"Файл перемещен в: {destination_path}")

    # 3) Создаст новый файл. Переместите и переименуйте его с помощью одной команды os
    new_file = 'new_file.txt'
    with open(new_file, 'w') as f:
        f.write("Это новый файл\n")
    
    new_location = os.path.join('src', 'secsem','lab3','dir1', 'moved_renamed_file.txt')
    os.rename(new_file, new_location)
    print(f"Файл создан и перемещен и переименован: {new_location}")

    # 4) Программно создайте ещё несколько файлов. Выведите все файлы и директории, лежащие в папке, в которой запущен скрипт. Переместитесь во вложенную директорию в которую переместили файл. Выведите все, что находится в этой директории
    for i in range(1, 4):
        with open(f'extra_file_{i}.txt', 'w') as f:
            f.write(f"Дополнительный файл {i}\n")
    
    print("\nСодержимое текущей директории:")
    for item in os.listdir('.'):
        print(f" - {item}")
    
    print(f"\nПеремещаемся в {nested_dirs}")
    os.chdir(nested_dirs)
    
    print("Содержимое вложенной директории:")
    for item in os.listdir('.'):
        print(f" - {item}")
    
    # 5) Вернитесь в папку со скриптом; Создайте пустую директорию, после чего удалите её. Создайте ещё несколько вложенных директорий и файлов;

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("\nВернулись в директорию со скриптом")
    
    empty_dir = 'empty_dir'
    os.makedirs(empty_dir, exist_ok=True)
    os.rmdir(empty_dir)
    print(f"Создана и удалена пустая директория: {empty_dir}")
    
    few_other = os.path.join('few', 'other', 'dirs')
    os.makedirs(few_other, exist_ok=True)
    
    for i in range(1, 3):
        file_path = os.path.join(few_other, f'deep_file_{i}.txt')
        with open(file_path, 'w') as f:
            f.write(f"Файл в глубокой директории {i}\n")
    print(f"Созданы вложенные директории и файлы в {few_other}")

    # 6) Обойдите текущую директорию и выведите: путь до каждой папки, список файлов в каждой папке.

    print("\nОбход директорий:")
    for root, dirs, files in os.walk('.'):
        print(f"\nДиректория: {root}")
        print("Поддиректории:", ', '.join(dirs) if dirs else "нет")
        print("Файлы:", ', '.join(files) if files else "нет")

if __name__ == '__main__':
    main()