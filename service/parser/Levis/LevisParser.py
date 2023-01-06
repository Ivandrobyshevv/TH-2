import time

from database.methods.add import InsertDataBase
from database.methods.get import GetDataBase
from database.methods.update import UpdateDataBase
from service.parser.Parser import Parser
from service.proxy.Proxy import Proxy
from bs4 import BeautifulSoup


class LevisParser(Parser):
    def __init__(self, base_url, headers):
        super().__init__(base_url, headers)
        self.get_db = GetDataBase()
        self.add_db = InsertDataBase()
        self.update_db = UpdateDataBase()
        self.category = 2

    async def open_url(self, url: str):
        time_out = 10
        driver = await Proxy().get_chromedriver(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        print(f'[INFO]Открываем страницу {url}')
        driver.get(url)
        time.sleep(time_out)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        try:
            total_product = soup.find(class_="filter-bar__results-count").text.replace("Items", '').strip()
        except:
            total_product = 0
        all_card = soup.find_all("div", class_="product-cell")
        return total_product, all_card
