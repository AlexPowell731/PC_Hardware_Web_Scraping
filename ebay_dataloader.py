import pandas as pd
import plotly.express as px
from main import EbayProduct
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector

urls = ["https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rx6400&_sacat=0&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&rt=nc&LH_Sold=1&LH_Complete=1",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=rx6500&_sacat=175673&LH_TitleDesc=0&_odkw=rx+6400&_osacat=175673&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=rx6600&_sacat=175673&LH_TitleDesc=0&_odkw=rx6500&_osacat=175673&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rx6600&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=2",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=rx6700&_sacat=175673&LH_TitleDesc=0&_odkw=rx6600&_osacat=175673&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rx6700&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=2",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=rx6800&_sacat=175673&LH_TitleDesc=0&_odkw=rx6700&_osacat=175673&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rx6800&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=2",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=rx6900&_sacat=175673&LH_TitleDesc=0&_odkw=rx6800&_osacat=175673&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3050&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&Chipset%2520Manufacturer=%21&rt=nc&_oaa=1&_dcat=27386",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=rtx+3060&_sacat=175673&LH_TitleDesc=0&_odkw=rtx+3050&_osacat=175673&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3060&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=2",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3060&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=3",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3060&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=4",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3060&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=5",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3060&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=6",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3060&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=7",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=rtx+3070&_sacat=175673&LH_TitleDesc=0&_odkw=rtx+3060&_osacat=175673&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3070&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=2",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3070&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=3",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3070&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=4",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3070&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=5",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3070&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=6",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3070&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=7",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3070&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=8",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=rtx+3080&_sacat=175673&LH_TitleDesc=0&_odkw=rtx+3070&_osacat=175673&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3080&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=2",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3080&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=3",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3080&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=4",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3080&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=5",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3080&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=6",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3080&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=7",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3080&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=8",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=rtx+3090&_sacat=175673&LH_TitleDesc=0&_odkw=rtx+30890&_osacat=175673&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3090&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=2",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3090&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=3",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3090&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=4",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3090&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=5",
        "https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=rtx+3090&_sacat=175673&LH_TitleDesc=0&LH_PrefLoc=1&_ipg=240&LH_Complete=1&LH_Sold=1&_pgn=6"]

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ToastedBuns69",
    database="pc_hardware_web_scraping"
)

mycursor = mydb.cursor()


def get_web_data(url):
    # Get the raw html
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
            'title': str(item.find('div', {'class': 's-item__title'})).replace
            ('<div class="s-item__title"><span aria-level="3" role="heading">', '').replace('</span></div>', '')
            .replace('<span class="LIGHT_HIGHLIGHT">New listing</span>', '')
            .replace('<div class="s-item__title s-item__title--with-icon">', '')
            .replace('<span aria-level="3" role="heading">', '')
            .replace('<span class="clipped">Charity item</span>', '')
            .replace('<svg aria-hidden="true" height="19" width="19"><use xlink:href="#CHARITY_ICON"></use></svg>', ''),
            'condition': item.find('span', {'class': 'SECONDARY_INFO'}).text,
            'soldprice': item.find('span', {'class': 's-item__price'}).text.replace('£', '').replace(',', ''),
            'solddate': str(item.find('span', {'class': 'POSITIVE'})).replace('<span class="POSITIVE">', '').replace
            ('</span>', '').replace('Sold  ', ''),
            'bids': str(item.find('span', {'class': 's-item__bids'})).replace
            ('<span class="s-item__bids s-item__bidCount">', '').replace('</span>', ''),
            'link': str(item.find('a', {'class': 's-item__link'})['href'])
        }

        # Filters out blank listing and checks listing sold before adding product to products list
        if product["title"] != 'Shop on eBay' and product["soldprice"] != '$20.00' and product["solddate"] != 'None':
            product["soldprice"] = product["soldprice"]
            product["solddate"] = datetime.strptime(product['solddate'], '%d %b %Y')
            products.append(product)

    return products


def db_cleanup():
    queries = ["DELETE FROM ebay_raw WHERE title LIKE '%replacement%'", "DELETE FROM ebay_raw WHERE title LIKE "
                                                                        "'%Replacement%'",
               "DELETE FROM ebay_raw WHERE title LIKE '%laptop%'", "DELETE FROM ebay_raw WHERE title LIKE '%Laptop%'",
               "DELETE FROM ebay_raw WHERE title LIKE '%keyboard%'", "DELETE FROM ebay_raw WHERE title LIKE "
                                                                     "'%Keyboard%'",
               "DELETE FROM ebay_raw WHERE title LIKE '%adapter%'", "DELETE FROM ebay_raw WHERE title LIKE '%Adapter%'",
               "DELETE FROM ebay_raw WHERE title LIKE '%backplate%'", "DELETE FROM ebay_raw WHERE title LIKE "
                                                                      "'%Backplate%'", "DELETE FROM ebay_raw WHERE "
                                                                                       "title LIKE '%box%'"]

    for sql in queries:
        mycursor.execute(sql)
        mydb.commit()
        print(f"{sql}")


for url in urls:
    soup = get_web_data(url)
    web_data = parse(soup)

    # Add each item to db after checking no unwanted data will be committed
    for row in web_data:
        bad_price = "to"
        product = EbayProduct(row['title'], row['condition'], row['soldprice'], row['solddate'], row['bids'], row['link'])

        if bad_price in product.soldprice:
            print("\n'to' detected in price, skipping entry!\n")

        else:
            print(product.json())
            sql = "INSERT INTO ebay_testing (title, part_condition, soldprice, solddate, bids, link) VALUES (%s, %s, " \
                  "%s, %s, %s, %s) "
            val = [product.title, product.condition, product.soldprice, product.solddate, product.bids, product.link]
            mycursor.execute(sql, val)
            mydb.commit()


db_cleanup()


