# Changelog — GitHub Student Dashboard

Este arquivo registra mudanças relevantes do projeto de forma legível para estudantes, contribuidores e pessoas que acompanham sua evolução.

## [Unreleased]

### Matriz Viva de Competências

- criada a rota pública `/competencias` para transformar a progressão educacional em **evidências verificáveis**, sem declarar domínio pessoal automaticamente;
- adicionada API JSON `GET /api/competencias`;
- a matriz avalia **10 competências** distribuídas entre fundamentos, algoritmos, recursividade, mini sistemas, backend/API, qualidade/CI, deploy, documentação, open source e IA aplicada;
- cada competência é classificada como `forte`, `parcial`, `sem_evidencia` ou `indisponivel` conforme os artefatos públicos encontrados;
- evidências individuais usam os estados `verificada`, `parcial`, `ausente` e `indisponivel`;
- árvores públicas dos repositórios acadêmicos são consultadas para confirmar código Python versionado;
- a coleção `conteudos/mini_sistemas` é verificada para confirmar presença dos 10 sistemas e seus testes;
- o Dashboard verifica arquivos reais do backend, workflows, configuração de cobertura, documentação e componentes da camada de IA;
- a execução mais recente da `GitHub Student Dashboard CI` é consultada para diferenciar CI verde de execução ainda em andamento ou indisponível;
- o healthcheck público do Render é consultado para evidência de operação;
- o PR externo `fork-commit-merge/fork-commit-merge#8150` é consultado diretamente: **PR aberto comprova contribuição enviada, mas somente merge público transforma essa evidência em aceita**;
- respostas externas indisponíveis não são convertidas em sucesso: a matriz preserva o estado `indisponivel` ou `parcial`;
- cache de **600 segundos** reduz chamadas repetidas à API pública do GitHub;
- interface usa DOM seguro com `textContent` para renderizar evidências retornadas pela API;
- `/competencias` foi incluída no sitemap, Dashboard e navegação do Laboratório;
- JavaScript da matriz passou a ser validado pela CI;
- testes cobrem estados do PR externo, CI em andamento/ausente/indisponível, healthcheck, falha parcial da GitHub API, rotas web, API, sitemap e navegação.

### Base educacional executável

- criada a rota pública `/trilha` com **6 níveis e 18 missões práticas**;
- níveis conectam fundamentos, estruturas e algoritmos, mini sistemas, aplicações reais, Engenharia de Software e IA aplicada;
- cada missão aponta para uma evidência inspecionável: código, teste, laboratório, endpoint, documentação de qualidade ou contribuição open source;
- progresso salvo localmente no navegador, sem criar conta ou banco para o estudante;
- adicionada API JSON `GET /api/trilha` para expor a mesma estrutura de aprendizagem;
- `/trilha` incluída no sitemap público;
- Dashboard e Laboratório agora exibem atalho direto para a Trilha Educacional;
- JavaScript de progresso da trilha validado pela CI;
- testes protegem quantidade de níveis/missões, IDs únicos, URLs de evidência, renderização da página, API, sitemap e atalhos de navegação;
- `GUIA_DE_ESTUDOS.md` agora diferencia mapa conceitual de execução prática e define evidências de domínio;
- `PADRAO_DE_ENSINO.md` passa a exigir evidência de conclusão, entregável verificável e ciclo `conceito → missão → modificação → teste → evidência`;
- `REFERENCIAS_OPEN_SOURCE.md` registra os padrões educacionais absorvidos de `BEPb/Python-100-days`, `BEPb/Programmer_Competency_Matrix`, `BEPb/first-contributions` e `msitarzewski/agency-agents`, sem copiar conteúdo ou personas;
- README do perfil destaca a Trilha como recurso executável, não como projeto apenas documentado.

### Qualidade verificável

