#Make a request to the ebay.com get a page
#collect data from each detail page
#collect all links to detail pages of each product
# write scraped data to a csv file

import requests
from bs4 import BeautifulSoup
import csv

def get_page(url):
    response = requests.get(url)
    
    if not response.ok:
        print('Server Responded', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')

    return soup
    #print(response.ok)
    #print(response.status_code)


def get_detail_data(soup):
    #title
    #price 
    #item sold
    try:

        title = soup.find('h1', id='itemTitle').get_text().replace('Details about', '').strip()
        
    except:
        title = ''
    
    try:
        p = soup.find('span', id='prcIsum').text.strip().split(' ')
        currency, price = p
    except:
        price = ''
        currency = ''

    try:
        sold = soup.find('span', class_='vi-qtyS-hot-red').find('a').text.strip().split(' ')[0]
    
    except:
        sold = ''

    data = {
        'title':title,
        'price': price,
        'currency': currency,
        'sold':sold
    }
    
    return data

def get_index_data(soup):

    try:
        links = soup.find_all('a', class_='s-item__link')

    except:
        links = []

    urls = [item.get('href') for item in links]
    return urls

def write_csv(data, url):

    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'], data['price'], data['currency'], data['sold'], url]
        writer.writerow(row)
        
def main():
    url = 'https://www.ebay.com/sch/i.html?_nkw=mens+watches&_pgn=1'
    

    product = get_index_data(get_page(url))

    for link in product:
        data = get_detail_data(get_page(link))
        write_csv(data, link)

if __name__ == '__main__':
    main()
