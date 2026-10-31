# Função e For 

def saudar(nome):
    return f"Olá, {nome}! Bem-vindo à Fonte Jr."

mensagem = saudar("Mauro")
print(mensagem)


def filtrar(lista):
    return [x for x in lista if x > 3 or x < 1]

print(filtrar([-1, 0, 1, 2, 3, 4, 5]))
