import Calculations.model as mat_model
from Calculations.model import Model
from RabbitReader.RabbitReader import APIReader
import threading

if __name__ == "__main__":
    md = Model()
    while True:
        Rabbit_response = APIReader().receive_message()
        # API_response = RabbitReader().connect_to_api()
        # if API_response != "":
        #     md.init_model(md.read_csv(year=2022, area="Астраханская область", plant="Рис"))
