# Mini Sistema 08 — Gerenciador de Hábitos

Oitavo projeto da coleção **Mini Sistemas Python** do GitHub `Videirafoo`.

## Objetivo

Construir um sistema simples para acompanhar hábitos recorrentes, metas semanais e sequência de dias concluídos.

O projeto introduz um tipo de problema diferente dos anteriores: **acompanhar comportamento ao longo do tempo**.

## O que este projeto ensina

- cadastro de hábitos;
- meta semanal de 1 a 7 dias;
- registros por data;
- prevenção de registros duplicados;
- busca por nome;
- sequência de dias consecutivos;
- progresso semanal;
- cálculo percentual;
- exclusão de hábitos;
- persistência em JSON;
- uso de `date` e `timedelta`;
- testes automatizados;
- CI.

## Funcionalidades

- criar hábito;
- impedir nomes duplicados;
- definir meta semanal;
- listar hábitos;
- buscar hábito;
- registrar conclusão do dia;
- remover conclusão do dia;
- calcular sequência atual;
- calcular progresso da semana;
- excluir hábito;
- salvar e carregar dados em JSON.

## Estrutura

```text
gerenciador_habitos/
├── __init__.py
├── app.py
├── test_app.py
└── README.md
```

O arquivo `habitos.json` é criado automaticamente quando os dados são salvos pela primeira vez.

## Como executar

Na raiz do repositório:

```bash
python conteudos/mini_sistemas/gerenciador_habitos/app.py
```

## Como testar

```bash
python -m unittest conteudos.mini_sistemas.gerenciador_habitos.test_app
```

A CI geral também descobre automaticamente todos os arquivos `test_*.py` da coleção.

## Conceito importante: registros por data

Cada conclusão é armazenada como uma data no formato ISO:

```text
AAAA-MM-DD
```

Exemplo:

```json
{
  "id": 1,
  "nome": "Estudar Python",
  "meta_semanal": 5,
  "registros": [
    "2026-09-13",
    "2026-09-14",
    "2026-09-15"
  ]
}
```

Esse formato é simples de ler e também pode ser convertido novamente para `date` pelo Python.

## Conceito importante: sequência

A sequência atual conta quantos dias consecutivos foram concluídos terminando na data de referência.

Se existem registros em:

```text
13/09
14/09
15/09
```

e a referência é `15/09`, a sequência é **3**.

Se o dia 15 não tiver registro, a sequência atual é **0**, mesmo que existam registros anteriores.

Essa escolha deixa a regra objetiva e testável.

## Conceito importante: progresso semanal

O progresso compara a quantidade de conclusões da semana com a meta definida.

Exemplo:

```text
Meta semanal: 4
Concluídos: 3
Progresso: 75%
```

O percentual é limitado a 100%, mesmo que existam registros além da meta.

## Checklist de revisão

Antes de considerar uma alteração pronta:

- [ ] nome vazio é rejeitado;
- [ ] nomes duplicados são rejeitados;
- [ ] meta menor que 1 ou maior que 7 é rejeitada;
- [ ] o mesmo dia não é registrado duas vezes;
- [ ] datas inválidas são rejeitadas;
- [ ] sequência consecutiva é calculada corretamente;
- [ ] progresso semanal respeita a meta;
- [ ] busca ignora maiúsculas/minúsculas;
- [ ] exclusão preserva os demais hábitos;
- [ ] JSON salva e carrega corretamente;
- [ ] testes passam na CI.

## Desafios para quem está estudando

Tente evoluir o sistema nesta ordem:

1. editar nome e meta do hábito;
2. mostrar maior sequência já alcançada;
3. exibir calendário mensal;
4. adicionar categorias;
5. mostrar percentual do mês;
6. criar hábitos com frequência específica por dia da semana;
7. adicionar lembretes;
8. gerar relatório mensal;
9. criar gráficos;
10. criar interface mobile.

## Próximo sistema

**Mini Sistema 09 — API de Tarefas**, levando os conceitos anteriores para HTTP, JSON, endpoints e testes de API.
