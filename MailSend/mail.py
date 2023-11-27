import email, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Prognosis.prognose_income import Prognose

class MailSender:
    def __int__(self):
        pass

    def send_report(self, receiver, year, area, plant, prolific_model, plant_cost_self=120, plant_cost_grow=58.9):
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
               <h1>
                На вход было получено: Культура: {plant}, Регион: {area}, Год: {year}
               </h1>
                <h1>
                Выходные данные: Урожайность культуры {plant} в регионе в {year} потенциально будет составлять {prolific_model} центнеров на гектар.
                </h1>
                 <h1>
                Учитывая рост себестоимости, себестоимость реализации продукта на гектаре территории будет составлять {prognosis_income.prognose_self_cost(prolific_model,plant_cost_self)} рублей.
                </h1>
                </h1>
                 <h1>
                Учитывая падения стоимости на центнер, стоимость на центнер будет равна {plant_cost_grow} руб.
                </h1> 
                 <h1>
                Финальный заработок с реализации продукции будет {prognosis_income.prognose_income()} руб.
                </h1>
                <h1>
                Вывод: Посадка культуры {plant} в регионе принесёт прибыль {prognosis_income.prognose_profit(prolific_model,plant_cost_grow,plant_cost_self)} руб с гектара.
                </h1>
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
