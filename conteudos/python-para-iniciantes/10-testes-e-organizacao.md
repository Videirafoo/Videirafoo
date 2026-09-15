# 10 — Erros, testes e organização

## O que você vai aprender

- `try/except`;
- validação de entrada;
- separar código em funções;
- ponto de entrada com `main()`;
- primeiros testes automatizados;
- ideia de CI.

## Tratando entrada inválida

```python
try:
    idade = int(input("Idade: "))
except ValueError:
    print("Digite um número inteiro válido.")
```

## Organizando o programa

```python
def ler_idade():
    while True:
        try:
            return int(input("Idade: "))
        except ValueError:
            print("Valor inválido. Tente novamente.")


def main():
    idade = ler_idade()
    print(f"Idade registrada: {idade}")


if __name__ == "__main__":
    main()
```

Esse padrão evita que o programa interativo execute automaticamente quando o arquivo for apenas importado por outro módulo ou por um teste.

## Primeiro teste

Código:

```python
def somar(a, b):
    return a + b
```

Teste com `pytest`:

```python
from programa import somar


def test_somar():
    assert somar(2, 3) == 5
```

Execução:

```bash
pytest
```

## O que é CI

Integração contínua executa verificações automaticamente a cada mudança. Em projetos Python simples, uma CI pode validar sintaxe e rodar testes.

Exemplo de comandos:

```bash
python -m compileall -q .
pytest
```

## Exercício guiado

Pegue um programa antigo seu e:

1. separe entrada, regra e saída em funções;
2. crie `main()`;
3. adicione tratamento de erro;
4. escreva pelo menos dois testes para funções que retornam valores.

## Tente sozinho

Crie uma função `calcular_media(notas)` e testes para:

- duas notas comuns;
- lista vazia;
- valores decimais.

Defina antes como sua função deve se comportar com lista vazia.

## Erros comuns

- usar `except:` para esconder qualquer erro;
- testar apenas o caminho feliz;
- misturar `input()` dentro de toda função de regra;
- não conseguir importar o módulo sem executar o sistema inteiro.

## Próximo passo

Você já tem a base para construir um pequeno sistema completo. Vamos juntar tudo no projeto final.
