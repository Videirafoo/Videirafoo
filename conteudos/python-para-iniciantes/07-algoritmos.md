# 07 — Busca, ordenação e Big O

## O que você vai aprender

- busca sequencial;
- busca binária;
- por que uma lista ordenada importa;
- ideia de custo de execução;
- introdução a Big O.

## Busca sequencial

Percorre os elementos até encontrar o valor.

```python
def busca_sequencial(lista, alvo):
    for indice, valor in enumerate(lista):
        if valor == alvo:
            return indice
    return -1
```

## Busca binária

Só funciona corretamente em uma coleção ordenada.

```python
def busca_binaria(lista, alvo):
    inicio = 0
    fim = len(lista) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2

        if lista[meio] == alvo:
            return meio
        if lista[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1

    return -1
```

## Intuição de Big O

- busca sequencial: pode precisar olhar muitos elementos → `O(n)`;
- busca binária: elimina metade do espaço a cada passo → `O(log n)`.

Big O não mede segundos exatos. Ele descreve como o custo cresce quando a entrada aumenta.

## Exercício guiado

Crie uma lista ordenada com 10 números e procure um valor usando as duas funções. Mostre o índice encontrado.

## Tente sozinho

Adapte as buscas para contar quantas comparações foram feitas.

## Erros comuns

- usar busca binária em lista desordenada;
- confundir índice com valor;
- assumir que algoritmo mais sofisticado é sempre necessário;
- decorar Big O sem entender o comportamento do algoritmo.

## Desafio extra

Compare busca sequencial e binária em listas de tamanhos diferentes contando comparações.

## Próximo passo

Vamos estudar recursividade e aprender a reconhecer caso base e passo recursivo.
