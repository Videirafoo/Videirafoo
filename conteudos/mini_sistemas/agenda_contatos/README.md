# Mini Sistema 01 — Agenda de Contatos

## O que este projeto ensina

- organização em funções;
- lista de dicionários;
- busca por nome;
- validação de dados;
- persistência em JSON;
- tratamento de arquivo inexistente;
- testes básicos;
- separação entre regra e interface.

## Funcionalidades

- cadastrar contato;
- listar contatos;
- buscar contato;
- editar contato;
- excluir contato;
- salvar dados em JSON.

## Executar

A partir da raiz do repositório:

```bash
python conteudos/mini_sistemas/agenda_contatos/main.py
```

## Rodar testes

```bash
python -m unittest conteudos.mini_sistemas.agenda_contatos.test_main
```

## Estrutura

```text
agenda_contatos/
├── README.md
├── main.py
└── test_main.py
```

O arquivo `contatos.json` é criado em tempo de execução e não precisa ser versionado.

## Como estudar este projeto

1. execute o sistema;
2. cadastre dois contatos;
3. feche e abra novamente;
4. confirme que os dados permaneceram;
5. leia cada função de `main.py`;
6. altere uma funcionalidade;
7. rode os testes.

## Desafios

- impedir telefones duplicados;
- ordenar contatos por nome;
- adicionar categoria ao contato;
- exportar contatos para CSV;
- criar interface gráfica;
- substituir JSON por banco de dados.

## Próximo sistema

**Lista de Tarefas**, adicionando status, prioridade e filtros.
