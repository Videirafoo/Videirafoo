# 08 — Recursividade

## O que você vai aprender

- caso base;
- passo recursivo;
- redução do problema;
- pilha de chamadas;
- quando uma solução iterativa pode ser mais simples.

## Exemplo — fatorial

```python
def fatorial(n):
    if n <= 1:
        return 1

    return n * fatorial(n - 1)
```

O caso base encerra as chamadas. Sem ele, a função continuaria chamando a si mesma até causar erro.

## Como pensar

Para cada problema recursivo pergunte:

1. qual é o menor caso que já sei resolver?
2. como reduzo o problema para chegar nesse caso?
3. o que cada chamada deve devolver?

## Exercício guiado — soma de 1 até n

```python
def soma_ate(n):
    if n <= 1:
        return n

    return n + soma_ate(n - 1)

print(soma_ate(5))  # 15
```

## Tente sozinho

Crie funções recursivas para:

- inverter uma string;
- calcular uma potência;
- somar os dígitos de um número positivo.

## Erros comuns

- esquecer o caso base;
- criar chamada que não aproxima do caso base;
- usar recursividade apenas porque parece mais avançado;
- não considerar o custo de muitas chamadas.

## Desafio extra

Implemente uma verificação recursiva de palíndromo.

## Próximo passo

Vamos fazer nossos dados sobreviverem ao encerramento do programa usando arquivos e JSON.
