# 05 — Funções

## O que você vai aprender

- `def`;
- parâmetros;
- retorno;
- escopo;
- reutilização;
- responsabilidade única.

## Exemplo mínimo

```python
def saudacao(nome):
    return f"Olá, {nome}!"

mensagem = saudacao("Ana")
print(mensagem)
```

## Parâmetro x retorno

O parâmetro entra na função. O `return` devolve um resultado.

```python
def somar(a, b):
    return a + b
```

Evite fazer tudo dentro de uma única função muito grande. Uma boa função tem uma responsabilidade clara.

## Exercício guiado — calculadora modular

```python
def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        return None
    return a / b


numero1 = float(input("Número 1: "))
numero2 = float(input("Número 2: "))

print("Soma:", somar(numero1, numero2))
print("Subtração:", subtrair(numero1, numero2))
print("Multiplicação:", multiplicar(numero1, numero2))

resultado_divisao = dividir(numero1, numero2)
if resultado_divisao is None:
    print("Divisão por zero não permitida")
else:
    print("Divisão:", resultado_divisao)
```

## Tente sozinho

Crie funções para:

- calcular média de duas notas;
- verificar se um número é par;
- retornar o maior entre dois números.

## Erros comuns

- esquecer de chamar a função;
- confundir `print()` com `return`;
- usar uma variável local fora da função;
- criar funções que fazem tarefas demais.

## Desafio extra

Crie um menu que chame funções diferentes conforme a opção escolhida.

## Próximo passo

Agora vamos trabalhar com grupos de dados usando listas e dicionários.
