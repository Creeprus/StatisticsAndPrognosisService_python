from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
import strings
from API.api_reader import API_Reader
import requests
import math


class Model:
    def normalize_dataframe(self, df):
        # df = pd.read_csv("data_set.csv", encoding="windows-1251")
        df = df.drop(columns="regionId") if "regionId" in df.columns else df
        df = df.drop(columns="cultureId") if "cultureId" in df.columns else df
        df = df.drop(columns="id") if "id" in df.columns else df
        return df

    def get_current_year(self):
        timeapi_url = "https://www.timeapi.io/api/Time/current/zone"
        headers = {
            "Accept": "application/json",
        }
        params = {"timeZone": "etc/utc"}
        date_object = None
        try:
            request = requests.get(timeapi_url, headers=headers, params=params)
            r_dict = request.json()
            date_object = datetime(year=r_dict["year"], month=r_dict["month"],
                                   day=r_dict["day"],
                                   hour=r_dict["hour"],
                                   minute=r_dict["minute"],
                                   second=r_dict["seconds"],
                                   microsecond=r_dict["milliSeconds"] * 1000, )
        except Exception:
            return 2024
        return date_object.year

    def normalize_dataframe_reverse(self, year, area, df):
        # df = pd.read_csv("data_set.csv", encoding="windows-1251")
        df = df.drop(columns="regionId") if "regionId" in df.columns else df
        df = df.drop(columns="id") if "id" in df.columns else df
        df = df.drop(columns="cultureId") if "cultureId" in df.columns else df
        df = df[df[strings.region].str.contains(area) == True]
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

    def init_model(self, df, year):
        planting_price = df.iloc[0, df.columns.get_loc(strings.planting_price)]
        stock_price = df.iloc[0, df.columns.get_loc(strings.stock_price)]
        df = self.encode_model(df)
        year_diff = math.fabs(self.get_current_year() - year)
        rfr = RandomForestRegressor()
        Y = df[strings.prolificy_value]
        X = df.drop(columns=strings.prolificy_value)
        kf = KFold(n_splits=4, shuffle=True, random_state=42)
        if len(Y) <= 1:
            print("Нельзя спрогнозировать, имея только одну строку данных")
            return
        if kf.n_splits > len(Y):
            kf = KFold(n_splits=len(Y), shuffle=True, random_state=42)
        while year_diff >= 0:
            for train_index, test_index in kf.split(df):
                print("TRAIN:", train_index, "TEST:", test_index)
                X_train_kfold = X.iloc[train_index]
                X_test_kfold = X.iloc[test_index]
                Y_train_kfold = Y.iloc[train_index]
                Y_test_kfold = Y.iloc[test_index]
                rfr.fit(X_train_kfold, Y_train_kfold)
                predict_rfr = rfr.predict(X_test_kfold)
                print("Случайный лес: ", predict_rfr, "\n")
            if year_diff > 0:
                df.loc[0] = [0, year - year_diff, 0, max(predict_rfr), stock_price, planting_price]
                Y = df[strings.prolificy_value]
                X = df.drop(columns=strings.prolificy_value)
                kf = KFold(n_splits=4, shuffle=True, random_state=42)
            year_diff -= 1
        return max(predict_rfr)

    def init_reverse_model(self, df, year, amount=2):
        dict_cultures = {}
        api = API_Reader()
        df = self.calculate_profit(df)
        for j in range(amount):
            dfmax = df.loc[df['Profit'].idxmax()]
            best_plant = dfmax.iloc[1]
            dfmax = df[df[strings.culture].str.contains(best_plant) == True]
            df = df[df[strings.culture].str.contains(best_plant) != True]
            dict_cultures.update({best_plant: self.init_model(dfmax, year)})
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
