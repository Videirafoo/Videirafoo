# GitHub Student Dashboard — MVP

Projeto público principal da trajetória educacional do GitHub `Videirafoo`.

## Missão

Ajudar estudantes a entenderem **como melhorar seus repositórios no GitHub** usando checks objetivos, evidências claras e orientação educacional.

> **Automatizar deterministicamente o que pode ser provado; usar IA para explicar, orientar e revisar onde existe ambiguidade.**

## Acesso público

Produção:

https://github-student-dashboard-videirafoo.onrender.com

Saúde do serviço:

```text
GET /healthz
```

Descoberta:

```text
GET /robots.txt
GET /sitemap.xml
```

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
- CLI;
- interface web;
- endpoints JSON;
- laboratório com 10 mini sistemas executando regras Python reais;
- testes automatizados;
- cobertura interna real com `coverage.py` e branches;
- gate mínimo de cobertura;
- auditoria informativa das dependências de produção com `pip-audit`;
- artefatos de qualidade anexados à CI;
- deploy público com Gunicorn no Render;
- `healthz`, `robots.txt` e `sitemap.xml`;
- formulário estruturado de feedback no GitHub;
- formulários públicos de bug e sugestão de melhoria;
- `good first issue` para contribuições de iniciantes;
- template de Pull Request.

## Qualidade interna verificada

