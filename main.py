from Calculations.model import Model
from RabbitReader.rabbit_reader import RabbitReader
import threading
import pandas as pd

if __name__ == "__main__":
    md = Model()
    Rabbit_response = RabbitReader()
    x = threading.Thread(target=Rabbit_response.receive_message_classic(), daemon=False)
    y = threading.Thread(target=Rabbit_response.receive_message_reverse(), daemon=False)
    x.start()
    y.start()
