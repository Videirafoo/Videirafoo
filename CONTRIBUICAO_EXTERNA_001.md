# Contribuição externa 001

## Projeto alvo

`fork-commit-merge/fork-commit-merge`

Issue escolhida:

- **#8017 — Fork, Commit, Merge - Easy Issue (Flask)**
- https://github.com/fork-commit-merge/fork-commit-merge/issues/8017

Pull Request:

- **#8150 — feat: complete Flask easy task**
- https://github.com/fork-commit-merge/fork-commit-merge/pull/8150

## Objetivo

Completar a tarefa Flask introdutória criando uma aplicação que responda `Hello, Flask!` na rota `/`.

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

- fork: `Videirafoo/fork-commit-merge`;
- branch: `feat/flask-easy-8017`;
- commit: `d2771f66b308575020b8c6bcda67553ae5553c9c`;
- Pull Request público: `#8150`;
- PR aberto, mergeável e não-draft;
- 1 commit e 1 arquivo alterado;
- somente `tasks/flask/easy/app.py` foi modificado;
- sem comentários ou reviews de mantenedores até a última verificação;
- duas execuções de GitHub Actions estão em `action_required`, sem jobs iniciados até a última verificação.

## Critério de sucesso

- [x] usar `Flask(__name__)`;
- [x] criar rota `/`;
- [x] retornar `Hello, Flask!`;
- [x] limitar a mudança ao arquivo da tarefa;
- [x] criar branch própria e commit público;
- [x] abrir Pull Request público para o repositório original;
- [x] registrar a URL pública do PR;
- [ ] acompanhar revisão dos mantenedores;
- [ ] responder a eventuais pedidos de mudança;
- [ ] registrar o merge, se aprovado.

## Estado

**Primeira contribuição externa com Pull Request público verificável aberta e aguardando revisão.**

Ela pode ser apresentada como **PR externo aberto**, mas não como contribuição aceita/merged antes do merge público.