- medição real de cobertura adicionada à CI com `coverage.py` e branch coverage;
- baseline inicial observado: **95 testes / 73,3% de cobertura**;
- evolução intermediária comprovada: **118 testes / 81,9% de cobertura**;
- laboratório chegou a **147 testes / 92,9%**;
- Trilha Educacional levou a suíte a **156 testes / 92,9%**;
- execução de referência atual: [GitHub Student Dashboard CI #125](https://github.com/Videirafoo/Videirafoo/actions/runs/35004424114);
- execução #125 confirmou **177 testes passando / 92,6% de cobertura total**;
- gate de regressão permanece em **90%** e foi aprovado na execução #125;
- `competency_matrix.py`: **89,5%**;
- `github_client.py`: **97,8%**;
- `ai_explainer.py`: **95,7%**;
- `lab_api.py`: **99,0%**;
- `lab_business.py`: **98,5%**;
- `lab_systems.py`: **94,8%**;
- `lab_web.py`: **94,3%**;
- auditoria informativa de dependências de produção mantida com `pip-audit`;
- execução #125 registrou `No known vulnerabilities found` para as dependências resolvidas naquele run;
- artefato `dashboard-quality-evidence` publica `coverage.txt`, `coverage.json` e `pip-audit.txt` em cada execução;
- artefato da execução #125: https://github.com/Videirafoo/Videirafoo/actions/runs/35004424114/artifacts/10411171361;
- `ResourceWarning` identificado pela primeira medição foi corrigido nos testes de recursos estáticos;
- `actions/checkout`, `actions/setup-python` e `actions/upload-artifact` permanecem na geração v7;
- evidências, limites e metodologia ficam documentados publicamente em `QUALITY.md`.

### Próximos alvos de qualidade

A cobertura orienta a prioridade de teste. Os próximos alvos úteis são:

- `engine.py` — **82,1%**, principalmente branches de erro e casos-limite;
- `web.py` — **86,4%**, especialmente respostas de erro e fluxos alternativos;
- `readme_quality.py` — **86,9%**, com foco em parsing e links internos de borda;
- `competency_matrix.py` — **89,5%**, com foco apenas em branches residuais que tenham valor real;
- manter o gate global em **90%** sem perseguir 100% apenas por aparência.

### Melhorias

- laboratório ampliado para os **10 mini sistemas**, todos com experiência prática e links para código/testes reais;
- **os 10 mini sistemas têm regras centrais processadas pelo backend Flask usando os módulos Python reais do repositório**;
- Mini Sistema 01 — Agenda de Contatos cria, valida duplicidade e exclui contatos pelo backend Flask reutilizando as funções Python originais;
- Mini Sistema 02 — Lista de Tarefas cria, conclui, reabre e exclui tarefas pelo backend Flask reutilizando o código Python original;
- Mini Sistema 03 — Cadastro de Alunos calcula e valida notas, média e situação acadêmica pelas funções Python originais;
- Mini Sistema 04 — Controle de Estoque usa as regras Python originais para cadastro, quantidade e exclusão;
- Mini Sistema 05 — Biblioteca usa o código Python original para livros, usuários, empréstimos e devoluções;
- Mini Sistema 06 — Caixa de Mercado usa o código Python original para catálogo, carrinho, estoque, desconto e fechamento de venda;
- Mini Sistema 07 — Controle Financeiro usa o código Python original para receitas, despesas, exclusões e cálculo de totais;
- Mini Sistema 08 — Gerenciador de Hábitos usa o código Python original para criação, conclusão diária, exclusão e progresso;
- Mini Sistema 09 deixou de ser apenas uma simulação de contrato: `GET`, `POST`, `PATCH` e `DELETE` passam pelo backend Flask real;
- Mini Sistema 10 monta um repositório temporário e isolado no servidor e executa o `analisar_repositorio()` original do projeto integrado;
- o estado didático permanece no navegador sempre que possível; o servidor recebe apenas o estado necessário para executar uma operação e devolver o resultado validado;
- estados antigos da Lista de Tarefas e Estoque são migrados para os formatos esperados pelas funções Python;
- limites de itens e validações foram adicionados aos endpoints do laboratório para reduzir abuso e estados inválidos;
- testes automatizados cobrem Agenda, Tarefas, Alunos, Estoque, Biblioteca, Caixa, Financeiro, Hábitos, API HTTP real e Projeto Integrado;
- CI valida sintaxe Python, JavaScripts do laboratório, da trilha e da matriz, além de toda a suíte de testes;
- detecção de arquivos de teste ampliada para padrões comuns de Python, JavaScript, TypeScript, JSX, Go, Dart/Flutter, Ruby, Java, Kotlin, C#, PHP e diretórios convencionais de teste;
- teste automatizado evita falsos positivos simples como `contest.py` e `latest.ts`;
- verificação determinística de links internos do README usa a árvore do próprio repositório;
- links internos quebrados aparecem na página de qualidade do README com ação concreta de correção;
- URLs externas não são consultadas por essa verificação, reduzindo risco de requisições arbitrárias;
- microinterações compartilhadas e acessíveis em desktop, teclado e touch/mobile;
- showcase público dentro do próprio GitHub;
- primeira `good first issue` aberta para contribuição da comunidade;
- labels `good first issue`, `documentation` e `help wanted` aplicadas à tarefa inicial;
- template de Pull Request orienta contribuidores iniciantes;
- roadmap atualizado para refletir somente entregas já verificadas.

## [0.1.0] — 2026-09-15

Primeiro MVP público em produção.

### Produto

- análise de repositório por `usuario/repositorio` ou URL;
- score determinístico com evidências verificáveis;
- análise de perfil público completo;
- verificação de README, descrição, licença, `.gitignore`, topics, CI, testes e dependências;
- status real da execução mais recente do GitHub Actions;
- análise estrutural de README;
- comparação entre dois repositórios;
- histórico versionado por commit;
- explicação pedagógica local;
- IA explicativa opcional sem alterar o diagnóstico;
- CLI, interface web e endpoints JSON.

### Engenharia

- testes automatizados;
- CI própria;
- Flask + Gunicorn;
- deploy público no Render;
- `/healthz`, `robots.txt` e `sitemap.xml`;
- renderização segura de conteúdo externo;
- documentação de deploy, segurança, comunidade e contribuição.

### Comunidade

- formulário estruturado de feedback;
- `CONTRIBUTING.md`;
- `CODE_OF_CONDUCT.md`;
- `SECURITY.md`;
- `COMMUNITY.md`;
- início da trilha de contribuição open source externa.

## Princípio de versionamento

As versões registram entregas públicas verificáveis. Commits isolados não são tratados como versões apenas para aumentar atividade no perfil.
