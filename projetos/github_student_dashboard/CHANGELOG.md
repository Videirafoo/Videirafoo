# Changelog — GitHub Student Dashboard

Este arquivo registra mudanças relevantes do projeto de forma legível para estudantes, contribuidores e pessoas que acompanham sua evolução.

## [Unreleased]

### Qualidade verificável

- medição real de cobertura adicionada à CI com `coverage.py` e branch coverage;
- baseline inicial observado: **95 testes / 73,3% de cobertura**;
- testes direcionados adicionados para CLI, cliente GitHub, provider de IA, adaptadores do laboratório, rotas HTTP e casos de borda;
- evolução intermediária comprovada: **118 testes / 81,9% de cobertura**;
- nova execução de referência: [GitHub Student Dashboard CI #108](https://github.com/Videirafoo/Videirafoo/actions/runs/34995444039);
- execução #108 confirmou **147 testes passando / 92,9% de cobertura total**;
- gate de regressão de cobertura elevado para **90%** e aprovado na execução #108;
- `cli.py`: **100,0%**;
- `github_client.py`: **97,5%**;
- `ai_explainer.py`: **95,7%**;
- `lab_api.py`: **99,0%**;
- `lab_business.py`: **98,5%**;
- `lab_systems.py`: **94,8%**;
- `lab_web.py`: **94,3%**;
- auditoria informativa de dependências de produção mantida com `pip-audit`;
- execução #108 registrou `No known vulnerabilities found` para as dependências resolvidas naquele run;
- artefato `dashboard-quality-evidence` publica `coverage.txt`, `coverage.json` e `pip-audit.txt` em cada execução;
- artefato da execução #108: https://github.com/Videirafoo/Videirafoo/actions/runs/34995444039/artifacts/10407506784;
- `ResourceWarning` identificado pela primeira medição foi corrigido nos testes de recursos estáticos;
- `actions/checkout`, `actions/setup-python` e `actions/upload-artifact` atualizadas para a geração v7;
- evidências, limites e metodologia documentados publicamente em `QUALITY.md`.

### Próximos alvos de qualidade

A cobertura passou a orientar a prioridade de teste. Os próximos alvos úteis são:

- `engine.py` — **82,1%**, principalmente branches de erro e casos-limite;
- `web.py` — **85,2%**, especialmente respostas de erro e fluxos alternativos;
- `readme_quality.py` — **86,9%**, com foco em parsing e links internos de borda;
- manter o gate global em **90%** sem perseguir 100% apenas por aparência.

### Melhorias

- laboratório ampliado para os **10 mini sistemas**, todos com experiência prática e links para código/testes reais;
- **os 10 mini sistemas agora têm regras centrais processadas pelo backend Flask usando os módulos Python reais do repositório**;
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
- CI valida sintaxe Python, os JavaScripts de integração real e toda a suíte de testes;
- detecção de arquivos de teste ampliada para padrões comuns de Python, JavaScript, TypeScript, JSX, Go, Dart/Flutter, Ruby, Java, Kotlin, C#, PHP e diretórios convencionais de teste;
- teste automatizado para evitar falsos positivos simples como `contest.py` e `latest.ts`;
- verificação determinística de links internos do README usando a árvore do próprio repositório;
- links internos quebrados aparecem na página de qualidade do README com ação concreta de correção;
- URLs externas não são consultadas por essa verificação, reduzindo risco de requisições arbitrárias;
- microinterações compartilhadas e acessíveis em desktop, teclado e touch/mobile;
- showcase público dentro do próprio GitHub;
- primeira `good first issue` aberta para contribuição da comunidade;
- labels `good first issue`, `documentation` e `help wanted` aplicadas à tarefa inicial;
- template de Pull Request para orientar contribuidores iniciantes;
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
