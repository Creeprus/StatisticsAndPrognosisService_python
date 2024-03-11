import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Prognosis.prognose_income import Prognose
from Prognosis.prognose_income_reverse import Prognose_Reverse
import strings
import jsonpickle
import html_to_send


class MailSender():
    def __init__(self, receiver, rabbit):
        super().__init__()
        self.receiver = receiver
        self.rabbit = rabbit

    def send_report_classic(self, year, area, plant, prolificy_model, stock_price=170,
                            planting_price=39100):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Отчёт по урожайности"
        message["From"] = strings.smtp_mail
        message["To"] = self.receiver
        prognosis_income = Prognose(prolificy=prolificy_model, planting_price=planting_price, stock_price=stock_price,
                                    plant=plant)
        html = html_to_send.html_normal.format(culture=plant, region=area, year=year,
                                               prognosed_productivity=round(prolificy_model, 2),
                                               prognosis=prognosis_income.return_prognose())
        body = {'To': self.receiver, 'Subject': "Отчёт по урожайности", 'Body': html}
        self.rabbit.send_message(body=jsonpickle.dumps(body), exchange=strings.rabbit_exchange_mail,
                                 routing_key=strings.routing_key_mail)
        print(' [*] Message sent: ', body)

    def send_report_reverse(self, year, area, desired_profit, best_plants, stock_planting_price
                            ):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Отчёт по урожайности"
        message["From"] = strings.smtp_mail
        message["To"] = self.receiver
        prognosis = Prognose()
        prognosis_reverse_first = Prognose_Reverse()
        prognosis_reverse_second = Prognose_Reverse()
        list_keys = prognosis.return_cultures(best_plants)
        list_values = prognosis.return_prolificies(best_plants)
        prognosis_reverse_first.plant, prognosis_reverse_second.plant = list_keys[0], list_keys[1]
        prognosis_reverse_first.prolificy, prognosis_reverse_second.prolificy = list_values[0], list_values[1]
        prognosis_reverse_first.stock_price, prognosis_reverse_second.stock_price = prognosis_reverse_first.return_prices(
            stock_planting_price, f"{list_keys[0]} stock price"), prognosis_reverse_second.return_prices(
            stock_planting_price,
            f"{list_keys[1]} stock price")
        prognosis_reverse_first.planting_price, prognosis_reverse_second.planting_price = prognosis_reverse_first.return_prices(
            stock_planting_price, f"{list_keys[0]} planting price"), prognosis_reverse_second.return_prices(
            stock_planting_price,
            f"{list_keys[1]} planting price")
        html = html_to_send.html_normal.format(region=area, year=year, desired_outcome=desired_profit,
                                               culture1=list_keys[0], culture2=list_keys[1],
                                               prognosed_productivity1=round(list_values[0], 2),
                                               prognosed_productivity2=round(list_values[1], 2),
                                               prognosis1=prognosis_reverse_first.check_profit(
                                                   desired_profit=desired_profit),
                                               prognosis2=prognosis_reverse_second.check_profit(
                                                   desired_profit=desired_profit)
                                               )
        body = {'To': self.receiver, 'Subject': "Отчёт по урожайности", 'Body': html}
        self.rabbit.send_message(body=jsonpickle.dumps(body), exchange=strings.rabbit_exchange_mail,
                                 routing_key=strings.routing_key_mail)
        print(' [*] Message sent: ', body)

    def send_report_fail(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Отчет по урожайности"
        message["From"] = strings.smtp_mail
        message["To"] = self.receiver
        html = f"""\
                <html>
                  <body>
                    <p>
                    <br>
                    <p>
                       К сожалению для вашей задачи в наших базах данных недостаточно данных. 
                       Мы приносим глубочайшие извинения.
                    </p>
                  </body>
                </html>
                """
        text_to_send = MIMEText(html, "html")
        message.attach(text_to_send)
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(strings.smtp_mail, strings.smtp_pass)
            server.sendmail(
                strings.smtp_mail, self.receiver, message.as_string()
            )

    # def send_report_fail_rabbit(self):
    #     rabbit = RabbitReader()
    #     body = {
    #         "fail": "Prognosis failed. Not enough data"
    #     }
    #     rabbit.send_message(body=body, exchange=strings.rabbit_exchange, routing_key=strings.rabbit_reverse_queue)
