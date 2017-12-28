import os
import pandas as pd
from sqlalchemy import create_engine

file_list = os.listdir('.')

engine = create_engine("mysql+mysqldb://root:"+"root"+"@localhost/sf_e")

for index,value in enumerate(file_list):
    print(value)
    try:
        file_csv = pd.read_csv(value)
        file_csv.to_sql(value.split('.')[0],engine,if_exists='append',index=False)
    except Exception as e:
        print(e)
