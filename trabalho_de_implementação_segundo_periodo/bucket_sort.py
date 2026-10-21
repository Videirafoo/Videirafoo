# Vantagem: eficiente quando os valores estão distribuídos uniformemente.
# Desvantagem: pode ficar lento se muitos números caírem no mesmo balde.
from insertion_sort import ordenar as insertion_sort


def ordenar(lista):
    if not lista:
        return []
    qtd = max(1, len(lista) // 100)
    maior = max(lista)
    baldes = [[] for _ in range(qtd)]
    for numero in lista:
        indice = numero * qtd // (maior + 1)
        baldes[indice].append(numero)
    resultado = []
    for balde in baldes:
        resultado.extend(insertion_sort(balde))
    return resultado
