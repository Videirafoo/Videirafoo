# Qualidade verificável — GitHub Student Dashboard

Este documento registra **evidências reproduzíveis** da qualidade do GitHub Student Dashboard. Os números abaixo são uma fotografia de uma execução real do GitHub Actions e podem evoluir conforme o código e os testes mudam.

## Estado verificado

Execução de referência: [GitHub Student Dashboard CI #135](https://github.com/Videirafoo/Videirafoo/actions/runs/35014194113)

| Evidência | Resultado observado |
|---|---:|
| Testes automatizados | **214 passando** |
| Cobertura total medida | **97,9%** |
| Gate mínimo de cobertura | **90% — aprovado nessa execução** |
| `competency_matrix.py` | **100,0%** |
| `readme_quality.py` | **100,0%** |
| `web.py` | **99,1%** |
| `lab_api.py` | **99,0%** |
| `lab_business.py` | **98,5%** |
| `github_client.py` | **97,8%** |
| `engine.py` | **97,0%** |
| `history.py` | **95,9%** |
| `ai_explainer.py` | **95,7%** |
| `lab_systems.py` | **94,8%** |
| `lab_web.py` | **94,3%** |
| Auditoria de dependências | **nenhuma vulnerabilidade conhecida reportada pelo `pip-audit` nessa execução** |
| Sintaxe Python | **OK** |
| Sintaxe JavaScript do laboratório, trilha e matriz | **OK** |
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

| Etapa | Testes | Cobertura | Foco |
|---|---:|---:|---|
| Primeira medição | 95 | 73,3% | descobrir lacunas reais |
| CLI + GitHub client + provider de IA | 118 | 81,9% | transporte, parsing, erros HTTP/rede/JSON |
| Bordas dos mini sistemas | 135 | 89,0% | estados inválidos, limites, 404 e regras de negócio |
| Adaptador da API do laboratório | 147 | 92,9% | normalização, CRUD, branches e checks |
| Trilha Educacional | 156 | 92,9% | rota, API, sitemap, progresso e navegação |
| Matriz Viva de Competências | 177 | 92,6% | evidências públicas, CI, runtime e PR externo |
| Runtime seguro da Matriz | 181 | 92,6% | host canônico e proxy reverso sem autochamada HTTP |
| Bordas do engine | 188 | 94,8% | URLs inválidas, estados de CI, perfil vazio e branches de erro |
| Bordas do README | 196 | 95,6% | parsing, encoding, links internos e falhas da API |
| Handlers web | 206 | 96,8% | respostas de erro e fluxos alternativos HTTP |
| Estados raros da Matriz | **214** | **97,9%** | cache, falhas parciais, PR/CI e evidências indisponíveis |

A execução #135 confirmou **214 testes passando**, **97,9% de cobertura total** e o **gate de 90% ativo**.

### Módulos fortalecidos

- `competency_matrix.py`: **100,0%**;
- `readme_quality.py`: **100,0%**;
- `cli.py`: **100,0%**;
- `comparison.py`: **100,0%**;
- `web.py`: **99,1%**;
- `lab_api.py`: **99,0%**;
- `lab_business.py`: **98,5%**;
- `github_client.py`: **97,8%**;
- `engine.py`: **97,0%**;
- `history.py`: **95,9%**;
- `ai_explainer.py`: **95,7%**;
- `lab_systems.py`: **94,8%**;
- `lab_web.py`: **94,3%**.

A melhoria veio de testes de comportamento e casos-limite; não de exclusões artificiais na configuração de cobertura.

## Próximos alvos de cobertura útil

O objetivo não é transformar 100% em meta estética. Com a cobertura global já em **97,9%**, a prioridade passa a ser proteger comportamento importante e evitar testes sem valor.

Próximos alvos úteis:

1. `lab_web.py` — **94,3%**, apenas branches de erro e validações que representem cenários reais;
2. `lab_systems.py` — **94,8%**, focando regras de negócio ainda sem caso de borda;
3. `ai_explainer.py` — **95,7%**, principalmente fallback e respostas de provider;
4. `history.py` — **95,9%**, somente se houver cenário real ainda não protegido;
5. manter `engine.py`, `web.py`, `readme_quality.py` e `competency_matrix.py` protegidos sem perseguir linhas irrelevantes.

O gate global permanece em **90%** de propósito: ele existe para impedir regressão importante, não para transformar cobertura em métrica de vaidade.

## Auditoria de dependências

A CI executa:

```bash
pip-audit -r projetos/github_student_dashboard/requirements.txt
```

A auditoria é **informativa**. Uma ocorrência futura aparece no resumo e no artefato da CI para revisão, sem ser tratada automaticamente como prova de exploração ou como motivo suficiente para derrubar produção sem análise.

Na execução #135, o log registrou:

```text
No known vulnerabilities found
```

## Evidências geradas pela CI

Cada execução de qualidade publica o artefato `dashboard-quality-evidence` contendo:

- `coverage.txt`;
- `coverage.json`;
- `pip-audit.txt`.

Artefato da execução #135: [dashboard-quality-evidence](https://github.com/Videirafoo/Videirafoo/actions/runs/35014194113/artifacts/10415166150)

## Princípio

> **Qualidade aqui precisa ser observável, reproduzível e ligada ao código real.**

A ordem adotada é:

`medir` → `encontrar lacunas` → `escrever testes úteis` → `medir novamente` → `proteger contra regressão`.
