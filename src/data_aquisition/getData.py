import requests
import pandas as pd
import os
import subprocess
import time

# ⚠️ Substitua por um token válido!
github_token = ""
github_api_url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {github_token}"}

def get_top_java_repositories(limit=10):
    repositories = []
    per_request = 10
    cursor = None  
    attempts = 0 
    while len(repositories) < limit:
        query = f"""
        query {{
          search(query: "language:Java sort:stars", type: REPOSITORY, first: {per_request}, after: {f'"{cursor}"' if cursor else "null"}) {{
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

        try:
            response = requests.post(github_api_url, json={'query': query}, headers=headers, timeout=10)
            data = response.json()

            if "errors" in data:
                print("Erro na API:", data["errors"])
                if attempts < 3:
                    attempts += 1
                    time.sleep(10) 
                    continue
                else:
                    break

            if "data" not in data or "search" not in data["data"]:
                print("Resposta inesperada da API:", data)
                break

            for repo in data["data"]["search"]["edges"]:
                repo_data = repo["node"]
                repositories.append({
                    "name": repo_data["nameWithOwner"],
                    "stars": repo_data["stargazers"]["totalCount"],
                    "created_at": repo_data["createdAt"],
                    "releases": repo_data["releases"]["totalCount"],
                    "url": repo_data["url"]
                })

            page_info = data["data"]["search"]["pageInfo"]
            cursor = page_info["endCursor"]

            if not page_info["hasNextPage"]:
                break  # Se não há mais páginas, interrompe o loop

        except requests.exceptions.RequestException as e:
            print("Erro de conexão:", e)
            time.sleep(10)  # Espera antes de tentar novamente

    return repositories

def save_repositories_to_csv(repositories, filename="java_repositories.csv"):
    if os.path.exists(filename):
        df_old = pd.read_csv(filename)
        new_repos = pd.DataFrame(repositories)
        df_final = pd.concat([df_old, new_repos]).drop_duplicates(subset="name")
    else:
        df_final = pd.DataFrame(repositories)

    df_final.to_csv(filename, index=False)
    print(f"Dados salvos em {filename}")

def analyze_code_with_ck(repo_path):
    ck_jar_path = "ck.jar"  # Certifique-se de ter o CK baixado
    output_dir = "ck_results"
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run(["java", "-jar", ck_jar_path, repo_path, "false", "0", "false", output_dir])
    class_metrics = pd.read_csv(os.path.join(output_dir, "class.csv"))
    return class_metrics[['class', 'cbo', 'dit', 'lcom']]

def main():
    repos = get_top_java_repositories()
    save_repositories_to_csv(repos)

if __name__ == "__main__":
    main()
