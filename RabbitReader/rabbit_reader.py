import threading, time

import pandas as pd
from pandas import json_normalize

import pika
import json
from Calculations.model import Model
from MailSend.mail import MailSender
from API.api_reader import API_Reader


class RabbitReader(Model):
    def __init__(self):
        pass

    def convert_to_JSON(self, cg, method, properties, body):
        print(f" [x] Received {body}")
        api = API_Reader()
        year = json.loads(body)[0]['SelectedYear']
        plant = json.loads(body)[0]['SelectedCulture']
        area = json.loads(body)[0]['SelectedRegion']
        desirable_profit = json.loads(body)[0]['Profit'] if "Profit" in json.loads(body)[0] else 0
        df = api.connect_to_api()
        df = self.normalize_dataframe(df=df, year=year, plant=plant,
                                      area=area)
        # этот метод сверху надо будет чутка переделать, как только с апишки начну читать
        result = self.init_model(df)
        mail = MailSender()
        # sokolov19868@gmail.com
        mail.send_report_classic(receiver="leva.kornienko@yandex.ru", area=area, plant=plant, year=year,
                                 prolific_model=result)

    def receive_message(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='ClassicReport', durable=True)

        channel.basic_consume(queue='ClassicReport', on_message_callback=self.convert_to_JSON, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
