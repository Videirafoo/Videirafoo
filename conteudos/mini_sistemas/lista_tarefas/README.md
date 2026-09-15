# Mini Sistema 02 — Lista de Tarefas

Segundo projeto da coleção **Mini Sistemas Python** do `Videirafoo`.

## Objetivo

Construir um sistema de tarefas simples, persistente e testável, mostrando como transformar fundamentos de Python em um programa organizado.

## O que este projeto ensina

- funções;
- listas e dicionários;
- IDs simples;
- busca textual;
- filtros;
- validação;
- persistência em JSON;
- tratamento de entrada inválida;
- separação entre lógica e interface de terminal;
- testes automatizados com `unittest`;
- CI com GitHub Actions.

## Funcionalidades

- adicionar tarefa;
- definir prioridade `baixa`, `media` ou `alta`;
- listar tarefas;
- buscar por título;
- marcar como concluída;
- excluir;
- filtrar pendentes;
- filtrar concluídas;
- salvar automaticamente em JSON.

## Estrutura

```text
lista_tarefas/
├── __init__.py
├── app.py
├── test_app.py
└── README.md
```

O arquivo `tarefas.json` é criado automaticamente quando o programa salva dados pela primeira vez.

## Como executar

Na raiz do repositório:

```bash
python conteudos/mini_sistemas/lista_tarefas/app.py
```

## Como testar

```bash
python -m unittest conteudos.mini_sistemas.lista_tarefas.test_app
```

## Conceito importante: lógica separada da interface

Funções como `criar_tarefa`, `buscar_tarefas`, `concluir_tarefa` e `excluir_tarefa` não dependem diretamente de `input()`.

Isso torna o código mais fácil de:

- testar;
- reutilizar;
- entender;
- evoluir depois para API, web ou mobile.

## Checklist de revisão

Antes de considerar uma alteração pronta, verifique de forma objetiva:

- [ ] o código compila;
- [ ] os testes passam;
- [ ] título vazio é rejeitado;
- [ ] prioridade inválida é rejeitada;
- [ ] o JSON salva e carrega corretamente;
- [ ] busca funciona sem diferenciar maiúsculas/minúsculas;
- [ ] concluir e excluir preservam os demais dados;
- [ ] a documentação continua compatível com o comportamento real.

Esse checklist segue o princípio: **automatizar deterministicamente o que pode ser provado e usar IA apenas para explicar, orientar e revisar pontos ambíguos**.

## Desafios para quem está estudando

Tente implementar, nesta ordem:

1. editar o título de uma tarefa;
2. ordenar por prioridade;
3. adicionar data de criação;
4. adicionar prazo;
5. impedir títulos duplicados;
6. criar categorias;
7. mostrar percentual concluído;
8. exportar relatório;
9. criar uma API para as mesmas funções;
10. criar uma interface web ou mobile.

## Erros comuns

### Misturar toda a lógica dentro do menu

Isso dificulta testes e manutenção. Prefira funções pequenas.

### Usar posição da lista como ID

Se uma tarefa for excluída, as posições mudam. Por isso o sistema mantém um campo `id` próprio.

### Salvar JSON somente ao sair

Se o programa encerrar inesperadamente, mudanças podem ser perdidas. Aqui os dados são salvos após operações que alteram o estado.

## Próximo sistema

**Mini Sistema 03 — Cadastro de Alunos**, adicionando cálculos de média, situação acadêmica, busca e relatórios simples.
