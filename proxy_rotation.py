import time
import requests
from bs4 import BeautifulSoup

def get_proxies():
    with open("valid_proxy_list.txt", "r") as f:
        proxies = f.read().split("\n")
    return proxies

def get_proxy_index(proxy_num):
    with open("last_used_proxy_index.txt", "r+") as f:
        last_used_proxy_index = int(f.readlines()[0])
        if last_used_proxy_index >= proxy_num:
            last_used_proxy_index = 0
        else:
            last_used_proxy_index += 1
        #delete
        f.seek(0)
        f.truncate()
        #write
        f.write(str(last_used_proxy_index))
    return last_used_proxy_index
    
def main():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    payload = {
        '_csrf': '',
        'username': 'test_user',
        'password': '123'
    }

    proxies = get_proxies()
    proxy_num = len(proxies)-1
    print("Number of proxies: " + str(proxy_num+1))
    last_used_proxy_index = get_proxy_index(proxy_num)
    proxy = proxies[last_used_proxy_index]
    print("Using proxy index " + str(last_used_proxy_index) + ": " + proxy)

    with requests.Session() as s:
        url = "https://chimeratool.com/pt/login"
        try:
            r = s.get(url, headers=headers) #, proxies={"https": proxy, "http": proxy}
            print(r.status_code)
        except:
            print("Proxy failed...")
            return
        
        soup = BeautifulSoup(r.content, 'html.parser')
        payload['_csrf'] = soup.find('input', {'name': '_csrf'})['value']
        print(payload)
        
        time.sleep(2)
        r = s.post(url, data=payload, headers=headers) #, proxies={"https": proxy, "http": proxy}
        soup = BeautifulSoup(r.content, 'html.parser')
        username =  soup.find("span", {"id": "headerUserName"})
        if username:
            print("Logged in as: " + username.text + "...")
        else:
            print("Not logged in... Error or captcha...")
            print(soup.find("title").text)
            print(soup.find("img", {"id": "w0-image"}))

if __name__ == "__main__":
    main()