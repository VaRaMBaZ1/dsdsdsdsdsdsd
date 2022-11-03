import cfscrape
from bs4 import BeautifulSoup

url = input('Введите адресс сайта: ')
print()

secure_mode = ['cloudflare', 'ddos-guard', 'storm-pro', 'yandexcloud', 'lowprotect', 'fortinet',
               'qrator.net', 'akam', 'awsdns', 'sucuridns', 'azure-dns']

list_site = []
list_site.append(url)

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

    with open('1.txt', 'w') as file:
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

        r = scraper.post(f'https://www.reg.ru/whois/{p}')
        soup = BeautifulSoup(r.text, 'lxml')
        line = soup.find('div', class_="b-whois__table").find('td')

        # for mode in secure_mode:
        #     try:
        #         if mode in str(line).lower():
        #             line_secure.append(i)
        #     except:
        #         pass

        if 'name server:' in str(line).lower():
            line_secure.append(i)


def final():
    for i in line_secure:
        list_checked_site.remove(str(i))

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