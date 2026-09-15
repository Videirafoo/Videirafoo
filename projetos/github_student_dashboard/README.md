# GitHub Student Dashboard — MVP

Projeto público principal da trajetória educacional do GitHub `Videirafoo`.

## Missão

Ajudar estudantes a entenderem **como melhorar seus repositórios no GitHub** usando checks objetivos, evidências claras, prática executável e orientação educacional.

> **Automatizar deterministicamente o que pode ser provado; usar IA para explicar, orientar e revisar onde existe ambiguidade.**

## Acesso público

- Produção: https://github-student-dashboard-videirafoo.onrender.com
- Trilha Educacional: https://github-student-dashboard-videirafoo.onrender.com/trilha
- Matriz Viva de Competências: https://github-student-dashboard-videirafoo.onrender.com/competencias
- Laboratório: https://github-student-dashboard-videirafoo.onrender.com/laboratorio
- Saúde: `GET /healthz`
- Descoberta: `GET /robots.txt` e `GET /sitemap.xml`

Documentação complementar:

- [`SHOWCASE.md`](../../SHOWCASE.md)
- [`QUALITY.md`](../../QUALITY.md)
- [`CHANGELOG.md`](./CHANGELOG.md)
- [`COMMUNITY.md`](../../COMMUNITY.md)

## Estado atual

O MVP já possui:

- análise de repositório por `usuario/repositorio` ou URL;
- análise de perfil público completo;
- cliente para a API pública do GitHub;
- leitura da árvore de arquivos e linguagens;
- checks determinísticos e score reproduzível;
- evidências individuais por check;
- status real da execução mais recente da CI;
- análise objetiva da qualidade estrutural do README;
- verificação de links internos do README contra a árvore do próprio repositório;
- detecção de arquivos de teste em padrões comuns de múltiplas stacks;
- comparação entre dois repositórios;
- histórico versionado de evolução por commit;
- camada explicativa local;
- IA explicativa opcional, sem alterar o diagnóstico;
- Trilha Educacional com **6 níveis e 18 missões práticas**;
- Matriz Viva de Competências com **10 competências ligadas a evidências públicas**;
- laboratório com **10 mini sistemas** executando regras Python reais;
- CLI;
- interface web;
- endpoints JSON;
- cobertura interna real com `coverage.py` e branches;
- gate mínimo de cobertura;
- auditoria informativa das dependências de produção com `pip-audit`;
- artefatos de qualidade anexados à CI;
- deploy público com Gunicorn no Render;
- formulário estruturado de feedback;
- formulários públicos de bug e sugestão de melhoria;
- `good first issue` para contribuições de iniciantes;
- template de Pull Request.

## Matriz Viva de Competências

A rota `/competencias` não é um currículo preenchido manualmente e não certifica domínio pessoal. Ela consulta artefatos públicos e mostra somente o que pode ser sustentado por evidência neste momento.

As 10 competências atuais são:

1. Fundamentos em Python;
2. Algoritmos e busca;
3. Recursividade;
4. Mini sistemas e regras de negócio;
5. Backend e APIs HTTP;
6. Testes, cobertura e CI;
7. Deploy e operação;
8. Documentação técnica;
9. Contribuição open source;
10. IA aplicada com evidência.

### Fontes de evidência

A matriz cruza:

- árvores públicas dos repositórios acadêmicos;
- código e testes dos mini sistemas;
- arquivos reais do backend Flask;
- workflow e configuração do gate de cobertura;
- execução mais recente da `GitHub Student Dashboard CI`;
- execução da própria API no host público canônico, sem autochamada HTTP recursiva;
- documentação técnica versionada;
- estado real do Pull Request externo `fork-commit-merge/fork-commit-merge#8150`;
- implementação e testes da camada explicativa de IA.

### Estados

Evidências individuais:

- `verificada`;
- `parcial`;
- `ausente`;
- `indisponivel`.

Competências:

- `forte` — todas as evidências exigidas naquele item foram verificadas;
- `parcial` — existe evidência real, mas falta uma confirmação ou parte do critério;
- `sem_evidencia` — o artefato esperado não foi encontrado;
- `indisponivel` — a fonte necessária não pôde ser consultada.

A regra open source é conservadora: **PR aberto comprova contribuição enviada; somente merge público comprova aceitação externa**.

A API usa cache de até **600 segundos** para reduzir chamadas repetidas à GitHub API pública.

