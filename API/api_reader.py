import requests
import pandas as pd
import jsonpickle


class API_Reader:
    def __int__(self):
        pass

    def connect_to_api_classic(self, cultureid, regionid):
        try:
            url = f'https://localhost:7158/Productivity?Filter=CultureId ="{cultureid}" and RegionId ="{regionid}"'
            response_API = requests.get(url, verify=False)
            result = jsonpickle.decode(response_API.content)
        # response_API = pd.read_csv("data_set.csv", encoding="windows-1251")
        except ConnectionError:
            return ""
        except ValueError:
            return ""
        return pd.DataFrame.from_dict(pd.json_normalize(result["collection"]), orient='columns')

    def connect_to_api_reverse(self, regionid):
        try:
            url = f'https://localhost:7158/Productivity?Filter=RegionId ="{regionid}"'
            response_API = requests.get(url, verify=False)
            result = jsonpickle.decode(response_API.content)
        # response_API = pd.read_csv("data_set.csv", encoding="windows-1251")
        except ConnectionError:
            return ""
        except ValueError:
            return ""
        return pd.DataFrame.from_dict(pd.json_normalize(result["collection"]), orient='columns')

    def get_prices_and_plant(self, cultureid):
        try:
            url = f'https://localhost:7158/Culture/{cultureid}'
            response_API = requests.get(url, verify=False)
            result = jsonpickle.decode(response_API.content)
        # response_API = pd.read_csv("data_set.csv", encoding="windows-1251")
        except ConnectionError:
            return ""
        except ValueError:
            return ""
        return result["costToPlant"], result["priceToSell"], result["name"]

    def get_region(self, regionid):
        try:
            url = f'https://localhost:7158/Region/{regionid}'
            response_API = requests.get(url, verify=False)
            result = jsonpickle.decode(response_API.content)
        # response_API = pd.read_csv("data_set.csv", encoding="windows-1251")
        except ConnectionError:
            return ""
        except ValueError:
            return ""
        return result["name"]

    def get_plant(self, plantid):
        try:
            url = f'https://localhost:7158/Culture/{plantid}'
            response_API = requests.get(url, verify=False)
            result = jsonpickle.decode(response_API.content)
        # response_API = pd.read_csv("data_set.csv", encoding="windows-1251")
        except ConnectionError:
            return ""
        except ValueError:
            return ""
        return result["name"]
