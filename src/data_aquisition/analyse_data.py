import os
import pandas as pd
import statistics

CK_OUTPUT_DIR = "ck_output"
RESULTS_FILE = "ck_metrics_summary.csv"

def calcular_moda(valores):
    try:
        return statistics.mode(valores)
    except statistics.StatisticsError:
        return "N/A"

def calcular_estatisticas(valores):
    if not valores:
        return {"média": "N/A", "mediana": "N/A", "moda": "N/A"}
    return {
        "média": round(statistics.mean(valores), 2),
        "mediana": round(statistics.median(valores), 2),
        "moda": calcular_moda(valores)
    }

def processar_metricas():
    resultados = []
    
    for repo_dir in os.listdir(CK_OUTPUT_DIR):
        repo_path = os.path.join(CK_OUTPUT_DIR, f"{repo_dir}class.csv")

        
        if os.path.exists(repo_path):
            print(f"Lendo: {repo_path}")  # Corrigido de csv_path para repo_path
            
            df = pd.read_csv(repo_path)
            print(df.head())  # Mostrar as primeiras linhas para debug
            
            # Certifique-se de que as colunas necessárias existem
            colunas = ["loc", "cbo", "dit", "lcom"]
            for col in colunas:
                if col not in df.columns:
                    df[col] = pd.Series(dtype=float)  # Corrigido de [] para Pandas Series vazia
            
            stats = {
                "Repositório": repo_dir,
                **{f"LOC_{k}": v for k, v in calcular_estatisticas(df["loc"].dropna().tolist()).items()},
                **{f"CBO_{k}": v for k, v in calcular_estatisticas(df["cbo"].dropna().tolist()).items()},
                **{f"DIT_{k}": v for k, v in calcular_estatisticas(df["dit"].dropna().tolist()).items()},
                **{f"LCOM_{k}": v for k, v in calcular_estatisticas(df["lcom"].dropna().tolist()).items()},
            }
            resultados.append(stats)
    
    if resultados:
        df_resultados = pd.DataFrame(resultados)
        df_resultados.to_csv(RESULTS_FILE, index=False)
        print(f"✅ Estatísticas salvas em {RESULTS_FILE}")
    else:
        print("⚠️ Nenhum dado foi processado. Verifique se os arquivos class.csv existem e contêm dados.")

if __name__ == "__main__":
    processar_metricas()
