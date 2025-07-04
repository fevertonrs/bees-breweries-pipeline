import os
import json
import pandas as pd
from datetime import datetime
import glob


def transform_to_silver():
    
    # Data atual para encontrar o bronze do dia
    raw_date = datetime.today().strftime("%Y-%m-%d")
    input_path = f"/opt/airflow/data/bronze/breweries/raw_date={raw_date}/breweries.json"
    output_path = f"/opt/airflow/data/silver/breweries/"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_path}")

    # Lê o JSON bruto
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Converte para DataFrame
    df = pd.json_normalize(data)

    # Remove registros sem estado (state)
    df = df[df['state'].notnull()]

    # Salva particionado por estado
    for state, group in df.groupby("state"):
        state_clean = state.replace(" ", "_").lower()
        state_path = os.path.join(output_path, f"state={state_clean}")
        os.makedirs(state_path, exist_ok=True)
        file_path = os.path.join(state_path, f"breweries_{raw_date}.parquet")
        group.to_parquet(file_path, index=False)

        print(f"Estado {state}: {len(group)} registros salvos em {file_path}")

    print("Transformação concluída. Dados prontos na camada Silver.")


def generate_gold_layer():

    raw_date = datetime.today().strftime("%Y-%m-%d")
    input_path = "/opt/airflow/data/silver/breweries/state=*/breweries_*.parquet"
    output_path = f"/opt/airflow/data/gold/breweries_agg_{raw_date}.parquet"

    # Lista todos os arquivos Parquet da silver
    parquet_files = glob.glob(input_path)

    if not parquet_files:
        raise FileNotFoundError("Nenhum arquivo parquet encontrado na silver.")

    # Concatena todos os arquivos em um único DataFrame
    df = pd.concat([pd.read_parquet(f) for f in parquet_files], ignore_index=True)

    # Agrupamento por estado e tipo de cervejaria
    agg_df = (
        df.groupby(["state", "brewery_type"])
        .size()
        .reset_index(name="brewery_count")
        .sort_values(["state", "brewery_type"])
    )

    # Cria diretório se não existir
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Salva o arquivo Parquet
    agg_df.to_parquet(output_path, index=False)

    print(f"Agregação concluída. Arquivo salvo em: {output_path}")
    print(agg_df.head())
