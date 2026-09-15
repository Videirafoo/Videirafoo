# Deploy público no Render

Este guia publica o **GitHub Student Dashboard** como serviço web Python usando Gunicorn.

## Repositório

```text
https://github.com/Videirafoo/Videirafoo
```

## Configuração do serviço

Estado verificado em 2026-09-15:

```text
Service: github-student-dashboard-videirafoo
Runtime: Python
Branch: main
Auto Deploy: yes
Auto Deploy Trigger: commit
Build Command:
python -m pip install -r projetos/github_student_dashboard/requirements.txt

Start Command:
gunicorn projetos.github_student_dashboard.web:app --bind 0.0.0.0:$PORT
```

URL pública:

```text
https://github-student-dashboard-videirafoo.onrender.com
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

## Fluxo normal de publicação

1. alteração entra em `main`;
2. GitHub Actions valida sintaxe, testes, cobertura e auditoria de dependências;
3. o Render detecta o novo commit e inicia promoção automática;
4. o deploy deve usar exatamente o SHA esperado;
5. depois de `live`, validar as rotas públicas.

## Smoke tests após o deploy

Validar pelo menos:

```text
/
/healthz
/trilha
/competencias
/laboratorio
/readme
/comparar
/historico
/explicar
/api/competencias
/api/analisar?repo=Videirafoo/Videirafoo
/api/perfil?usuario=Videirafoo
```

Critérios mínimos:

- página inicial responde HTTP 200;
- `/healthz` responde corretamente;
- Matriz Viva e sua API estão disponíveis;
- análise de `Videirafoo/Videirafoo` retorna relatório;
- CI real é exibida quando a GitHub API permitir;
- nenhum segredo aparece em resposta, HTML ou logs.

## Servidor de desenvolvimento x produção

Localmente, para estudo:

```powershell
python -m projetos.github_student_dashboard.web
```

Em produção, não use o servidor de desenvolvimento do Flask. O Render deve iniciar o app com Gunicorn.

## Fallback manual

O deploy manual existe apenas como recuperação quando o auto-deploy não iniciar.

Antes de disparar manualmente:

1. confirmar que não existe promoção automática em andamento;
2. confirmar o SHA atual da `main`;
3. disparar uma única promoção;
4. verificar que o deploy terminou `live` no SHA esperado;
5. executar smoke das rotas críticas.

Não disparar deploy manual quando o fluxo automático estiver funcionando, para evitar promoções duplicadas.

## Incidente de 2026-09-15

O serviço reporta `autoDeploy=yes` e `autoDeployTrigger=commit`, ligado a `Videirafoo/Videirafoo` na branch `main`. Apesar disso, commits recentes da Matriz Viva não iniciaram promoção automaticamente.

A versão `faf512a7d9a7d96fa0559cf08d088a26a29e500d` precisou ser promovida manualmente e terminou `live` no deploy `dep-dakp6u8ae00c73a0531g`.

A Issue #10 acompanha a causa e a correção definitiva. Este documento serve também como teste legítimo do gatilho: o commit desta atualização deve produzir uma promoção automática sem chamada manual ao Render.