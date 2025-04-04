import pandas as pd

# Carregar o CSV de métricas CK
ck_metrics = pd.read_csv("ck_metrics_summary.csv")

# Carregar o CSV de popularidade dos repositórios
repo_data = pd.read_csv("java_repositories.csv")  # Nome do seu arquivo original

# Padronizar os nomes dos repositórios (substituir '__' por '/')
ck_metrics["Repositório"] = ck_metrics["Repositório"].str.replace("__", "/")

# Fazer o merge dos dados
merged_data = pd.merge(repo_data, ck_metrics, left_on="name", right_on="Repositório", how="left")

# Salvar o resultado
merged_data.to_csv("repositorios_com_metricas.csv", index=False)

print("✅ Dados combinados e salvos em 'repositorios_com_metricas.csv'")
