import threading, time
import requests
import json


class APIReader:
    def __init__(self):
        pass

    def connect_to_api(self):
        time.sleep(5)
        try:
            response_API = requests.get('httpsa://api.covid19india.org/state_district_wise.json')
        except ConnectionError:
            return ""
        except ValueError:
            return ""
        return response_API
