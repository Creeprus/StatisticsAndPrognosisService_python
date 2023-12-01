class Prognose:
    def __init__(self):
        pass

    def prognose_income(self, stock_price, prolificy):
        return round(prolificy * stock_price, 2)

    def prognose_profit(self, prolificy, planting_price, stock_price, plant):
        if round(prolificy * stock_price - planting_price, 2) > 0:
            html = f"""\
                             <p>
                            Финальный заработок с реализации продукции 
                            будет {self.prognose_income(prolificy=prolificy, stock_price=stock_price)} руб.
                            </p>
                             <p>
                            Стоимость посадки: {planting_price} руб.
                            </p>
                            <p>
                            Вывод: Посадка культуры {plant} в регионе принесёт 
                            прибыль {round(prolificy * stock_price - planting_price, 2)} руб 
                            с гектара.
                            </p>
                    """
            return html
        else:
            html = f"""\
                                        Вывод: Посадка культуры {plant} в регионе принесёт 
                                        убыток {round(prolificy * stock_price - planting_price, 2) * -1} руб 
                                        с гектара.
                                        </p>
                                """
            return html
