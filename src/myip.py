import json
import requests
import random

class myip():
    def __init__(self):
        self.baseUrls = ["https://api.myip.com","https://api.ipify.org?format=json","https://api.my-ip.io/ip.json"]

    def requestIP(self):
        __name__ = "requestIP"

        random.shuffle(self.baseUrls)
        for url in self.baseUrls:
            print('[{name}] Sending request to {url}'.format(name=__name__, url=url))
            response = requests.get(
                url=url
            )
            print('[{name}] Response HTTP Status Code: {status_code}'.format(name=__name__, status_code=response.status_code))
            if response.status_code == 200:
                return json.loads(response.content)