from pandas._testing import assert_frame_equal

from API.api_reader import *
from DataSender import *
from Model.model import Model
from RabbitReader import *


class Test:
    def assert_frame_not_equal(*args, **kwargs):
        try:
            assert_frame_equal(*args, **kwargs)
        except AssertionError:
            # frames are not equal
            pass
        else:
            # frames are equal
            raise AssertionError

    def test_1_api_classic(self, plant, area):
        try:
            api = API_Reader()
            # plant = api.get_prices_and_plant(plant)
            # area = api.get_region(area)
            df = api.connect_to_api_classic(cultureid=plant, regionid=area)
            df_test = pd.read_csv("data_set.csv", encoding="windows-1251")
            self.assert_frame_not_equal(df, df_test)
            print("test_1_api_classic: Success")
        except:
            print("test_1_api_classic: Failure")
            assert False

    def test_2_api_reverse(self, area):
        try:
            api = API_Reader()
            # plant = api.get_prices_and_plant(plant)
            # area = api.get_region(area)
            df = api.connect_to_api_reverse(regionid=area)
            df_test = pd.read_csv("data_set.csv", encoding="windows-1251")
            self.assert_frame_not_equal(df, df_test)
            print("test_2_api_reverse: Success")
        except:
            print("test_2_api_reverse: Failure")
            assert False

    def test_3_wrongtype(self, plant, area):
        try:
            api = API_Reader()
            # plant = api.get_prices_and_plant(plant)
            # area = api.get_region(area)
            df = api.connect_to_api_classic(cultureid=plant, regionid=area)
            assert True
            print("test_2_wrongtype: Success")
        except:
            print("test_2_wrongtype: Failure")
            assert False

    def test_4_model(self, area, plant):
        try:
            md = Model()
            df_test = pd.read_csv("data_set.csv", encoding="windows-1251")
            df_test = df_test[df_test[strings.region].str.contains(area) == True]
            df_test = df_test[df_test[strings.culture].str.contains(plant) == True]
            result = md.init_model(df=df_test, year=2024)
            if result != None:
                print("test_4_model: Success")
            else:
                assert False
        except:
            print("test_4_model: Failure")
            assert False


if __name__ == "__main__":
    test = Test()
    test.test_1_api_classic(plant="08cd5e4b-46b3-4bff-b76a-08dc19157960", area="6516be21-5293-4768-8a77-08dc191579c6")
    test.test_2_api_reverse(area="6516be21-5293-4768-8a77-08dc191579c6")
    test.test_3_wrongtype(plant="08cd5e4b-46b3-4bff-b76a-08dc19157960", area="6516be21-5293-4768-8a77-08dc191579c6")
    test.test_4_model(area="Республика Татарстан", plant='просо')
