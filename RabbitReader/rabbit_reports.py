from Model.model import Model
from DataSender.mail import MailSender
from API.api_reader import API_Reader
import json
import strings
import pika


class RabbitReports(Model):
    def __init__(self):
        super().__init__()
        self.__channel = self.create_channel()

    def create_channel(self):
        credentials = pika.PlainCredentials(strings.rabbit_user, strings.rabbit_pass)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=strings.rabbit_host, credentials=credentials))
        channel = connection.channel()
        channel.exchange_declare(exchange=strings.rabbit_exchange_mail)
        channel.exchange_declare(exchange=strings.rabbit_exchange_statistic)
        channel.queue_declare(queue=strings.rabbit_mail_queue, durable=True)
        channel.queue_declare(queue=strings.rabbit_mail_statistic, durable=True)
        channel.queue_declare(queue=strings.rabbit_classic_queue, durable=True)
        channel.queue_declare(queue=strings.rabbit_reverse_queue, durable=True)
        channel.basic_consume(queue=strings.rabbit_reverse_queue, on_message_callback=self.reverse_report,
                              auto_ack=True)
        channel.basic_consume(queue=strings.rabbit_classic_queue, on_message_callback=self.classic_report,
                              auto_ack=True)
        channel.queue_bind(queue=strings.rabbit_mail_queue, exchange=strings.rabbit_exchange_mail,
                           routing_key=strings.routing_key_mail)
        channel.queue_bind(queue=strings.rabbit_mail_statistic, exchange=strings.rabbit_exchange_statistic,
                           routing_key=strings.routing_key_statistic)
        return channel

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
        df = self.normalize_dataframe(df=df)
        mail = MailSender(receiver=email, rabbit=self)
        if len(df) <= 1:
            print("[x] Not enough data. Can't do a prognosis")
            return
        result = self.init_model(df, year)
        mail.send_report_classic(area=area, plant=plant, year=year,
                                 prolificy_model=result, stock_price=stock_price, planting_price=planting_price)
        # mail.send_report_classic_rabbit(area=area, plant=plant, year=year,
        #                                 prolificy_model=result, stock_price=stock_price, planting_price=planting_price)

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
        mail = MailSender(receiver=email, rabbit=self)
        if len(df) <= 1:
            print(" [*] Not enough data. Can't do a prognosis")
            return
        result_plants = self.init_reverse_model(df, year)
        plant_stock_price = {}
        for key, value in result_plants.items():
            stock_price = self.get_stock_price(df, area, key, year)
            planting_price = self.get_planting_price(df, area, key, year)
            plant_stock_price.update({f"{key} stock price": stock_price})
            plant_stock_price.update({f"{key} planting price": planting_price})
        mail.send_report_reverse(area=area, best_plants=result_plants, year=year,
                                 desired_profit=desired_profit, stock_planting_price=plant_stock_price)
        # mail.send_report_reverse_rabbit(area=area, best_plants=result_plants, year=year,
        #                                 desired_profit=desired_profit, stock_planting_price=plant_stock_price)

    def receive_message(self):
        print(' [*] Waiting for report queue')
        self.__channel.start_consuming()

    def send_message(self, body, routing_key, exchange):
        self.__channel.basic_publish(exchange=exchange,
                                     routing_key=routing_key,
                                     body=body)
