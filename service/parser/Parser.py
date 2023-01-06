class Parser:
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers

    async def open_url(self, url: str):
        pass
