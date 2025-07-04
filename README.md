# Projeto BEES – Breweries Case

Este projeto implementa um pipeline de engenharia de dados baseado em arquitetura **medallion** (bronze, silver, gold), utilizando a API pública [Open Brewery DB](https://www.openbrewerydb.org/). O pipeline é orquestrado com **Apache Airflow**, rodando em ambiente **Docker**.

---

## Objetivo

- Consumir dados da API Open Brewery DB
- Armazenar os dados em um Data Lake simulado
- Aplicar transformações organizadas em camadas:
  - **Bronze**: dados brutos (JSON)
  - **Silver**: dados limpos e particionados (Parquet por estado)
  - **Gold**: agregações analíticas (contagem por tipo e local)

---

## Arquitetura Medallion

[API REST]
↓
[Bronze Layer] → JSON bruto por data
↓
[Silver Layer] → Parquet particionado por estado
↓
[Gold Layer] → Agregado por brewery_type + state

