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

    def classic_report(self, cg, method, properties, body):
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
        stock_price, planting_price = self.get_costs(df, year=year, plant=plant,
                                                     area=area)
        mail.send_report_classic(receiver="leva.kornienko@yandex.ru", area=area, plant=plant, year=year,
                                 prolificy_model=result, stock_price=stock_price, planting_price=planting_price)

    def receive_message_classic(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='ClassicReport', durable=True)

        channel.basic_consume(queue='ClassicReport', on_message_callback=self.classic_report, auto_ack=True)

        print(' [*] Waiting for classic report queue')
        channel.start_consuming()

    def reverse_report(self, cg, method, properties, body):
        print(f" [x] Received {body}")
        api = API_Reader()
        area = json.loads(body)[0]['SelectedRegion']
        year = json.loads(body)[0]['SelectedYear']
        desired_profit = json.loads(body)[0]['DesiredProfit']
        df = api.connect_to_api()
        df = self.normalize_dataframe_reverse(df=df, year=year, area=area)
        # этот метод сверху надо будет чутка переделать, как только с апишки начну читать
        result = {self.init_reverse_model(df)}
        mail = MailSender()
        # sokolov19868@gmail.com
        stock_price, planting_price = self.get_costs(df, year=year, plant=plant,
                                                     area=area)
        mail.send_report_reverse(receiver="leva.kornienko@yandex.ru", area=area, best_plants=result, year=year,
                                 stock_price=stock_price, planting_price=planting_price, desired_profit=desired_profit)

    def receive_message_reverse(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='ReverseReport', durable=True)

        channel.basic_consume(queue='ReverseReport', on_message_callback=self.reverse_report, auto_ack=True)

        print(' [*] Waiting for reverse report queue')
        channel.start_consuming()
