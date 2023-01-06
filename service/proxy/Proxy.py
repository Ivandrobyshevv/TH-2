import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import zipfile


class Proxy:
    @staticmethod
    async def get_chromedriver(use_proxy=False, user_agent=None):
        PROXY_HOST = os.getenv('proxy_host')
        PROXY_PORT = '8000'
        PROXY_USER = os.getenv('proxy_user')
        PROXY_PASS = os.getenv('proxy_pass')

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"76.0.0"
        }
        """

        background_js = """
        let config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            plugin_file = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(plugin_file, 'w') as zp:
                zp.writestr('manifest.json', manifest_json)
                zp.writestr('background.js', background_js)

            chrome_options.add_extension(plugin_file)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        if user_agent:
            chrome_options.add_argument(f'--user-agent={user_agent}')
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        s = Service(
            executable_path='path_to_chromedriver'
        )
        driver = webdriver.Chrome(
            service=s,
            options=chrome_options
        )

        return driver
