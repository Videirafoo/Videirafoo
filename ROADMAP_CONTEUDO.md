# Roadmap de Conteúdo e Open Source

## Missão

Transformar o GitHub `Videirafoo` em uma referência prática para estudantes iniciantes, mostrando evolução acadêmica, pequenos sistemas úteis, boas práticas e participação open source.

## Fase 1 — Base educacional

- [x] README de perfil profissional
- [x] Guia de estudos
- [x] Ideias de projetos
- [x] Padrão de ensino
- [x] padronizar README dos projetos acadêmicos
- [x] adicionar CI aos projetos em que a validação automática é útil
- [ ] revisar descrições, topics e licenças dos repositórios
- [ ] adicionar screenshots quando aplicável

## Fase 2 — Conteúdo para iniciantes

### Python para iniciantes

- [x] índice do curso
- [x] módulo 00 — preparação
- [x] módulo 01 — variáveis e entrada
- [x] módulo 02 — operadores e cálculos
- [x] módulo 03 — condicionais
- [x] módulo 04 — laços
- [x] módulo 05 — funções
- [x] módulo 06 — listas e dicionários
- [x] módulo 07 — busca, ordenação e Big O
- [x] módulo 08 — recursividade
- [x] módulo 09 — arquivos e JSON
- [x] módulo 10 — erros, testes e organização
- [x] projeto final guiado

Conteúdo atual: `conteudos/python-para-iniciantes/`.

### Próximas coleções

- [ ] `algoritmos-e-estruturas`
- [ ] `projetos-web-iniciante`
- [ ] `desafios-mobile-flutter`

Todas as coleções devem seguir `PADRAO_DE_ENSINO.md`.

## Fase 3 — Mini Sistemas Python

Objetivo: transformar fundamentos em pequenos sistemas completos, testáveis e fáceis de estudar.

- [x] estrutura da coleção
- [x] Mini Sistema 01 — Agenda de Contatos
- [x] Mini Sistema 02 — Lista de Tarefas
- [x] Mini Sistema 03 — Cadastro de Alunos
- [x] Mini Sistema 04 — Controle de Estoque
- [x] Mini Sistema 05 — Sistema de Biblioteca
- [x] Mini Sistema 06 — Caixa de Mercado
- [x] Mini Sistema 07 — Controle Financeiro Pessoal
- [x] Mini Sistema 08 — Gerenciador de Hábitos
- [x] Mini Sistema 09 — API de Tarefas
- [x] Mini Sistema 10 — Projeto Integrado: Analisador Local de Repositórios
- [x] persistência em JSON quando aplicável
- [x] testes automatizados em todos os sistemas
- [x] CI geral com descoberta automática de testes
- [x] CI com instalação das dependências da API

Conteúdo atual: `conteudos/mini_sistemas/`.

### Resultado da fase

A coleção agora ensina progressivamente:

- CRUD;
- validação;
- persistência;
- busca e filtros;
- regras de negócio;
- cálculos e relatórios;
- datas e sequências;
- relações entre entidades;
- HTTP e REST;
- testes;
- CI;
- análise determinística de projetos.

## Referências arquiteturais estudadas

- [x] `alibaba/open-code-review` estudado como referência de arquitetura híbrida: validações determinísticas + agente/LLM para contexto e julgamento.
- [x] princípio incorporado: **automatizar deterministicamente o que pode ser provado e usar IA para explicar, orientar e revisar pontos ambíguos**.
- [x] `DenverCoder1` estudado como referência de descoberta, projetos reutilizáveis e apresentação de contribuições open source.
- [x] `IanLunn/Hover` estudado como referência de microinterações; os padrões úteis foram reimplementados com CSS próprio, acessível e mobile-friendly.
- [x] referências registradas em `REFERENCIAS_OPEN_SOURCE.md` quando aplicável.

## Fase 4 — Projeto público principal

### GitHub Student Dashboard

Status: **MVP público em produção e recebendo feedback**.

Produção:

https://github-student-dashboard-videirafoo.onrender.com

Código:

`projetos/github_student_dashboard/`

### Arquitetura aplicada

**Camada determinística**

- ler metadados e arquivos via GitHub API;
- verificar README, licença, topics, CI, testes e estrutura;
- produzir evidências objetivas;
- evitar recomendações inventadas ou baseadas apenas em prompt.