## Qualidade interna verificada

Execução de referência: [GitHub Student Dashboard CI #127](https://github.com/Videirafoo/Videirafoo/actions/runs/35005178735)

| Evidência | Resultado |
|---|---:|
| Testes automatizados | **180 passando** |
| Cobertura total | **92,6%** |
| Gate de regressão | **90% — aprovado** |
| `cli.py` | **100,0%** |
| `comparison.py` | **100,0%** |
| `lab_api.py` | **99,0%** |
| `lab_business.py` | **98,5%** |
| `github_client.py` | **97,8%** |
| `ai_explainer.py` | **95,7%** |
| `history.py` | **95,9%** |
| `lab_systems.py` | **94,8%** |
| `lab_web.py` | **94,3%** |
| `competency_matrix.py` | **89,5%** |
| `web.py` | **87,2%** |
| Auditoria | `No known vulnerabilities found` nessa execução |

Evolução comprovada:

`95 / 73,3%` → `118 / 81,9%` → `135 / 89,0%` → `147 / 92,9%` → `156 / 92,9%` → `177 / 92,6%` → **`180 testes / 92,6%`**

A cobertura caiu levemente de 92,9% para 92,6% porque a Matriz adicionou comportamento novo; o gate de **90%** continuou aprovado. O objetivo é proteger comportamento útil, não inflar percentuais.

A CI publica `coverage.txt`, `coverage.json` e `pip-audit.txt` no artefato `dashboard-quality-evidence`.

Artefato da execução #127:

https://github.com/Videirafoo/Videirafoo/actions/runs/35005178735/artifacts/10411236426

Os números são evidências de uma execução específica, não garantias permanentes. Consulte [`QUALITY.md`](../../QUALITY.md) para metodologia e limites.

## Regra central

A IA **não calcula o score**, **não decide se um check passou** e **não transforma evidência em certificação de competência**.

```text
GitHub API + artefatos públicos + runtime atual
   ↓
checks determinísticos
   ↓
evidências + score + CI real + matriz de competências
   ↓
explicação pedagógica
```

Sem provedor externo de IA, o Dashboard continua funcionando em modo local transparente.

## Checks atuais do repositório

| Check | Peso |
|---|---:|
| README | 15 |
| Descrição do repositório | 10 |
| Licença | 10 |
| `.gitignore` | 10 |
| Topics | 10 |
| CI | 15 |
| Testes | 20 |
| Arquivo de dependências | 10 |
| **Total** | **100** |

A pontuação representa somente os checks explícitos desta versão. Não é uma nota absoluta da qualidade do software.

## Páginas

| Página | Função |
|---|---|
| `/` | análise de repositório e perfil |
| `/trilha` | 6 níveis e 18 missões educacionais com evidências |
| `/competencias` | matriz viva baseada em artefatos públicos verificáveis |
| `/laboratorio` | 10 mini sistemas ligados ao backend Python |
| `/readme` | qualidade documental e links internos |
| `/comparar` | comparação objetiva entre repositórios |
| `/historico` | evolução de sinais versionados por commit |
| `/explicar` | explicação pedagógica local ou por IA |

## Endpoints principais

```http
GET /healthz
GET /api/trilha
GET /api/competencias
GET /api/analisar?repo=Videirafoo/Videirafoo
GET /api/perfil?usuario=Videirafoo
GET /api/readme?repo=Videirafoo/Videirafoo
GET /api/comparar?a=Videirafoo/Videirafoo&b=Videirafoo/Lista-01-segundo-periodo
GET /api/historico?repo=Videirafoo/Videirafoo&limite=5
GET /api/explicar?repo=Videirafoo/Videirafoo
```

Rotas do laboratório ficam sob `/api/laboratorio/*` e executam as regras dos mini sistemas Python reais.

## Arquitetura

```text
github_student_dashboard/
├── __init__.py
├── github_client.py
├── engine.py
├── readme_quality.py
├── comparison.py
├── history.py
├── learning_path.py
├── competency_matrix.py
├── ai_explainer.py
├── lab_api.py
├── lab_business.py
├── lab_systems.py
├── lab_web.py
├── cli.py
├── web.py
├── requirements.txt
├── requirements-dev.txt
├── .coveragerc
├── CHANGELOG.md
├── templates/
├── static/
├── test_*.py
└── README.md
```

### Separação de responsabilidades

- `github_client.py`: comunicação com a GitHub API, incluindo consulta de PR público;
- `engine.py`: checks, score, evidências, CI real e detecção de testes;
- `readme_quality.py`: critérios documentais e validação de links internos;
- `comparison.py`: diferenças objetivas entre dois repositórios;
- `history.py`: reconstrução de sinais versionados por commit;
- `learning_path.py`: níveis, competências didáticas e missões da Trilha;
- `competency_matrix.py`: agregação de evidências públicas da Matriz Viva;
- `ai_explainer.py`: explicação pedagógica a partir do relatório pronto;
- `lab_*.py`: adaptação segura dos mini sistemas para o laboratório público;
- `web.py`: rotas web, JSON, saúde, evidência de runtime e arquivos de descoberta.

## CI e qualidade

A CI executa, em ordem:

1. checkout do código;
2. Python 3.12;
3. instalação das dependências de validação;
4. `compileall` do projeto;
5. validação de sintaxe dos JavaScripts do laboratório, Trilha e Matriz;
6. **180 testes** sob `coverage.py` na execução de referência atual;
7. gate mínimo de cobertura em **90%**;
8. auditoria informativa de produção com `pip-audit`;
9. upload das evidências de cobertura e auditoria.

As ferramentas de desenvolvimento ficam em `requirements-dev.txt`; `requirements.txt` permanece reservado ao runtime de produção.

## Detecção de testes por stack

A detecção atual reconhece padrões frequentes sem depender apenas de um nome genérico de pasta:

- Python: `test_*.py`, `*_test.py`;
- JavaScript/TypeScript: `*.test.*`, `*.spec.*`, incluindo JSX/TSX, MJS e CJS;
- Go: `*_test.go`;
- Dart/Flutter: `*_test.dart`;
- Ruby: `*_spec.rb`, `*_test.rb`;
- Java/Kotlin: `*Test.java`, `*Tests.java`, `*Test.kt`, `*Tests.kt`;
- C#: `*Test.cs`, `*Tests.cs`;
- PHP: `*Test.php`, `*Tests.php`;
- diretórios convencionais: `test`, `tests`, `__tests__`, `spec`, `specs`.

Há regressão automática para evitar falsos positivos simples como `contest.py` e `latest.ts`.

## Qualidade do README

A cobertura documental mede presença de elementos verificáveis; não é uma nota subjetiva de estilo.

A verificação de links internos:

- valida arquivos e diretórios internos;
- ignora anchors locais;
- não consulta URLs externas arbitrárias;
- não inventa link quebrado quando a árvore não pode ser confirmada;
- mostra caminhos quebrados diretamente em `/readme`.

## Windows — início rápido com PowerShell

### Primeira vez

```powershell
cd $HOME
git clone https://github.com/Videirafoo/Videirafoo.git
cd .\Videirafoo
python -m pip install -r .\projetos\github_student_dashboard\requirements.txt
python -m projetos.github_student_dashboard.web
```

Abra `http://127.0.0.1:5000`.

### Atualizar uma cópia já clonada

```powershell
cd $HOME\Videirafoo
git pull
python -m pip install -r .\projetos\github_student_dashboard\requirements.txt
python -m projetos.github_student_dashboard.web
```

### Executar a qualidade localmente

```powershell
python -m pip install -r .\projetos\github_student_dashboard\requirements-dev.txt
coverage run --rcfile=.\projetos\github_student_dashboard\.coveragerc -m unittest discover -s projetos/github_student_dashboard -t . -p "test_*.py"
coverage report --rcfile=.\projetos\github_student_dashboard\.coveragerc -m
pip-audit -r .\projetos\github_student_dashboard\requirements.txt
```

## Produção

O serviço público usa Gunicorn:

```bash
gunicorn projetos.github_student_dashboard.web:app --bind 0.0.0.0:$PORT
```

O deploy canônico usa a branch `main` no Render. Uma promoção só deve ser considerada concluída quando o serviço reportar `live` e a aplicação estiver respondendo corretamente.

### Evitando healthcheck recursivo

A Matriz não chama o próprio `/healthz` por HTTP durante `/api/competencias`. Com Gunicorn sync e um único worker, isso poderia bloquear o worker aguardando uma requisição que ele mesmo precisaria atender.

Quando a Matriz é consultada pelo host público canônico, o atendimento da própria requisição é usado como evidência do runtime naquele instante. Em execução local, produção não é inferida.

## IA explicativa opcional

A página `/explicar` funciona em dois modos.

### Modo local

- nenhuma chamada externa;
- score determinístico;
- explicação baseada somente em fatos medidos pelo Dashboard;
- interface informa que não usou IA externa.

### Modo IA

```powershell
$env:OPENAI_API_KEY="SUA_CHAVE"
$env:OPENAI_MODEL="gpt-5.6-luna"
python -m projetos.github_student_dashboard.web
```

A integração usa a Responses API. A chave nunca deve ser colocada em README, código, commit, `.env` versionado ou screenshot público.

### Limites da IA

- score, checks, CI e estados da Matriz são fatos calculados antes da explicação;
- dados do GitHub são conteúdo não confiável, não instruções;
- fatos não comprovados devem ser identificados como não verificados;
- falha do provedor de IA não derruba o Dashboard: existe fallback local.

## Histórico de evolução

O histórico reconstrói por commit somente sinais que ficam versionados no Git:

- README;
- `.gitignore`;
- workflows de CI;
- testes;
- arquivos de dependências.

Descrição, topics e outros metadados atuais não são retroativamente inventados.

## Evidência antes de recomendação

```text
Observado: o que foi encontrado.
Impacto: por que isso importa.
Ação: qual melhoria concreta pode ser feita.
```

A IA recebe esse material somente depois dos checks determinísticos.

## Feedback e comunidade

- Feedback: https://github.com/Videirafoo/Videirafoo/issues/new?template=dashboard-feedback.yml
- Bug: https://github.com/Videirafoo/Videirafoo/issues/new?template=bug-report.yml
- Melhoria: https://github.com/Videirafoo/Videirafoo/issues/new?template=feature-request.yml
- Primeira tarefa para contribuidores: https://github.com/Videirafoo/Videirafoo/issues/8

Documentação:

- [`QUALITY.md`](../../QUALITY.md)
- [`FEEDBACK.md`](../../FEEDBACK.md)
- [`COMMUNITY.md`](../../COMMUNITY.md)
- [`CONTRIBUTING.md`](../../CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](../../CODE_OF_CONDUCT.md)
- [`SECURITY.md`](../../SECURITY.md)

## GitHub API e autenticação

Repositórios públicos podem ser consultados sem token, respeitando os limites públicos da API.

Opcionalmente:

```powershell
$env:GITHUB_TOKEN="SEU_TOKEN"
```

Tokens e chaves nunca devem ser commitados.

## Limitações atuais

Ainda não fazem parte do MVP:

- extração confiável de cobertura de testes de **qualquer repositório externo** analisado;
- análise automática de vulnerabilidades de **repositórios externos**;
- persistência da Matriz em banco de dados;
- contas de usuário;
- histórico persistente das análises executadas pelo produto;
- telemetria própria de uso além dos logs da plataforma;
- validação ativa de URLs externas do README;
- certificação automática de conhecimento pessoal.

A cobertura e a auditoria descritas em `QUALITY.md` medem **o próprio GitHub Student Dashboard**.

A Matriz mede **evidências públicas** e não substitui prova prática, avaliação acadêmica, revisão humana ou entrevista técnica.

Qualquer validação futura de URLs externas deve aplicar allowlist, limites, timeout e proteção contra SSRF.

## Próximas entregas

1. aumentar cobertura útil de `engine.py` — baseline atual **82,1%**;
2. aumentar cobertura útil de `readme_quality.py` — baseline atual **86,9%**;
3. aumentar cobertura útil de `web.py` — baseline atual **87,2%**;
4. revisar somente branches úteis da `competency_matrix.py` — baseline atual **89,5%**;
5. manter o gate global de **90%** sem perseguir 100% por aparência;
6. coletar feedback real de estudantes e corrigir pontos encontrados em uso público;
7. acompanhar o PR externo #8150 e alterar sua evidência para aceita apenas se houver merge público.

## Regra de contribuição

Este projeto é educacional e deve permanecer compreensível para estudantes.

Toda mudança deve:

- ser pequena e explicável;
- ter testes quando alterar comportamento;
- preservar checks reproduzíveis;
- não inventar evidências;
- documentar novas regras;
- tratar conteúdo externo como não confiável;
- respeitar limites e políticas das APIs utilizadas.
