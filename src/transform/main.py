import pandas as pd
import sqlite3
from datetime import datetime

#Lendo Arquivo Jsonl que contém os dados estraídos
df = pd.read_json('../data/data.jsonl', lines=True)

#código para permitir ver todas as colunas no terminal
pd.options.display.max_columns = None

#Tratando Marcas Nulas com 'Sem Marca'
df['Brand'] = df['Brand'].fillna('Sem Marca')

#Tratando valores numéricos, definindo seus tipos e ajustando os nulos.
df["Old_Price_Reais"] = df["Old_Price_Reais"].fillna(0).astype(float)
df["Old_Price_Cents"] = df["Old_Price_Cents"].fillna(0).astype(float)
df["New_Price_Reais"] = df["New_Price_Reais"].fillna(0).astype(float)
df["New_Price_Cents"] = df["New_Price_Cents"].fillna(0).astype(float)
df["Reviews_Rating"] = df["Reviews_Rating"].fillna(0).astype(float)

#Removendo Símbolos () os Reviews_Total e definindo type
df["Reviews_Total"] = df["Reviews_Total"].str.replace(r'[\(\)]','',regex=True)
df["Reviews_Total"] = df["Reviews_Total"].fillna(0).astype(int)

#Criando coluna única com valores em Reais e centavos juntos já tratados.
df['Old_Price_Total'] = df["Old_Price_Reais"] + df["Old_Price_Cents"] / 100
df['New_Price_Total'] = df["New_Price_Reais"] + df["New_Price_Cents"] / 100

#Removendo colunas que não vamos mais utilizar, já que criamos novas colunas com valores totais
df.drop(columns=['Old_Price_Reais', 'Old_Price_Cents', "New_Price_Reais", "New_Price_Cents"])

#Variável para ajustar a ordem das colunas
nova_ordem = ["Marketplace", "Brand", "Name", 
              "Category",'Old_Price_Total', 'New_Price_Total', 
              "Reviews_Rating", "Reviews_Total",
              "Extraction_Date", "Ad_Link"]

df = df[nova_ordem]

#Abrindo conexão Banco SQLite3 e criando o DB
conn = sqlite3.connect('../data/mercadolivre.db')

#Convertendo o Dataframe DF em tabela SQLite e adicionando ao bancoo pela conexão SQLite3
df.to_sql('mercadolivre_items', conn, index=False, if_exists="replace")

#Fechando a conexão
conn.close()


