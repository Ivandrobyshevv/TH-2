from database.models import Products
from service.parser.Levis.LevisParser import LevisParser


class LevisParserPage(LevisParser):
    def __init__(self, base_url, headers):
        super().__init__(base_url, headers)

    async def start(self):
        date_db = self.get_db.get_product_links_all(category=self.category)
        page = 1
        links = []
        category = "US/en_US/sale/c/levi_clothing_sale_us"
        total_product, all_card = await self.open_url(await self.__generator_url(category))
        links.extend(await self.__parser_page(all_card, date_db))
        while True:
            print(f'[INFO]Обработано ссылок {len(links)}')
            total_product, all_card = await self.open_url(await self.__generator_url(category, page))
            if len(all_card) < 1:
                break
            else:
                page += 1
                links.extend(await self.__parser_page(all_card, date_db))

        dis = await self.__is_publish_check(links)
        print(dis)

    async def __generator_url(self, category, page=None):
        if page is None:
            return f'{self.base_url}{category}'
        else:
            return f'{self.base_url}{category}?page={page}'

    async def __parser_page(self, all_card, date_db):
        spent_links = []
        for card in all_card:
            try:
                title = card.find(class_="product-name").text
                card_link = "https://www.levi.com" + card.find("a").get("href")

                old_price = card.find(class_="strikedOut").text
                if "Original Price Range was" in old_price:
                    old_price = float(old_price.replace("Original Price Range was", '').split("-")[0].replace("$", ""))
                else:
                    old_price = float(old_price.replace("$", ""))

                new_price = float(card.find(class_="hard-sale").text.replace("$", '').replace('-', '').strip())
                img = card.find("img", class_="processed-image").get("data-src")
                spent_links.append(card_link)
            except:
                continue

            if card_link in date_db:
                print(f'[INFO] Обновляем цену {title}')
                self.update_db.update_price(card_link, old_price, new_price)
            else:
                print(f'[INFO]Добавляем товар {title}')
                i = Products(title, old_price, new_price, img, card_link, self.category)
                self.add_db.add_item_autoincrement(i)
        return spent_links

    async def __is_publish_check(self, links):
        """Проверка то что товар из БД есть на сайте"""
        disabled = 0
        date_db = self.get_db.get_is_publish_true(category=self.category)  # Получаем опубликованные товары
        for _ in date_db:
            if _ not in links:
                disabled += 1
                self.update_db.disabled_products(_)  # Products.is_publish меняем на False
            else:
                continue
        return disabled
