import requests
import pandas as pd


class API_Reader:
    def __int__(self):
        pass

    def connect_to_api(self):
        try:
            # response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
            response_API = pd.read_csv("data_set.csv", encoding="windows-1251")
        except ConnectionError:
            return ""
        except ValueError:
            return ""
        return response_API
