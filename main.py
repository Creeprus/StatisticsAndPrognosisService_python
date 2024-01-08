from RabbitReader.rabbit_reader import RabbitReader

if __name__ == "__main__":
    Rabbit_response = RabbitReader().receive_message()
