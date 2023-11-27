class Prognose:
    def __init__(self):
        pass

    def prognose_income(self, prolificy, plant_cost_grow):
        return round(plant_cost_grow * round(prolificy, 2), 2)

    def prognose_self_cost(self, prolificy, self_cost):
        return round(self_cost * round(prolificy, 2), 2)

    def prognose_profit(self, prolificy, plant_cost_grow, plant_cost_self):
        return round((plant_cost_grow * round(prolificy, 2)) - (plant_cost_self * round(prolificy, 2)), 2)
