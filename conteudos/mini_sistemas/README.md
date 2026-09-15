# Mini Sistemas Python

Coleção prática do GitHub `Videirafoo` para transformar fundamentos de programação em pequenos sistemas completos.

## Objetivo

Cada mini sistema deve resolver um problema simples e ensinar como sair de exercícios isolados para um programa organizado.

## Padrão obrigatório

Cada projeto terá:

- problema e objetivo claros;
- código executável;
- funções organizadas;
- validação;
- persistência quando fizer sentido;
- README didático;
- testes básicos;
- CI;
- checklist de revisão;
- desafios de evolução.

## Sistemas

1. [Agenda de Contatos](./agenda_contatos/README.md) — cadastro, busca, edição, exclusão e JSON
2. [Lista de Tarefas](./lista_tarefas/README.md) — prioridades, filtros, conclusão, busca e JSON
3. [Cadastro de Alunos](./cadastro_alunos/README.md) — matrícula, notas, média, situação acadêmica, relatório e JSON
4. [Controle de Estoque](./controle_estoque/README.md) — produtos, entradas, saídas, estoque mínimo e JSON
5. [Sistema de Biblioteca](./sistema_biblioteca/README.md) — livros, usuários, empréstimos, devoluções e JSON
6. [Caixa de Mercado](./caixa_mercado/README.md) — catálogo, carrinho, estoque, descontos, vendas e JSON
7. [Controle Financeiro Pessoal](./controle_financeiro/README.md) — receitas, despesas, categorias, saldo, filtros, relatórios e JSON
8. [Gerenciador de Hábitos](./gerenciador_habitos/README.md) — metas semanais, registros diários, sequência, progresso e JSON
9. [API de Tarefas](./api_tarefas/README.md) — HTTP, REST, JSON, Flask, validação e testes de API
10. Projeto final integrado

## Progressão

Os primeiros projetos usam terminal e JSON. Depois entram testes mais completos, banco de dados, API e interface.

O objetivo é que cada sistema reutilize conhecimentos anteriores e acrescente apenas algumas ideias novas por vez.

## Regra de qualidade

A coleção adota uma regra simples:

> **Automatizar deterministicamente o que pode ser provado; usar IA para explicar, orientar e revisar onde existe ambiguidade.**

Por isso, sintaxe, testes e comportamentos objetivos devem ser validados automaticamente sempre que possível.
