# Referências Open Source — Videirafoo

Este documento registra projetos públicos estudados como referência de **boas práticas e arquitetura**, sem copiar código, identidade visual ou conteúdo proprietário.

## Alibaba OpenCodeReview

Fonte estudada: `alibaba/open-code-review`  
Licença do projeto de origem: **Apache-2.0**.

### Por que é relevante

OpenCodeReview combina duas camadas:

1. **engenharia determinística** para tarefas que precisam ser previsíveis e verificáveis;
2. **agente com LLM** para decisões, busca de contexto e explicações que exigem julgamento.

Essa separação é especialmente útil para o **GitHub Student Dashboard** do `Videirafoo`.

### Padrões absorvidos

#### 1. Determinístico primeiro

Checks objetivos não devem depender de IA quando podem ser calculados diretamente.

No GitHub Student Dashboard isso significa verificar por código:

- existência de `README.md`;
- existência e tipo de licença;
- presença de topics;
- existência de `.gitignore`;
- existência de CI;
- status das workflows;
- presença de testes;
- estrutura básica do repositório;
- links locais inválidos quando detectáveis;
- idade da última atualização;
- linguagens e arquivos principais.

A IA entra depois para **explicar o resultado, priorizar melhorias e ensinar o estudante**.

#### 2. Precisão acima de quantidade

Uma ferramenta educacional não deve gerar dezenas de alertas genéricos. Cada recomendação precisa ser:

- verificável;
- relevante;
- explicada em linguagem simples;
- acompanhada de uma ação concreta.

#### 3. Regras específicas por contexto

Regras devem poder variar por tipo de arquivo ou projeto.

Exemplo:

- Python → `.gitignore`, testes, organização de módulos;
- Web → acessibilidade, HTML semântico, responsividade;
- API → validação, erros HTTP, documentação;
- projeto educacional → objetivo, nível, execução, exercício e próximo passo.

#### 4. Contexto antes da recomendação

Uma análise não deve avaliar apenas uma linha ou arquivo isolado quando o restante do projeto muda o significado da alteração.

#### 5. Revisão orientada a evidências

Toda recomendação futura do dashboard deverá indicar **o que foi observado** e **por que aquilo importa**.

Formato desejado:

```text
Observado: README não possui instruções de execução.
Impacto: uma pessoa nova não sabe como testar o projeto.
Ação: adicionar seção "Como executar" com pré-requisitos e comando.
Nível: importante.
```

#### 6. Qualidade automatizada

Adotar progressivamente:

- testes;
- CI;
- análise estática quando apropriada;
- checks de dependências e segurança em projetos que precisarem;
- critérios de aceite claros.

#### 7. Contribuição responsável com IA

Quando IA ajudar a produzir uma contribuição para projeto externo:

- ler e entender todo o conteúdo antes de enviar;
- respeitar as regras específicas do repositório;
- declarar uso de IA quando o projeto exigir;
- nunca enviar código que o próprio contribuinte não consiga explicar;
- manter PRs pequenos e focados.

### Aplicação no Videirafoo

O projeto da Alibaba **não será copiado nem incorporado como segunda plataforma**.

Usamos apenas ideias arquiteturais generalizadas para melhorar:

- processo de revisão dos mini sistemas;
- GitHub Student Dashboard;
- checklists educacionais;
- CI e qualidade;
- preparação para contribuições open source.

### Regra canônica

> **Automatize deterministicamente o que pode ser provado; use IA para raciocinar, explicar e orientar onde existe ambiguidade.**

---

## DenverCoder1

Fontes estudadas: perfil `DenverCoder1/DenverCoder1` e projetos públicos como `readme-typing-svg`, `github-readme-streak-stats` e `custom-icon-badges`.

### Por que é relevante

O perfil mostra um padrão importante para crescimento open source: não depender apenas de um README visual, mas construir **ferramentas reutilizáveis por outras pessoas**, destacar contribuições externas e transformar projetos em produtos pequenos e fáceis de descobrir.

O projeto `readme-typing-svg`, por exemplo, resolve um problema simples de personalização de perfis. O aprendizado principal não é copiar a ferramenta, e sim entender o padrão: **uma utilidade pequena, clara, compartilhável e fácil de experimentar pode alcançar muita gente**.

### Padrões absorvidos

#### 1. Mostrar projetos que outras pessoas realmente usam

O perfil deve destacar primeiro projetos com valor público, não apenas exercícios acadêmicos.

Aplicação no `Videirafoo`:

- GitHub Student Dashboard;
- ferramentas educacionais pequenas;
- utilitários para estudantes;
- geradores/checkers simples;
- projetos com demo e instruções rápidas.

#### 2. Separar “meus projetos” de “projetos para os quais contribuí”

Contribuições externas reais ficam em seção específica. Isso mostra colaboração, revisão de código e participação em comunidades diferentes.

#### 3. Transformar ensino em produto open source

Conteúdo educacional pode virar ferramenta.

Exemplos de direção:

- verificador de README para iniciantes;
- checklist de projeto acadêmico;
- analisador de organização de repositório;
- estrutura inicial de projeto Python;
- painel de progresso de estudos;
- badges educacionais baseados em evidências reais.

#### 4. Facilitar descoberta

Projetos públicos importantes devem ter:

- descrição curta e específica;
- topics relevantes;
- licença adequada;
- README com resultado visível rapidamente;
- exemplo de uso;
- link de demonstração quando possível;
- contribuição fácil para iniciantes.

#### 5. Perfil como índice, não como depósito

O README do perfil deve funcionar como uma página de entrada para o melhor conteúdo.

