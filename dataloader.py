from main import Product
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rx+6600&_sacat=0&LH_TitleDesc=0&LH_PrefLoc=1&LH_Sold=1&rt=nc"

# Connect with database
engine = create_engine('sqlite:///data.sqlite', echo=True)
# Manage tables
base = declarative_base()
# New session
Session = sessionmaker(bind=engine)
session = Session()
base.metadata.create_all(engine)

def get_data(url):
    # Get the html
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    # Search through information in html
    # Finds all divs that have s-item__info clearfix (each listing on ebay)
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    products = []

    # Finds each element for product dictionary with defined types and filters out unwanted html from results
    for item in results:
        product = {
            'id': int(0),
            'title': str(item.find('h3', {'class': 's-item__title s-item__title--has-tags'})).replace
            ('<h3 class="s-item__title s-item__title--has-tags">', '').replace('</h3>', '').replace(
                '<span class="LIGHT_HIGHLIGHT">', ""),
            'soldprice': item.find('span', {'class': 's-item__price'}).text.replace('£', '').replace(',', ''),
            'solddate': str(item.find('span', {'class': 'POSITIVE'})).replace('<span class="POSITIVE">', '').replace
            ('</span>', '').replace('Sold  ', ''),
            'bids': str(item.find('span', {'class': 's-item__bids'})).replace
            ('<span class="s-item__bids s-item__bidCount">', '').replace('</span>', ''),
            'link': str(item.find('a', {'class': 's-item__link'})['href'])
        }

        # Filters out blank listing and checks listing sold before adding product to products list
        if product["title"] != 'None' and product["soldprice"] != '$20.00' and product["solddate"] != 'None':
            product["soldprice"] = product["soldprice"]
            product["solddate"] = datetime.strptime(product['solddate'], '%d %b %Y')
            products.append(product)
            for product in products:
                product["id"] += 1
    return products


soup = get_data(url)
data = parse(soup)

# Add each item to db
for row in data:
    product = Product(row['id'], row['title'], row['soldprice'], row['solddate'], row['bids'], row['link'])
    session.add(product)
    session.commit()
