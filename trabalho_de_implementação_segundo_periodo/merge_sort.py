# Vantagem: desempenho previsível (O(n log n)).
# Desvantagem: precisa de memória extra para juntar as partes.
def ordenar(lista):
    if len(lista) <= 1:
        return lista.copy()
    meio = len(lista) // 2
    esq, dir = ordenar(lista[:meio]), ordenar(lista[meio:])
    resultado = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        if esq[i] <= dir[j]:
            resultado.append(esq[i]); i += 1
        else:
            resultado.append(dir[j]); j += 1
    return resultado + esq[i:] + dir[j:]
