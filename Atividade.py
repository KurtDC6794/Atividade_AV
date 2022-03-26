from numpy import False_
import pandas as pd
import seaborn as sns
import requests
from io import StringIO

orig_url='https://drive.google.com/file/d/1pkOP40FvztNt0pnWgKMG5iTXzRt4TW_N/view?usp=sharing'

RED = '\033[31m'
ENDC = '\033[m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
PINK = '\033[45m'
BLUE = '\033[46m'

file_id = orig_url.split('/')[-2]
dwn_url='https://drive.google.com/uc?export=download&id=' + file_id

url = requests.get(dwn_url).text
csv_raw = StringIO(url)
dfs = pd.read_csv(csv_raw)

# Questão 1.1: total de reclamações no ano de 2016 
total_rec = sum(dfs['ï»¿AnoCalendario'] == 2016)

print(f"Reclamações no ano de 2016: {total_rec}")
print("-----------------------")

# Questão 1.2: região com maior e menor número de reclamações
sorted_values = dfs.groupby(['Regiao']).size().sort_values()

total_max_reg = sorted_values.tail(1)
total_min_reg = sorted_values.head(1)

print(f"{GREEN}Região com menor número de reclamações:{ENDC} {total_min_reg.keys()[0]}")
print(f"{RED}Região com maior número de reclamações:{ENDC} {total_max_reg.keys()[0]}")
print("-----------------------")

# Questão 1.3: quantidade de reclamações realizadas por homens e mulheres
total_masc = sum(dfs['SexoConsumidor'] == 'M')
total_fem = sum(dfs['SexoConsumidor'] == 'F')

print(f"Reclamações feitas por {BLUE} ♂️ {ENDC}: {total_masc}")
print(f"Reclamações feitas por {PINK} ♀️ {ENDC}: {total_fem}")
print("-----------------------")

# Questão 2.1: região em que homens fizeram mais reclamações que mulheres

lst_sex_reg = dfs[['Regiao', 'SexoConsumidor']].groupby(['Regiao'])

regioes = {}
rmhqm = []

for Regiao, SexoConsumidor in lst_sex_reg:
    
    ms = (SexoConsumidor['SexoConsumidor']).groupby(SexoConsumidor['SexoConsumidor'] == "M").count()[1]
    fs = (SexoConsumidor['SexoConsumidor']).groupby(SexoConsumidor['SexoConsumidor'] == "F").count()[1]    
    
    if ms > fs:
        rmhqm.append({"Regiao": Regiao, "Diff": ms - fs })    

rmhqm.sort(key = lambda diff: diff["Diff"], reverse = True)

print(f"Região em que homens fizeram mais reclamações que mulheres: {PINK} {rmhqm[0]['Regiao']} {ENDC}")
print("-----------------------")

# Questão 2.2: g