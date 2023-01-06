from service.parser.Armani.ArmaniParserCard import ArmaniParserCard
from service.parser.Armani.ArmaniParserPage import ArmaniParserPage

base_url = "https://www.armaniexchange.com/us/"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}


async def armani_parser_card():
    task_card = ArmaniParserCard(base_url, headers)
    return task_card


async def armani_parser_page():
    task_page = ArmaniParserPage(base_url, headers)
    return task_page


async def all_armani_page():
    all_obj = [await armani_parser_page(), await armani_parser_card()]
    return all_obj
