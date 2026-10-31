# 1. Soma direta (exibe a imprecisão do ponto flutuante)
soma_direta = 0.1 + 0.2
print(f"Soma direta: {soma_direta}")  # Saída: 0.30000000000000004


# 2. Usando round() para arredondar na exibição
soma_arredondada = round(0.1 + 0.2, 1)
print(f"Com round(): {soma_arredondada}")  # Saída: 0.3


# 3. Usando o módulo decimal para precisão exata
from decimal import Decimal

soma_precisa = Decimal('0.1') + Decimal('0.2')
print(f"Com Decimal: {soma_precisa}")  # Saída: 0.3