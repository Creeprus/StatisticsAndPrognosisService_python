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
import strings
from MailSend.mail import MailSender


class Model:
    def normalize_dataframe(self, year, plant, area, df):
        # df = pd.read_csv("data_set.csv", encoding="windows-1251")
        # этот метод надо будет чутка передалть, как только с апишки начну читать
        df = df.drop(columns="RegionId") if "RegionId" in df.columns else df
        df = df.drop(columns="CultureId") if "CultureId" in df.columns else df
        df = df.drop(columns="Id") if "Id" in df.columns else df
        df = df[df[strings.region].str.contains(area) == True]
        # df = df[df[strings.year] == year]
        df = df[df[strings.culture].str.contains(plant) == True]
        return df

    def normalize_dataframe_reverse(self, year, area, df):
        # df = pd.read_csv("data_set.csv", encoding="windows-1251")
        # этот метод надо будет чутка передалть, как только с апишки начну читать
        df = df.drop(columns="RegionId") if "RegionId" in df.columns else df
        df = df.drop(columns="CultureId") if "CultureId" in df.columns else df
        df = df.drop(columns="Id") if "Id" in df.columns else df
        df = df[df[strings.region].str.contains(area) == True]
        # df = df[df[strings.year] == year]
        return df

    def encode_model(self, df):
        Lenc = LabelEncoder()
        df[strings.region] = Lenc.fit_transform(df[strings.region])
        df[strings.culture] = Lenc.fit_transform(df[strings.culture])
        return df

    def get_stock_price(self, df, area, plant, year):
        df = df[df[strings.region].str.contains(area) == True]
        df = df[df[strings.culture].str.contains(plant) == True]
        stock_price = df.iloc[0, df.columns.get_loc(strings.stock_price)]
        return stock_price

    def get_planting_price(self, df, area, plant, year):
        df = df[df[strings.region].str.contains(area) == True]
        df = df[df[strings.culture].str.contains(plant) == True]
        planting_price = df.iloc[0, df.columns.get_loc(strings.planting_price)]
        return planting_price

    def init_model(self, df):
        df = self.encode_model(df)
        Y = df[strings.prolificy_value]
        X = df.drop(columns=strings.prolificy_value)
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

        print("Случайный лес: ", predict_rfr, "\n")
        return max(predict_rfr)

    def reverse_model_predict(self, df):
        df = self.encode_model(df)
        rfr = RandomForestRegressor()
        Y = df[strings.prolificy_value]
        X = df.drop(columns=strings.prolificy_value)
        kf = KFold(n_splits=4, shuffle=True, random_state=42)
        if len(Y) <= 1:
            print("Нельзя спрогнозировать, имея только одну строку данных")
            return
        if kf.n_splits > len(Y):
            kf = KFold(n_splits=len(Y), shuffle=True, random_state=42)
        for train_index, test_index in kf.split(df):
            print("TRAIN:", train_index, "TEST:", test_index)
            X_train_kfold = X.iloc[train_index]
            X_test_kfold = X.iloc[test_index]
            Y_train_kfold = Y.iloc[train_index]
            Y_test_kfold = Y.iloc[test_index]
            rfr.fit(X_train_kfold, Y_train_kfold)
            predict_rfr = rfr.predict(X_test_kfold)
        print("Случайный лес: ", predict_rfr, "\n")
        return max(predict_rfr)

    def init_reverse_model(self, df, amount=2):
        dict_cultures = {}
        df = self.calculate_profit(df)
        for j in range(amount):
            dfmax = df.loc[df['Profit'].idxmax()]
            best_plant = dfmax.iloc[2]
            dfmax = df[df[strings.culture].str.contains(best_plant) == True]
            df = df[df[strings.culture].str.contains(best_plant) != True]
            dict_cultures.update({best_plant: self.reverse_model_predict(dfmax)})
        return dict_cultures

    def calculate_profit(self, df):
        list = []
        for i in range(len(df)):
            stock_price = df.iloc[i, df.columns.get_loc(strings.stock_price)]
            prolificy = float(df.iloc[i, df.columns.get_loc(strings.prolificy_value)])
            planting_price = df.iloc[i, df.columns.get_loc(strings.planting_price)]
            final = (prolificy * stock_price) - planting_price
            list.append(int(final))
        df["Profit"] = list
        return df
