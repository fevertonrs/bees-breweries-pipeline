import requests
import os
import json
from datetime import datetime

def fetch_brewery_data():
    print("🔄 Iniciando extração da API Open Brewery DB...")

    BASE_URL = "https://api.openbrewerydb.org/breweries"
    per_page = 50
    page = 1
    all_data = []

    while True:
        url = f"{BASE_URL}?per_page={per_page}&page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Erro ao acessar a API: {response.status_code}")
            break

        data = response.json()

        if not data:
            print("Fim da paginação. Total de páginas:", page - 1)
            break

        all_data.extend(data)
        print(f"Página {page} com {len(data)} registros carregados.")
        page += 1

    # Define pasta destino
    raw_date = datetime.today().strftime("%Y-%m-%d")
    output_dir = f"/opt/airflow/data/bronze/breweries/raw_date={raw_date}"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "breweries.json")

    # Salva como JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)

    print(f"Dados salvos em: {output_file}")
    print(f"Total de registros salvos: {len(all_data)}")