Execução de referência: [GitHub Student Dashboard CI #102](https://github.com/Videirafoo/Videirafoo/actions/runs/34993966082)

- **118 testes automatizados passando**;
- **81,9% de cobertura total**;
- `cli.py`: **100,0%**;
- `github_client.py`: **97,5%**;
- `ai_explainer.py`: **95,7%**;
- gate de regressão configurado em **80%**;
- `pip-audit`: nenhuma vulnerabilidade conhecida reportada nas dependências resolvidas naquela execução.

A CI publica `coverage.txt`, `coverage.json` e `pip-audit.txt` no artefato `dashboard-quality-evidence`.

Os números são evidências de uma execução específica, não garantias permanentes. Consulte [`QUALITY.md`](../../QUALITY.md) para metodologia, limites e próximos alvos.

## Regra central

A IA **não calcula o score** e **não decide se um check passou**.

O fluxo é:

```text
GitHub API
   ↓
checks determinísticos
   ↓
evidências + score + CI real
   ↓
explicação pedagógica
```

Se a IA estiver desativada ou indisponível, o Dashboard continua funcionando e usa um modo explicativo local transparente.

## Checks atuais do repositório

| Check | Peso |
| --- | ---: |
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
| --- | --- |
| `/` | análise de repositório e perfil |
| `/laboratorio` | 10 mini sistemas educacionais ligados ao backend Python |
| `/readme` | qualidade documental do README e links internos |
| `/comparar` | comparação objetiva entre repositórios |
| `/historico` | evolução de sinais versionados por commit |
| `/explicar` | explicação pedagógica local ou por IA |

## Endpoints

```http
GET /healthz
GET /api/analisar?repo=Videirafoo/Videirafoo
GET /api/perfil?usuario=Videirafoo
GET /api/readme?repo=Videirafoo/Videirafoo
GET /api/comparar?a=Videirafoo/Videirafoo&b=Videirafoo/Lista-01-segundo-periodo
GET /api/historico?repo=Videirafoo/Videirafoo&limite=5
GET /api/explicar?repo=Videirafoo/Videirafoo
```

Rotas do laboratório também estão disponíveis sob `/api/laboratorio/*` e executam as regras dos mini sistemas Python reais.

## Arquitetura

```text
github_student_dashboard/
├── __init__.py
├── github_client.py
├── engine.py
├── readme_quality.py
├── comparison.py
├── history.py
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

- `github_client.py`: comunicação com a GitHub API;
- `engine.py`: checks, score, evidências, CI real e detecção de testes;
- `readme_quality.py`: critérios documentais e validação de links internos;
- `comparison.py`: diferenças objetivas entre dois repositórios;
- `history.py`: reconstrução de sinais versionados por commit;
- `ai_explainer.py`: explicação pedagógica a partir do relatório pronto;
- `lab_*.py`: adaptação segura dos mini sistemas para o laboratório público;
- `web.py`: rotas web, JSON, saúde e arquivos de descoberta.

## CI e qualidade

A CI executa, em ordem:

1. checkout do código;
2. Python 3.12;
3. instalação das dependências de validação;
4. `compileall` do projeto;
5. validação de sintaxe dos JavaScripts do laboratório;
6. **118+ testes** sob `coverage.py`;
7. gate mínimo de cobertura em **80%**;
8. auditoria informativa de produção com `pip-audit`;
9. upload das evidências de cobertura e auditoria.

As ferramentas de desenvolvimento ficam em `requirements-dev.txt`; `requirements.txt` continua reservado ao runtime de produção.

## Detecção de testes por stack

A detecção atual reconhece padrões frequentes sem depender apenas de um nome genérico de pasta.

Exemplos suportados:

- Python: `test_*.py`, `*_test.py`;
- JavaScript/TypeScript: `*.test.*`, `*.spec.*`, incluindo JSX/TSX, MJS e CJS;
- Go: `*_test.go`;
- Dart/Flutter: `*_test.dart`;
- Ruby: `*_spec.rb`, `*_test.rb`;
- Java/Kotlin: `*Test.java`, `*Tests.java`, `*Test.kt`, `*Tests.kt`;
- C#: `*Test.cs`, `*Tests.cs`;
- PHP: `*Test.php`, `*Tests.php`;
- diretórios convencionais: `test`, `tests`, `__tests__`, `spec`, `specs`.

Há teste de regressão para evitar falsos positivos simples como `contest.py` e `latest.ts`.

## Qualidade do README

README de perfil e README de projeto comum usam critérios diferentes.

A cobertura documental mede presença de elementos verificáveis; não é uma nota subjetiva de estilo ou escrita.

Além da estrutura documental, a análise remota verifica links internos do README contra a árvore do próprio repositório.

A verificação:

- valida arquivos e diretórios internos;
- ignora anchors locais;
- não consulta URLs externas arbitrárias;
- não inventa link quebrado quando a árvore do repositório não pode ser confirmada;
- mostra caminhos internos quebrados diretamente na interface `/readme`.

## Windows — início rápido com PowerShell

Execute sempre a partir da raiz local do repositório.

### Primeira vez

```powershell
cd $HOME
git clone https://github.com/Videirafoo/Videirafoo.git
cd .\Videirafoo
python -m pip install -r .\projetos\github_student_dashboard\requirements.txt
python -m projetos.github_student_dashboard.web
```

Abra:

```text
http://127.0.0.1:5000
```

### Atualizar uma cópia já clonada

Com o servidor parado por **Ctrl+C no teclado**:

```powershell
cd $HOME\Videirafoo
git pull
python -m pip install -r .\projetos\github_student_dashboard\requirements.txt
python -m projetos.github_student_dashboard.web
```

### Executar a validação de qualidade localmente

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

O deploy atual está no Render e usa a branch `main`.

## IA explicativa opcional

A página `/explicar` funciona em dois modos.

### Modo local

É o padrão quando `OPENAI_API_KEY` não existe.

- nenhuma chamada externa é feita;
- o score permanece determinístico;
- a explicação reorganiza somente fatos medidos pelo Dashboard;
- a interface informa claramente que não usou IA externa.

### Modo IA

Para habilitar temporariamente no PowerShell atual:

```powershell
$env:OPENAI_API_KEY="SUA_CHAVE"
$env:OPENAI_MODEL="gpt-5.6-luna"
python -m projetos.github_student_dashboard.web
```

A integração usa a Responses API. O modelo pode ser alterado por `OPENAI_MODEL` sem modificar o código.

A chave **não deve** ser colocada em README, código, commit, `.env` versionado ou screenshot público.

Para remover a variável da sessão atual:

```powershell
Remove-Item Env:OPENAI_API_KEY
```

### Limites da IA

- score, checks e CI são fatos imutáveis para a explicação;
- dados vindos do GitHub são conteúdo não confiável, não instruções;
- no máximo três prioridades devem ser sugeridas;
- fatos não comprovados devem ser identificados como não verificados;
- falha da API de IA não derruba o Dashboard: há fallback local.

## Histórico de evolução

O histórico reconstrói por commit somente sinais que realmente ficam versionados no Git:

- README;
- `.gitignore`;
- workflows de CI;
- testes;
- arquivos de dependências.

Descrição, topics e outros metadados atuais do GitHub não são retroativamente inventados.

## Evidência antes de recomendação

O Dashboard deve conseguir responder:

```text
Observado: o que foi encontrado.
Impacto: por que isso importa.
Ação: qual melhoria concreta pode ser feita.
```

A IA recebe esse material somente depois.

## Feedback e comunidade

### Feedback do Dashboard

https://github.com/Videirafoo/Videirafoo/issues/new?template=dashboard-feedback.yml

### Relatar bug

https://github.com/Videirafoo/Videirafoo/issues/new?template=bug-report.yml

### Sugerir melhoria

https://github.com/Videirafoo/Videirafoo/issues/new?template=feature-request.yml

### Primeira tarefa para contribuidores

https://github.com/Videirafoo/Videirafoo/issues/8

Documentação:

- [`QUALITY.md`](../../QUALITY.md)
- [`FEEDBACK.md`](../../FEEDBACK.md)
- [`COMMUNITY.md`](../../COMMUNITY.md)
- [`CONTRIBUTING.md`](../../CONTRIBUTING.md)
- [`CODE_OF_CONDUCT.md`](../../CODE_OF_CONDUCT.md)
- [`SECURITY.md`](../../SECURITY.md)

A prioridade de correção é:

1. erro que impede uso;
2. diagnóstico incorreto ou sem evidência;
3. ponto que confunde iniciante;
4. acessibilidade e clareza;
5. melhoria de fluxo;
6. recurso novo.

## GitHub API e autenticação

Repositórios públicos podem ser consultados sem token, respeitando os limites públicos da API.

Opcionalmente:

```powershell
$env:GITHUB_TOKEN="SEU_TOKEN"
```

Tokens e chaves nunca devem ser commitados.

## Limitações atuais

Ainda não fazem parte do MVP:

- extração confiável de **cobertura de testes de qualquer repositório externo analisado**;
- análise automática de vulnerabilidades de **repositórios externos**;
- persistência em banco de dados;
- contas de usuário;
- histórico persistente das análises executadas pelo produto;
- telemetria própria de uso além dos logs da plataforma;
- validação ativa de URLs externas do README.

A cobertura e a auditoria descritas em `QUALITY.md` medem **o próprio GitHub Student Dashboard**, não qualquer repositório externo enviado ao produto.

A validação de URLs externas permanece fora do MVP de propósito: qualquer implementação futura deve aplicar allowlist, limites, timeout e proteção contra SSRF antes de fazer requisições externas.

## Próximas entregas

1. elevar cobertura útil de `lab_business.py`, `lab_api.py`, `lab_web.py` e `lab_systems.py`;
2. aprofundar branches de erro do engine;
3. coletar feedback real de estudantes e corrigir pontos encontrados no uso público;
4. estudar como ler cobertura de projetos externos somente quando existir evidência confiável da stack;
5. estudar análise informativa de dependências de projetos externos sem substituir scanners especializados;
6. acompanhar contribuições open source externas e registrar como aceitas somente depois de merge público.

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
