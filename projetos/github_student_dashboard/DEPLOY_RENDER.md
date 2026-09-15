# Deploy público no Render

Este guia publica o **GitHub Student Dashboard** como serviço web Python usando Gunicorn.

## Repositório

```text
https://github.com/Videirafoo/Videirafoo
```

## Configuração do serviço

Use estes valores no Render:

```text
Runtime: Python
Branch: main
Build Command:
python -m pip install -r projetos/github_student_dashboard/requirements.txt

Start Command:
gunicorn -b 0.0.0.0:$PORT projetos.github_student_dashboard.web:app
```

## Variáveis de ambiente

Nenhuma variável é obrigatória para o modo básico.

### GitHub API

Sem `GITHUB_TOKEN`, o Dashboard funciona com o limite público da API do GitHub.

Para uso público com maior margem de requisições, configure no Render:

```text
GITHUB_TOKEN=<token configurado diretamente no painel do Render>
```

Nunca grave o token no código, README, commit ou arquivo versionado.

### IA explicativa

A IA externa é opcional. Sem chave, `/explicar` usa o modo local transparente.

Se quiser ativar um provedor compatível com a implementação atual, configure diretamente no ambiente do serviço:

```text
OPENAI_API_KEY=<chave configurada no Render>
OPENAI_MODEL=<modelo escolhido>
```

Nunca publique a chave em screenshots, logs ou arquivos do repositório.

## Smoke tests após o deploy

Depois que o Render fornecer a URL pública, validar:

```text
/
/readme
/comparar
/historico
/explicar
/api/analisar?repo=Videirafoo/Videirafoo
/api/perfil?usuario=Videirafoo
```

Critérios mínimos:

- página inicial responde HTTP 200;
- análise de `Videirafoo/Videirafoo` retorna relatório;
- CI real é exibida quando a GitHub API permitir;
- `/readme` analisa o README de perfil;
- `/comparar` compara dois repositórios diferentes;
- `/historico` reconstrói commits reais;
- `/explicar` funciona mesmo sem IA externa;
- nenhum segredo aparece em resposta, HTML ou logs.

## Servidor de desenvolvimento x produção

Localmente, para estudo:

```powershell
python -m projetos.github_student_dashboard.web
```

Em produção, não use o servidor de desenvolvimento do Flask. O Render deve iniciar o app com Gunicorn:

```text
gunicorn -b 0.0.0.0:$PORT projetos.github_student_dashboard.web:app
```

## Auto deploy

Com auto deploy habilitado, novos commits na branch `main` podem gerar uma nova implantação automaticamente.

Antes de considerar uma versão pronta, confirme:

1. GitHub Actions verde;
2. deploy concluído;
3. smoke tests públicos;
4. nenhum segredo exposto;
5. comportamento público coerente com o ambiente local.
