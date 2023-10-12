from datetime import datetime
import requests
from bs4 import BeautifulSoup
import grpc
import product_pb2
from product import Product
def scrape_amazon_bestsellers():
    baseUrl = 'https://www.amazon.com.tr'
    url = baseUrl + '/gp/bestsellers?ref_=nav_cs_bestsellers/'
    productList = []

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_titles = soup.find_all('div', class_='_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL')
        for title in article_titles:
            response = requests.get(baseUrl + title.a.get('href'))
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                paginations = soup.find_all('ul', class_='a-pagination')
                for page in paginations:
                    p = page.find_all('li')
                    for a in p[1:-1]:
                        response = requests.get(baseUrl + a.a.get('href'))
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            products = soup.find_all('div', id=['gridItemRoot'])
                            for product in products:
                                productName = product.find('div', class_='_cDEzb_p13n-sc-css-line-clamp-3_g3dy1')
                                rating = product.find('span', class_='a-icon-alt')
                                feedBack = product.find('span', class_='a-size-small')
                                price = product.find('span', class_='p13n-sc-price')
                                if price is not None:
                                    price_text = price.text.replace('\xa0', '')
                                else:
                                    price_text = 0
                                prod = product_pb2.Product(
                                    productName.text if productName is not None else "",
                                    rating.text if rating is not None else "",
                                    feedBack.text if feedBack is not None else "",
                                    price_text
                                )
                                productList.append(prod)

    return productList
                    






