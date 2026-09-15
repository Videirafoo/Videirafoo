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
- comparação entre dois repositórios;
- histórico versionado de evolução por commit;
- camada explicativa local;
- IA explicativa opcional, sem alterar o diagnóstico;
- CLI;
- interface web;
- endpoints JSON;
- testes automatizados;
- CI própria;
- deploy público com Gunicorn no Render;
- `healthz`, `robots.txt` e `sitemap.xml`;
- formulário estruturado de feedback no GitHub.

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
| `/readme` | qualidade documental do README |
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
├── cli.py
├── web.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── readme.html
│   ├── comparar.html
│   ├── historico.html
│   └── explicar.html
├── test_*.py
└── README.md
```

### Separação de responsabilidades

- `github_client.py`: comunicação com a GitHub API;
- `engine.py`: checks, score, evidências e CI real;
- `readme_quality.py`: critérios documentais verificáveis;
- `comparison.py`: diferenças objetivas entre dois repositórios;
- `history.py`: reconstrução de sinais versionados por commit;
- `ai_explainer.py`: explicação pedagógica a partir do relatório pronto;
- `web.py`: rotas web, JSON, saúde e arquivos de descoberta.

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

## Qualidade do README

README de perfil e README de projeto comum usam critérios diferentes.

A cobertura documental mede presença de elementos verificáveis; não é uma nota subjetiva de estilo ou escrita.

## Evidência antes de recomendação

O Dashboard deve conseguir responder:

```text
Observado: o que foi encontrado.
Impacto: por que isso importa.
Ação: qual melhoria concreta pode ser feita.
```

A IA recebe esse material somente depois.

## Feedback real de estudantes

Formulário estruturado:

https://github.com/Videirafoo/Videirafoo/issues/new?template=dashboard-feedback.yml

Documentação:

- [`FEEDBACK.md`](../../FEEDBACK.md)
- [`COMMUNITY.md`](../../COMMUNITY.md)

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

- cobertura real de testes por ferramenta específica;
- verificação automática de links quebrados;
- análise de vulnerabilidades/dependências;
- persistência em banco de dados;
- contas de usuário;
- histórico persistente das análises executadas pelo produto;
- telemetria própria de uso além dos logs da plataforma.

## Próximas entregas

1. coletar feedback real de estudantes;
2. corrigir pontos encontrados no uso público;
3. melhorar checks com base em casos reais;
4. consolidar acessibilidade e navegação;
5. iniciar contribuições open source externas progressivas;
6. documentar PRs externos aceitos somente quando existirem publicamente.

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
