import json
import requests

class myip():
    def __init__(self):
        self.baseUrl = "https://api.myip.com"

    def requestIP(self):
        __name__ = "requestIP"
        try:
            response = requests.get(
                url="{baseUrl}".format(baseUrl=self.baseUrl)
            )
            print('[{name}] Response HTTP Status Code: {status_code}'.format(
                name=__name__, status_code=response.status_code))
            return json.loads(response.content)
        except requests.exceptions.RequestException:
            print('HTTP Request failed')