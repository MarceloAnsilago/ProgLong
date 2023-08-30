import pandas as pd
import tkinter as tk
from tkinter import filedialog
import yfinance as yf
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime as dt
import os
import time

# Procurar ultimo fechamento no yahoo
yf.pdr_override()
simbolo = "^BVSP"
    # Obtenha os dados históricos para o índice Bovespa
acao = yf.Ticker(simbolo)
dados_ultimos = acao.history(period="1d")  # 1 dia de dados
    # Converta as datas do Yahoo Finance para não ter informações de fuso horário
dados_ultimos.index = dados_ultimos.index.tz_localize(None)
    # Exiba a data do último fechamento do índice Bovespa
DataUltimoFechamento = dados_ultimos.index[0].strftime("%Y-%m-%d")
print(f"A data do último fechamento de {simbolo} foi: {DataUltimoFechamento}")
    # Definir o intervalo de datas
start_date = "2022-08-01"
end_date = DataUltimoFechamento
print("Baixando dados do yahoo pra criar a planilha dados_de_fechamento")    
excel_filename = "Ativos.xlsx"
DataProducao = pd.read_excel(excel_filename, header=0)
print("Ativos que irá baixar ",DataProducao)

    ###########################
symbols = (DataProducao) # Certifique-se de que DataProducao contenha os símbolos correto
# start_time = time.time()
data_dict = {}
for symbol in symbols:
        data = web.get_data_yahoo(symbol, start=start_date, end=end_date, period="1d")[
            "Close"
        ]
        data_dict[symbol] = data
 # Medir o tempo de término
        # end_time = time.time()

        # Calcular o tempo total
        # elapsed_time = end_time - start_time

       
    # Crie um DataFrame a partir do dicionário
        Portfolio = pd.DataFrame(data_dict)
        Portfolio.index = pd.to_datetime(Portfolio.index)  # Converter o índice para o tipo de data
      

    # Imprima o DataFrame
        print(Portfolio)
        # Imprimir o tempo total
# print(f"Tempo total para carregar os dados e criar o DataFrame: {elapsed_time:.2f} segundos")  
   


retornos = Portfolio.pct_change().dropna()
print(retornos)
yf.pdr_override()


# Plot os retornos
plt.figure(figsize=(20, 10))
retornos.plot()
plt.show()  # Isso exibirá o gráfico no ambiente de visualização


# aula 16
