import os
import requests
import pandas as pd

url_base = "https://api.themoviedb.org/3/movie/"
api_key = "3a60bcd46fb4a996cf7465f164fd6558"

movies_data = []  # lista para armazenar os dados dos filmes em formato JSON
genres_data = []
companies_data = []  # lista para armazenar os dados das empresas de produção em formato JSON
countries_data = []  # lista para armazenar os dados dos países de produção em formato JSON
languages_data = []  # lista para armazenar os dados dos idiomas falados em formato JSON

for i in range(1, 1000):  # limite do range definido como 10
    url = f"{url_base}{i}?api_key={api_key}"
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        movie_data = response.json()  # armazena a resposta em formato JSON em uma variável
        movies_data.append(movie_data)  # adiciona a resposta à lista 'movies_data'

        # Obtém os dados das empresas de produção do filme
        genres = movie_data['genres']
        for genre in genres:
            company['movie_id'] = i 
            genres_data.append(company)  

        # Obtém os dados das empresas de produção do filme
        companies = movie_data['production_companies']
        for company in companies:
            company['movie_id'] = i  # adiciona o ID do filme aos dados das empresas de produção
            companies_data.append(company)  # adiciona os dados das empresas de produção à lista 'companies_data'

        # Obtém os dados dos países de produção do filme
        countries = movie_data['production_countries']
        for country in countries:
            country['movie_id'] = i  # adiciona o ID do filme aos dados dos países de produção
            countries_data.append(country)  # adiciona os dados dos países de produção à lista 'countries_data'

        # Obtém os dados dos idiomas falados do filme
        languages = movie_data['spoken_languages']
        for language in languages:
            language['movie_id'] = i  # adiciona o ID do filme aos dados dos idiomas falados
            languages_data.append(language)  # adiciona os dados dos idiomas falados à lista 'languages_data'

        print(f"Requisição para o filme com ID {i}: Status Code {response.status_code}")
    else:
        print(f"Requisição para o filme com ID {i}: Status Code {response.status_code} - Ignorada")

# Cria um DataFrame a partir dos dados dos filmes
movies_df = pd.DataFrame(movies_data)

# Cria um DataFrame a partir dos dados das empresas de produção
genres_df = pd.json_normalize(genres_data)

# Cria um DataFrame a partir dos dados das empresas de produção
companies_df = pd.json_normalize(companies_data)

# Cria um DataFrame a partir dos dados dos países de produção
countries_df = pd.json_normalize(countries_data)

# Cria um DataFrame a partir dos dados dos idiomas falados
languages_df = pd.json_normalize(languages_data)

# Salva os DataFrames em arquivos CSV com os nomes alterados
caminho_movies_csv = r"C:\Users\bhwak\OneDrive\Desktop\Requests project\dim_movies.csv"
caminho_genres_csv = r"C:\Users\bhwak\OneDrive\Desktop\Requests project\fact_genres.csv"
caminho_companies_csv = r"C:\Users\bhwak\OneDrive\Desktop\Requests project\fact_production_companies.csv"
caminho_countries_csv = r"C:\Users\bhwak\OneDrive\Desktop\Requests project\fact_production_countries.csv"
caminho_languages_csv = r"C:\Users\bhwak\OneDrive\Desktop\Requests project\fact_spoken_languages.csv"

# Salva o DataFrame dos filmes em arquivo CSV com separador ";"
movies_df.to_csv(caminho_movies_csv, sep=";", decimal=",", index=False)


genres_df.to_csv(caminho_genres_csv, sep=";", decimal=",", index=False)

# Salva o DataFrame das empresas de produção em arquivo CSV com separador ";"
companies_df.to_csv(caminho_companies_csv, sep=";", decimal=",", index=False)

# Salva o DataFrame dos países de produção em arquivo CSV com separador ";"
countries_df.to_csv(caminho_countries_csv, sep=";", decimal=",", index=False)

# Salva o DataFrame dos idiomas falados em arquivo CSV com separador ";"
languages_df.to_csv(caminho_languages_csv, sep=";", decimal=",", index=False)

print("Arquivos CSV salvos com sucesso!")
