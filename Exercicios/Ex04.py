#Pandas

import pandas as pd

dados = {
    "Nome": ["Ana", "Pedro"], 
    "Nota": [9.5, 8.0]
}

df = pd.DataFrame(dados)

print(df)