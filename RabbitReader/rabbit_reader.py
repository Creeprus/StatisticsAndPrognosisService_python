import pika
import json

import strings
from Calculations.model import Model
from MailSend.mail import MailSender
from API.api_reader import API_Reader


class RabbitReader(Model):
    def __init__(self):
        pass

    def classic_report(self, cg, method, properties, body):
        print(f" [x] Received {body}")
        api = API_Reader()
        year = json.loads(body)[strings.year]
        plant = json.loads(body)[strings.cultureid]
        area = json.loads(body)[strings.regionid]
        email = json.loads(body)[strings.email]
        df = api.connect_to_api_classic(cultureid=plant, regionid=area)
        planting_price, stock_price, plant = api.get_prices_and_plant(plant)
        area = api.get_region(area)
        df = self.normalize_dataframe(df=df, stock_price=stock_price, planting_price=planting_price)
        mail = MailSender(receiver=email)
        if len(df) <= 1:
            mail.send_report_fail()
            return
        result = self.init_model(df, year)
        # mail.send_report_classic(area=area, plant=plant, year=year,
        #                          prolificy_model=result, stock_price=stock_price, planting_price=planting_price)
        mail.send_report_classic_rabbit(area=area, plant=plant, year=year,
                                        prolificy_model=result, stock_price=stock_price, planting_price=planting_price)

    def create_channel(self):
        credentials = pika.PlainCredentials(strings.rabbit_user, strings.rabbit_pass)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=strings.rabbit_host, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=strings.rabbit_mail_queue, durable=True)
        channel.queue_declare(queue=strings.rabbit_classic_queue, durable=True)
        channel.basic_consume(queue=strings.rabbit_classic_queue, on_message_callback=self.classic_report,
                              auto_ack=True)
        channel.queue_declare(queue=strings.rabbit_reverse_queue, durable=True)
        channel.basic_consume(queue=strings.rabbit_reverse_queue, on_message_callback=self.reverse_report,
                              auto_ack=True)
        return channel

    def receive_message(self):
        channel = self.create_channel()
        print(' [*] Waiting for report queue')
        channel.start_consuming()

    def send_message(self, body, routing_key, exchange):
        channel = self.create_channel()
        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body)

    def reverse_report(self, cg, method, properties, body):
        print(f" [x] Received {body}")
        api = API_Reader()
        area = json.loads(body)[strings.regionid]
        year = json.loads(body)[strings.year]
        desired_profit = json.loads(body)[strings.desirable_profit]
        email = json.loads(body)[strings.email]
        df = api.connect_to_api_reverse(area)
        area = api.get_region(area)
        df = self.normalize_dataframe_reverse(df=df, year=year, area=area)
        mail = MailSender(receiver=email)
        if len(df) <= 1:
            mail.send_report_fail()
            return
        result_plants = self.init_reverse_model(df, year)
        plant_stock_price = {}
        for key, value in result_plants.items():
            stock_price = self.get_stock_price(df, area, key, year)
            planting_price = self.get_planting_price(df, area, key, year)
            plant_stock_price.update({f"{key} stock price": stock_price})
            plant_stock_price.update({f"{key} planting price": planting_price})
        # mail.send_report_reverse(area=area, best_plants=result_plants, year=year,
        #                          desired_profit=desired_profit, stock_planting_price=plant_stock_price)
        mail.send_report_reverse_rabbit(area=area, best_plants=result_plants, year=year,
                                        desired_profit=desired_profit, stock_planting_price=plant_stock_price)
