# Guia de Estudos para Iniciantes

Este guia organiza uma progressão simples para quem está começando em programação e Engenharia de Software.

## Use a trilha interativa

O guia abaixo explica **o que estudar**. A Trilha Educacional transforma esse mapa em **missões práticas com evidências reais**.

- **Trilha pública:** https://github-student-dashboard-videirafoo.onrender.com/trilha
- **Laboratório:** https://github-student-dashboard-videirafoo.onrender.com/laboratorio

A trilha possui **6 níveis e 18 missões**. O progresso fica salvo apenas no navegador e uma missão só deve ser marcada quando você executou a atividade e consegue explicar a evidência.

Regra prática:

`aprender` → `executar` → `explicar` → `modificar` → `testar` → `provar`

---

## 1. Lógica de programação

Aprenda primeiro:

- variáveis e tipos de dados;
- entrada e saída;
- operadores;
- condicionais `if`, `elif`, `else`;
- laços `for` e `while`;
- funções.

### Pratique com

1. calculadora simples;
2. classificação de notas;
3. tabuada;
4. soma e média de valores;
5. verificação de números pares e ímpares.

### Evidência de domínio

Você deve conseguir pegar um programa pequeno e explicar claramente:

`entrada` → `processamento` → `decisão/repetição` → `saída`.

---

## 2. Estruturas de dados

Depois avance para:

- listas;
- matrizes;
- dicionários;
- strings;
- tuplas;
- arquivos e JSON.

### Pratique com

1. cadastro de alunos;
2. agenda de contatos;
3. controle de estoque;
4. lista de tarefas;
5. boletim escolar.

### Evidência de domínio

Você deve conseguir justificar por que escolheu uma lista, dicionário ou outra estrutura para um problema simples e modificar o programa sem quebrar o fluxo existente.

---

## 3. Algoritmos

Estude como os dados são percorridos e organizados:

- busca sequencial;
- busca binária;
- ordenação;
- contagem de comparações;
- recursividade;
- noções de complexidade Big O.

Não tente decorar. Execute os algoritmos passo a passo e observe o que muda a cada repetição.

### Evidência de domínio

Use a busca binária visual do laboratório e consiga explicar `início`, `meio`, `fim`, número de comparações e por que os dados precisam estar ordenados.

---

## 4. Organização de código

Quando os exercícios começarem a crescer:

- separe responsabilidades em funções;
- use nomes claros;
- elimine repetições;
- trate entradas inválidas;
- crie um `main` para controlar o fluxo;
- documente como executar o projeto.

### Evidência de domínio

Escolha um exercício antigo, extraia uma responsabilidade para uma função e confirme que o comportamento continua correto.

---

## 5. Git e GitHub

Aprenda o fluxo básico:

```bash
git status
git add .
git commit -m "descrição da mudança"
git push
```

Depois estude:

- branches;
- pull requests;
- resolução de conflitos;
- `.gitignore`;
- GitHub Actions.

### Evidência de domínio

Você deve conseguir fazer uma alteração pequena em branch própria, criar um commit focado e abrir um Pull Request que outra pessoa consiga revisar.

Guia: [`OPEN_SOURCE_START.md`](./OPEN_SOURCE_START.md).

---

## 6. Pequenos sistemas

Antes de partir para aplicações grandes, construa sistemas completos de terminal:

- biblioteca;
- estoque;
- agenda;
- caixa;
- financeiro pessoal;
- sistema escolar.

O objetivo é praticar fluxo, validação, organização e persistência de dados.

### Evidência de domínio

No laboratório, provoque uma entrada inválida, encontre a validação no Python, leia o teste correspondente e depois faça uma pequena modificação mantendo a suíte verde.

---

## 7. Backend e banco de dados

Quando estiver confortável com Python ou Java:

1. aprenda HTTP e REST;
2. crie uma API CRUD;
3. conecte PostgreSQL;
4. adicione validação;
5. implemente autenticação;
6. adicione logs e testes.

### Evidência de domínio

Você deve conseguir diferenciar `GET`, `POST`, `PATCH` e `DELETE`, explicar códigos HTTP básicos e mostrar um endpoint funcionando com teste automatizado.

---

## 8. Web e mobile

### Web

`HTML` → `CSS` → `JavaScript` → `TypeScript` → `React` → `Next.js`

### Mobile

`Dart` → `Flutter` → `estado` → `persistência` → `APIs` → `autenticação`

### Evidência de domínio

A interface deve consumir comportamento real, tratar erros e permitir que outra pessoa execute o projeto seguindo o README.

---

## 9. Engenharia de Software

Antes de chamar um projeto de pronto, pratique:

- testes e cobertura;
- CI/CD;
- documentação;
- revisão de código;
- dependências e segurança;
- logs e healthcheck;
- deploy reproduzível.

### Evidência de domínio

Leia [`QUALITY.md`](./QUALITY.md) e consiga identificar:

- quantidade de testes;
- cobertura medida;
- gate de regressão;
- resultado da auditoria de dependências;
- limites do que essas métricas realmente provam.

---

## 10. Engenharia de IA

Depois dos fundamentos de software:

- consumo de APIs de modelos;
- engenharia de prompts e contexto;
- RAG;
- embeddings;
- agentes;
- ferramentas;
- memória;
- avaliações;
- fallback;
- segurança, proveniência e governança.

IA deve complementar uma base sólida de Engenharia de Software, não substituí-la.

### Evidência de domínio

Você deve conseguir separar:

- **fato verificado por código**;
- **interpretação ou explicação da IA**;
- **informação ainda não comprovada**.

No Student Dashboard, score e checks continuam determinísticos mesmo quando a explicação usa IA.

---

## Método recomendado

Para cada assunto:

1. leia o conceito;
2. faça um exemplo pequeno;
3. resolva sozinho;
4. teste casos diferentes;
5. provoque pelo menos um erro;
6. corrija o erro;
7. explique com suas próprias palavras;
8. faça uma pequena modificação;
9. valide novamente;
10. publique de forma organizada.

## Quando considerar uma etapa concluída

Não marque um assunto como dominado apenas porque você assistiu, leu ou copiou um exemplo.

Uma etapa está pronta para avançar quando você consegue pelo menos:

- **executar**;
- **explicar**;
- **modificar**;
- **testar**;
- **mostrar a evidência**.

> Aprender programação exige prática consistente. Projetos pequenos concluídos ensinam mais do que projetos enormes abandonados.
