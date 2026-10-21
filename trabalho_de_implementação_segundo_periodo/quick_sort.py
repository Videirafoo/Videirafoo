# Vantagem: costuma ser muito rápido (média O(n log n)).
# Desvantagem: pode piorar para O(n²) e usa listas extras nesta versão.
def ordenar(lista):
    if len(lista) <= 1:
        return lista.copy()
    pivo = lista[len(lista) // 2]
    menores = [x for x in lista if x < pivo]
    iguais = [x for x in lista if x == pivo]
    maiores = [x for x in lista if x > pivo]
    return ordenar(menores) + iguais + ordenar(maiores)
