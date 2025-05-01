import requests
import time
import asyncio
import aiohttp

# Синхронная версия 
def fetch_sync(url):
    start_time = time.time()
    response = requests.get(url)
    elapsed_time = time.time() - start_time
    return f"{url} | Status: {response.status_code} | Time: {elapsed_time:.2f}s"

def main_sync():
    urls = [
        "https://google.com",        # Быстрый
        "https://youtube.com",       # Средний
        "https://reddit.com",        # Медленный
    ]

    start_total = time.time()
    for url in urls:
        print(fetch_sync(url))
    
    total_time = time.time() - start_total
    print(f"\nTotal time (sync): {total_time:.2f}s")

# Асинхронная версия
async def fetch_async(session, url):
    start_time = time.time()
    async with session.get(url) as response:
        elapsed_time = time.time() - start_time
        return f"{url} | Status: {response.status} | Time: {elapsed_time:.2f}s"

async def main_async():
    urls = [
        "https://google.com",
        "https://youtube.com",
        "https://reddit.com",
    ]

    start_total = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_async(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            print(result)
    
    total_time = time.time() - start_total
    print(f"\nTotal time (async): {total_time:.2f}s")

if __name__ == "__main__":
    print("=== Synchronous execution ===")
    main_sync()
    
    print("\n=== Asynchronous execution ===")
    asyncio.run(main_async())