import json
import requests
import pandas as pd
import time

#Gettoken
url = "http://api.precifica.com.br/authentication"

headers = {
  'client_key': '8GA5GGIEk54SFksarb_ZVo1Vb5qxVeBpA1Iqy29vguelgZHbVOyempMb',
  'secret_key': 'vUKzMrlueDU9Xy2PAi3hW5XxcAZMxY1pmtQ6Mz8W',
  'Accept': 'application/vnd.api+json',
  'Content-Type': 'application/vnd.api+json'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    response_data = response.json()  # Parse JSON response
    token = response_data["data"]["token"]
# print(token)

#Get products
product = "pfc509734"
url_fact = f"http://api.precifica.com.br/platform/consumerbrands/provider.precifica.com.br/scan/last/{product}"

payload_fact = {}
headers_fact = {
  'Accept': 'application/vnd.api+json',
  'Content-Type': 'application/vnd.api+json',
  'Authorization': f'Bearer {token}'
}

response_fact = requests.request("GET", url_fact, headers=headers_fact, data=payload_fact)

response_fact_json = response_fact.json()

print(response_fact_json)
# import pandas as pd

# # Caminho para o arquivo CSV
# caminho_arquivo = r"D:\Users\bruno_wakiyama\OneDrive - wella\VENDAS\DASHBOARD PRECIFICA\dim_products.csv"

# # Lê o arquivo CSV em um DataFrame do pandas
# dados = pd.read_csv(caminho_arquivo)

# # Agora você pode trabalhar com os dados no DataFrame 'dados'
# print(dados.head())  # Exibe as primeiras linhas do DataFrame



