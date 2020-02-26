from bs4 import BeautifulSoup
import requests

HEADER = {'User-Agent': 'Mozilla/5.0'}

def naver_smart_store_1(url):
    response = requests.get(url, headers=HEADER)
    bs = BeautifulSoup(response.text, "html.parser")
    out_of_order = bs.find('div', class_='not_goods')
    print(out_of_order)

def welkeepsmall_1(url):
    response = requests.get(url, headers=HEADER)
    bs = BeautifulSoup(response.text, "html.parser")
    out_of_order = bs.find('div', class_='soldout')
    print(out_of_order)


def run(store):
    """
    Crawl store

    go to product_url and get information
    """
    url = store.product_url
    crawling_type = store.crawling_type
    method_to_call = globals().get(crawling_type)    
    now_in_stock = method_to_call(url)
    
    return now_in_stock
