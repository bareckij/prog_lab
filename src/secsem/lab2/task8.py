import threading

counter = 0
lock = threading.Lock()

def safe_increment_counter():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

def run_threads(thread_count=5):
    global counter
    counter = 0  
    
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=safe_increment_counter)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    return f"Итоговое значение counter: {counter} (корректно: {thread_count * 100000})"

if __name__ == "__main__":
    result = run_threads()
    print(result)