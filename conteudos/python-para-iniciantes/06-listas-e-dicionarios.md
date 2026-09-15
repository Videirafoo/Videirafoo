# 06 — Listas e dicionários

## O que você vai aprender

- criar e percorrer listas;
- acessar índices;
- adicionar e remover elementos;
- usar dicionários;
- combinar listas e dicionários em pequenos cadastros.

## Lista

```python
nomes = ["Ana", "Bruno", "Carla"]

for nome in nomes:
    print(nome)
```

Adicionar e remover:

```python
nomes.append("Diego")
nomes.remove("Bruno")
```

## Dicionário

```python
aluno = {
    "nome": "Ana",
    "idade": 20,
    "curso": "Engenharia de Software"
}

print(aluno["nome"])
```

## Lista de dicionários

```python
alunos = [
    {"nome": "Ana", "nota": 8.5},
    {"nome": "Bruno", "nota": 6.0},
]

for aluno in alunos:
    print(aluno["nome"], aluno["nota"])
```

## Exercício guiado — lista de tarefas

```python
tarefas = []

while True:
    print("\n1 - Adicionar")
    print("2 - Listar")
    print("0 - Sair")
    opcao = input("Opção: ")

    if opcao == "1":
        tarefa = input("Nova tarefa: ")
        tarefas.append(tarefa)
    elif opcao == "2":
        for indice, tarefa in enumerate(tarefas, start=1):
            print(f"{indice}. {tarefa}")
    elif opcao == "0":
        break
    else:
        print("Opção inválida")
```

## Tente sozinho

Crie um cadastro de alunos com nome e nota usando uma lista de dicionários.

## Erros comuns

- acessar índice que não existe;
- alterar uma lista enquanto a percorre sem entender o efeito;
- usar chave de dicionário inexistente;
- guardar dados relacionados em várias listas paralelas em vez de um dicionário.

## Desafio extra

Permita buscar um aluno pelo nome e mostrar sua nota.

## Próximo passo

Vamos estudar estratégias de busca, ordenação e uma primeira noção de eficiência.
