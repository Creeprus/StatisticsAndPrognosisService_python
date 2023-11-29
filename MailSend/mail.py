import email, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Prognosis.prognose_income import Prognose


class MailSender:
    def __int__(self):
        pass

    def send_report_classic(self, receiver, year, area, plant, prolific_model, plant_cost_self=170,
                            plant_cost_grow=39100):
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
                Выходные данные: Урожайность культуры {plant} в регионе в {year} потенциально будет составлять {round(prolific_model, 2)} центнеров на гектар.
                </p>
                 <p>
                Учитывая рост себестоимости, себестоимость реализации продукта на гектаре территории будет составлять {prognosis_income.prognose_self_cost(prolific_model, plant_cost_self)} рублей.
                </p>
                </p>
                 <p>
                Финальный заработок с реализации продукции будет {prognosis_income.prognose_income(prolific_model, plant_cost_grow)} руб.
                </p>
                <p>
                Вывод: Посадка культуры {plant} в регионе принесёт прибыль {prognosis_income.prognose_profit(prolific_model, plant_cost_grow, plant_cost_self)} руб с гектара.
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
