import logging

from database.models import Products
from service.parser.Armani.ArmaniParser import ArmaniParser
from bs4 import BeautifulSoup


class ArmaniParserPage(ArmaniParser):
    def __init__(self, base_url: str, headers: dict):
        super().__init__(base_url, headers)

    async def start(self):
        links = []
        category = ["/men/view-all-sale-man", "/women/view-all-sale-woman"]
        for url_cat in category:
            soup = await self.open_url(await self.__generator_url(url_cat))
            total_page, cards = await self.__get_data_page(soup)
            links.extend(await self.add_product(cards))
            for page in range(2, total_page + 1):
                total_items = await self.__get_data_page(await self.open_url(await self.__generator_url(url_cat, page)))
                links.extend(await self.add_product(total_items[1]))

        disabled_products = await self.__is_publish_check(links)
        print(f"[INFO]Отключено карточек {disabled_products}")
        return links

    async def add_product(self, all_card: list):
        """Добаление карточки в БД"""
        links = []
        date_db = self.get_db.get_product_links_all(category=self.category)
        for card in all_card:
            _ = card.find("a", class_="item-card__pdp-link-image").get("href")
            if _ not in links:
                try:
                    title = card.find("span", class_="modelName").text.strip()
                    card_link = card.find("a", class_="item-card__pdp-link-image").get("href")
                    old_price = float(card.find("span", class_="full").text.strip().split("\n")[-1])
                    new_price = float(card.find("span", class_="discounted").text.strip().split("\n")[-1])
                    img = card.find("img").get("data-origin")
                    links.append(card_link)
                except Exception as e:
                    continue
                try:
                    if _ not in date_db:  # Если ссылки с сайта нет в БД, то добавляем каточку
                        print(f"[INFO]Добавляем в базу товар: {title}")
                        i = Products(title, old_price, new_price, img, card_link, self.category)
                        self.add_db.add_item_autoincrement(i)
                    else:  # Если есть, то проверяем на актуальность цены
                        print(f"[INFO]Проверяем цену: {title}")
                        self.update_db.update_price(card_link, old_price, new_price)
                except Exception as e:
                    logging.info(e)
        return links

    @staticmethod
    async def __get_data_page(soup: BeautifulSoup):
        """Получение данных со страницы"""
        total_page = int(soup.find("div", class_="pagination__info").text.strip().split(" ")[-1])
        cards = soup.find("section", class_="product-list").find_all("div", class_="item-card__variant")
        return total_page, cards

    async def __generator_url(self, url_cat: str, page=None):
        """Генерирует ссылки"""
        if page is not None:
            return f'{self.base_url}{url_cat}?page={page}'
        else:
            return f'{self.base_url}{url_cat}'

    async def __is_publish_check(self, links):
        """Проверка то что товар из БД есть на сайте"""
        disabled = 0
        date_db = self.get_db.get_is_publish_true()  # Получаем опубликованные товары
        for _ in date_db:
            if _ not in links:
                disabled += 1
                self.update_db.disabled_products(_)  # Products.is_publish меняем на False
            else:
                continue
        return disabled
