import aiohttp as aiohttp
from bs4 import BeautifulSoup

from database.methods.add import InsertDataBase
from database.methods.get import GetDataBase
from database.methods.update import UpdateDataBase
from service.parser.Parser import Parser


class ArmaniParser(Parser):
    def __init__(self, base_url: str, headers: dict):
        super().__init__(base_url, headers)
        self.get_db = GetDataBase()
        self.add_db = InsertDataBase()
        self.update_db = UpdateDataBase()
        self.category = 1

    async def open_url(self, url: str) -> BeautifulSoup:
        print(f'[INFO]Подключаемся к {url}')
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=url, headers=self.headers)
            soup = BeautifulSoup(await response.text(), 'lxml')
            return soup
