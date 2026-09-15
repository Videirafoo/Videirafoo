# Padrão de Ensino — Videirafoo

Este documento define como os conteúdos educacionais deste GitHub devem ser produzidos e mantidos.

## Objetivo

Ajudar quem está começando em programação e Engenharia de Software com conteúdo claro, prático, progressivo e atualizado.

## Princípios

1. **Explicar antes de complicar** — começar pelo conceito, depois mostrar código.
2. **Aprender construindo** — cada assunto deve levar a um exercício, desafio ou pequeno sistema.
3. **Código legível** — nomes claros, exemplos pequenos e estrutura fácil de entender.
4. **Progressão real** — iniciante → intermediário → projeto aplicado.
5. **Mostrar o porquê** — não ensinar apenas comandos; explicar decisões e consequências.
6. **Erros fazem parte** — incluir erros comuns, como identificar e como corrigir.
7. **Testar sempre que fizer sentido** — validação manual, testes automatizados ou CI.
8. **Documentar para outra pessoa conseguir usar** — README, requisitos, execução e exemplos.
9. **Fonte oficial primeiro** — conteúdos mutáveis devem ser revisados contra documentação oficial.
10. **Sem atalhos artificiais** — nada de commits falsos, métricas infladas ou conteúdo copiado sem contexto/licença.
11. **Competência precisa de evidência** — “estudei” não significa “sei fazer”; cada etapa deve indicar uma prova prática observável.
12. **Entregável antes de badge** — código, teste, endpoint, PR ou relatório valem mais que decoração ou contagem de atividade.

## Estrutura recomendada para cada aula/projeto

1. O que você vai aprender
2. Conceito em linguagem simples
3. Exemplo mínimo
4. Exercício guiado
5. Desafio para tentar sozinho
6. Solução comentada
7. Erros comuns
8. Como testar
9. Evidência de conclusão
10. Próximo passo
11. Fontes oficiais

## Evidência de conclusão

Cada conteúdo deve definir o que uma pessoa precisa **conseguir fazer** antes de avançar.

Uma evidência pode ser:

- executar um exemplo sem copiar comandos cegamente;
- explicar entrada, processamento e saída;
- alterar uma regra mantendo o comportamento esperado;
- provocar e corrigir um erro;
- escrever ou interpretar um teste;
- obter CI verde;
- publicar um endpoint funcional;
- abrir um Pull Request pequeno e revisável;
- confirmar uma recomendação contra a fonte original.

A evidência deve apontar para algo inspecionável sempre que possível: código, teste, execução, commit, PR, endpoint ou relatório.

## Ciclo pedagógico padrão

```text
conceito
  ↓
exemplo mínimo
  ↓
missão prática
  ↓
explicação do aluno
  ↓
modificação
  ↓
teste / validação
  ↓
evidência
  ↓
próximo nível
```

## Níveis

### Nível 1 — Fundamentos
Lógica, variáveis, entrada/saída, condicionais, laços e funções.

**Evidência esperada:** executar e explicar programas pequenos, alterar condições e criar funções simples.

### Nível 2 — Estruturas
Listas, matrizes, dicionários, busca, ordenação, recursividade e complexidade.

**Evidência esperada:** escolher estruturas adequadas e explicar passo a passo o comportamento de algoritmos básicos.

### Nível 3 — Pequenos sistemas
Menus, arquivos, JSON, CRUD, validação, organização em módulos e testes.

**Evidência esperada:** modificar uma regra de negócio, tratar entrada inválida e manter testes verdes.

### Nível 4 — Aplicações reais
APIs, banco de dados, autenticação, frontend, mobile, deploy e observabilidade.

**Evidência esperada:** integrar partes reais de uma aplicação, entender HTTP, validar erro e demonstrar o software em execução.

### Nível 5 — Engenharia
Arquitetura, segurança, qualidade, CI/CD, desempenho, documentação e manutenção.

**Evidência esperada:** proteger comportamento com testes, interpretar cobertura, usar CI, revisar mudanças e produzir PRs pequenos.

### Nível 6 — IA aplicada
Prompts, RAG, agentes, ferramentas, avaliação, segurança e governança.

**Evidência esperada:** separar fatos de interpretação, validar respostas contra fontes, implementar fallback e explicar limites da automação.

A implementação interativa desses níveis fica em:

https://github-student-dashboard-videirafoo.onrender.com/trilha

## Papéis como forma de prática

Nos níveis mais avançados, um mesmo projeto pode ser estudado por responsabilidades diferentes:

- **desenvolvedor backend:** endpoint, validação, erros e testes;
- **frontend:** experiência, estado, acessibilidade e integração;
- **code reviewer:** evidência, impacto, ação e escopo;
- **DevOps/SRE:** CI, deploy, healthcheck e logs;
- **technical writer:** execução reproduzível para outra pessoa;
- **AI engineer:** contexto, avaliação, proveniência e fallback.

O papel só deve ser adicionado quando existir uma missão concreta e um entregável verificável.

## Regra de atualização

Sempre que uma tecnologia, biblioteca, versão ou prática puder ter mudado:

- verificar documentação oficial;
- registrar a data da revisão quando relevante;
- evitar ensinar sintaxe obsoleta como padrão atual;
- manter exemplos antigos apenas quando forem úteis para comparação histórica;
- indicar claramente o que é fundamento durável e o que depende de versão.

## Compromisso

O objetivo não é parecer avançado. O objetivo é fazer outra pessoa entender, conseguir executar, explicar, modificar, testar e evoluir o que aprendeu.
