# Mini Sistemas Python — aprender usando código real

Esta coleção existe para levar quem está começando de exercícios isolados para **programas completos, executáveis e testáveis**.

## Comece usando antes de ler

Quatro conceitos da coleção possuem playground no navegador:

**https://github-student-dashboard-videirafoo.onrender.com/laboratorio**

No laboratório você pode usar:

- lista de tarefas;
- cadastro de aluno e cálculo de média;
- controle de estoque;
- busca binária visual.

Depois de usar, volte para esta pasta e abra o código Python correspondente.

## Como estudar cada projeto

Use sempre a mesma sequência:

1. **Use** a aplicação ou leia o exemplo de uso.
2. **Preveja** o que o programa deveria fazer.
3. **Abra** `app.py` ou `main.py`.
4. **Leia** uma função de cada vez.
5. **Abra** `test_app.py` ou `test_main.py` e veja quais comportamentos são comprovados.
6. **Clone** o repositório e execute os testes.
7. **Mude** uma regra e observe qual teste precisa mudar.
8. **Crie** uma melhoria pequena por conta própria.

## Rodar localmente

Na raiz do repositório:

```bash
git clone https://github.com/Videirafoo/Videirafoo.git
cd Videirafoo
python -m unittest discover -s conteudos/mini_sistemas -t . -p "test_*.py"
```

Para executar um sistema específico, consulte o README dentro da pasta dele.

## Sistemas com código versionado

1. [Agenda de Contatos](./agenda_contatos/) — cadastro, busca, edição, exclusão e JSON
2. [Lista de Tarefas](./lista_tarefas/) — prioridades, filtros, conclusão, busca e JSON
3. [Cadastro de Alunos](./cadastro_alunos/) — matrícula, notas, média, situação acadêmica, relatório e JSON
4. [Controle de Estoque](./controle_estoque/) — produtos, entradas, saídas, estoque mínimo e JSON
5. [Sistema de Biblioteca](./sistema_biblioteca/) — livros, usuários, empréstimos, devoluções e JSON
6. [Caixa de Mercado](./caixa_mercado/) — catálogo, carrinho, estoque, descontos, vendas e JSON
7. [Controle Financeiro Pessoal](./controle_financeiro/) — receitas, despesas, categorias, saldo, filtros, relatórios e JSON
8. [Gerenciador de Hábitos](./gerenciador_habitos/) — metas semanais, registros diários, sequência, progresso e JSON
9. [API de Tarefas](./api_tarefas/) — HTTP, REST, JSON, Flask, validação e testes de API
10. [Projeto Integrado — Analisador Local de Repositórios](./projeto_integrado/) — checks determinísticos, score, evidências, recomendações e JSON

## O que precisa existir para chamarmos algo de projeto

Nesta coleção, um título no roadmap não basta. Um projeto deve ter, quando aplicável:

- código executável;
- entrada e saída observáveis;
- funções organizadas;
- validação;
- persistência quando fizer sentido;
- README com instruções de execução;
- testes automatizados;
- CI para validar o conjunto.

## Progressão

`funções` → `CRUD` → `JSON` → `regras de negócio` → `relações entre dados` → `datas e cálculos` → `HTTP/REST` → `testes` → `CI` → `projeto integrado`

## Regra de qualidade

> **Documentação explica o software; não substitui o software.**

Quando algo estiver apenas planejado, será identificado como **planejado** até existir implementação verificável.
