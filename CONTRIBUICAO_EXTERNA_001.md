# Contribuição externa 001

## Projeto alvo

`fork-commit-merge/fork-commit-merge`

Issue escolhida:

- **#8017 — Fork, Commit, Merge - Easy Issue (Flask)**
- https://github.com/fork-commit-merge/fork-commit-merge/issues/8017

## Objetivo

Completar a tarefa Flask introdutória criando uma aplicação que responda `Hello, Flask!` na rota `/`.

## Por que esta é a contribuição 001

Ela foi escolhida deliberadamente como primeira contribuição externa porque o próprio projeto foi criado para ensinar o fluxo de contribuição open source e a issue informa que não é necessário pedir atribuição antes de começar.

## Arquivo alvo

```text
tasks/flask/easy/app.py
```

## Implementação realizada

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)
```

## Evidências atuais

- fork criado em `Videirafoo/fork-commit-merge`;
- branch criada: `feat/flask-easy-8017`;
- commit: `d2771f66b308575020b8c6bcda67553ae5553c9c`;
- a branch está 1 commit à frente da `main`;
- somente `tasks/flask/easy/app.py` foi alterado;
- a implementação segue exatamente o pedido da issue #8017.

## Critério de sucesso

- [x] usar `Flask(__name__)`;
- [x] criar rota `/`;
- [x] retornar `Hello, Flask!`;
- [x] limitar a mudança ao arquivo da tarefa;
- [x] criar branch própria e commit público;
- [ ] abrir Pull Request público para o repositório original;
- [ ] acompanhar revisão dos mantenedores;
- [ ] registrar a URL e o resultado do PR no perfil.

## Abrir o Pull Request

A integração conectada consegue escrever no fork `Videirafoo`, mas o GitHub bloqueia a criação automática do PR no repositório upstream com `403 Resource not accessible by integration`.

Use o comparador público:

https://github.com/fork-commit-merge/fork-commit-merge/compare/main...Videirafoo:feat/flask-easy-8017?expand=1

Título preparado:

```text
Complete Flask easy task
```

## Estado

**Código concluído e publicado no fork. Pull Request externo pendente de criação pela interface do GitHub.**

A contribuição só será apresentada como conquista depois que existir um Pull Request público verificável.
