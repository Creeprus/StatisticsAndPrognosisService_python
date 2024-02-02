from RabbitReader.rabbit_reports import RabbitReports

if __name__ == "__main__":
    Rabbit_response = RabbitReports().receive_message()
