import os
import sys
import psutil
import platform
import subprocess
from typing import Dict, List, Optional

def clear_screen() -> None:
    """Очистка экрана консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu() -> None:
    """Отображение главного меню"""
    print("\n" + "="*50)
    print("Системный монитор и менеджер процессов".center(50))
    print("="*50)
    print("a) Список всех запущенных процессов")
    print("b) Детальная информация о процессе")
    print("c) Завершить процесс по PID")
    print("d) Управление переменными окружения")
    print("e) Изменить приоритет процесса")
    print("f) Информация о системе")
    print("g) Выход")
    print("="*50)

def get_user_choice() -> str:
    """Получение выбора пользователя"""
    while True:
        choice = input("\nВыберите опцию (a-g): ").lower()
        if choice in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
            return choice
        print("Ошибка: введите букву от a до g")

def show_processes() -> None:
    """Отображение списка всех запущенных процессов"""
    clear_screen()
    print("\n" + "="*50)
    print("Список запущенных процессов".center(50))
    print("="*50)
    print("{:<8} {:<25} {:<10} {:<10}".format("PID", "Имя", "Пользователь", "Статус"))
    print("-"*50)
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status']):
        try:
            pid = proc.info['pid']
            name = proc.info['name']
            user = proc.info['username'] or "N/A"
            status = proc.info['status']
            print("{:<8} {:<25} {:<10} {:<10}".format(pid, name[:24], user.split('\\')[-1][:9], status))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def show_process_details() -> None:
    """Отображение детальной информации о процессе"""
    clear_screen()
    try:
        pid = int(input("Введите PID процесса: "))
        proc = psutil.Process(pid)
        
        print("\n" + "="*50)
        print(f"Детальная информация о процессе PID: {pid}".center(50))
        print("="*50)
        
        with proc.oneshot():
            print(f"Имя: {proc.name()}")
            print(f"Статус: {proc.status()}")
            print(f"Пользователь: {proc.username()}")
            print(f"Запущен: {proc.create_time()}")
            print(f"Использует CPU: {proc.cpu_percent()}%")
            print(f"Использует памяти: {proc.memory_info().rss / 1024 / 1024:.2f} MB")
            print(f"Исполняемый файл: {proc.exe() or 'N/A'}")
            print(f"Рабочая директория: {proc.cwd() or 'N/A'}")
            print(f"Аргументы командной строки: {' '.join(proc.cmdline()) or 'N/A'}")
            
    except ValueError:
        print("Ошибка: PID должен быть числом")
    except psutil.NoSuchProcess:
        print(f"Ошибка: процесс с PID {pid} не найден")
    except psutil.AccessDenied:
        print(f"Ошибка: нет прав доступа к процессу {pid}")

def terminate_process() -> None:
    """Завершение процесса по PID"""
    clear_screen()
    try:
        pid = int(input("Введите PID процесса для завершения: "))
        proc = psutil.Process(pid)
        
        print(f"\nПроцесс: {proc.name()} (PID: {pid})")
        confirm = input("Вы уверены, что хотите завершить этот процесс? (y/n): ").lower()
        
        if confirm == 'y':
            proc.terminate()
            print(f"Процесс {pid} был отправлен сигнал на завершение.")
    except ValueError:
        print("Ошибка: PID должен быть числом")
    except psutil.NoSuchProcess:
        print(f"Ошибка: процесс с PID {pid} не найден")
    except psutil.AccessDenied:
        print(f"Ошибка: нет прав доступа к процессу {pid}")

def manage_environment_variables() -> None:
    """Управление переменными окружения"""
    clear_screen()
    print("\n" + "="*50)
    print("Управление переменными окружения".center(50))
    print("="*50)
    print("1) Показать все переменные окружения")
    print("2) Добавить/изменить переменную окружения")
    print("3) Вернуться в главное меню")
    
    choice = input("\nВыберите опцию (1-3): ")
    
    if choice == '1':
        print("\nТекущие переменные окружения:")
        for key, value in os.environ.items():
            print(f"{key}={value}")
    elif choice == '2':
        key = input("Введите имя переменной: ")
        value = input("Введите значение переменной: ")
        os.environ[key] = value
        print(f"Переменная {key} установлена в {value}")
    elif choice == '3':
        return
    else:
        print("Неверный выбор")

def change_process_priority() -> None:
    """Изменение приоритета процесса"""
    clear_screen()
    try:
        pid = int(input("Введите PID процесса: "))
        proc = psutil.Process(pid)
        
        print("\nТекущий приоритет (nice):", proc.nice())
        print("\nДоступные уровни приоритета:")
        print(" - Высокий приоритет (меньшее значение nice)")
        print(" - Низкий приоритет (большее значение nice)")
        
        try:
            new_nice = int(input("\nВведите новое значение nice (-20 до 19): "))
            if -20 <= new_nice <= 19:
                proc.nice(new_nice)
                print(f"Приоритет процесса {pid} изменен на {new_nice}")
            else:
                print("Ошибка: значение nice должно быть между -20 и 19")
        except ValueError:
            print("Ошибка: введите число")
            
    except ValueError:
        print("Ошибка: PID должен быть числом")
    except psutil.NoSuchProcess:
        print(f"Ошибка: процесс с PID {pid} не найден")
    except psutil.AccessDenied:
        print(f"Ошибка: нет прав доступа к процессу {pid}")

def show_system_info() -> None:
    """Отображение информации о системе"""
    clear_screen()
    print("\n" + "="*50)
    print("Информация о системе".center(50))
    print("="*50)
    
    # Информация о системе
    print("\nСистема:")
    print(f"ОС: {platform.system()} {platform.release()}")
    print(f"Версия: {platform.version()}")
    print(f"Архитектура: {platform.machine()}")
    print(f"Процессор: {platform.processor()}")
    
    # Информация о памяти
    mem = psutil.virtual_memory()
    print("\nПамять:")
    print(f"Всего: {mem.total / 1024 / 1024:.2f} MB")
    print(f"Использовано: {mem.used / 1024 / 1024:.2f} MB")
    print(f"Свободно: {mem.free / 1024 / 1024:.2f} MB")
    print(f"Использование: {mem.percent}%")
    
    # Информация о диске
    disk = psutil.disk_usage('/')
    print("\nДиск (/):")
    print(f"Всего: {disk.total / 1024 / 1024 / 1024:.2f} GB")
    print(f"Использовано: {disk.used / 1024 / 1024 / 1024:.2f} GB")
    print(f"Свободно: {disk.free / 1024 / 1024 / 1024:.2f} GB")
    print(f"Использование: {disk.percent}%")

def main() -> None:
    """Главная функция"""
    # Проверка зависимостей
    try:
        import psutil
    except ImportError:
        print("Ошибка: для работы скрипта требуется установить модуль psutil")
        print("Установите его командой: pip install psutil")
        sys.exit(1)
    
    while True:
        show_menu()
        choice = get_user_choice()
        
        if choice == 'a':
            show_processes()
        elif choice == 'b':
            show_process_details()
        elif choice == 'c':
            terminate_process()
        elif choice == 'd':
            manage_environment_variables()
        elif choice == 'e':
            change_process_priority()
        elif choice == 'f':
            show_system_info()
        elif choice == 'g':
            print("\nВыход из программы...")
            break
        
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main()