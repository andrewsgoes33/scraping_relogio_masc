import pandas as pd
import sqlite3

df = pd.read_json('../data/data.jsonl', lines=True)

pd.options.display.max_columns = None

df['Brand'] = df['Brand'].fillna('Sem Marca')

df["Old_Price_Reais"] = df["Old_Price_Reais"].fillna(0).astype(float)
df["Old_Price_Cents"] = df["Old_Price_Cents"].fillna(0).astype(float)
df["New_Price_Reais"] = df["New_Price_Reais"].fillna(0).astype(float)
df["New_Price_Cents"] = df["New_Price_Cents"].fillna(0).astype(float)
df["Reviews_Rating"] = df["Reviews_Rating"].fillna(0).astype(float)

df["Reviews_Total"] = df["Reviews_Total"].str.replace(r'[\(\)]','',regex=True)
df["Reviews_Total"] = df["Reviews_Total"].fillna(0).astype(int)

df['Old_Price_Total'] = df["Old_Price_Reais"] + df["Old_Price_Cents"] / 100
df['New_Price_Total'] = df["New_Price_Reais"] + df["New_Price_Cents"] / 100

df.drop(columns=['Old_Price_Reais', 'Old_Price_Cents', "New_Price_Reais", "New_Price_Cents"])

nova_ordem = ["Marketplace", "Brand", "Name", 
              "Category",'Old_Price_Total', 'New_Price_Total', 
              "Reviews_Rating", "Reviews_Total",
              "Extraction_Date", "Ad_Link"]

df = df[nova_ordem]

conn = sqlite3.connect('../data/mercadolivre.db')

df.to_sql('mercadolivre_items', conn, index=False, if_exists="replace")

conn.close()

