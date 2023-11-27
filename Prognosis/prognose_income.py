import math


class Prognose:
    def __init__(self):
        pass
    def prognose_income(self,prolificy,plant_cost_grow):
        return plant_cost_grow*prolificy

    def prognose_self_cost(self,prolificy,self_cost):
        return self_cost*prolificy

    def prognose_profit(self,prolificy,plant_cost_grow,plant_cost_self):
        return (plant_cost_grow * prolificy) - (plant_cost_self * prolificy)