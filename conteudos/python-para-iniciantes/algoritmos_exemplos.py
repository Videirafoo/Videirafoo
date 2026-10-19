"""Exemplos executáveis de busca e ordenação para iniciantes."""


def busca_sequencial(valores: list[int], alvo: int) -> int:
    for indice, valor in enumerate(valores):
        if valor == alvo:
            return indice
    return -1


def busca_binaria(valores: list[int], alvo: int) -> int:
    """Recebe valores ordenados em ordem crescente."""
    inicio, fim = 0, len(valores) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if valores[meio] == alvo:
            return meio
        if valores[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1


def ordenacao_bolha(valores: list[int]) -> list[int]:
    resultado = valores.copy()
    for fim in range(len(resultado) - 1, 0, -1):
        trocou = False
        for i in range(fim):
            if resultado[i] > resultado[i + 1]:
                resultado[i], resultado[i + 1] = resultado[i + 1], resultado[i]
                trocou = True
        if not trocou:
            break
    return resultado
