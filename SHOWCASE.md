# GitHub Student Dashboard — Showcase

Este documento reúne, **dentro do próprio GitHub**, o que já está funcionando no projeto público principal do `Videirafoo`.

> Objetivo: permitir que estudantes, recrutadores, mantenedores open source e pessoas da comunidade entendam rapidamente o produto, como ele funciona e quais resultados ele já consegue comprovar.

## Status público

<p align="center">
  <img src="./docs/github-student-dashboard-status.svg" alt="Status público do GitHub Student Dashboard" width="960" />
</p>

- Produção: https://github-student-dashboard-videirafoo.onrender.com
- Laboratório: https://github-student-dashboard-videirafoo.onrender.com/laboratorio
- Healthcheck: https://github-student-dashboard-videirafoo.onrender.com/healthz
- CI: [GitHub Student Dashboard CI](https://github.com/Videirafoo/Videirafoo/actions/workflows/student-dashboard.yml)
- Qualidade verificável: [`QUALITY.md`](./QUALITY.md)
- Changelog: [`projetos/github_student_dashboard/CHANGELOG.md`](./projetos/github_student_dashboard/CHANGELOG.md)
- Feedback: https://github.com/Videirafoo/Videirafoo/issues/new?template=dashboard-feedback.yml
- Comunidade: [`COMMUNITY.md`](./COMMUNITY.md)
- Primeira tarefa aberta para contribuidores: [Issue #8](https://github.com/Videirafoo/Videirafoo/issues/8)
- Primeiro PR externo verificável: [fork-commit-merge#8150](https://github.com/fork-commit-merge/fork-commit-merge/pull/8150) — **aberto e mergeável, aguardando mantenedor**

## Qualidade medida, não declarada

Execução de referência: [CI #108](https://github.com/Videirafoo/Videirafoo/actions/runs/34995444039)

| Evidência | Resultado |
|---|---:|
| Testes | **147 passando** |
| Cobertura total | **92,9%** |
| Gate de regressão | **90%** |
| `lab_api.py` | **99,0%** |
| `lab_business.py` | **98,5%** |
| `github_client.py` | **97,5%** |
| `ai_explainer.py` | **95,7%** |
| `lab_systems.py` | **94,8%** |
| `lab_web.py` | **94,3%** |
| Auditoria de dependências | **nenhuma vulnerabilidade conhecida reportada pelo `pip-audit` nessa execução** |

A cobertura começou em **73,3% com 95 testes**. Os testes foram ampliados a partir das lacunas reais encontradas: **81,9%/118**, depois **89,0%/135** e finalmente **92,9%/147**. A CI publica `coverage.txt`, `coverage.json` e `pip-audit.txt` como artefatos verificáveis.

Artefato da execução #108: [dashboard-quality-evidence](https://github.com/Videirafoo/Videirafoo/actions/runs/34995444039/artifacts/10407506784)

> O resultado do `pip-audit` é uma evidência daquela execução, não uma afirmação de segurança absoluta.

## O que o produto já faz

| Área | Entrega atual |
|---|---|
| Repositório | score determinístico + 8 checks verificáveis |
| Perfil | cobertura de descrição, topics e licença; stars, forks e linguagens |
| CI | consulta a execução real mais recente do GitHub Actions |
| README | análise estrutural + verificação segura de links internos do próprio repositório |
| Comparação | dois repositórios lado a lado sem declarar vencedor subjetivo |
| Histórico | reconstrução por commit de README, `.gitignore`, CI, testes e dependências |
| Testes | detecção por padrões comuns de Python, JS/TS, Go, Dart/Flutter, Ruby, Java/Kotlin, C#, PHP e diretórios convencionais |
| Explicação | modo local transparente + IA externa opcional |
| Laboratório | **10 mini sistemas utilizáveis, com regras centrais executadas pelo Python real** |
| Qualidade interna | **147 testes, 92,9% de cobertura, gate 90% e auditoria informativa** |
| Produção | Flask + Gunicorn no Render |
| Descoberta | `robots.txt`, `sitemap.xml` e healthcheck |
| Comunidade | feedback estruturado, formulários de bug/melhoria, segurança, contribuição, código de conduta e `good first issue` |

## Laboratório — interface + backend + código original

A coleção educacional não é apenas uma lista de títulos nem uma coleção de mockups. Os 10 mini sistemas podem ser experimentados em:

https://github-student-dashboard-videirafoo.onrender.com/laboratorio

A arquitetura didática é:

```text
navegador
   ↓
interface do playground
   ↓
endpoint Flask do laboratório
   ↓
funções Python originais de conteudos/mini_sistemas
   ↓
resultado validado
   ↓
estado isolado no navegador do visitante
```

| # | Sistema | O que é executado pelo Python real |
|---:|---|---|
| 01 | Agenda de Contatos | cadastro, duplicidade e exclusão |
| 02 | Lista de Tarefas | criação, conclusão, reabertura e exclusão |
| 03 | Cadastro de Alunos | notas, média e situação acadêmica |
| 04 | Controle de Estoque | cadastro, quantidade e exclusão |
| 05 | Sistema de Biblioteca | livros, usuários, empréstimos e devoluções |
| 06 | Caixa de Mercado | catálogo, carrinho, estoque, desconto e fechamento |
| 07 | Controle Financeiro | receitas, despesas, exclusões e totais |
| 08 | Gerenciador de Hábitos | criação, conclusão diária, exclusão e progresso |
| 09 | API de Tarefas | GET, POST, PATCH e DELETE via Flask real |
| 10 | Projeto Integrado | repositório temporário + `analisar_repositorio()` original |

O laboratório também inclui **busca binária visual** como bônus.

Os dados didáticos permanecem no navegador quando isso é suficiente. O backend público recebe apenas o estado necessário para executar a operação; isso evita misturar dados de visitantes e mantém a relação entre **comportamento → código → teste** clara para quem está aprendendo.

A regra de ensino é:

`usar` → `prever` → `quebrar uma regra` → `abrir código` → `abrir testes` → `alterar` → `validar`

## Resultados reais já verificados

Os exemplos abaixo foram observados usando o próprio `Videirafoo` como caso de teste.

### `Videirafoo/Videirafoo`

- score observado na rodada de validação: **80/100**;
- CI real: **success**;
- README: **100% de cobertura documental, 7/7 critérios**;
- checks atendidos: README, licença, `.gitignore`, CI, testes e dependências;
- lacunas objetivas observadas naquele momento: descrição do repositório e topics.

> Esses valores podem mudar conforme os metadados e o código do repositório evoluem.

### Comparação real usada durante o desenvolvimento

`Videirafoo/Videirafoo` vs `Videirafoo/Lista-01-segundo-periodo`

| Evidência | Perfil principal | Lista 01 |
|---|---:|---:|
| Score observado | 80/100 | 50/100 |
| README | 100% | 55,6% |
| CI real | success | success |
| Dependências | OK | falta |
| Licença | OK | falta |
| Testes | OK | falta |
| Descrição | falta | OK |
| Topics | falta | falta |

A comparação não declara um vencedor geral. Ela mostra somente diferenças verificáveis.

## Histórico de evolução

O histórico não tenta reconstruir metadados que o Git não preserva com segurança. Ele acompanha somente sinais realmente versionados:

- README;
- `.gitignore`;
- workflow de CI;
- testes;
- dependências.

## Qualidade do README e links internos

A análise de README verifica caminhos internos Markdown/HTML contra a árvore do repositório. Anchors locais e URLs externas não são transformados em requisições arbitrárias.

## IA explicativa

A camada explicativa segue uma restrição arquitetural deliberada:

```text
GitHub API
   ↓
checks determinísticos
   ↓
evidências + score + CI real
   ↓
explicação pedagógica local ou por IA
```

A IA **não calcula o score**, **não decide se um check passou** e **não substitui evidências**. Sem `OPENAI_API_KEY`, o produto continua utilizável em modo local transparente.

## Teste em menos de 3 minutos

1. Abra https://github-student-dashboard-videirafoo.onrender.com
2. Em **Analisar repositório**, use `Videirafoo/Videirafoo`.
3. Abra **Qualidade do README** e analise o mesmo repositório.
4. Em **Comparar**, use `Videirafoo/Videirafoo` e `Videirafoo/Lista-01-segundo-periodo`.
5. Em **Histórico**, analise 5 commits.
6. Em **Explicação**, confira o modo local e as prioridades detectadas.
7. Abra **Laboratório** e use alguns dos 10 mini sistemas.
8. Em cada card, provoque uma validação e depois abra o código Python e o teste correspondente.
9. Abra [`QUALITY.md`](./QUALITY.md) e confira como a qualidade interna é medida.
10. Se algo ficar confuso, envie feedback pelo formulário público.

## Endpoints públicos principais

```http
GET /healthz
GET /api/analisar?repo=Videirafoo/Videirafoo
GET /api/perfil?usuario=Videirafoo
GET /api/readme?repo=Videirafoo/Videirafoo
GET /api/comparar?a=Videirafoo/Videirafoo&b=Videirafoo/Lista-01-segundo-periodo
GET /api/historico?repo=Videirafoo/Videirafoo&limite=5
GET /api/explicar?repo=Videirafoo/Videirafoo

POST   /api/laboratorio/agenda
POST   /api/laboratorio/lista-tarefas
POST   /api/laboratorio/aluno-media
POST   /api/laboratorio/estoque
POST   /api/laboratorio/biblioteca
POST   /api/laboratorio/caixa
POST   /api/laboratorio/financeiro
POST   /api/laboratorio/habitos
GET    /api/laboratorio/tarefas
POST   /api/laboratorio/tarefas
PATCH  /api/laboratorio/tarefas
DELETE /api/laboratorio/tarefas
POST   /api/laboratorio/analisar
```

## Open source externo

A primeira contribuição externa verificável da trajetória já foi enviada:

- Issue alvo: [fork-commit-merge#8017](https://github.com/fork-commit-merge/fork-commit-merge/issues/8017)
- Pull Request: [fork-commit-merge#8150](https://github.com/fork-commit-merge/fork-commit-merge/pull/8150)
- Estado verificado nesta etapa: **aberto, mergeável e sem nova revisão/comentário do mantenedor**.

O perfil diferencia contribuição enviada de contribuição aceita: o PR só será registrado como **merged** depois que o repositório upstream fizer o merge público.

## Comece a contribuir

Se você está começando em open source, a [Issue #8](https://github.com/Videirafoo/Videirafoo/issues/8) foi escrita especificamente como uma primeira contribuição pequena e verificável.

O repositório também possui:

- [`CONTRIBUTING.md`](./CONTRIBUTING.md);
- [`COMMUNITY.md`](./COMMUNITY.md);
- [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md);
- [`SECURITY.md`](./SECURITY.md);
- [formulário de bug](https://github.com/Videirafoo/Videirafoo/issues/new?template=bug-report.yml);
- [formulário de melhoria](https://github.com/Videirafoo/Videirafoo/issues/new?template=feature-request.yml);
- [template de Pull Request](./.github/PULL_REQUEST_TEMPLATE.md).

## Por que este projeto existe

O Dashboard não foi criado para produzir uma nota decorativa. Ele faz parte de uma trajetória educacional maior:

**fundamentos → conteúdo para iniciantes → mini sistemas → produto público → qualidade mensurável → feedback → open source externo → comunidade → reconhecimento**.

O objetivo é transformar boas práticas de GitHub em algo que uma pessoa iniciante consiga **usar, ver, entender, testar e aplicar**.

## Próximo estágio

- aumentar cobertura útil de `engine.py`, `web.py` e `readme_quality.py` onde houver branches relevantes;
- coletar e priorizar feedback real de estudantes;
- acompanhar a revisão e o merge do PR externo #8150 sem interferir enquanto não houver solicitação do mantenedor;
- histórico persistente das análises quando houver motivo de produto para armazená-las;
- incorporar melhorias vindas de uso real.
