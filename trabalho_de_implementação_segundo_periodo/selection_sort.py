# Vantagem: simples e faz poucas trocas.
# Desvantagem: lento para listas grandes (O(n²)).
def ordenar(lista):
    a = lista.copy()
    for i in range(len(a)):
        menor = i
        for j in range(i + 1, len(a)):
            if a[j] < a[menor]:
                menor = j
        a[i], a[menor] = a[menor], a[i]
    return a
