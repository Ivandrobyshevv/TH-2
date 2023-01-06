import asyncio
import time

from bs4 import BeautifulSoup

from service.parser.Levis.LevisParser import LevisParser
from service.proxy.Proxy import Proxy


class LevisParserCard(LevisParser):
    def __init__(self, base_url, headers):
        super().__init__(base_url, headers)

    async def start(self):
        product_links = self.get_db.get_is_publish_card_none(category=self.category)
        for link in product_links:
            card = await self.open_url(link)
            try:
                description = card.find("div", class_="contentContainer").text
            except:
                description = None
            try:
                colors = await self.__get_color(card)
            except:
                colors = None
            try:
                size = await self.__get_size(card)
            except:
                size = None
            try:
                composition = card.find("div", class_="product-spec-overview").text.replace("How it Fits", "").replace(
                    "Composition & Care", " ")
            except:
                composition = None

            self.update_db.update_items_card(card_link=link,
                                             description=description,
                                             composition=composition,
                                             colors=colors,
                                             size=size)
            print(f"[INFO]Продукт {link} в публикации")

    async def open_url(self, url: str):
        driver = await Proxy().get_chromedriver(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        print(f'[INFO]Открываем страницу {url}')
        driver.get(url)
        time.sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        return soup

    @staticmethod
    async def __get_color(card):
        colors = []
        ul_color = card.find("ul", class_="swatches-expand")
        for li in ul_color:
            colors.append(li.find("img", class_="outOfStockImg").get("alt"))

        return ". ".join(colors)

    @staticmethod
    async def __get_size(card):
        size = []
        ul_size = card.find("ul", class_="tiles-inner-grid-container")
        for li in ul_size:
            size.append(li.find("span", class_="product-size-tile-value").text)

        return ". ".join(size)
