import numpy as np
import pandas as pd
import requests
from sklearn.preprocessing import LabelEncoder
import json
from sklearn.model_selection import KFold
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import Normalizer

class Model:
    def connect_to_api(self):
        response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
        return response_API

    def read_csv(self):
        df = pd.read_csv("data_set.csv", encoding="windows-1251")
        return df

    def encode_model(self):
        df=self.read_csv()
        Oenc = OrdinalEncoder()
        #Oenc.fit(df[["УРОЖАЙНОСТЬ тыс тонн"]])
        Lenc = LabelEncoder()
        df["ОБЛАСТЬ"] = Lenc.fit_transform(df["ОБЛАСТЬ"])
        df["КУЛЬТУРА"] = Lenc.fit_transform(df["КУЛЬТУРА"])
        return df
    def init_model(self):
        df = self.encode_model()
        Y = df["УРОЖАЙНОСТЬ тыс тонн"]
        X = df.drop(columns="УРОЖАЙНОСТЬ тыс тонн")
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=160)
        model_indexes=[X_train,X_test,Y_train,Y_test]
        return model_indexes