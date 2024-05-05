from Prognosis.prognose_income import Prognose
import strings
import jsonpickle
from RabbitReader.rabbit_reports import RabbitReports
from Prognosis.prognose_income_reverse import Prognose_Reverse


class StatisticSender:
    def __init__(self, rabbit):
        super().__init__()
        self.__rabbit = RabbitReports()

    def send_metrics_classic(self, year, area, plant, prolificy_model, stock_price=170,
                             planting_price=39100):
        prognosis = Prognose(prolificy=prolificy_model, planting_price=planting_price, stock_price=stock_price,
                             plant=plant)
        income = prognosis.prognose_income()
        profit = prognosis.prognose_profit()
        body = {'Plant': plant, 'Area': area, 'Income': income, 'Profit': profit}

        self.__rabbit.send_message(body=jsonpickle.dumps(body), exchange=strings.rabbit_exchange_statistic,
                                   routing_key=strings.routing_key_statistic)
        print(' [*] Message sent: ', body)

    def send_metrics_reverse(self, year, area, desired_profit, best_plants, stock_planting_price):
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
        body = {
            f"{list_keys[0]}": list_values[0],
            f"{list_keys[1]}": list_values[1],
            f"{list_keys[0]} income": prognosis_reverse_first.prognose_income(),
            f"{list_keys[0]} profit": prognosis_reverse_first.prognose_profit(),
            f"{list_keys[1]} income": prognosis_reverse_second.prognose_income(),
            f"{list_keys[1]} profit": prognosis_reverse_second.prognose_income()
        }
        self.__rabbit.send_message(body=jsonpickle.dumps(body), exchange=strings.rabbit_exchange_statistic,
                                   routing_key=strings.routing_key_statistic)
        print(' [*] Message sent: ', body)
