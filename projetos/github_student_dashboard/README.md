# GitHub Student Dashboard — MVP

Projeto público principal da trajetória educacional do GitHub `Videirafoo`.

## Missão

Ajudar estudantes a entenderem **como melhorar seus repositórios no GitHub** usando checks objetivos, evidências claras e orientação educacional.

O projeto nasce depois da trilha Python e dos 10 mini sistemas, reaproveitando o princípio adotado durante todo o percurso:

> **Automatizar deterministicamente o que pode ser provado; usar IA para explicar, orientar e revisar onde existe ambiguidade.**

## Estado atual

O MVP já possui:

- entrada por `usuario/repositorio` ou URL do GitHub;
- cliente para a API pública do GitHub;
- leitura de metadados do repositório;
- leitura da árvore de arquivos da branch padrão;
- leitura de linguagens reportadas pelo GitHub;
- checks determinísticos;
- score reproduzível;
- evidências;
- recomendações objetivas;
- CLI;
- endpoint `GET /api/analisar`;
- interface web responsiva;
- testes da engine;
- testes da interface web;
- CI própria.

## Checks do MVP

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

A pontuação não mede qualidade absoluta do software. Ela representa apenas o conjunto de checks explícitos desta versão.

## Arquitetura atual

```text
github_student_dashboard/
├── __init__.py
├── github_client.py
├── engine.py
├── cli.py
├── web.py
├── requirements.txt
├── templates/
│   └── index.html
├── test_engine.py
├── test_web.py
└── README.md
```

### `github_client.py`

Responsável pela comunicação com a GitHub API.

### `engine.py`

Responsável por:

- normalizar a referência do repositório;
- transformar respostas da API em snapshot;
- executar checks;
- calcular score;
- produzir evidências;
- gerar recomendações.

### `cli.py`

Interface para uso pelo terminal.

### `web.py`

Expõe a interface web e o endpoint JSON sem misturar regras de análise com apresentação.

## Importante: execute na raiz do repositório

Os comandos abaixo **não funcionam a partir de `C:\Windows\System32` nem diretamente de `C:\Users\Usuario`** se o repositório ainda não estiver clonado ou se o terminal não estiver dentro dele.

O Python precisa enxergar a pasta `projetos/`, portanto o terminal deve estar na raiz local de `Videirafoo/Videirafoo`.

## Windows — início rápido com PowerShell

PowerShell, Prompt de Comando e terminal integrado do VS Code funcionam. Para iniciantes no Windows, recomendamos **PowerShell** ou o **terminal do VS Code**.

### Primeira vez

```powershell
cd $HOME
git clone https://github.com/Videirafoo/Videirafoo.git
cd .\Videirafoo
python -m pip install -r .\projetos\github_student_dashboard\requirements.txt
python -m projetos.github_student_dashboard.web
```

Depois abra no navegador:

```text
http://127.0.0.1:5000
```

### Se o repositório já estiver clonado

Entre na pasta onde ele foi salvo. Exemplo:

```powershell
cd $HOME\Videirafoo
git pull
python -m pip install -r .\projetos\github_student_dashboard\requirements.txt
python -m projetos.github_student_dashboard.web
```

Para confirmar que está na pasta correta:

```powershell
Get-Location
Get-ChildItem
```

A listagem deve mostrar pastas/arquivos do repositório, incluindo `projetos`.

## Instalação — macOS/Linux ou terminal já posicionado na raiz

```bash
python -m pip install -r projetos/github_student_dashboard/requirements.txt
```

## Usar pelo terminal

Na raiz do repositório:

```bash
python -m projetos.github_student_dashboard.cli Videirafoo/Videirafoo
```

Relatório completo em JSON:

```bash
python -m projetos.github_student_dashboard.cli Videirafoo/Videirafoo --json
```

Também é possível informar uma URL:

```bash
python -m projetos.github_student_dashboard.cli https://github.com/Videirafoo/Videirafoo
```

## Executar a interface web

```bash
python -m projetos.github_student_dashboard.web
```

O Flask inicia localmente em `http://127.0.0.1:5000` por padrão.

## Endpoint de análise

```http
GET /api/analisar?repo=Videirafoo/Videirafoo
```

A resposta contém score, checks, evidências e recomendações.

## Erros comuns

### `No such file or directory: projetos/.../requirements.txt`

Causa: terminal aberto fora da raiz do repositório.

Correção: entre primeiro na pasta `Videirafoo` clonada.

### `ModuleNotFoundError: No module named 'projetos'`

Causa: o comando `python -m projetos...` foi executado fora da raiz do repositório.

Correção:

```powershell
cd $HOME\Videirafoo
python -m projetos.github_student_dashboard.web
```

## GitHub API e autenticação

O MVP pode consultar repositórios públicos sem token, respeitando os limites da API pública.

Opcionalmente, a variável de ambiente abaixo pode ser usada:

```bash
GITHUB_TOKEN=seu_token
```

O token não deve ser commitado no repositório.

## Exemplo conceitual de resultado

```json
{
  "repositorio": "Videirafoo/exemplo",
  "score": 70,
  "checks": {
    "readme": true,
    "descricao": true,
    "licenca": false,
    "gitignore": true,
    "topics": false,
    "ci": true,
    "testes": true,
    "dependencias": true
  }
}
```

## Evidência antes de recomendação

O dashboard não deve afirmar algo sem antes conseguir mostrar a evidência usada.

Exemplo:

```text
Observado: topics está vazio nos metadados retornados pela GitHub API.
Impacto: o projeto perde contexto e descoberta dentro do GitHub.
Ação: adicionar topics relacionados à linguagem, domínio e finalidade do projeto.
```

## Limitações atuais

Ainda não existe nesta versão:

- análise do perfil inteiro;
- comparação entre repositórios;
- evidência detalhada individual para cada recomendação;
- qualidade interna do README;
- status real da última CI;
- cobertura de testes;
- verificação de links;
- segurança de dependências;
- camada de IA explicativa;
- banco de dados;
- histórico de análises;
- deploy público.

## Próximas entregas

1. análise do perfil completo do estudante;
2. evidências detalhadas por check;
3. melhorar detecção de testes por stack;
4. verificar status real da CI;
5. analisar qualidade mínima do README;
6. comparação entre repositórios;
7. histórico de análises;
8. camada de IA somente para explicação e priorização;
9. deploy público;
10. coletar feedback de usuários e evoluir os checks.

## Regra de contribuição

Este projeto é educacional e deverá permanecer compreensível para estudantes.

Toda mudança deve:

- ser pequena e explicável;
- ter testes quando alterar comportamento;
- preservar checks reproduzíveis;
- não inventar evidências;
- documentar novas regras;
- respeitar limites e políticas da GitHub API.
