# Vantagem: rápido com muitos inteiros de poucos dígitos.
# Desvantagem: só aceita inteiros >= 0 e usa memória extra.
def ordenar(lista):
    a = lista.copy()
    if not a:
        return a
    casa = 1
    while max(a) // casa > 0:
        baldes = [[] for _ in range(10)]
        for numero in a:
            baldes[(numero // casa) % 10].append(numero)
        a = [numero for balde in baldes for numero in balde]
        casa *= 10
    return a
