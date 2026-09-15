# Mini Sistema 05 — Sistema de Biblioteca

Quinto projeto da coleção **Mini Sistemas Python** do `Videirafoo`.

## Objetivo

Construir um sistema simples de biblioteca relacionando três tipos de dados: **livros, usuários e empréstimos**.

## O que este projeto ensina

- modelagem de entidades;
- relacionamento entre dados;
- identificadores próprios;
- regras de disponibilidade;
- consistência entre registros;
- busca por título, autor ou ISBN;
- persistência em JSON;
- testes automatizados;
- CI.

## Funcionalidades

- cadastrar livros;
- impedir ISBN duplicado;
- cadastrar usuários;
- impedir documento duplicado;
- emprestar livro disponível;
- bloquear empréstimo duplicado do mesmo exemplar;
- devolver livro;
- listar empréstimos ativos;
- buscar livros;
- persistir o estado completo em JSON.

## Estrutura

```text
sistema_biblioteca/
├── __init__.py
├── app.py
├── test_app.py
└── README.md
```

O arquivo `biblioteca.json` é criado automaticamente quando os dados são salvos pela primeira vez.

## Como executar

```bash
python conteudos/mini_sistemas/sistema_biblioteca/app.py
```

## Como testar

```bash
python -m unittest conteudos.mini_sistemas.sistema_biblioteca.test_app
```

## Conceito importante: relacionamento entre entidades

Um empréstimo não repete todos os dados do livro e do usuário. Ele registra referências simples:

```python
{
    "isbn": "978-1",
    "documento": "DOC1",
    "devolvido": False
}
```

Isso evita duplicar informações desnecessariamente e prepara o estudante para entender relações em bancos de dados.

## Consistência dos dados

O sistema precisa manter algumas regras verdadeiras:

- um ISBN representa um único livro;
- um documento representa um único usuário;
- livro emprestado fica indisponível;
- livro devolvido volta a ficar disponível;
- não existe empréstimo válido para livro inexistente;
- não existe empréstimo válido para usuário inexistente.

## Checklist de revisão

- [ ] ISBN vazio é rejeitado;
- [ ] ISBN duplicado é rejeitado;
- [ ] documento vazio é rejeitado;
- [ ] documento duplicado é rejeitado;
- [ ] empréstimo exige livro existente;
- [ ] empréstimo exige usuário existente;
- [ ] livro indisponível não pode ser emprestado novamente;
- [ ] devolução encerra o empréstimo ativo;
- [ ] devolução torna o livro disponível;
- [ ] busca funciona por título, autor e ISBN;
- [ ] JSON preserva livros, usuários e empréstimos;
- [ ] testes passam na CI.

## Desafios para quem está estudando

Tente implementar nesta ordem:

1. excluir usuário sem empréstimo ativo;
2. excluir livro disponível;
3. impedir exclusão com empréstimo ativo;
4. registrar data do empréstimo;
5. registrar data prevista de devolução;
6. listar histórico de um usuário;
7. adicionar mais de um exemplar do mesmo título;
8. calcular atrasos;
9. adicionar multas didáticas;
10. migrar os dados para banco relacional.

## Próximo sistema

**Mini Sistema 06 — Caixa de Mercado**, introduzindo produtos, itens de venda, subtotais, total e fechamento de compra.
