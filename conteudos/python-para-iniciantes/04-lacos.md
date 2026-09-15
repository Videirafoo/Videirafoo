# 04 — Laços de repetição

## O que você vai aprender

- `for` e `while`;
- `range()`;
- contadores e acumuladores;
- `break` e `continue`;
- quando usar cada tipo de laço.

## `for`

Use quando você sabe quantas vezes quer repetir ou quando percorre uma coleção.

```python
for numero in range(1, 6):
    print(numero)
```

## `while`

Use quando a repetição depende de uma condição.

```python
senha = ""

while senha != "1234":
    senha = input("Senha: ")

print("Acesso liberado")
```

## Contador e acumulador

```python
total = 0

for numero in range(1, 6):
    total += numero

print(total)
```

## Exercício guiado — tabuada

```python
numero = int(input("Digite um número: "))

for multiplicador in range(1, 11):
    resultado = numero * multiplicador
    print(f"{numero} x {multiplicador} = {resultado}")
```

## Tente sozinho

Crie um menu que se repita até o usuário escolher `0` para sair.

Opções sugeridas:

1. mostrar uma mensagem;
2. somar dois números;
3. exibir uma tabuada;
0. sair.

## Erros comuns

- criar `while` infinito sem condição de saída;
- esquecer de atualizar a variável usada na condição;
- usar `range(1, 10)` esperando incluir o 10;
- colocar `break` onde a repetição ainda deveria continuar.

## Desafio extra

Leia cinco notas, calcule a soma e a média sem repetir cinco comandos `input()` manualmente.

## Próximo passo

Vamos organizar código repetido em funções reutilizáveis.
