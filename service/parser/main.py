from asyncio import get_event_loop
from service.parser.Armani.main import all_armani_page
from service.parser.Levis.main import all_levis_page


async def all_tasks():
    tasks = []
    tasks.extend(await all_levis_page())
    tasks.extend(await all_armani_page())
    for task in tasks:
        res = await task.start()
        print(res)


def parser_event_loop():
    loop = get_event_loop()
    loop.run_until_complete(all_tasks())
