# Mini Sistema 07 — Controle Financeiro Pessoal

Sétimo projeto da coleção **Mini Sistemas Python** do GitHub `Videirafoo`.

## Objetivo

Construir um controle financeiro pessoal simples, persistente e testável, mostrando como representar receitas, despesas, categorias, saldo e relatórios sem misturar regras de negócio com a interface do terminal.

## O que este projeto ensina

- receitas e despesas;
- categorias;
- datas em formato ISO;
- IDs simples;
- saldo;
- filtros;
- relatórios;
- agregação de valores;
- persistência em JSON;
- validação;
- funções pequenas e reutilizáveis;
- testes automatizados;
- CI.

## Funcionalidades

- adicionar receita;
- adicionar despesa;
- registrar descrição, valor, categoria e data;
- listar lançamentos;
- calcular total de receitas;
- calcular total de despesas;
- calcular saldo;
- filtrar por tipo;
- filtrar por categoria;
- filtrar por mês;
- gerar resumo por categoria;
- excluir lançamento;
- salvar tudo em JSON.

## Estrutura

```text
controle_financeiro/
├── __init__.py
├── app.py
├── test_app.py
└── README.md
```

O arquivo `financeiro.json` é criado automaticamente na primeira gravação.

## Como executar

Na raiz do repositório:

```bash
python conteudos/mini_sistemas/controle_financeiro/app.py
```

## Como testar

```bash
python -m unittest conteudos.mini_sistemas.controle_financeiro.test_app
```

A CI geral da coleção também descobre e executa automaticamente todos os arquivos `test_*.py` dos mini sistemas.

## Conceito importante: lançamento não é saldo

Um lançamento representa um evento financeiro individual.

Exemplos:

```text
Receita: Salário = R$ 3.000,00
Despesa: Mercado = R$ 450,00
Despesa: Internet = R$ 120,00
```

O saldo não precisa ser salvo separadamente. Ele pode ser calculado a partir dos lançamentos:

```text
saldo = receitas - despesas
```

Isso reduz o risco de manter dois valores diferentes para a mesma informação.

## Conceito importante: dados derivados

Receitas totais, despesas totais, saldo e resumo por categoria são **dados derivados**.

Eles são calculados a partir da lista de lançamentos.

Esse padrão é importante porque evita duplicação de estado e facilita testes.

## Exemplo

Com os lançamentos:

```text
+ R$ 3.000,00 | Renda       | Salário
- R$   450,00 | Alimentação | Mercado
- R$   120,00 | Casa        | Internet
```

O sistema calcula:

```text
Receitas: R$ 3.000,00
Despesas: R$   570,00
Saldo:    R$ 2.430,00
```

## Regras determinísticas

O sistema valida automaticamente:

- tipo deve ser `receita` ou `despesa`;
- descrição não pode ficar vazia;
- valor precisa ser maior que zero;
- categoria não pode ficar vazia;
- data precisa ser válida no formato `AAAA-MM-DD`;
- filtro mensal usa o formato `AAAA-MM`;
- saldo é sempre calculado a partir dos lançamentos.

## Checklist de revisão

Antes de considerar uma alteração pronta:

- [ ] receita é registrada corretamente;
- [ ] despesa é registrada corretamente;
- [ ] valor zero ou negativo é rejeitado;
- [ ] data inválida é rejeitada;
- [ ] total de receitas está correto;
- [ ] total de despesas está correto;
- [ ] saldo está correto;
- [ ] filtro por tipo funciona;
- [ ] filtro por categoria funciona sem depender de maiúsculas/minúsculas;
- [ ] filtro por mês funciona;
- [ ] resumo por categoria agrega os valores corretamente;
- [ ] exclusão remove somente o lançamento escolhido;
- [ ] JSON salva e carrega corretamente;
- [ ] testes passam na CI.

## Desafios para quem está estudando

Evolua o sistema nesta ordem:

1. editar um lançamento;
2. criar categorias favoritas;
3. definir orçamento mensal por categoria;
4. avisar quando uma categoria ultrapassar o orçamento;
5. adicionar despesas recorrentes;
6. adicionar receitas recorrentes;
7. gerar relatório mensal;
8. calcular percentual gasto por categoria;
9. exportar CSV;
10. criar gráficos em uma interface web.

## Próximo sistema

**Mini Sistema 08 — Gerenciador de Hábitos**, introduzindo hábitos, registros diários, sequência de dias, metas e progresso.
