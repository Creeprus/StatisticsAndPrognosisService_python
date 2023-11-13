import Calculations.model as mat_model
from Calculations.model import Model

if __name__ == "__main__":
  md=Model()
  print(mat_model.np.__version__)
  print(mat_model.pd.__version__)
  #model.connect_to_api()
  #print(md.read_csv())
  print(md.encode_model())

