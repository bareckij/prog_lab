import time
import threading

def print_with_delay(message):
    """Функция, которая ждёт 2 секунды и печатает сообщение."""
    time.sleep(2)  
    print(message)

thread = threading.Thread(target=print_with_delay, args=("Сообщение после 2 секунд",))
thread.start()

print("Основной поток продолжает работу...")

thread.join()
print("Поток завершил работу.")