Não precisamos copiar a quantidade de imagens ou badges do DenverCoder1. A referência é a estrutura:

- identidade clara;
- projetos principais;
- contribuições externas;
- prova de atividade;
- links para conteúdo útil.

#### 6. Construir utilidades ao redor do próprio GitHub

Projetos que melhoram a experiência de outros desenvolvedores no GitHub têm potencial natural de descoberta dentro da própria comunidade.

### Regra aplicada

> **Não copiar o perfil de quem já tem visibilidade; copiar o princípio de criar algo tão útil que outras pessoas tenham motivo para voltar, compartilhar e contribuir.**

---

## BEPb — progressão, competências e prática pública

Fontes estudadas:

- `BEPb/BEPb`;
- `BEPb/Python-100-days`;
- `BEPb/Programmer_Competency_Matrix`;
- `BEPb/first-contributions`.

### Por que é relevante

O conjunto mostra quatro padrões educacionais úteis quando vistos em conjunto:

1. **progressão longa dividida em etapas pequenas**;
2. **muitos exemplos concretos**, em vez de apenas tópicos teóricos;
3. **competências avaliadas por níveis observáveis**;
4. **redução da barreira para a primeira contribuição open source**.

O perfil principal também mostra muitas métricas, badges e elementos visuais. Para o `Videirafoo`, o aprendizado útil não é reproduzir essa quantidade visual, e sim tornar **progresso e evidências fáceis de enxergar**.

### Padrões absorvidos

#### 1. Trilha progressiva

`Python-100-days` reforça que uma base grande pode ser dividida em unidades pequenas e encadeadas.

Aplicação no `Videirafoo`:

- Nível 1 — Fundamentos;
- Nível 2 — Estruturas e Algoritmos;
- Nível 3 — Mini Sistemas;
- Nível 4 — Aplicações Reais;
- Nível 5 — Engenharia de Software;
- Nível 6 — IA Aplicada.

Essa progressão agora existe também como **rota interativa `/trilha`**, e não apenas como texto no repositório.

#### 2. Competência precisa de evidência

A matriz de competências reforça que “sei Git”, “sei testes” ou “sei algoritmos” é vago demais.

No `Videirafoo`, cada competência deve ser conectada a uma evidência observável, como:

- explicar um algoritmo passo a passo;
- modificar código e preservar testes;
- criar uma branch e um PR pequeno;
- interpretar cobertura e CI;
- verificar manualmente uma evidência apresentada pelo Dashboard.

#### 3. Aprender com exemplos antes de aumentar complexidade

Uma trilha educacional deve oferecer exemplos curtos, depois exercícios guiados, depois desafios independentes e finalmente sistemas.

Isso complementa `PADRAO_DE_ENSINO.md` e o laboratório dos mini sistemas.

#### 4. Primeira contribuição com baixo atrito

A referência `first-contributions` mostra a importância de explicar claramente o ciclo:

`fork/branch` → `alteração pequena` → `commit` → `push` → `pull request` → `review`.

No `Videirafoo`, isso se conecta a:

- `OPEN_SOURCE_START.md`;
- `CONTRIBUICAO_EXTERNA_001.md`;
- `good first issue`;
- primeira contribuição externa verificável.

### O que não vamos copiar

- excesso de badges sem função pedagógica;
- métricas como substituto de software executável;
- conteúdo traduzido ou exemplos de terceiros como se fossem nossos;
- checklists marcados sem prova prática.

### Regra aplicada

> **Progresso educacional deve mostrar o que a pessoa consegue fazer, explicar, modificar e testar — não apenas o que ela já leu.**

---

## Agency Agents — aprender por papel e entregável

Fonte estudada: `msitarzewski/agency-agents`.

### Por que é relevante

A coleção organiza especialistas por papéis claros, missão, processo e entregáveis. Para uma base educacional, o padrão útil é transformar assuntos avançados em **responsabilidades que a pessoa consegue praticar**.

### Padrões absorvidos

#### 1. Papel antes da ferramenta

Em vez de ensinar apenas nomes de bibliotecas, a trilha pode perguntar “o que esse papel precisa entregar?”.

Exemplos:

- Backend → endpoint correto, validação e erro HTTP;
- DevOps → CI reproduzível e deploy verificável;
- Code Reviewer → evidência, impacto e ação;
- Technical Writer → outra pessoa consegue executar sem ajuda;
- SRE → healthcheck, logs e sinais de falha;
- AI Engineer → avaliação, fallback e proveniência.

#### 2. Entregável verificável

Cada etapa deve terminar em algo que possa ser inspecionado:

- código;
- teste;
- endpoint;
- relatório;
- PR;
- execução de CI;
- evidência de produção.

#### 3. Especialização só depois da base

Papéis especializados fazem mais sentido depois que a pessoa domina fundamentos, estruturas, pequenos sistemas e aplicações reais.

Isso evita transformar a trilha em catálogo de buzzwords.

### O que não vamos copiar

- prompts/personas integrais;
- identidades dos agentes;
- catálogos enormes apenas para aumentar quantidade;
- especialização sem exercício executável.

### Regra aplicada

> **Uma competência avançada só entra na trilha quando pode virar uma missão prática com entregável verificável.**

---

## Síntese para a base educacional

As referências convergem para uma arquitetura simples:

```text
conceito
  ↓
exemplo pequeno
  ↓
missão prática
  ↓
evidência observável
  ↓
teste / CI / revisão
  ↓
próximo nível
```

A implementação canônica dessa direção é a **Trilha Educacional pública** do GitHub Student Dashboard, combinada com os mini sistemas executáveis e com a qualidade verificável do próprio repositório.
