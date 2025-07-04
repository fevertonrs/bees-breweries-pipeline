FROM apache/airflow:2.6.3

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 🔑 Adiciona o diretório raiz ao PYTHONPATH
ENV PYTHONPATH="/opt/airflow"
