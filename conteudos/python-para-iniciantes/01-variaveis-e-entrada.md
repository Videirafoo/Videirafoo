# 01 — Variáveis e entrada de dados

## O que você vai aprender

- `str`, `int`, `float` e `bool`;
- `input()`;
- conversão de tipos;
- f-strings;
- como guardar e reutilizar dados.

## Conceito

Uma variável é um nome que aponta para um valor.

```python
nome = "Ana"
idade = 19
altura = 1.67
estudando = True
```

## Entrada de dados

```python
nome = input("Digite seu nome: ")
idade = int(input("Digite sua idade: "))

print(f"Olá, {nome}. Você tem {idade} anos.")
```

`input()` sempre devolve texto. Por isso usamos `int()` quando precisamos de um número inteiro.

## Exercício guiado — ficha simples

```python
nome = input("Nome: ")
curso = input("Curso: ")
periodo = int(input("Período: "))

print("\n--- Ficha ---")
print(f"Nome: {nome}")
print(f"Curso: {curso}")
print(f"Período: {periodo}")
```

## Tente sozinho

Crie uma ficha com:

- nome;
- idade;
- cidade;
- linguagem que está aprendendo.

Depois mostre tudo em uma frase.

## Erros comuns

- tentar somar texto com número;
- esquecer de converter `input()`;
- usar nomes vagos como `x` quando um nome claro seria melhor;
- sobrescrever uma variável sem perceber.

## Desafio extra

Pergunte o ano de nascimento e calcule uma idade aproximada usando o ano atual informado pelo usuário.

## Próximo passo

No próximo módulo vamos usar operadores para fazer cálculos e comparações.
