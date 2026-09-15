# Mini Sistema 10 — Projeto Integrado

Décimo projeto da coleção **Mini Sistemas Python** do GitHub `Videirafoo`.

## Projeto: Analisador Local de Repositórios

Este projeto fecha a sequência dos mini sistemas e prepara a transição para o futuro **GitHub Student Dashboard**.

A ideia é simples: analisar uma pasta de projeto localmente e produzir um diagnóstico objetivo sobre alguns elementos básicos de qualidade e organização.

## Objetivo

Reunir conceitos praticados ao longo da trilha:

- funções;
- listas e dicionários;
- arquivos;
- JSON;
- validação;
- busca;
- regras determinísticas;
- relatórios;
- testes;
- CI;
- organização de código.

Ao mesmo tempo, o projeto introduz um novo tema: **análise automatizada de repositórios**.

## O que é verificado

O analisador procura evidências objetivas de:

- README;
- `.gitignore`;
- licença;
- GitHub Actions/CI;
- testes;
- arquivo de dependências;
- arquivos de código;
- linguagens estimadas pelas extensões.

## Score

A pontuação atual usa pesos simples:

| Check | Pontos |
| --- | ---: |
| README | 20 |
| `.gitignore` | 10 |
| Licença | 15 |
| CI | 20 |
| Testes | 20 |
| Dependências | 15 |
| **Total** | **100** |

O score não tenta dizer se o código é “bom” ou “ruim”. Ele apenas resume a presença de itens verificáveis definidos para este exercício.

## Regra arquitetural

Este projeto aplica diretamente a regra adotada no `Videirafoo`:

> **Automatizar deterministicamente o que pode ser provado; usar IA para explicar, orientar e revisar onde existe ambiguidade.**

Nesta versão local, toda a análise é determinística.

A IA ainda não participa da decisão de score.

## Estrutura

```text
projeto_integrado/
├── __init__.py
├── app.py
├── test_app.py
└── README.md
```

## Como executar

Na raiz do repositório:

```bash
python conteudos/mini_sistemas/projeto_integrado/app.py
```

Depois informe o caminho da pasta que deseja analisar.

Exemplo:

```text
Caminho do repositório/pasta que deseja analisar: ./meu-projeto
```

## Exemplo de saída

```text
=== Diagnóstico: meu-projeto ===
Score: 70/100

Checks:
- readme: OK
- gitignore: OK
- licenca: FALTA
- ci: OK
- testes: FALTA
- dependencias: OK
```

O programa também pode salvar o diagnóstico em JSON.

## Evidências

Além do score, o relatório informa:

- número de arquivos analisados;
- linguagens estimadas;
- resultado individual de cada check;
- recomendações para os itens ausentes.

Exemplo:

```json
{
  "score": 70,
  "checks": {
    "readme": true,
    "gitignore": true,
    "licenca": false,
    "ci": true,
    "testes": false,
    "dependencias": true
  }
}
```

## Por que isso é melhor do que pedir para uma IA “dar uma nota”

Porque os critérios objetivos são calculados por código.

A ferramenta não precisa imaginar se existe README ou CI: ela verifica diretamente os arquivos.

Em uma evolução futura, uma camada de IA poderá receber essas evidências e explicar:

```text
Observado: não existe arquivo de licença.
Impacto: quem deseja reutilizar o projeto não possui permissões claramente definidas.
Ação: avaliar e adicionar uma licença apropriada ao objetivo do projeto.
```

A observação continua vindo de um check determinístico.

## Limitações desta versão

O analisador ainda não verifica:

- qualidade real do README;
- cobertura dos testes;
- segurança das dependências;
- qualidade do código;
- links quebrados;
- status real da CI;
- topics do GitHub;
- stars, forks ou issues;
- dados remotos da API do GitHub.

Esses itens pertencem à evolução para o **GitHub Student Dashboard**.

## Como testar

```bash
python -m unittest conteudos.mini_sistemas.projeto_integrado.test_app
```

Os testes criam repositórios temporários para verificar o comportamento sem depender dos projetos reais do usuário.

## Checklist de revisão

- [ ] caminho inexistente é rejeitado;
- [ ] arquivo não é aceito no lugar de pasta;
- [ ] README é detectado;
- [ ] `.gitignore` é detectado;
- [ ] licença é detectada;
- [ ] workflow de CI é detectado;
- [ ] testes são detectados;
- [ ] dependências são detectadas;
- [ ] pastas como `.venv` e `node_modules` são ignoradas;
- [ ] linguagens são contadas;
- [ ] score é reproduzível;
- [ ] recomendações dependem dos checks reais;
- [ ] relatório JSON é exportável;
- [ ] testes passam na CI.

## Desafios para quem está estudando

1. detectar mais linguagens;
2. validar se o README possui seção “Como executar”;
3. detectar links locais quebrados;
4. detectar arquivos muito grandes;
5. ler cobertura de testes;
6. verificar `pyproject.toml` ou `package.json` em mais detalhes;
7. consumir a API pública do GitHub;
8. analisar um repositório pelo nome `usuario/repositorio`;
9. criar uma interface web para o relatório;
10. adicionar camada de IA apenas para explicar as evidências.

## Próxima etapa da trajetória

Com os 10 mini sistemas concluídos, a próxima fase deixa de ser um exercício isolado e passa a ser um **projeto público principal**:

# GitHub Student Dashboard

Ele reutilizará este núcleo de checks e evoluirá para análise remota, interface web, API do GitHub, relatórios mais ricos e orientação educacional.
