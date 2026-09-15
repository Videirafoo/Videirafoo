# Primeira contribuição open source externa — Videirafoo

Esta etapa marca o início das contribuições externas da trajetória educacional do GitHub `Videirafoo`.

## Primeira contribuição escolhida

Repositório externo:

- `fork-commit-merge/fork-commit-merge`
- Issue: **#8017 — Fork, Commit, Merge - Easy Issue (Flask)**
- Link: https://github.com/fork-commit-merge/fork-commit-merge/issues/8017

A própria issue informa que foi criada para novos contribuidores e que **não é necessário pedir atribuição antes de começar**.

## Por que essa issue foi escolhida

Ela é adequada como primeira contribuição porque:

- usa Python e Flask, tecnologias já praticadas no `Videirafoo`;
- possui escopo pequeno e objetivo;
- tem resultado verificável no navegador;
- ensina o fluxo completo `fork → branch → commit → push → pull request`;
- reduz o risco de começar open source com uma tarefa grande demais.

## Estado atual encontrado no projeto externo

O arquivo indicado pela issue é:

```text
tasks/flask/easy/app.py
```

O conteúdo atual possui o esqueleto Flask e um TODO. A implementação esperada é um endpoint `/` que retorne:

```text
Hello, Flask!
```

## Implementação preparada

A solução mínima esperada é:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)
```

Além de implementar a rota, o exemplo usa corretamente `Flask(__name__)`.

## Validação local

Depois de instalar Flask, executar:

```bash
python tasks/flask/easy/app.py
```

Abrir:

```text
http://127.0.0.1:5000/
```

Resultado esperado:

```text
Hello, Flask!
```

## Fluxo para enviar a contribuição

### 1. Fazer fork

Na página do repositório externo, usar **Fork** para criar uma cópia na conta `Videirafoo`.

### 2. Clonar o fork

```bash
git clone https://github.com/Videirafoo/fork-commit-merge.git
cd fork-commit-merge
```

### 3. Criar branch

```bash
git checkout -b feat/flask-easy-8017
```

### 4. Alterar somente o arquivo da tarefa

```text
tasks/flask/easy/app.py
```

### 5. Testar

```bash
python tasks/flask/easy/app.py
```

### 6. Commit

```bash
git add tasks/flask/easy/app.py
git commit -m "feat: complete basic Flask app task"
```

### 7. Push

```bash
git push -u origin feat/flask-easy-8017
```

### 8. Abrir Pull Request

Base:

```text
fork-commit-merge/fork-commit-merge:main
```

Head:

```text
Videirafoo/fork-commit-merge:feat/flask-easy-8017
```

Título sugerido:

```text
feat: complete basic Flask application task
```

Descrição sugerida:

```md
## Summary

Implements the Flask easy task from #8017.

- creates the root `/` route;
- returns `Hello, Flask!`;
- keeps the example intentionally small for new contributors.

## Validation

- ran the Flask app locally;
- verified `http://127.0.0.1:5000/` returns `Hello, Flask!`.
```

## Regra desta trajetória

Uma contribuição externa só entra como conquista no perfil `Videirafoo` depois de existir evidência pública do Pull Request.

Não vamos criar contribuições artificiais, commits vazios ou atividade apenas para aumentar o gráfico do GitHub.

## Próximo nível depois da primeira contribuição

Depois de concluir uma contribuição introdutória, buscar tarefas progressivamente mais reais em:

- documentação técnica;
- testes Python;
- Flask;
- acessibilidade web;
- CI/GitHub Actions;
- APIs;
- ferramentas educacionais.

O objetivo é aumentar a dificuldade gradualmente, mantendo qualidade e aprendizado verificável.
