# 11 — Projeto final

## Objetivo

Construir um pequeno sistema completo usando os fundamentos estudados.

Escolha um tema:

- biblioteca;
- controle de estoque;
- cadastro de alunos;
- tarefas;
- finanças pessoais;
- agenda de contatos.

## Requisitos mínimos

O projeto deve ter:

- menu interativo;
- funções pequenas e claras;
- validação de entrada;
- listas e/ou dicionários;
- persistência em JSON;
- tratamento de erros;
- `main()` com `if __name__ == "__main__":`;
- README com instruções;
- `.gitignore`;
- pelo menos 3 testes básicos;
- CI para validar sintaxe e testes.

## Estrutura sugerida

```text
projeto/
├── main.py
├── dados.json
├── README.md
├── .gitignore
├── sistema/
│   ├── __init__.py
│   ├── dados.py
│   └── regras.py
└── tests/
    └── test_regras.py
```

## Etapas

### 1. Defina o problema

Escreva em uma frase o que o sistema resolve.

### 2. Liste as operações

Exemplo para agenda:

- cadastrar contato;
- listar contatos;
- buscar;
- editar;
- excluir;
- salvar.

### 3. Modele os dados

Exemplo:

```python
contato = {
    "nome": "Ana",
    "telefone": "99999-0000",
    "email": "ana@example.com"
}
```

### 4. Implemente uma função por responsabilidade

Evite uma função gigante que faça tudo.

### 5. Teste as regras

Priorize funções que recebem valores e retornam resultados sem depender de `input()`.

### 6. Documente

O README deve responder:

- o que é;
- o que ensina;
- como executar;
- estrutura;
- funcionalidades;
- próximos passos.

## Critério de conclusão

O sistema está concluído quando outra pessoa consegue clonar, entender, executar e modificar sem precisar perguntar como funciona.

## Depois da conclusão

O próximo estágio da trajetória é a coleção **Mini Sistemas**, onde cada projeto será tratado como um produto pequeno e evolutivo.
