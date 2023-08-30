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


if not os.path.exists("dados_de_fechamento.xlsx"):
    print("Baixando dados do yahoo pra criar a planilha dados_de_fechamento")    
    excel_filename = "Ativos.xlsx"
    DataProducao = pd.read_excel(excel_filename, header=0)
    print(DataProducao)

    ###########################
    symbols = (DataProducao) # Certifique-se de que DataProducao contenha os símbolos correto
    start_time = time.time()
    data_dict = {}
    for symbol in symbols:
        data = web.get_data_yahoo(symbol, start=start_date, end=end_date, period="1d")[
            "Close"
        ]
        data_dict[symbol] = data
 # Medir o tempo de término
        end_time = time.time()

        # Calcular o tempo total
        elapsed_time = end_time - start_time

        # Imprimir o tempo total
        print(f"Tempo total para carregar os dados e criar o DataFrame: {elapsed_time:.2f} segundos")
    # Crie um DataFrame a partir do dicionário
    Portfolio = pd.DataFrame(data_dict)
    Portfolio.index = pd.to_datetime(Portfolio.index)  # Converter o índice para o tipo de data

    # Imprima o DataFrame
    print(Portfolio)

    # Salve o DataFrame em um arquivo Excel
    excel_filename = "dados_de_fechamento.xlsx"
    Portfolio.to_excel(excel_filename, index=True)  # Defina index=False se não quiser incluir o índice no Excel
    print(f'Dados salvos em "{excel_filename}" na mesma pasta do script.')
    

else:
    print("O arquivo 'dados_de_fechamento.xlsx' já existe. Etapa pulada.")
excel_filename = "dados_de_fechamento.xlsx"
novo_portifolio = pd.read_excel(excel_filename, header=0)

# Defina a coluna "Date" como índice
novo_portifolio.set_index("Date", inplace=True)

# Encontre a data mais recente no portfólio
DataMaisRecentePortifolio = novo_portifolio.index[-1]
print('O erro pode estar aqui, tem que ser a data maior',DataMaisRecentePortifolio)

# Obtenha a data do último fechamento para o símbolo do seu interesse (substitua simbolo pelo valor correto)
DataUltimoFechamento = dados_ultimos.index[-1]

# Certifique-se de que os dados estão disponíveis para o dia anterior à DataUltimoFechamento
DataAnteriorFechamento = DataUltimoFechamento - pd.DateOffset(days=1)

# Encontrar os ativos presentes na planilha
ativos = novo_portifolio.columns
print(ativos)
# Atualizar os dados para os ativos que possuem dados faltantes

if DataMaisRecentePortifolio < DataAnteriorFechamento:
    start_time = time.time()
    data_dict2 = {}
    for ativos in ativos:
        data2 = web.get_data_yahoo(ativos, start=DataMaisRecentePortifolio + pd.DateOffset(days=1), end=DataUltimoFechamento, period="1d")["Close"]
        data_dict2[ativos] = data2
        # Medir o tempo de término
        end_time = time.time()

        # Calcular o tempo total
        elapsed_time = end_time - start_time

        # Imprimir o tempo total
        print(f"Tempo total para carregar os dados e criar o DataFrame: {elapsed_time:.2f} segundos")
    # Crie um DataFrame a partir do dicionário
    NPortfolio = pd.DataFrame(data_dict2)
    NPortfolio.index = pd.to_datetime(NPortfolio.index)  # Converter o índice para o tipo de data

    # Imprima o DataFrame
    print(NPortfolio)
       # Atualize o novo_portifolio com os dados faltantes do NPortfolio
    novo_portifolio = pd.concat([novo_portifolio, NPortfolio])

    # Salvar o novo_portifolio de volta no Excel
    excel_filename = "dados_de_fechamento.xlsx"
    novo_portifolio.to_excel(excel_filename, index=True)
else:
    print("Não ha dados a atualizar")   

# Salvar o DataFrame atualizado de volta no Excel
#         novo_portifolio.to_excel(excel_filename, index=True)  # Adicionei index=True para incluir o índice "Date"
# print("terminou")
# retornos = Portofilio.pct_change().dropna()
# print(retornos)
# yf.pdr_override()


# # Plot os retornos
# plt.figure(figsize=(20, 10))
# retornos.plot()
# plt.show()  # Isso exibirá o gráfico no ambiente de visualização


# aula 16
