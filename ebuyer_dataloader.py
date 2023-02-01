from main import NewProduct
import requests
from bs4 import BeautifulSoup
from datetime import date
import mysql.connector

urls = ['https://www.ebuyer.com/store/Components/cat/Memory---PC',
        'https://www.ebuyer.com/store/Components/cat/Memory---PC?page=2',
        'https://www.ebuyer.com/store/Components/cat/Memory---PC?page=3',
        'https://www.ebuyer.com/store/Components/cat/Memory---PC?page=4',
        'https://www.ebuyer.com/store/Components/cat/Memory---PC?page=5',
        'https://www.ebuyer.com/store/Components/cat/Memory---PC?page=6',
        'https://www.ebuyer.com/store/Components/cat/Memory---PC?page=7',
        'https://www.ebuyer.com/store/Components/cat/Memory---PC?page=8',
        'https://www.ebuyer.com/store/Components/cat/Memory---PC?page=9',
        'https://www.ebuyer.com/store/Components/cat/Memory---PC?page=10',
        'https://www.ebuyer.com/store/Components/cat/Memory---PC?page=11',
        'https://www.ebuyer.com/store/Components/cat/Motherboards-Intel',
        'https://www.ebuyer.com/store/Components/cat/Motherboards-Intel?page=2',
        'https://www.ebuyer.com/store/Components/cat/Motherboards-Intel?page=3',
        'https://www.ebuyer.com/store/Components/cat/Motherboards-Intel?page=4',
        'https://www.ebuyer.com/store/Components/cat/Motherboards-Intel?page=5',
        'https://www.ebuyer.com/store/Components/cat/Motherboards-Intel?page=6',
        'https://www.ebuyer.com/store/Components/cat/Motherboards-AMD',
        'https://www.ebuyer.com/store/Components/cat/Motherboards-AMD?page=2',
        'https://www.ebuyer.com/store/Components/cat/Motherboards-AMD?page=3',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia?page=2',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia?page=3',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia?page=4',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia?page=5',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia?page=6',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia?page=7',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia?page=8',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia?page=9',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia?page=10',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-AMD',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-AMD?page=2',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-AMD?page=3',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-AMD?page=4',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-AMD?page=5',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-AMD?page=6',
        'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-AMD?page=7',
        'https://www.ebuyer.com/store/Components/cat/Power-Supplies',
        'https://www.ebuyer.com/store/Components/cat/Power-Supplies?page=2',
        'https://www.ebuyer.com/store/Components/cat/Power-Supplies?page=3',
        'https://www.ebuyer.com/store/Components/cat/Processors-Intel',
        'https://www.ebuyer.com/store/Components/cat/Processors-Intel?page=2',
        'https://www.ebuyer.com/store/Components/cat/Processors-Intel?page=3',
        'https://www.ebuyer.com/store/Components/cat/Processors-Intel?page=4',
        'https://www.ebuyer.com/store/Components/cat/Processors-AMD',
        'https://www.ebuyer.com/store/Components/cat/Processors-AMD?page=2',
        'https://www.ebuyer.com/store/Components/cat/Processors-AMD?page=3',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---SSD/subcat/2.5%22-SSD',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---SSD/subcat/2.5%22-SSD?page=2',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---SSD/subcat/2.5%22-SSD?page=3',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---SSD/subcat/2.5%22-SSD?page=4',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---SSD/subcat/M.2-SSD',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---SSD/subcat/M.2-SSD?page=2',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---SSD/subcat/M.2-SSD?page=3',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---SSD/subcat/M.2-SSD?page=4',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---SSD/subcat/M.2-SSD?page=5',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---SSD/subcat/M.2-SSD?page=6',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---Internal/subcat/3.5%22-SATA-Drives',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---Internal/subcat/3.5%22-SATA-Drives?page=2',
        'https://www.ebuyer.com/store/Storage/cat/Hard-Drive---Internal/subcat/3.5%22-SATA-Drives?page=3'
        ]

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ToastedBuns69",
    database="pc_hardware_web_scraping"
)

mycursor = mydb.cursor()


def get_web_data(url):
    # Get raw HTML
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def parse(soup):
    results = soup.find_all('div', {'class': 'grid-item js-listing-product'})
    products = []

    for item in results:
        product = {
            'title': str(item.find('h3', {'class': 'grid-item__title'})).replace
            ('<h3 class="grid-item__title">\n<a data-analytics-event="click" data-event-action="Product Click" '
             'data-event-category="Search Listings - Grid" data-event-label="Title" href="/', '').replace
            ('\n            </a>\n</h3>', ''),
            'price': str(item.find('div', {'class': 'inc-vat'})).replace
            ('<div class="inc-vat"><p class="price">\n<span class="smaller currency-symbol">£</span>\n        ', '')
            .replace('\n        <span class="vat-text">\xa0inc. vat</span> </p>', '').replace(',', ''),
            'link': str(item.find('h3', {'class': 'grid-item__title'}))
            .replace('<h3 class="grid-item__title">\n<a data-analytics-event="click" data-event-action="Product '
                     'Click" data-event-category="Search Listings - Grid" data-event-label="Title" href="', '').replace(
                '\n            </a>\n</h3>', '')
        }
        if product['price'] != 'None':
            product['website'] = 'Ebuyer UK'
            products.append(product)

    for product in products:
        title_start = product['title'].index('>\n                ')
        price_end = product['price'].index('<')
        link_end = product['title'].index('"')
        product['title'] = product['title'][title_start + 18:]
        product['link'] = "https://www.ebuyer.com" + product['link'][:link_end]
        product['price'] = product['price'][:price_end]
        product['price'] = float(product['price'])
        product['date'] = date.today()

    return products


for url in urls:
    soup = get_web_data(url)
    web_data = parse(soup)

    for row in web_data:
        product = NewProduct(row['title'], row['price'], row['link'], row['date'])
        print(product.json())
        sql = "INSERT INTO ebuyer_raw (title, price, link, date) VALUES (%s, %s, %s, %s)"
        val = [product.title, product.price, product.link, product.date]
        mycursor.execute(sql, val)
        mydb.commit()
