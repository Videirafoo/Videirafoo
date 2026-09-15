# Qualidade verificável — GitHub Student Dashboard

Este documento registra **evidências reproduzíveis** da qualidade do GitHub Student Dashboard. Os números abaixo são uma fotografia de uma execução real do GitHub Actions e podem evoluir conforme o código e os testes mudam.

## Estado verificado

Execução de referência: [GitHub Student Dashboard CI #132](https://github.com/Videirafoo/Videirafoo/actions/runs/35013263915)

| Evidência | Resultado observado |
|---|---:|
| Testes automatizados | **188 passando** |
| Cobertura total medida | **94,8%** |
| Gate mínimo de cobertura | **90% — aprovado nessa execução** |
| `engine.py` | **97,0%** |
| `competency_matrix.py` | **89,5%** |
| `web.py` | **87,3%** |
| `readme_quality.py` | **86,9%** |
| `github_client.py` | **97,8%** |
| `lab_api.py` | **99,0%** |
| `lab_business.py` | **98,5%** |
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
| Bordas do engine | **188** | **94,8%** | URLs inválidas, estados de CI, perfil vazio e branches de erro |

A execução #132 confirmou **188 testes passando**, **94,8% de cobertura total** e o **gate de 90% ativo**.

### Módulos fortalecidos

- `cli.py`: **100,0%**;
- `comparison.py`: **100,0%**;
- `lab_api.py`: **99,0%**;
- `lab_business.py`: **98,5%**;
- `github_client.py`: **97,8%**;
- `engine.py`: **97,0%**;
- `ai_explainer.py`: **95,7%**;
- `history.py`: **95,9%**;
- `lab_systems.py`: **94,8%**;
- `lab_web.py`: **94,3%**;
- `competency_matrix.py`: **89,5%**;
- `web.py`: **87,3%**;
- `readme_quality.py`: **86,9%**.

A melhoria veio de testes de comportamento e casos-limite; não de exclusões artificiais na configuração de cobertura.

## Próximos alvos de cobertura útil

O objetivo não é buscar 100% por aparência. Os próximos testes devem proteger branches que realmente importam:

1. `readme_quality.py` — **86,9%**, principalmente parsing e links internos de borda;
2. `web.py` — **87,3%**, especialmente handlers de falha e respostas alternativas;
3. `competency_matrix.py` — **89,5%**, principalmente estados de evidência menos frequentes;
4. manter `engine.py` protegido após o salto para **97,0%**;
5. manter o gate global em **90%** sem perseguir 100% apenas para melhorar a aparência do perfil.

## Auditoria de dependências

A CI executa:

```bash
pip-audit -r projetos/github_student_dashboard/requirements.txt
```

A auditoria é **informativa**. Uma ocorrência futura aparece no resumo e no artefato da CI para revisão, sem ser tratada automaticamente como prova de exploração ou como motivo suficiente para derrubar produção sem análise.

Na execução #132, o log registrou:

```text
No known vulnerabilities found
```

## Evidências geradas pela CI

Cada execução de qualidade publica o artefato `dashboard-quality-evidence` contendo:

- `coverage.txt`;
- `coverage.json`;
- `pip-audit.txt`.

Artefato da execução #132: [dashboard-quality-evidence](https://github.com/Videirafoo/Videirafoo/actions/runs/35013263915/artifacts/10414615853)

## Princípio

> **Qualidade aqui precisa ser observável, reproduzível e ligada ao código real.**

A ordem adotada é:

`medir` → `encontrar lacunas` → `escrever testes úteis` → `medir novamente` → `proteger contra regressão`.
