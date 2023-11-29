from Calculations.model import Model
from RabbitReader.rabbit_reader import RabbitReader
import threading

if __name__ == "__main__":
    md = Model()
    while True:
        Rabbit_response = RabbitReader().receive_message()
