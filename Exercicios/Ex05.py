# Exemplo de Tupla em Python

coordenadas = (-21.76, -43.35) 
dias_semana = ("Seg", "Ter", "Qua")

# Acesso idêntico ao de listas:
print(coordenadas[0]) # -21.76

# Tentar alterar a coordenada1 gera Erro (TypeError):

# Assim vai se eu colocar isso
coordenadas = (-20.00, coordenadas[1])
print(coordenadas)
