# Qualidade verificável — GitHub Student Dashboard

Este documento registra **evidências reproduzíveis** da qualidade do GitHub Student Dashboard. Os números abaixo são uma fotografia de uma execução real do GitHub Actions e podem evoluir conforme o código e os testes mudam.

## Estado verificado

Execução de referência: [GitHub Student Dashboard CI #104](https://github.com/Videirafoo/Videirafoo/actions/runs/34994310410)

| Evidência | Resultado observado |
|---|---:|
| Testes automatizados | **118 passando** |
| Cobertura total medida | **81,9%** |
| Gate mínimo de cobertura | **80% — aprovado nessa execução** |
| Auditoria de dependências | **nenhuma vulnerabilidade conhecida reportada pelo `pip-audit` nessa execução** |
| Sintaxe Python | **OK** |
| Sintaxe JavaScript do laboratório | **OK** |
| CI | **success** |

> A frase sobre vulnerabilidades é limitada ao que o `pip-audit` conseguiu verificar naquela execução. Ela não significa que o software seja livre de qualquer vulnerabilidade.

## Como a cobertura é medida

A CI executa a suíte real de `unittest` com `coverage.py`, incluindo cobertura de branches.

```bash
coverage run --rcfile=projetos/github_student_dashboard/.coveragerc \
  -m unittest discover -s projetos/github_student_dashboard -t . -p "test_*.py"
coverage report --rcfile=projetos/github_student_dashboard/.coveragerc -m
```

A medição não usa um número escrito manualmente no README. Se a cobertura total cair abaixo de **80%**, a etapa de testes falha.

## Evolução comprovada

A primeira medição desta etapa encontrou:

- **95 testes**;
- **73,3%** de cobertura total;
- `cli.py`: **0,0%**;
- `github_client.py`: **25,0%**;
- `ai_explainer.py`: **45,3%**.

Depois de adicionar testes direcionados às lacunas encontradas, a execução #104 confirmou, já com o gate de 80% ativo:

- **118 testes**;
- **81,9%** de cobertura total;
- `cli.py`: **100,0%**;
- `github_client.py`: **97,5%**;
- `ai_explainer.py`: **95,7%**.

A melhoria veio de testes de comportamento, erros de rede/HTTP/JSON, parsing do provider de IA e interface de linha de comando — não de exclusões artificiais na configuração de cobertura.

## Próximos alvos de cobertura

A cobertura agora orienta a prioridade de testes. Os módulos com espaço mais claro para evolução são:

1. `lab_business.py` — **72,8%**;
2. `lab_api.py` — **74,4%**;
3. `lab_web.py` — **75,9%**;
4. `lab_systems.py` — **76,6%**;
5. `engine.py` — **82,1%**, principalmente branches de erro e casos-limite.

O objetivo não é buscar 100% por aparência. Novos testes devem proteger regras de negócio, bordas e falhas que realmente importam.

## Auditoria de dependências

A CI executa:

```bash
pip-audit -r projetos/github_student_dashboard/requirements.txt
```

A auditoria é **informativa**. Uma ocorrência futura aparecerá no resumo e no artefato da CI para revisão, sem ser tratada automaticamente como prova de exploração ou motivo suficiente para quebrar produção sem análise.

Na execução #104, o log registrou:

```text
No known vulnerabilities found
```

## Evidências geradas pela CI

Cada execução de qualidade publica um artefato `dashboard-quality-evidence` contendo:

- `coverage.txt`;
- `coverage.json`;
- `pip-audit.txt`.

Artefato da execução #104: [dashboard-quality-evidence](https://github.com/Videirafoo/Videirafoo/actions/runs/34994310410/artifacts/10406963062)

## Princípio

> **Qualidade aqui precisa ser observável, reproduzível e ligada ao código real.**

A ordem adotada é:

`medir` → `encontrar lacunas` → `escrever testes úteis` → `medir novamente` → `proteger contra regressão`.
