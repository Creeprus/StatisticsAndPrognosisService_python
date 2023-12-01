import email, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Prognosis.prognose_income import Prognose
from Prognosis.prognose_income_reverse import Prognose_Reverse


class MailSender:
    def __int__(self):
        pass

    def send_report_classic(self, receiver, year, area, plant, prolificy_model, stock_price=170,
                            planting_price=39100):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Отчет по урожайности"
        message["From"] = "smtptester193@gmail.com"
        message["To"] = receiver
        prognosis_income = Prognose()
        html = f"""\
        <html>
          <body>
            <p>
            <br>
               <p>
                На вход было получено: Культура: {plant}, Регион: {area}, Год: {year}.
               </p>
                <p>
                Выходные данные: Урожайность культуры {plant} в регионе  в {year} году потенциально 
                будет составлять {round(prolificy_model, 2)} центнеров на гектар.
                </p>
                 <p>
                Учитывая рост себестоимости, себестоимость реализации продукта на гектаре территории 
                будет составлять {planting_price} рублей.
                </p>
                </p>
                {prognosis_income.prognose_profit(prolificy=prolificy_model, planting_price=planting_price, stock_price=stock_price, plant=plant)}
            </p>
          </body>
        </html>
        """
        text_to_send = MIMEText(html, "html")
        message.attach(text_to_send)
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login("smtptester193@gmail.com", "oddn eqnc mrlg kcrs")
            server.sendmail(
                "smtptester193@gmail.com", receiver, message.as_string()
            )

    def send_report_reverse(self, receiver, year, area, desired_profit, best_plants,
                            stock_price=170,
                            planting_price=39100):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Отчет по урожайности"
        message["From"] = "smtptester193@gmail.com"
        message["To"] = receiver
        prognosis_income_reverse = Prognose_Reverse()
        list_keys = [prognosis_income_reverse.return_cultures(best_plants)]
        list_values = [prognosis_income_reverse.return_prolificies(best_plants)]
        html = f"""\
        <html>
          <body>
            <p>
            <br>
               <p>
                На вход было получено: Год: {year}, Регион: {area}, Прибыль с гектара: {desired_profit}
               </p>
                <p>
               Учитывая прибыль и урожайность в регионе наиболее оптимальным выбором будет: {list_keys[0]} и {list_keys[1]}
                </p>                
                <p>
                Урожайность культуры {list_keys[0]} в регионе {area} в {year} году  потенциально будет составлять {round(list_values[0], 2)} центнеров на гектар.
                </p>
                 <p>
                Учитывая рост себестоимости культуры {list_keys[0]}, себестоимость реализации продукта на гектаре территории 
                будет составлять {planting_price} рублей.
                </p>
                    <p>
               Урожайность культуры {list_keys[1]} в регионе {area} в {year} году  потенциально будет составлять {round(list_values[1], 2)} центнеров на гектар.
                </p>
                 <p>
                Учитывая рост себестоимости культуры {list_keys[1]}, себестоимость реализации продукта на гектаре территории 
                будет составлять {planting_price} рублей.
                </p>
                </p>
                 <p>
                {prognosis_income_reverse.prognose_profit(list_values[0], planting_price, stock_price=stock_price, plant=list_keys[0])} .
                </p>
                <p>
                {prognosis_income_reverse.check_profit(list_keys[0], list_values[0], desired_profit, planting_price=planting_price, stock_price=stock_price)}
                </p>
                    <p>
               {prognosis_income_reverse.prognose_profit(list_values[1], planting_price, stock_price=stock_price, plant=list_keys[1])} .
                </p>
                <p>
                {prognosis_income_reverse.check_profit(list_keys[1], list_values[1], desired_profit, planting_price=planting_price, stock_price=stock_price)}
                </p>
            </p>
          </body>
        </html>
        """
        text_to_send = MIMEText(html, "html")
        message.attach(text_to_send)
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login("smtptester193@gmail.com", "oddn eqnc mrlg kcrs")
            server.sendmail(
                "smtptester193@gmail.com", receiver, message.as_string()
            )
