# Referências Open Source — Videirafoo

Este documento registra projetos públicos estudados como referência de **boas práticas e arquitetura**, sem copiar código, identidade visual ou conteúdo proprietário.

## Alibaba OpenCodeReview

Fonte estudada: `alibaba/open-code-review`  
Licença do projeto de origem: **Apache-2.0**.

### Por que é relevante

OpenCodeReview combina duas camadas:

1. **engenharia determinística** para tarefas que precisam ser previsíveis e verificáveis;
2. **agente com LLM** para decisões, busca de contexto e explicações que exigem julgamento.

Essa separação é especialmente útil para o futuro **GitHub Student Dashboard** do `Videirafoo`.

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

Vamos usar apenas ideias arquiteturais generalizadas para melhorar:

- processo de revisão dos nossos mini sistemas;
- futuro GitHub Student Dashboard;
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

O projeto `readme-typing-svg`, por exemplo, resolve um problema simples de personalização de perfis, possui licença MIT, topics claros e milhares de stars/forks. O aprendizado principal não é copiar a ferramenta, e sim entender o padrão: **uma utilidade pequena, clara, compartilhável e fácil de experimentar pode alcançar muita gente**.

### Padrões absorvidos

#### 1. Mostrar projetos que outras pessoas realmente usam

O perfil deve destacar primeiro projetos com valor público, não apenas exercícios acadêmicos.

Aplicação futura no `Videirafoo`:

- GitHub Student Dashboard;
- ferramentas educacionais pequenas;
- utilitários para estudantes;
- geradores/checkers simples;
- projetos com demo e instruções rápidas.

#### 2. Separar “meus projetos” de “projetos para os quais contribuí”

Quando houver contribuições externas reais, o perfil deverá ganhar uma seção específica para elas. Isso mostra colaboração, revisão de código e participação em comunidades diferentes.

#### 3. Transformar ensino em produto open source

Conteúdo educacional pode virar ferramenta.

Exemplos de direção para o `Videirafoo`:

- verificador de README para iniciantes;
- gerador de checklist de projeto acadêmico;
- analisador de organização de repositório;
- gerador de estrutura inicial de projeto Python;
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

Essa ideia reforça o GitHub Student Dashboard como projeto principal da trajetória `Videirafoo`.

### Regra aplicada

> **Não copiar o perfil de quem já tem visibilidade; copiar o princípio de criar algo tão útil que outras pessoas tenham motivo para voltar, compartilhar e contribuir.**
