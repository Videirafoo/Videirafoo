# Vantagem: bom para listas pequenas ou quase ordenadas.
# Desvantagem: lento para listas grandes e bagunçadas (O(n²)).
def ordenar(lista):
    a = lista.copy()
    for i in range(1, len(a)):
        atual = a[i]
        j = i - 1
        while j >= 0 and a[j] > atual:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = atual
    return a
