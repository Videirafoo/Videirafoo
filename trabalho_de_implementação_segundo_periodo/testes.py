"""Confere se todos os nove algoritmos ordenam sem alterar a lista original."""
from main import ALGORITMOS

CASOS = [
    [], [5], [5, 2, 9, 1, 4], [3, 3, 1, 2, 1, 3],
    [0, 0, 0, 0], list(range(30)), list(range(29, -1, -1)),
]

for nome, ordenar in ALGORITMOS.items():
    for numeros in CASOS:
        original = numeros.copy()
        assert ordenar(numeros) == sorted(original), f"Falha no {nome}"
        assert numeros == original, f"{nome} alterou a entrada"
    print(f"{nome}: OK")
print("Todos os testes passaram.")
