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
5. Sistema de Biblioteca
6. Caixa de Mercado
7. Controle Financeiro Pessoal
8. Gerenciador de Hábitos
9. API de Tarefas
10. Projeto final integrado

## Progressão

Os primeiros projetos usam terminal e JSON. Depois entram testes mais completos, banco de dados, API e interface.

O objetivo é que cada sistema reutilize conhecimentos anteriores e acrescente apenas algumas ideias novas por vez.

## Regra de qualidade

A coleção adota uma regra simples:

> **Automatizar deterministicamente o que pode ser provado; usar IA para explicar, orientar e revisar onde existe ambiguidade.**

Por isso, sintaxe, testes e comportamentos objetivos devem ser validados automaticamente sempre que possível.
