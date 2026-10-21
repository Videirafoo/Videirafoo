# Vantagem: muito rápido se os valores estão numa faixa pequena.
# Desvantagem: usa memória proporcional ao maior valor; aceita inteiros >= 0.
def ordenar(lista):
    if not lista:
        return []
    contagem = [0] * (max(lista) + 1)
    for numero in lista:
        contagem[numero] += 1
    resultado = []
    for numero, quantidade in enumerate(contagem):
        resultado.extend([numero] * quantidade)
    return resultado
