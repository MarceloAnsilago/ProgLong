import pandas as pd
import tkinter as tk
from tkinter import filedialog
import yfinance as yf
import numpy as np
import pandas_datareader.data as web
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
import datetime as dt

# def ler_banco_de_dados():
#     root = tk.Tk()
#     root.withdraw()
#     caminho = filedialog.askopenfilename()
#     if not caminho:
#         print("Nenhum arquivo selecionado!")
#         return None
#     banco_de_dados = pd.read_excel(caminho)
#     banco_de_dados = banco_de_dados.astype(str)
#     return banco_de_dados

# DataProducao = ler_banco_de_dados()
excel_filename ="Ativos.xlsx"
DataProducao = pd.read_excel(excel_filename, header=0)
print(DataProducao)

###########################

yf.pdr_override()
# Definir o intervalo de datas
start_date = '2022-08-01'
end_date = '2023-08-28'
symbols = DataProducao  # Certifique-se de que DataProducao contenha os símbolos correto

data_dict = {}
for symbol in symbols:
    data = web.get_data_yahoo(symbol, start=start_date, end=end_date)['Close']
    data_dict[symbol] = data

# Crie um DataFrame a partir do dicionário
Portofilio = pd.DataFrame(data_dict)
Portofilio.index = pd.to_datetime(Portofilio.index)  # Converter o índice para o tipo de data

# Imprima o DataFrame
print(Portofilio)


# Salve o DataFrame em um arquivo Excel
excel_filename = 'dados_de_fechamento.xlsx'
Portofilio.to_excel(excel_filename, index=True)  # Defina index=False se não quiser incluir o índice no Excel

print(f'Dados salvos em "{excel_filename}" na mesma pasta do script.')

# # Carregar o novo portfólio a partir do arquivo Excel

# Carregar o novo portfólio a partir do arquivo Excel
excel_filename = 'dados_de_fechamento.xlsx'
novo_portifolio = pd.read_excel(excel_filename, header=0)

# Definir a coluna de datas como o índice do DataFrame
# Defina a coluna "Date" como índice
novo_portifolio.set_index("Date", inplace=True)

# Exibir o DataFrame
print(novo_portifolio)

#Verificar atualizações
# Encontre a data mais recente no portfólio
DataMaisRecentePortifolio = novo_portifolio.index[-1]
print("Data mais recente no portfólio:", DataMaisRecentePortifolio)

# Símbolo do índice Bovespa
simbolo = "^BVSP"

# Obtenha os dados históricos para o índice Bovespa
acao = yf.Ticker(simbolo)
dados_ultimos = acao.history(period="1d")  # 1 dia de dados

# Converta as datas do Yahoo Finance para não ter informações de fuso horário
dados_ultimos.index = dados_ultimos.index.tz_localize(None)

# Exiba a data do último fechamento do índice Bovespa
DataUltimoFechamento = dados_ultimos.index[0].strftime("%Y-%m-%d")
print(f"A data do último fechamento de {simbolo} foi: {DataUltimoFechamento}")

# Compare as datas para verificar se os dados estão atualizados
if DataMaisRecentePortifolio >= dados_ultimos.index[0]:
    print("Os dados estão atualizados.")
else:
    print("Há novos dados disponíveis no Yahoo Finance.")











# retornos = Portofilio.pct_change().dropna()
# print(retornos)
# yf.pdr_override()





# # Plot os retornos
# plt.figure(figsize=(20, 10))
# retornos.plot()
# plt.show()  # Isso exibirá o gráfico no ambiente de visualização


#aula 16