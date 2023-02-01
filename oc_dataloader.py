from main import NewProduct
import requests
from bs4 import BeautifulSoup
from datetime import date
import mysql.connector

urls = ['https://www.overclockers.co.uk/pc-components/motherboards/amd-motherboards',
        'https://www.overclockers.co.uk/pc-components/motherboards/amd-motherboards?page=2',
        'https://www.overclockers.co.uk/pc-components/motherboards/amd-motherboards?page=3',
        'https://www.overclockers.co.uk/pc-components/motherboards/intel-motherboards',
        'https://www.overclockers.co.uk/pc-components/motherboards/intel-motherboards?page=2',
        'https://www.overclockers.co.uk/pc-components/motherboards/intel-motherboards?page=3',
        'https://www.overclockers.co.uk/pc-components/motherboards/intel-motherboards?page=4',
        'https://www.overclockers.co.uk/pc-components/processors/amd-processors',
        'https://www.overclockers.co.uk/pc-components/processors/intel-processors',
        'https://www.overclockers.co.uk/pc-components/graphics-cards/amd-graphics-cards',
        'https://www.overclockers.co.uk/pc-components/graphics-cards/amd-graphics-cards?page=2',
        'https://www.overclockers.co.uk/pc-components/graphics-cards/nvidia-graphics-cards',
        'https://www.overclockers.co.uk/pc-components/graphics-cards/nvidia-graphics-cards?page=2',
        'https://www.overclockers.co.uk/pc-components/graphics-cards/nvidia-graphics-cards?page=3',
        'https://www.overclockers.co.uk/pc-components/graphics-cards/nvidia-graphics-cards?page=4',
        'https://www.overclockers.co.uk/pc-components/graphics-cards/intel-arc-graphics-cards',
        'https://www.overclockers.co.uk/pc-components/pc-power-supplies',
        'https://www.overclockers.co.uk/pc-components/pc-power-supplies?page=2',
        'https://www.overclockers.co.uk/pc-components/pc-power-supplies?page=3',
        'https://www.overclockers.co.uk/pc-components/pc-power-supplies?page=4',
        'https://www.overclockers.co.uk/pc-components/pc-power-supplies?page=5',
        'https://www.overclockers.co.uk/pc-components/pc-power-supplies?page=6',
        'https://www.overclockers.co.uk/pc-components/memory',
        'https://www.overclockers.co.uk/pc-components/memory?page=2',
        'https://www.overclockers.co.uk/pc-components/memory?page=3',
        'https://www.overclockers.co.uk/pc-components/memory?page=4',
        'https://www.overclockers.co.uk/pc-components/storage/ssd-solid-state',
        'https://www.overclockers.co.uk/pc-components/storage/ssd-solid-state?page=2',
        'https://www.overclockers.co.uk/pc-components/storage/ssd-solid-state?page=3',
        'https://www.overclockers.co.uk/pc-components/storage/internal-hard-drives-hdd',
        'https://www.overclockers.co.uk/pc-components/storage/internal-hard-drives-hdd?page=2']

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
    results = soup.find_all('div', {'class': 'col'})
    products = []

    for item in results:
        product = {
            'title': str(item.find('div', {'class': 'col position-relative'})).replace('</a>', '').replace('(N206S2'
                                                                                                           '-08D6X'
                                                                                                           '-1710VA',
                                                                                                           ''),
            'price': str(item.find('span', {'data-qa': 'price-current'})).replace('<span class="price__amount" '
                                                                                  'data-qa="price-current">',
                                                                                  '').replace('\n', '').replace(
                '</span>', '').replace('£', '').replace(',', '').replace('<span class="price__amount '
                                                                         'price__amount--original" '
                                                                         'data-qa="price-original">', ''),
            'link': str(item.find('h6', {'class': 'h5 mb-0 text-break'})).
            replace('<h6 class="h5 mb-0 text-break" data-qa="ck-product-box-product-name"><a class="text-inherit '
                    'text-decoration-none js-gtm-product-link" href="', '')
        }

        if product['title'] != 'None' and product['price'] != 'None':
            product['website'] = 'Overclockers UK'
            products.append(product)

    for product in products:
        title_start = product['title'].index('l">')
        title_end = product['title'].index('</h6>\n')
        link_end = product['link'].index('">')
        product['title'] = product['title'][title_start + 3:title_end]
        product['price'] = float(product['price'])
        product['link'] = "https://www.overclockers.co.uk" + product['link'][:link_end]
        product['date'] = date.today()

    return products


for url in urls:
    soup = get_web_data(url)
    web_data = parse(soup)

    for row in web_data:
        product = NewProduct(row['title'], row['price'], row['link'], row['date'])
        print(product.json())
        sql = "INSERT INTO oc_raw (title, price, link, date) VALUES (%s, %s, %s, %s)"
        val = [product.title, product.price, product.link, product.date]
        mycursor.execute(sql, val)
        mydb.commit()


