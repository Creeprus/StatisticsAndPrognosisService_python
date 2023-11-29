from Calculations.model import Model
from RabbitReader.rabbit_reader import RabbitReader
import threading
import pandas as pd

if __name__ == "__main__":
    md = Model()
    # while True:
    md.init_reverse_model(md.normalize_dataframe_reverse(area="Астраханская область",
                                                         df=pd.read_csv("data_set.csv", encoding="windows-1251"),
                                                         year=2024))
    # Rabbit_response = RabbitReader().receive_message()
