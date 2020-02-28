from bs4 import BeautifulSoup
import requests

HEADER = {'User-Agent': 'Mozilla/5.0'}

def _get_soup(url):
    response = requests.get(url, headers=HEADER)
    return BeautifulSoup(response.text, "html.parser")

def naver_smart_store_1(soup):
    out_of_order = soup.find('div', class_='not_goods')
    if out_of_order:
        return False
    return True

def welkeepsmall_1(soup):
    out_of_order = soup.find('div', class_='soldout')
    if out_of_order:
        return False
    return True

def kakao_store_1(soup):
    bottom_button = soup.find('div', class_='_bottom_buttons wrap_btn_detail')
    bottom_text = bottom_button.text.strip()
    if bottom_text == '품절':
        return False
    return True



# MAIN
def is_mask_available(store):
    parser_fn = globals()[store.crawling_type]  # execption raised if parser not exists
    soup = _get_soup(store.product_url)

    return parser_fn(soup)
