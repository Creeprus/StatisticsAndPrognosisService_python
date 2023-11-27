import threading, time

import pandas as pd
from pandas import json_normalize
import requests
import pika
import json
from Calculations.model import Model
from MailSend.mail import MailSender


class APIReader(Model):
    def __init__(self):
        pass

    def convert_to_JSON(self, cg, method, properties, body):
        print(f" [x] Received {body}")
        dict = json.loads(body)
        df = json_normalize(dict[0]['Dataset'])
        year = json.loads(body)[0]['SelectedYear']
        plant = json.loads(body)[0]['SelectedCulture']
        area = json.loads(body)[0]['SelectedRegion']
        df = self.read_dataframe(df=df, year=year, plant=plant,
                                 area=area)
        result = self.init_model(self.encode_model(df))
        mail = MailSender()
        mail.send_report(receiver="leva.kornienko@yandex.ru", area=area, plant=plant, year=year, prolific_model=result)

    def receive_message(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='ClassicTask', durable=True)

        channel.basic_consume(queue='ClassicTask', on_message_callback=self.convert_to_JSON, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def connect_to_api(self):
        time.sleep(5)
        try:
            response_API = requests.get('https://api.covid19india.org/state_district_wise.json')
        except ConnectionError:
            return ""
        except ValueError:
            return ""
        return response_API
