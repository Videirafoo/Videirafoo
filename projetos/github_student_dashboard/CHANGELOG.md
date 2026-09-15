# Changelog — GitHub Student Dashboard

Este arquivo registra mudanças relevantes do projeto de forma legível para estudantes, contribuidores e pessoas que acompanham sua evolução.

## [Unreleased]

### Melhorias

- laboratório ampliado para os **10 mini sistemas**, todos com experiência prática e links para código/testes reais;
- Mini Sistema 09 deixou de ser apenas uma simulação de contrato: `GET`, `POST`, `PATCH` e `DELETE` agora passam pelo backend Flask real;
- regras do playground da API reutilizam as funções Python versionadas em `conteudos/mini_sistemas/api_tarefas/app.py`;
- estado didático da API permanece no navegador, evitando misturar dados de visitantes no servidor público;
- limites e validações foram adicionados ao endpoint do laboratório para reduzir abuso e estados inválidos;
- testes automatizados cobrem criação `201`, listagem `200`, atualização `200`, exclusão `204`, erros `400/404` e integração da página com o backend real;
- CI agora valida a sintaxe dos dois arquivos JavaScript do laboratório;
- detecção de arquivos de teste ampliada para padrões comuns de Python, JavaScript, TypeScript, JSX, Go, Dart/Flutter, Ruby, Java, Kotlin, C#, PHP e diretórios convencionais de teste;
- teste automatizado para evitar falsos positivos simples como `contest.py` e `latest.ts`;
- verificação determinística de links internos do README usando a árvore do próprio repositório;
- links internos quebrados agora aparecem na página de qualidade do README com ação concreta de correção;
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
