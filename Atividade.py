from numpy import False_
import pandas as pd
import seaborn as sns
import requests
from io import StringIO

RED = '\033[31m'
ENDC = '\033[m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
PINK = '\033[45m'
BLUE = '\033[46m'

orig_url='https://drive.google.com/file/d/1pkOP40FvztNt0pnWgKMG5iTXzRt4TW_N/view?usp=sharing'
file_id = orig_url.split('/')[-2]
dwn_url='https://drive.google.com/uc?export=download&id=' + file_id

url = requests.get(dwn_url).text
csv_raw = StringIO(url)
dfs = pd.read_csv(csv_raw)


def get_borda(direcao, desc_text, key_name):
    i_sorted = dfs.groupby([key_name]).size().sort_values()
    borda = i_sorted.tail(1) if direcao == "teto" else i_sorted.head(1)
    print(f"{YELLOW}{desc_text}:{ENDC} {borda.keys()[0]}")
    print("-----------------------")

def topCampo(desc, key):
    get_borda("teto", desc, key)   

def botCampo(desc, key):
    get_borda("piso", desc, key) 



# Questão 1.1: total de reclamações no ano de 2016

total_rec = sum(dfs['ï»¿AnoCalendario'] == 2016)

print(f"{YELLOW}Reclamações no ano de 2016:{ENDC} {total_rec}")
print("-----------------------")

# Questão 1.2: região com maior e menor número de reclamações

botCampo("Região com menor número de reclamações", "Regiao")
topCampo("Região com maior número de reclamações", "Regiao")


# Questão 1.3: Quantidade de reclamações realizadas por homens e mulheres

total_masc = sum(dfs['SexoConsumidor'] == 'M')
total_fem = sum(dfs['SexoConsumidor'] == 'F')

print(f"{YELLOW}Reclamações feitas por homens:{ENDC} {total_masc}")
print(f"{YELLOW}Reclamações feitas por mulheres:{ENDC}: {total_fem}")
print("-----------------------")


# Questão 2.1: região em que homens fizeram mais reclamações que mulheres

lst_sex_reg = dfs[['Regiao', 'SexoConsumidor']]

rmhqm = []

for Regiao, SexoConsumidor in lst_sex_reg.groupby(['Regiao']):
    
    ms = (SexoConsumidor['SexoConsumidor']).groupby(SexoConsumidor['SexoConsumidor'] == "M").count()[1]
    fs = (SexoConsumidor['SexoConsumidor']).groupby(SexoConsumidor['SexoConsumidor'] == "F").count()[1]
    
    if ms > fs:
        rmhqm.append({"Regiao": Regiao, "Diff": ms - fs })    

rmhqm.sort(key = lambda d: d["Diff"], reverse = True)

print(f"{YELLOW}Região em que homens fizeram mais reclamações que mulheres: {rmhqm[0]['Regiao']}{ENDC}")
print("-----------------------")


# Questão 2.2: Qual a faixa etária que realizou mais reclamações
topCampo("Faixa etária que realizou mais reclamações", "FaixaEtariaConsumidor")


# Questão 2.3: Quais assuntos apresentaram mais reclamações em 2016
topCampo("Assuntos apresentaram mais reclamações em 2016", "DescricaoAssunto")


# Questão 2.4: Qual empresa recebeu mais reclamações em 2016
topCampo("Empresa recebeu mais reclamações em 2016", "strNomeFantasia")

# Questão 2.5: Qual empresa possui um maior percentual de resolução de reclamações

lista_t = dfs[['strRazaoSocial', 'Atendida']].value_counts(ascending=True)

perc = 0.0
empresa = ''

for razao_social in dfs['strRazaoSocial'].unique():
    qtd_atend = 0
    qtd_natend = 0

    if (razao_social,'S') in lista_t:        
        qtd_atend = lista_t[razao_social,'S']

    if (razao_social,'N') in lista_t:
        qtd_natend = lista_t[razao_social,'N']

    if qtd_atend != 0 and qtd_natend != 0:        
        perc_calc = qtd_atend / qtd_natend
        if perc_calc > perc:
            perc = perc_calc
            empresa = razao_social

print(f"{YELLOW}Empresa possui um maior percentual de resolução de reclamações:{ENDC} {empresa}: Percentual: {perc}")
print("-----------------------")

# Monte um gráfico mostrando a quantidade de reclamações por região, separando as mesmas por sexo.

graph = sns.countplot(x='Regiao', hue='SexoConsumidor',data=lst_sex_reg)
graph.show()

# Elabore um gráfico de linhas com a quantidade de reclamações por mês. Este gráfico lembra alguma distribuição estatística?
# Elabore um gráfico boxplot mostrando a quantidade de reclamações por região.
# Pontuação (0,5 Pontos)

# É possível afirmar que existe correlação entre o número de reclamações E o número de habitantes por Estado? Elabore um gráfico de dispersão e calcule o índice de correlação destes dois fatores.
lst_join = []
estados = {
'AL': 3120494,
'AM': 3483985,
'BA': 14016906,
'CE': 8452381,
'DF': 2570160,
'ES': 3514952,
'GO': 6003788,
'MA': 6574789,
'MG': 19597330,
'MS': 2449024,
'MT': 3035122,
'PA': 7581051,
'PB': 3766528 ,
'PE': 8796448,
'PI': 3118360,
'PR': 10444526,
'RJ': 15989929,
'RN': 10693929,
'RO': 1562409,
'RS': 10693929,
'SC': 6248436 ,
'SP': 41262199,
'TO': 1383445}

lst_rec_uf = dfs['UF'].value_counts()
for estado in dfs['UF'].unique():
    if estado in estados:
        lst_join.append({'UF': estado, 'Rec': lst_rec_uf[estado],'Pop' : estados[estado] })


ser = pd.Series(data=estados, index=[
'AL',
'AM',
'BA',
'CE',
'DF',
'ES',
'GO',
'MA',
'MG',
'MS',
'MT',
'PA',
'PB' ,
'PE',
'PI',
'PR',
'RJ',
'RN',
'RO',
'RS',
'SC' ,
'SP',
'TO'])
print(lst_rec_uf)


#Fazendo analise estatistica do dataset
print(dfs.describe())