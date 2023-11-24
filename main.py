import Calculations.model as mat_model
from Calculations.model import Model
from APIReader.APIReader import APIReader
import threading

if __name__ == "__main__":
    md = Model()
    while True:
        API_response = APIReader().connect_to_api()
        if API_response != "":
            md.init_model(md.read_csv(year=2022, area="Астраханская область", plant="Рис"))
