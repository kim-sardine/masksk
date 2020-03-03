import requests
import random
from bs4 import BeautifulSoup


from mask.core.exceptions import RequestsException

USER_AGENT = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931'
]


def _get_soup(url):
    try:
        response = requests.get(
            url,
            headers={
                'User-Agent': random.choice(USER_AGENT)
            },
            timeout=10
        )
    except Exception as e:
        raise RequestsException(e)

    return BeautifulSoup(response.text, "html.parser")

def naver_smart_store_1(soup):
    is_available = soup.find('div', class_='sum_total')
    if is_available:
        return True
    return False

# FIXME: 재고 있는 모습을 못봐서.. 아직 재고 있는 기준을 정하지 못함
def welkeepsmall_1(soup):
    out_of_order = soup.find('div', class_='soldout')
    if not out_of_order:
        return True
    return False

def welkeepsmall_all(soup):
    masks = soup.find_all('div', class_="tb-center")
    for mask in masks:
        sold_out = mask.find('li', class_="soldout")
        if not sold_out:  # 한개라도 sold out 이 아니면 재고 있음으로 판단
            return True

    return False

def kakao_store_1(soup):
    bottom_button = soup.find('div', class_='_bottom_buttons wrap_btn_detail')
    if bottom_button:
        bottom_text = bottom_button.text.strip()
        if bottom_text == '구매하기':
            return True
    return False

def bling_market_1(soup):
    buying_button = soup.find('div', class_='btn_wrap mt40')
    if buying_button:
        return True
    return False

def coupang_1(soup):
    buying_button = soup.find('div', class_=['prod-buy', 'new-oos-style'])
    if buying_button:
        classes = buying_button.get('class')
        if classes:
            if 'sold-out' not in classes:
                return True
    return False

def ssg_1(soup):
    buying_button = soup.find('a', id='actionPayment')
    if buying_button:
        return True
    return False


# MAIN
def is_mask_available(store):
    soup = _get_soup(store.product_url)
    parser_fn = globals()[store.crawling_type]  # execption raised if parser not exists

    return parser_fn(soup)
