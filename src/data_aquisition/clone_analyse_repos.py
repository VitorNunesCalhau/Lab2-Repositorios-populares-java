import os
import subprocess
import pandas as pd
import requests

# Configuração
GITHUB_TOKEN = ""
GITHUB_API_URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
CK_JAR_PATH = "C:\\Users\\PESSOAL\\Desktop\\Faculdade_caralho\\LAB6\\Lab2-Repositorios-populares-java\\src\\data_aquisition\\ck.jar"
REPOS_DIR = "repositorios_java"
CK_OUTPUT_DIR = "C:\\Users\\PESSOAL\\Desktop\\Faculdade_caralho\\LAB6\\Lab2-Repositorios-populares-java\\src\\data_aquisition\\ck_output"
RESULTS_FILE = "final_repo_metrics.csv"
MAX_REPOS = 1000  # Ajuste conforme necessário

# Criar diretórios necessários
os.makedirs(REPOS_DIR, exist_ok=True)
os.makedirs(CK_OUTPUT_DIR, exist_ok=True)

# --- Buscar repositórios do GitHub ---
def buscar_repositorios():
    print("Buscando repositórios Java no GitHub...")
    repos = []
    cursor = None
    per_page = 10

    while len(repos) < MAX_REPOS:
        query = f"""
        query {{
          search(query: "language:Java sort:stars", type: REPOSITORY, first: {per_page}, after: {f'"{cursor}"' if cursor else "null"}) {{
            pageInfo {{
              endCursor
              hasNextPage
            }}
            edges {{
              node {{
                ... on Repository {{
                  nameWithOwner
                  stargazers {{
                    totalCount
                  }}
                  createdAt
                  releases {{
                    totalCount
                  }}
                  url
                }}
              }}
            }}
          }}
        }}
        """
        response = requests.post(GITHUB_API_URL, json={"query": query}, headers=HEADERS)
        data = response.json()

        if "errors" in data:
            print("Erro na consulta:", data["errors"])
            break

        edges = data.get("data", {}).get("search", {}).get("edges", [])
        for edge in edges:
            node = edge["node"]
            repos.append({
                "name": node["nameWithOwner"],
                "stars": node["stargazers"]["totalCount"],
                "created_at": node["createdAt"],
                "releases": node["releases"]["totalCount"],
                "url": node["url"]
            })
            if len(repos) >= MAX_REPOS:
                break

        cursor = data.get("data", {}).get("search", {}).get("pageInfo", {}).get("endCursor")
        if not data.get("data", {}).get("search", {}).get("pageInfo", {}).get("hasNextPage", False):
            break

    print(f"{len(repos)} repositórios obtidos.")
    return pd.DataFrame(repos)

# --- Clonar repositórios ---
def clonar_repositorios(df_repos):
    print("Clonando repositórios...")

    for repo in df_repos["name"]:
        repo_dir = os.path.join(REPOS_DIR, repo.replace("/", "_"))
        if not os.path.exists(repo_dir):
            os.system(f"git clone --depth=1 https://github.com/{repo}.git {repo_dir}")
        else:
            print(f"Repositório {repo} já clonado.")

# --- Executar CK ---
def executar_ck():
    print("Executando CK...")
    if not os.path.exists(CK_JAR_PATH):
        print("Erro: ck.jar não encontrado.")
        return

    for repo in os.listdir(REPOS_DIR):
        repo_path = os.path.join(REPOS_DIR, repo)
        output_dir_repo = os.path.join(CK_OUTPUT_DIR, repo)
        os.makedirs(output_dir_repo, exist_ok=True)

        class_file_path = os.path.join(output_dir_repo, "class.csv")
        if not os.path.exists(class_file_path):
            print(f"Analisando {repo} com CK...")
            result = subprocess.run(
                ["java", "-jar", CK_JAR_PATH, repo_path, "true", "0", "false", output_dir_repo],
                capture_output=True,
                text=True
            )
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
        else:
            print(f"Métricas já geradas para {repo}.")

# --- Processar métricas CK ---
def processar_metricas():
    print("Processando métricas CK...")

    if not os.path.exists(CK_OUTPUT_DIR) or not os.listdir(CK_OUTPUT_DIR):
        print("Diretório CK_OUTPUT não contém arquivos. Verifique se o CK foi executado corretamente.")
        return pd.DataFrame(columns=["name"])

    resultados = []

    for file in os.listdir(CK_OUTPUT_DIR):
        if file.endswith("class.csv"):
            repo_name = file.replace("class.csv", "")
            class_file = os.path.join(CK_OUTPUT_DIR, file)

            try:
                df = pd.read_csv(class_file)
            except Exception as e:
                print(f"Erro ao ler {class_file}: {e}")
                continue

            colunas = ["loc", "cbo", "dit", "lcom"]
            for col in colunas:
                if col not in df.columns:
                    df[col] = pd.Series(dtype="float")

            stats = {
                "name": repo_name.replace("_", "/"),
                "LOC_média": df["loc"].mean(),
                "CBO_média": df["cbo"].mean(),
                "DIT_média": df["dit"].mean(),
                "LCOM_média": df["lcom"].mean()
            }
            resultados.append(stats)

    df_ck = pd.DataFrame(resultados)
    if df_ck.empty:
        print("Nenhuma métrica CK encontrada.")
        df_ck = pd.DataFrame(columns=["name"])
    return df_ck

# --- Unir dados e salvar ---
def unir_dados():
    print("Unindo dados do GitHub e CK...")

    df_repos = buscar_repositorios()
    clonar_repositorios(df_repos)
    executar_ck()
    df_ck = processar_metricas()

    if df_ck.empty or "name" not in df_ck.columns:
        print("df_ck está vazio ou sem a coluna 'name'. Salvando apenas os dados do GitHub.")
        df_repos.to_csv(RESULTS_FILE, index=False)
        print(f"Dados salvos em {RESULTS_FILE} (apenas GitHub).")
        return

    df_final = pd.merge(df_repos, df_ck, on="name", how="left")
    df_final.to_csv(RESULTS_FILE, index=False)
    print(f"Dados salvos em {RESULTS_FILE}")

# Executar o script
if __name__ == "__main__":
    unir_dados()
