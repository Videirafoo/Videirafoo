# Mini Sistema 03 — Cadastro de Alunos

Terceiro projeto da coleção **Mini Sistemas Python** do `Videirafoo`.

## Objetivo

Construir um sistema escolar simples para cadastrar alunos, registrar notas, calcular média, classificar a situação acadêmica e gerar relatórios.

## O que este projeto ensina

- funções;
- listas e dicionários;
- dados aninhados;
- regras de negócio;
- validação;
- busca por nome e matrícula;
- cálculo de média;
- classificação por critérios;
- persistência em JSON;
- separação entre lógica e interface de terminal;
- testes automatizados;
- CI com GitHub Actions.

## Funcionalidades

- cadastrar aluno;
- impedir matrícula duplicada;
- adicionar notas de 0 a 10;
- buscar por nome ou matrícula;
- calcular média automaticamente;
- classificar como `aprovado`, `recuperacao`, `reprovado` ou `sem notas`;
- gerar relatório simples;
- excluir aluno;
- salvar e carregar dados em JSON.

## Regra didática de situação

Neste projeto usamos a seguinte regra apenas para fins de aprendizagem:

- média **7 ou mais** → aprovado;
- média **5 até 6,99** → recuperação;
- média **abaixo de 5** → reprovado;
- sem notas → sem classificação final.

Em um sistema real, essas regras devem vir da instituição responsável.

## Estrutura

```text
cadastro_alunos/
├── __init__.py
├── app.py
├── test_app.py
└── README.md
```

O arquivo `alunos.json` é criado automaticamente quando os dados são salvos pela primeira vez.

## Como executar

Na raiz do repositório:

```bash
python conteudos/mini_sistemas/cadastro_alunos/app.py
```

## Como testar

```bash
python -m unittest conteudos.mini_sistemas.cadastro_alunos.test_app
```

## Conceito importante: regra de negócio em função própria

O cálculo da situação acadêmica fica separado da interface.

Isso permite alterar a regra depois sem precisar reescrever o menu inteiro.

Exemplo:

```python
media = calcular_media(aluno)
situacao = calcular_situacao(aluno)
```

Esse padrão é importante em sistemas reais: **regras de negócio não devem ficar espalhadas pela interface**.

## Checklist de revisão

Antes de considerar uma alteração pronta, confirme:

- [ ] matrícula vazia é rejeitada;
- [ ] matrícula duplicada é rejeitada;
- [ ] nota abaixo de 0 é rejeitada;
- [ ] nota acima de 10 é rejeitada;
- [ ] média é calculada corretamente;
- [ ] situação acadêmica corresponde à média;
- [ ] busca funciona por nome e matrícula;
- [ ] exclusão não altera outros alunos;
- [ ] JSON salva e carrega sem perda de dados;
- [ ] testes passam no GitHub Actions.

## Desafios para quem está estudando

Tente implementar, nesta ordem:

1. editar nome do aluno;
2. remover uma nota específica;
3. ordenar alunos por média;
4. mostrar melhor e pior média;
5. calcular média geral da turma;
6. mostrar quantidade de aprovados e reprovados;
7. adicionar disciplinas;
8. separar notas por disciplina;
9. exportar boletim em arquivo;
10. transformar o sistema em API.

## Erros comuns

### Aceitar qualquer valor como nota

Sem validação, uma nota `15` ou `-2` poderia entrar no sistema e invalidar os cálculos.

### Usar nome como identificador único

Pessoas podem ter nomes iguais. Por isso usamos a **matrícula** como chave de busca principal.

### Misturar cálculo de média com impressão

Uma função que calcula deve retornar um valor. A interface decide como exibir esse valor.

## Próximo sistema

**Mini Sistema 04 — Controle de Estoque**, adicionando produtos, quantidades, movimentações e alertas de estoque baixo.
