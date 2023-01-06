from service.parser.Levis.LevisParserCard import LevisParserCard
from service.parser.Levis.LevisParserPage import LevisParserPage

base_url = "https://www.levi.com/"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}


async def levis_parser_card():
    task_card = LevisParserCard(base_url, headers)
    return task_card


async def levis_parser_page():
    task_page = LevisParserPage(base_url, headers)
    return task_page


async def all_levis_page():
    all_obj = [await levis_parser_page(), await levis_parser_card()]
    return all_obj
