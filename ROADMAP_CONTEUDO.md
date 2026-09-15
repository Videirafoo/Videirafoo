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
- [x] persistência em JSON na Agenda
- [x] testes automatizados da Agenda
- [x] CI dos conteúdos Python
- [x] Mini Sistema 02 — Lista de Tarefas
- [x] persistência em JSON na Lista de Tarefas
- [x] testes automatizados da Lista de Tarefas
- [x] Mini Sistema 03 — Cadastro de Alunos
- [x] persistência em JSON no Cadastro de Alunos
- [x] testes automatizados do Cadastro de Alunos
- [x] CI configurada para descobrir todos os testes dos mini sistemas
- [x] Mini Sistema 04 — Controle de Estoque
- [x] persistência em JSON no Controle de Estoque
- [x] testes automatizados do Controle de Estoque
- [x] Mini Sistema 05 — Sistema de Biblioteca
- [x] persistência em JSON no Sistema de Biblioteca
- [x] testes automatizados do Sistema de Biblioteca
- [ ] Mini Sistema 06 — Caixa de Mercado
- [ ] Mini Sistema 07 — Controle Financeiro Pessoal
- [ ] Mini Sistema 08 — Gerenciador de Hábitos
- [ ] Mini Sistema 09 — API de Tarefas
- [ ] Mini Sistema 10 — Projeto integrado

Conteúdo atual: `conteudos/mini_sistemas/`.

## Referências arquiteturais estudadas

- [x] `alibaba/open-code-review` estudado como referência de arquitetura híbrida: validações determinísticas + agente/LLM para contexto e julgamento.
- [x] princípio incorporado: **automatizar deterministicamente o que pode ser provado e usar IA para explicar, orientar e revisar pontos ambíguos**.
- [x] referência registrada em `REFERENCIAS_OPEN_SOURCE.md`.

## Fase 4 — Projeto público principal

### GitHub Student Dashboard

Construir uma ferramenta realmente útil para estudantes que analise repositórios e identifique:

- README ausente ou incompleto;
- falta de licença;
- falta de topics;
- organização de projetos;
- linguagens usadas;
- progresso de estudos;
- sugestões de melhoria;
- checklist de boas práticas.

### Arquitetura planejada

Inspirada em padrões generalizados estudados em projetos open source maduros:

**Camada determinística**

- ler metadados e arquivos via GitHub API;
- verificar README, licença, topics, CI, testes e estrutura;
- produzir evidências objetivas;
- evitar recomendações inventadas ou baseadas apenas em prompt.

**Camada de IA**

- explicar os achados para iniciantes;
- priorizar melhorias;
- sugerir próximos passos;
- adaptar a explicação ao nível do projeto;
- nunca substituir uma verificação objetiva quando ela puder ser feita por código.

Objetivos técnicos:

- consumir GitHub API;
- ter interface web simples;
- documentação completa;
- testes e CI;
- deploy público;
- receber feedback de usuários.

## Fase 5 — Open source externo

- [ ] encontrar projetos beginner-friendly
- [ ] começar por documentação, testes ou pequenos bugs
- [ ] abrir PRs pequenos e bem descritos
- [ ] aprender revisão de código
- [ ] registrar contribuições relevantes no perfil

## Fase 6 — Comunidade

- [ ] publicar conteúdos curtos baseados nos projetos
- [ ] criar desafios semanais para estudantes
- [ ] incentivar issues e PRs de iniciantes
- [ ] organizar pequenos encontros ou workshops
- [ ] explorar elegibilidade para GitHub Campus Experts

## Fase 7 — Reconhecimento

Buscar reconhecimento como consequência de trabalho útil:

- Developer Program Member
- contribuições open source relevantes
- participação em hackathons
- Campus Experts, quando elegível
- crescimento orgânico de stars, forks e seguidores
- GitHub Stars como objetivo de longo prazo

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
