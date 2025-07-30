import pandas as pd
import numpy as np
import os

workdir = '/home/'+os.getlogin()+'/Документы/Codes/Python/testing/'
filepath = workdir+'Под рассылку.csv'

df = pd.read_csv(filepath)

vals = df.values
columns = df.columns

logins = vals[:, 0]
emails = vals[:, 1]
passwords = vals[:, 2]

first_login = vals[1] #admin
first_column = columns[0] #login

df.at[0, first_column] = 'test'

df.rename(columns={columns[0]: 'Новый_заголовок'}, inplace=True)

counts = ''

for value in emails:
    counts = counts + value + '\n'

print(df)

df.to_csv(filepath, index=False)





