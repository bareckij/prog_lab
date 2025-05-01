import threading
import time

counter = 0

def increment_counter():
    """Функция, увеличивающая глобальную переменную counter"""
    global counter
    for _ in range(100000):  
        temp = counter       
        temp += 1      
        time.sleep(0.000001)     
        counter = temp       

threads = []
for _ in range(5):
    thread = threading.Thread(target=increment_counter)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(f"Итоговое значение counter: {counter} (ожидалось: 500000)")