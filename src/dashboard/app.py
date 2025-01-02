import streamlit as st
import pandas as pd
import sqlite3

#Conectando ao banco de Dados
conn = sqlite3.connect('../data/mercadolivre.db')

#Lendo os dados do banco e salvando em um Dataframe
df = pd.read_sql_query('SELECT * FROM mercadolivre_items',conn)

#Fechando a conexão do banco SQL
conn.close()

#Título da Aplicação
st.title('Dashboard - Relógios Masculinos do Mercado Livre')

st.markdown("---")

#Subtítulo
st.subheader('Principais KPIs do Sistema')
col1, col2, col3 = st.columns(3)

#Contagem de Total de Produtos Extraídos
qtd_products= df.shape[0]
col1.metric(label='Total de Produtos', value=qtd_products)

#Total de MArcas únicas
unique_brands = df['Brand'].nunique()
col2.metric(label='Número de Marcas Únicas', value=unique_brands)

#Total de Categorias Únicas
qtd_category = df['Category'].nunique()
col3.metric(label='Número de Categorias Únicas', value=qtd_category)

#Preço Médio antigo
col4, col5, col6 = st.columns(3)
average_old_price = df['Old_Price_Total'].mean()
col4.metric(label= 'Preço Médio Antigo (R$)', value=f'{average_old_price:.2f}') 

#Preço Médio Novo
average_new_price = df['New_Price_Total'].mean()
col5.metric(label= 'Preço Médio Atual (R$)', value=f'{average_new_price:.2f}')

#Data da Última Coleta
last_extraction_date = df['Extraction_Date'].max()
col6.metric(label='Data da Última Coleta de Dados', value=last_extraction_date)

st.markdown("---")

#Top 10 Marcas com Maior Quantidade de Reviews
st.subheader('Top 10 Marcas com Maior Quantidade de Reviews')
col1, col2 = st.columns([10,4])
df_non_zero_reviews = df[df['Reviews_Rating'] > 0]
top10_brands_by_max_reviews = df_non_zero_reviews.groupby('Brand')['Reviews_Total'].max().sort_values(ascending=False).head(10)
col1.line_chart(top10_brands_by_max_reviews)
col2.write(top10_brands_by_max_reviews)

#Top 10 Produtos com Maior Preço
st.subheader('Top 10 Produtos com Maior Preço (R$)')
col1, col2 = st.columns([10,1])
top10_products_max_price = df.groupby('Name')['New_Price_Total'].max().sort_values(ascending=False).head(10)
col1.bar_chart(top10_products_max_price)

#Top 10 Produtos com Menor Preço
st.subheader('Top 10 Produtos com Menor Preço (R$)')
col1, col2 = st.columns([10,1])
df_non_zero_prices = df[df['New_Price_Total'] > 0]
top10_products_min_price = df_non_zero_prices.groupby('Name')['New_Price_Total'].min().sort_values(ascending=True).head(10)
col1.bar_chart(top10_products_min_price)

#Qual o preço médio por marca?
st.subheader('Preço médio por marca (R$)')
col1, col2 = st.columns([4,2])
average_price_by_brand = df.groupby('Brand')['New_Price_Total'].mean().sort_values(ascending=False)
col1.line_chart(average_price_by_brand)
col2.write(average_price_by_brand)

#Qual a satisfação por marca?
st.subheader('Satisfação por marca')
col1, col2 = st.columns([4,2])
df_non_zero_reviews = df[df['Reviews_Rating'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('Brand')['Reviews_Rating'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)