# Qualidade verificável — GitHub Student Dashboard

Este documento registra **evidências reproduzíveis** da qualidade do GitHub Student Dashboard. Os números abaixo são uma fotografia de uma execução real do GitHub Actions e podem evoluir conforme o código e os testes mudam.

## Estado verificado

Execução de referência: [GitHub Student Dashboard CI #108](https://github.com/Videirafoo/Videirafoo/actions/runs/34995444039)

| Evidência | Resultado observado |
|---|---:|
| Testes automatizados | **147 passando** |
| Cobertura total medida | **92,9%** |
| Gate mínimo de cobertura | **90% — aprovado nessa execução** |
| `lab_api.py` | **99,0%** |
| `lab_business.py` | **98,5%** |
| `lab_systems.py` | **94,8%** |
| `lab_web.py` | **94,3%** |
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

A medição não usa um número escrito manualmente no README. Se a cobertura total cair abaixo de **90%**, a etapa de testes falha.

## Evolução comprovada

A cobertura foi usada como mapa de trabalho, em vez de aumentar números artificialmente:

| Etapa | Testes | Cobertura | Foco |
|---|---:|---:|---|
| Primeira medição | 95 | 73,3% | descobrir lacunas reais |
| CLI + GitHub client + provider de IA | 118 | 81,9% | transporte, parsing, erros HTTP/rede/JSON |
| Bordas dos mini sistemas | 135 | 89,0% | estados inválidos, limites, 404 e regras de negócio |
| Adaptador da API do laboratório | 147 | **92,9%** | normalização, CRUD, branches e checks |

A execução #108 confirmou o resultado final desta etapa já com o **gate de 90% ativo**.

### Módulos fortalecidos

- `cli.py`: **100,0%**;
- `comparison.py`: **100,0%**;
- `lab_api.py`: **99,0%**;
- `lab_business.py`: **98,5%**;
- `github_client.py`: **97,5%**;
- `ai_explainer.py`: **95,7%**;
- `history.py`: **95,9%**;
- `lab_systems.py`: **94,8%**;
- `lab_web.py`: **94,3%**.

A melhoria veio de testes de comportamento e casos-limite; não de exclusões artificiais na configuração de cobertura.

## Próximos alvos de cobertura útil

O objetivo não é buscar 100% por aparência. Os próximos testes devem proteger branches que realmente importam:

1. `engine.py` — **82,1%**;
2. `web.py` — **85,2%**;
3. `readme_quality.py` — **86,9%**;
4. branches residuais de tratamento de erro nos módulos já acima de 94%.

## Auditoria de dependências

A CI executa:

```bash
pip-audit -r projetos/github_student_dashboard/requirements.txt
```

A auditoria é **informativa**. Uma ocorrência futura aparece no resumo e no artefato da CI para revisão, sem ser tratada automaticamente como prova de exploração ou como motivo suficiente para derrubar produção sem análise.

Na execução #108, o log registrou:

```text
No known vulnerabilities found
```

## Evidências geradas pela CI

Cada execução de qualidade publica o artefato `dashboard-quality-evidence` contendo:

- `coverage.txt`;
- `coverage.json`;
- `pip-audit.txt`.

Artefato da execução #108: [dashboard-quality-evidence](https://github.com/Videirafoo/Videirafoo/actions/runs/34995444039/artifacts/10407506784)

## Princípio

> **Qualidade aqui precisa ser observável, reproduzível e ligada ao código real.**

A ordem adotada é:

`medir` → `encontrar lacunas` → `escrever testes úteis` → `medir novamente` → `proteger contra regressão`.
