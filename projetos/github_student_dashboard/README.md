# GitHub Student Dashboard — MVP

Projeto público principal da trajetória educacional do GitHub `Videirafoo`.

## Missão

Ajudar estudantes a entenderem **como melhorar seus repositórios no GitHub** usando checks objetivos, evidências claras e orientação educacional.

O projeto nasce depois da trilha Python e dos 10 mini sistemas, reaproveitando o princípio adotado durante todo o percurso:

> **Automatizar deterministicamente o que pode ser provado; usar IA para explicar, orientar e revisar onde existe ambiguidade.**

## Estado atual

Primeiro núcleo funcional implementado:

- recebe `usuario/repositorio` ou URL do GitHub;
- consulta a API pública do GitHub;
- lê metadados do repositório;
- lê árvore de arquivos da branch padrão;
- lê linguagens reportadas pelo GitHub;
- executa checks determinísticos;
- calcula score reproduzível;
- gera evidências;
- gera recomendações objetivas;
- possui CLI;
- possui testes automatizados;
- possui CI própria.

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
├── test_engine.py
└── README.md
```

### `github_client.py`

Responsável por comunicação com a GitHub API.

### `engine.py`

Responsável por:

- normalizar a referência do repositório;
- transformar respostas da API em snapshot;
- executar checks;
- calcular score;
- produzir evidências;
- gerar recomendações.

### `cli.py`

Interface inicial para uso pelo terminal.

## Como executar

Na raiz do repositório `Videirafoo/Videirafoo`:

```bash
python -m projetos.github_student_dashboard.cli Videirafoo/Videirafoo
```

Para receber o relatório completo em JSON:

```bash
python -m projetos.github_student_dashboard.cli Videirafoo/Videirafoo --json
```

Também é possível informar uma URL:

```bash
python -m projetos.github_student_dashboard.cli https://github.com/Videirafoo/Videirafoo
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

- interface web;
- análise de perfil inteiro;
- comparação entre repositórios;
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

1. interface web simples;
2. endpoint de análise;
3. análise do perfil completo do estudante;
4. evidências detalhadas por check;
5. melhorar detecção de testes por stack;
6. verificar status real da CI;
7. analisar qualidade mínima do README;
8. histórico de análises;
9. camada de IA somente para explicação e priorização;
10. deploy público e feedback de usuários.

## Regra de contribuição

Este projeto é educacional e deverá permanecer compreensível para estudantes.

Toda mudança deve:

- ser pequena e explicável;
- ter testes quando alterar comportamento;
- preservar checks reproduzíveis;
- não inventar evidências;
- documentar novas regras;
- respeitar limites e políticas da GitHub API.
