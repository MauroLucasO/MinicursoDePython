import pandas as pd

# Caminho exato para o train.csv na sua Área de Trabalho sincronizada com o OneDrive
#caminho = r"C:\Users\"seuNomedeUsuario"\OneDrive\Área de Trabalho\train.csv"

# Lê o arquivo CSV
df = pd.read_csv(caminho)

# Exibe as primeiras linhas
print(df.head())