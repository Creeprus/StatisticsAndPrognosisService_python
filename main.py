from Calculations.model import Model
from RabbitReader.rabbit_reader import RabbitReader
import threading
import pandas as pd

if __name__ == "__main__":
    md = Model()
    Rabbit_response = RabbitReader().receive_message()

