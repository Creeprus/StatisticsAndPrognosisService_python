import numpy as np
import pandas as pd
import requests
import json
from sklearn.model_selection import KFold
from sklearn import metrics

class Model:

    def connect_to_api(self):
        response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
        return response_API

    def read_csv(self):
        df = pd.read_csv("data_set.csv")
        print(df)

    def init_model(self):
        pass
