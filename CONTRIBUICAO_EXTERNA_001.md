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

## Mudança planejada

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)
```

## Critério de sucesso

- aplicação inicia sem erro;
- `GET /` retorna `Hello, Flask!`;
- mudança fica limitada ao arquivo da tarefa;
- Pull Request público é aberto a partir da conta `Videirafoo`;
- o PR é registrado no perfil apenas depois de existir publicamente.

## Estado

**Preparada para fork e Pull Request.**

O conector atual do GitHub não oferece ação de `fork`, então a criação do fork precisa ser feita uma vez pela interface do GitHub. Depois disso, o restante do fluxo pode continuar na conta `Videirafoo`.
