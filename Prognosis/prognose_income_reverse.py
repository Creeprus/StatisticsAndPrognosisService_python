from Prognosis.prognose_income import Prognose


class Prognose_Reverse(Prognose):
    def __int__(self):
        pass

    def return_cultures(self, dict_cultures):
        for key in dict_cultures.items():
            return key

    def return_prolificies(self, dict_cultures):
        for value in dict_cultures.items():
            return value

    def check_profit(self, culture, prolificy, desired_profit, stock_price, planting_price):
        profit = round(prolificy * stock_price - planting_price, 2)
        if profit <= 0:
            return f"Посадка культуры {culture} в регионе принесёт убытки: {round(prolificy * stock_price - planting_price, 2) * -1} "
        if desired_profit >= profit:
            return f"Посадка культуры {culture} в регионе принесёт прибыль {self.prognosis_income_reverse.prognose_profit(prolificy, stock_price, planting_price)} руб с гектара."
        else:
            return f"К сожалению, максимальную ожидаюмую прибыль с посадки культуры {culture} в регионе принесёт прибыль {self.prognosis_income_reverse.prognose_profit(prolificy, stock_price, planting_price)} руб с гектара, что меньше вашей ожидаемой прибыли"
