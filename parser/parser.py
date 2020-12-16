import requests #импортируем пакет обеспечивающий работу с HTTP запросами
from bs4 import BeautifulSoup #импортируем пакет для того чтобы распарсить дерево
import csv #импортируем пакет для csv(excel) файлов 

#задаем константы
URL = 'https://auto.ru/moskva/cars/gmc/all/'
HEADERS = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.456',
    'accept': '*/*'
}
HOST = 'https://auto.ru'
FILE = 'cars.csv'

#функция для получения web-страницы
def get_html(url, params=None):
	r = requests.get(url, headers=HEADERS, params=params)
	return r

#функция для того чтобы парсить сразу мгого страниц
def get_pages_count(html):
	soup = BeautifulSoup(html, 'html.parser')
	pagination = soup.find_all('span',class_='Button__text')
	if pagination:
		return int(pagination[-4].get_text())
	else:
		return 1

#функция для получения контента из html 
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div',class_='ListingItem-module__main')
    cars = []
    for item in items:
    	price = item.find('div', class_='ListingItemPrice-module__content')
    	price = price.get_text().replace(u'\xa0',u' ')
    	cars.append({
    		'title': item.find('a',class_='Link ListingItemTitle-module__link').get_text(strip=True),
    		'link': item.find('a',class_='Link ListingItemTitle-module__link').get('href'),
    		'price': price,
    		'city' : item.find('span',class_="MetroListPlace__regionName MetroListPlace_nbsp").get_text(),
    		})
    return cars
 
#функция для создания и сохранения в файле данных
def save_file(items, path):
	with open(path, 'w', newline = '',encoding = "utf-8") as file:
		writer = csv.writer(file, delimiter = ';')
		writer.writerow(['Марка','Cсылка','Цена','Город']) 
		for item in items:
			writer.writerow([item['title'],item['link'],item['price'],item['city']])

#основная функция для парсинга
def parse():
	URL = input('Введите ссылку:  ')
	html = get_html(URL)
	if html.status_code==200:
		cars=[]
		pages_count = get_pages_count(html.text)
		for page in range(1, pages_count + 1):
			print('\n')
			print(f'Парсинг страницы {page} из {pages_count} ...')
			html = get_html(URL, params={'page': page})
			cars.extend(get_content(html.text))
		
		save_file(cars,FILE)
		print('\n\n' + f'Получено {len(cars)} автомобилей')
	else:
		print('ERROR')


parse()