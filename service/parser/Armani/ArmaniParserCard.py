import asyncio
import time

from selenium.webdriver.common.by import By

from service.parser.Armani.ArmaniParser import ArmaniParser
from time import sleep
from bs4 import BeautifulSoup

from service.proxy.Proxy import Proxy


class ArmaniParserCard(ArmaniParser):
    def __init__(self, base_url, headers):
        super().__init__(base_url, headers)

    async def start(self):
        product_links = self.get_db.get_is_publish_card_none(category=self.category)
        for link in product_links:
            card = await self.open_url(link)
            try:
                id_product = card.find(class_="modelFabricColor").find("span", class_="value").text
            except:
                id_product = None
            try:
                description = card.find("div", class_="item-info__accordion-content").text.replace("Product Code", "").replace(
                    id_product, "").strip()
            except:
                description = None
            colors = await self.__get_color(link)  # цвета
            size = await self.__get_size(link)
            composition = await self.__get_composition(card)  # состав
            self.update_db.update_items_card(link,
                                             id_product=id_product,
                                             description=description,
                                             composition=composition,
                                             size=size,
                                             colors=colors)
            print(f"[INFO]Продукт {link} в публикации")

    @staticmethod
    async def __get_composition(card):
        composition = []
        try:
            values = card.find("div", attrs={"data-ytos-tab": "Detail-Features"}).find_all("li")
            for li in values:
                composition.append(li.text.strip())
            return ". ".join(composition)
        except:
            return None

    @staticmethod
    async def __get_size(url):
        size = []
        driver = await Proxy().get_chromedriver(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        print(f'[INFO]Открываем страницу {url}')
        driver.get(url)
        time.sleep(10)
        try:
            element = driver.find_element(By.XPATH, '//*[@id="itemInfo"]/div[4]/div[1]/div[1]/div[3]/div/div[1]')
            element.click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            div_size = soup.find_all("div", "option")
            for s in div_size:
                size.append(s.text)
            res = ".".join(size)
            return res.replace("Size.", "")
        except:
            return None

    @staticmethod
    async def __get_color(url_card):
        colors = []
        driver = await Proxy().get_chromedriver(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
        driver.get(url_card)
        sleep(15)
        html = driver.page_source
        driver.close()
        driver.quit()
        b = BeautifulSoup(html, 'lxml')
        ul = b.find("ul", class_="ps").find_all("li")
        if ul:
            for li in ul:
                colors.append(li.find("div", class_="inner").text.strip())
            return ". ".join(colors)
        else:
            color = b.find("div", class_="item-info__section item-info__colors").text.strip()
            return color
