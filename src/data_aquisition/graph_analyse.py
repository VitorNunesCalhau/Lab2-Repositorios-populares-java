import pandas as pd
import matplotlib.pyplot as plt

# Nome do arquivo CSV
file_name = "final_repo_metrics.csv"

# Colunas esperadas no CSV
columns = ["name", "stars", "created_at", "releases", "url", "LOC_média", "CBO_média", "DIT_média", "LCOM_média"]

# Ler o arquivo CSV
try:
    df = pd.read_csv(file_name, usecols=columns)
except FileNotFoundError:
    print(f"Erro: O arquivo {file_name} não foi encontrado.")
    exit()
except ValueError as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    exit()

# Criar gráficos
metrics = ["LOC_média", "CBO_média", "DIT_média", "LCOM_média"]
plt.figure(figsize=(12, 8))

for i, metric in enumerate(metrics, 1):
    plt.subplot(2, 2, i)
    plt.bar(df["name"], df[metric], color='skyblue')
    plt.xticks(rotation=90)
    plt.ylabel(metric)
    plt.title(f"Média de {metric}")

plt.tight_layout()
plt.show()
