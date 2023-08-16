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

# Read the products CSV file
csv_products = "Wella/products.csv"
df_products = pd.read_csv(csv_products, sep=';', decimal=',', encoding='utf-8')

# Lista para armazenar os DataFrames individuais
data_frames = []

# Iterate through each row in the products DataFrame
for index, row in df_products.iterrows():
    product = row['Product']  # Get the product value from the current row
    
    # Make an API request to get product data
    url_fact = f"http://api.precifica.com.br/platform/consumerbrands/provider.precifica.com.br/scan/last/{product}"
    payload_fact = {}
    headers_fact = {
        'Accept': 'application/vnd.api+json',
        'Content-Type': 'application/vnd.api+json',
        'Authorization': f'Bearer {token}'
    }

    response_fact = requests.request("GET", url_fact, headers=headers_fact, data=payload_fact)
    response_fact_json = response_fact.json()
    if response_fact.status_code == 429:
      print("Rate limit exceeded. Waiting for a second before continuing...")
      time.sleep(1)  # Wait for 1 second before continuing
      continue  # Move to the next iteration
 
    data = response_fact_json['data']

    for item in data:
        account_cluster_code = item['account_cluster_code']
        sku = item['sku']

        for scan in item['last_scan']['data']:
            product_id = scan['product_id']
            domain = scan['domain']
            date_occurrence = scan['date_occurrence']
            availability = scan['availability']
            price = scan.get('price', None)  # Get the price if it exists, otherwise None
            offer_price = scan.get('offer_price', None)  # Get the offer_price if it exists, otherwise None
            sold_by = scan['sold_by']

            for seller in scan['sellers']:
                seller_name = seller['sold_by']
                seller_price = seller['price']
                seller_offer_price = seller['offer_price']

                # Create a dictionary with the data
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
                    'seller_offer_price': seller_offer_price
                }

                # Add the dictionary to the list
                data_frames.append(row_data)

# Create a DataFrame consolidated from the list of dictionaries
consolidated_df = pd.DataFrame(data_frames)
# print(consolidated_df)
# Save the DataFrame to a CSV file
csv_data = consolidated_df.to_csv(index=False, sep=';', decimal=',')
csv_filename = "Wella/fact_precifica.csv"

# Save the file in the GitHub environment (in the current directory)
with open(csv_filename, 'w', encoding='utf-8') as f:
    f.write(csv_data)
