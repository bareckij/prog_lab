import time
import threading

def print_message(message, delay):
    """Функция, которая выводит сообщение с заданной задержкой"""
    time.sleep(delay)
    print(message)

messages = ["Сообщение 1", "Сообщение 2", "Сообщение 3"]
delay = 2  

print("Последовательный запуск:")
start_time = time.time()

for msg in messages:
    print_message(msg, delay)

sequential_time = time.time() - start_time
print(f"Общее время (последовательно): {sequential_time:.2f} сек\n")

print("Параллельный запуск в потоках:")
start_time = time.time()

threads = []
for msg in messages:
    thread = threading.Thread(target=print_message, args=(msg, delay))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

parallel_time = time.time() - start_time
print(f"Общее время (параллельно): {parallel_time:.2f} сек")

print("\nСравнение:")
print(f"Последовательно: {sequential_time:.2f} сек")
print(f"Параллельно:    {parallel_time:.2f} сек")
print(f"Ускорение:      {sequential_time/parallel_time:.1f}x")