**Camada de explicação**

- explicar os achados para iniciantes;
- priorizar melhorias;
- sugerir próximos passos;
- adaptar a explicação ao nível do projeto;
- nunca substituir uma verificação objetiva quando ela puder ser feita por código;
- funcionar também sem provedor externo de IA.

### Núcleo reaproveitado

O Mini Sistema 10 originou os primeiros checks locais:

- detecção de README;
- `.gitignore`;
- licença;
- CI;
- testes;
- dependências;
- linguagens estimadas;
- score reproduzível;
- evidências;
- recomendações;
- exportação JSON.

### Entregas concluídas

- [x] consumir GitHub API pública;
- [x] aceitar `usuario/repositorio` e URL do GitHub;
- [x] analisar repositório remoto;
- [x] analisar perfil completo do estudante;
- [x] ler metadados, árvore de arquivos e linguagens;
- [x] separar engine de checks da interface;
- [x] calcular score reproduzível;
- [x] gerar recomendações objetivas;
- [x] evidências detalhadas por check;
- [x] verificar status real da última CI;
- [x] analisar qualidade estrutural do README;
- [x] comparação entre repositórios;
- [x] histórico versionado de evolução por commit;
- [x] camada explicativa local;
- [x] IA opcional apenas para explicação e priorização;
- [x] CLI;
- [x] endpoints JSON;
- [x] interface web responsiva;
- [x] testes automatizados;
- [x] CI própria do Dashboard;
- [x] deploy público com Gunicorn no Render;
- [x] `/healthz`, `robots.txt` e `sitemap.xml`;
- [x] formulário e issue pública para feedback;
- [x] documentação de comunidade e segurança;
- [x] navegação rápida entre as ferramentas;
- [x] microinterações acessíveis para desktop, teclado e touch/mobile;
- [x] perfil GitHub atualizado para destacar o Dashboard e suas evidências públicas.

### Próximas melhorias do produto

- [ ] melhorar detecção de testes por stack;
- [ ] cobertura real de testes quando a stack fornecer essa informação;
- [ ] verificação de links quebrados;
- [ ] análise de vulnerabilidades/dependências em modo informativo;
- [ ] histórico persistente das análises executadas pelo produto;
- [ ] priorizar melhorias a partir de feedback real de estudantes;
- [ ] screenshots e demonstrações curtas para documentação.

## Fase 5 — Open source externo

- [x] encontrar projeto beginner-friendly para a primeira contribuição;
- [x] selecionar uma tarefa pequena e verificável: `fork-commit-merge/fork-commit-merge` Issue #8017;
- [x] documentar o passo a passo em `OPEN_SOURCE_START.md`;
- [x] preparar a contribuição em `CONTRIBUICAO_EXTERNA_001.md`;
- [x] registrar o acompanhamento na Issue #6 do `Videirafoo`;
- [ ] criar o fork na conta `Videirafoo`;
- [ ] implementar a mudança no fork;
- [ ] abrir o primeiro Pull Request externo;
- [ ] acompanhar revisão e responder aos maintainers;
- [ ] registrar no perfil apenas contribuições públicas verificáveis.

## Fase 6 — Comunidade

- [x] criar `COMMUNITY.md`;
- [x] criar `CODE_OF_CONDUCT.md`;
- [x] criar `SECURITY.md`;
- [x] abrir canal estruturado de feedback para o Dashboard;
- [ ] publicar conteúdos curtos baseados nos projetos;
- [ ] criar desafios semanais para estudantes;
- [ ] incentivar issues e PRs de iniciantes;
- [ ] organizar pequenos encontros ou workshops;
- [ ] explorar elegibilidade para GitHub Campus Experts.

## Fase 7 — Reconhecimento

Buscar reconhecimento como consequência de trabalho útil:

- Developer Program Member;
- contribuições open source relevantes;
- participação em hackathons;
- Campus Experts, quando elegível;
- crescimento orgânico de stars, forks e seguidores;
- GitHub Stars como objetivo de longo prazo.

## Métricas saudáveis

Acompanhar:

- pessoas que conseguem usar o projeto;
- issues respondidas;
- PRs recebidos/aceitos;
- forks e stars orgânicos;
- documentação melhorada;
- projetos concluídos;
- contribuições externas aceitas.

Evitar usar número de commits como principal métrica de qualidade.
