# Vantagem: O(n log n) até no pior caso.
# Desvantagem: é um pouco mais difícil de entender.
def ordenar(lista):
    a = lista.copy()
    n = len(a)

    def ajustar(tamanho, raiz):
        while True:
            maior = raiz
            esq, dir = 2 * raiz + 1, 2 * raiz + 2
            if esq < tamanho and a[esq] > a[maior]:
                maior = esq
            if dir < tamanho and a[dir] > a[maior]:
                maior = dir
            if maior == raiz:
                break
            a[raiz], a[maior] = a[maior], a[raiz]
            raiz = maior

    for i in range(n // 2 - 1, -1, -1):
        ajustar(n, i)
    for fim in range(n - 1, 0, -1):
        a[0], a[fim] = a[fim], a[0]
        ajustar(fim, 0)
    return a
