import numpy as np
import pandas as pd
import requests
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
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

    def read_csv(self, year, plant, area):
        df = pd.read_csv("data_set.csv", encoding="windows-1251")
        df = df[df["ОБЛАСТЬ"].str.contains(area) == True]
        df = df[df["ГОД"] == year]
        df = df[df["КУЛЬТУРА"].str.contains(plant) == True]
        return df

    def encode_model(self, df):
        Oenc = OrdinalEncoder()
        # Oenc.fit(df[["УРОЖАЙНОСТЬ тыс тонн"]])
        Lenc = LabelEncoder()
        df["ОБЛАСТЬ"] = Lenc.fit_transform(df["ОБЛАСТЬ"])
        df["КУЛЬТУРА"] = Lenc.fit_transform(df["КУЛЬТУРА"])
        return df

    def init_model(self, df):
        Y = df["УРОЖАЙНОСТЬ тыс тонн"]
        X = df.drop(columns="УРОЖАЙНОСТЬ тыс тонн")
        kf = KFold(n_splits=4, shuffle=True, random_state=42)
        if len(Y) <= 1:
            print("Нельзя спрогнозировать, имея только одну строку данных")
            return
        if kf.n_splits > len(Y):
            kf = KFold(n_splits=len(Y), shuffle=True, random_state=42)
        # проверка на количество сплитов
        rfr = RandomForestRegressor()
        for train_index, test_index in kf.split(df):
            print("TRAIN:", train_index, "TEST:", test_index)
            X_train_kfold = X.iloc[train_index]
            X_test_kfold = X.iloc[test_index]
            Y_train_kfold = Y.iloc[train_index]
            Y_test_kfold = Y.iloc[test_index]
            rfr.fit(X_train_kfold, Y_train_kfold)
            predict_rfr = rfr.predict(X_test_kfold)
        print("Случайного лес: ", max(predict_rfr), "\n")
