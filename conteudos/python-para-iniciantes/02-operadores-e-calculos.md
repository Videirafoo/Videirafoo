# 02 — Operadores e cálculos

## O que você vai aprender

- soma, subtração, multiplicação e divisão;
- resto e potência;
- comparação;
- precedência;
- como transformar fórmulas em código.

## Operadores principais

```python
print(10 + 2)   # 12
print(10 - 2)   # 8
print(10 * 2)   # 20
print(10 / 2)   # 5.0
print(10 // 3)  # 3
print(10 % 3)   # 1
print(2 ** 3)   # 8
```

## Exemplo — média

```python
nota1 = float(input("Nota 1: "))
nota2 = float(input("Nota 2: "))
media = (nota1 + nota2) / 2

print(f"Média: {media:.2f}")
```

## Exercício guiado — calculadora básica

```python
numero1 = float(input("Primeiro número: "))
numero2 = float(input("Segundo número: "))

print(f"Soma: {numero1 + numero2}")
print(f"Subtração: {numero1 - numero2}")
print(f"Multiplicação: {numero1 * numero2}")

if numero2 != 0:
    print(f"Divisão: {numero1 / numero2}")
else:
    print("Não é possível dividir por zero.")
```

## Tente sozinho

Crie um programa que calcule:

- área de um retângulo;
- perímetro;
- diferença entre largura e altura.

## Erros comuns

- esquecer parênteses em fórmulas;
- dividir por zero;
- usar `int()` quando o valor pode ter casas decimais;
- confundir `=` com `==`.

## Desafio extra

Calcule o IMC usando `peso / altura ** 2`.

## Próximo passo

Agora vamos ensinar o programa a tomar decisões com condicionais.
