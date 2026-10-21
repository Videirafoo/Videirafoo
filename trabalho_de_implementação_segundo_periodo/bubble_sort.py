# Vantagem: fácil de entender; para se já estiver ordenado.
# Desvantagem: faz muitas comparações (O(n²)).
def ordenar(lista):
    a = lista.copy()
    for fim in range(len(a) - 1, 0, -1):
        trocou = False
        for i in range(fim):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                trocou = True
        if not trocou:
            break
    return a
