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
                desc = card.find("div", class_="item-info__accordion-content").text.replace("Product Code", "").replace(
                    id_product, "").strip()
            except:
                id_product = None
                desc = None
            # size =  # размеры
            colors = await self.get_color(link)  # цвета
            composition = await self.get_detail(card)  # состав
            self.update_db.update_items_card(link,
                                             id_product=id_product,
                                             description=desc,
                                             composition=composition,
                                             colors=colors)
            print(f"[INFO]Продукт {link} в публикации")

    @staticmethod
    async def get_detail(card):
        composition = []
        values = card.find("div", attrs={"data-ytos-tab": "Detail-Features"}).find_all("li")
        for li in values:
            composition.append(li.text.strip())
        return ". ".join(composition)

    @staticmethod
    async def get_color(url_card):
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
