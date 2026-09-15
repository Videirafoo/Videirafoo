# 03 — Condicionais

## O que você vai aprender

- `if`, `elif` e `else`;
- comparações;
- operadores `and`, `or` e `not`;
- como transformar regras em decisões.

## Exemplo simples

```python
idade = int(input("Idade: "))

if idade >= 18:
    print("Maior de idade")
else:
    print("Menor de idade")
```

## Várias condições

```python
nota = float(input("Nota: "))

if nota >= 7:
    print("Aprovado")
elif nota >= 5:
    print("Recuperação")
else:
    print("Reprovado")
```

## Operadores lógicos

```python
idade = 20
possui_documento = True

if idade >= 18 and possui_documento:
    print("Entrada permitida")
```

## Exercício guiado — classificador de notas

Peça duas notas, calcule a média e mostre:

- `Aprovado` para média >= 7;
- `Recuperação` para média >= 5 e < 7;
- `Reprovado` abaixo de 5.

```python
n1 = float(input("Nota 1: "))
n2 = float(input("Nota 2: "))
media = (n1 + n2) / 2

if media >= 7:
    resultado = "Aprovado"
elif media >= 5:
    resultado = "Recuperação"
else:
    resultado = "Reprovado"

print(f"Média: {media:.2f} — {resultado}")
```

## Tente sozinho

Crie um programa que classifique uma temperatura como fria, agradável ou quente. Defina claramente seus limites.

## Erros comuns

- usar `=` no lugar de `==`;
- criar condições que nunca podem acontecer;
- esquecer a indentação;
- repetir condições desnecessárias.

## Desafio extra

Crie um sistema simples de desconto baseado no valor da compra e em uma condição de cliente fidelidade.

## Próximo passo

Vamos repetir tarefas automaticamente com `for` e `while`.
