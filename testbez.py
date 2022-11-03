import cfscrape
from bs4 import BeautifulSoup

url = input('Введите адресс сайта: ')
print()

secure_mode = ['cloudflare', 'ddos-guard', 'storm-pro', 'yandexcloud', 'lowprotect', 'fortinet',
               'qrator.net', 'akam', 'awsdns', 'sucuridns', 'azure-dns', 'OVH']

list_site = []
list_checked_site = []
line_no_secure = []
line_secure = []


def get_ip(site):
    print('Получаю IP сайта...')
    scraper = cfscrape.create_scraper()
    r = scraper.get(f'https://www.reg.ru/misc/ip_host_lookup?ip_address_or_host={site}').json()
    data = str(r['ipv4']).replace("['", "").replace("']", "")
    return data


def scan_one_ip():
    scraper = cfscrape.create_scraper()
    r = scraper.post('https://2ip.online/domain-list-by-ip/', data={"ip": get_ip(url)})
    print('Ищу сайты на одном IP...')
    soup = BeautifulSoup(r.text, 'lxml')
    line = soup.find('table', class_="TableStart").find_all('a')

    for i in line:
        try:
            list_site.append(str(i['href']))
        except:
            pass


def scan_site():
    print('Проверяю найденные сайты...')
    scraper = cfscrape.create_scraper()
    for i in list_site:
        try:
            p = scraper.post(i)
            if not 'gov' in i:
                list_checked_site.append(i)
        except:
            pass


def check_host():
    print('Проверяю на уязвимости...')
    scraper = cfscrape.create_scraper()
    for i in list_checked_site:
        if 'https://' in str(i):
            p = str(i).replace('https:', '').replace('/', '').strip()
        elif 'http://' in str(i):
            p = str(i).replace('http:', '').replace('/', '').strip()

        r = scraper.post(f'https://2ip.ua/ru/services/information-service/site-information', data={'a': 'act', 'ip': p})
        soup = BeautifulSoup(r.text, 'lxml')
        line = soup.find('table', class_="table table-striped").find_all('td')[1].text

        for mode in secure_mode:
            try:
                if mode in str(line).lower():
                    list_checked_site.remove(i)
            except:
                pass




def final():
    if len(list_checked_site) == 0:
        print('\nУязвимости не найдены!')
    else:
        print('\nНайдены уязвимости на сайтах: ')
        for i in list_checked_site:
            print(f'    {i}')


scan_one_ip()
scan_site()
check_host()
final()

input()