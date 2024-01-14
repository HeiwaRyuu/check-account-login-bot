import threading
import queue
import requests

q = queue.Queue()
valid_proxies = []

with open("proxy_list.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)


def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        print("Checking proxy: " + proxy)
        try:
            r = requests.get("https://chimeratool.com/pt/login", proxies={"https": proxy, "http": proxy})
        except:
            continue
        if r.status_code == 200:
            print(proxy)


for _ in range(10):
    threading.Thread(target=check_proxies).start()