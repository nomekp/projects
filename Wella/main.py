import json
import requests
import pandas as pd

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

# Lista para armazenar os DataFrames individuais
data_frames = []

data = response_fact_json['data']

# Iterar sobre os dados e criar DataFrames para cada "last_scan"
for item in data:
    account_cluster_code = item['account_cluster_code']
    sku = item['sku']
    
    for scan in item['last_scan']['data']:
        product_id = scan['product_id']
        domain = scan['domain']
        date_occurrence = scan['date_occurrence']
        availability = scan['availability']
        
        # Verificar se o campo 'price' existe
        if 'price' in scan:
            price = scan['price']
        else:
            price = None  # ou algum valor que você preferir
        
        if 'offer_price' in scan:
            offer_price = scan['offer_price']
        else:
            offer_price = None  # ou algum valor que você preferir
        
        sold_by = scan['sold_by']
        
        for seller in scan['sellers']:
            seller_name = seller['sold_by']
            seller_price = seller['price']
            seller_offer_price = seller['offer_price']  # Novo campo
            
            # Criar um dicionário com os dados
            row_data = {
                'account_cluster_code': account_cluster_code,
                'sku': sku,
                'product_id': product_id,
                'domain': domain,
                'date_occurrence': date_occurrence,
                'availability': availability,
                'price': price,
                'offer_price': offer_price,
                'sold_by': sold_by,
                'seller_name': seller_name,
                'seller_price': seller_price,
                'seller_offer_price': seller_offer_price  # Novo campo
            }
            
            # Adicionar o dicionário à lista
            data_frames.append(row_data)

# Criar um DataFrame consolidado a partir da lista de dicionários
consolidated_df = pd.DataFrame(data_frames)

# Salvar o DataFrame em um arquivo CSV
csv_data = consolidated_df.to_csv(index=False, sep=';', decimal=',')
csv_filename = "consolidated_data.csv"

# Salvar o arquivo no ambiente do GitHub (no diretório atual)
with open(csv_filename, 'w', encoding='utf-8') as f:
    f.write(csv_data)
