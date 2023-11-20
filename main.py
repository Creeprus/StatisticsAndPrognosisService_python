import Calculations.model as mat_model
from Calculations.model import Model

if __name__ == "__main__":
    md = Model()
    md.init_model(md.read_csv(year=2022,area="Астраханская область",plant="Рис"))
