import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import Normalizer
from MailSend.mail import MailSender


class Model:
    def normalize_dataframe(self, year, plant, area, df):
        # df = pd.read_csv("data_set.csv", encoding="windows-1251")
        # этот метод надо будет чутка передалть, как только с апишки начну читать
        df = df.drop(columns="RegionId") if "RegionId" in df.columns else df
        df = df.drop(columns="CultureId") if "CultureId" in df.columns else df
        df = df.drop(columns="Id") if "Id" in df.columns else df
        df = df[df["Region"].str.contains(area) == True]
        # df = df[df["Year"] == year]
        df = df[df["Culture"].str.contains(plant) == True]
        return df

    def encode_model(self, df):
        Lenc = LabelEncoder()
        df["Region"] = Lenc.fit_transform(df["Region"])
        df["Culture"] = Lenc.fit_transform(df["Culture"])
        return df

    def get_costs(self, df, area, plant, year):
        df = df.loc[df['Region'].isin(area) & df['Culture'].isin(plant) & df['Year'].isin(year)]
        return df

    def init_model(self, df):
        df = self.encode_model(df)
        Y = df["ProductivityValue"]
        X = df.drop(columns="ProductivityValue")
        kf = KFold(n_splits=4, shuffle=True, random_state=42)
        if len(Y) <= 1:
            print("Нельзя спрогнозировать, имея только одну строку данных")
            return
        if kf.n_splits > len(Y):
            kf = KFold(n_splits=len(Y), shuffle=True, random_state=42)
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
        return max(predict_rfr)

    def init_reverse_model(self, df):
        pass
