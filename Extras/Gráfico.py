import matplotlib.pyplot as plt

dias = ["Seg", "Ter", "Qua", "Qui", "Sex"]
vendas = [10, 15, 7, 22, 18]

plt.plot(dias, vendas, marker='o', color='blue', linestyle='--')

plt.title("Vendas da Semana")
plt.xlabel("Dias da Semana")
plt.ylabel("Quantidade de Vendas")
plt.grid(True)

plt.show()