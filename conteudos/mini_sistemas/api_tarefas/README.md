# Mini Sistema 09 — API de Tarefas

Nono projeto da coleção **Mini Sistemas Python** do GitHub `Videirafoo`.

## Objetivo

Transformar a lógica de uma lista de tarefas em uma API HTTP simples e testável.

Até aqui, os mini sistemas interagiam principalmente pelo terminal. Neste projeto, outra aplicação pode conversar com o sistema enviando requisições HTTP e recebendo respostas em JSON.

## Tecnologias

- Python 3.12;
- Flask;
- JSON;
- `unittest`;
- GitHub Actions.

## O que este projeto ensina

- conceito de API;
- HTTP;
- métodos `GET`, `POST`, `PATCH` e `DELETE`;
- endpoints;
- parâmetros de rota;
- query strings;
- corpo JSON;
- códigos de status HTTP;
- validação de entrada;
- persistência em JSON;
- separação entre regra de negócio e camada HTTP;
- testes usando cliente HTTP de teste;
- CI com dependências externas.

## Endpoints

| Método | Rota | Função |
| --- | --- | --- |
| `GET` | `/` | informa o nome da API |
| `GET` | `/tarefas` | lista tarefas |
| `GET` | `/tarefas?status=pendentes` | lista pendentes |
| `GET` | `/tarefas?status=concluidas` | lista concluídas |
| `POST` | `/tarefas` | cria tarefa |
| `GET` | `/tarefas/<id>` | consulta uma tarefa |
| `PATCH` | `/tarefas/<id>` | altera tarefa |
| `DELETE` | `/tarefas/<id>` | exclui tarefa |

## Estrutura

```text
api_tarefas/
├── __init__.py
├── app.py
├── test_app.py
├── requirements.txt
└── README.md
```

O arquivo `tarefas_api.json` é criado automaticamente quando a API salva uma tarefa pela primeira vez.

## Instalação

Na raiz do repositório:

```bash
python -m pip install -r conteudos/mini_sistemas/api_tarefas/requirements.txt
```

## Como executar

```bash
python conteudos/mini_sistemas/api_tarefas/app.py
```

Por padrão, o servidor de desenvolvimento do Flask ficará disponível localmente.

## Exemplos

### Criar tarefa

Requisição:

```http
POST /tarefas
Content-Type: application/json
```

```json
{
  "titulo": "Estudar APIs",
  "prioridade": "alta"
}
```

Resposta esperada:

```json
{
  "id": 1,
  "titulo": "Estudar APIs",
  "prioridade": "alta",
  "concluida": false
}
```

Status HTTP:

```text
201 Created
```

### Atualizar tarefa

```http
PATCH /tarefas/1
Content-Type: application/json
```

```json
{
  "concluida": true
}
```

### Excluir tarefa

```http
DELETE /tarefas/1
```

Resposta sem corpo:

```text
204 No Content
```

## Códigos HTTP usados

- `200` — operação concluída;
- `201` — recurso criado;
- `204` — recurso removido sem corpo de resposta;
- `400` — dados enviados são inválidos;
- `404` — recurso não encontrado.

## Conceito importante: API não é só uma função acessada pela internet

A camada HTTP possui responsabilidades próprias:

1. receber a requisição;
2. interpretar rota, método e JSON;
3. validar o formato básico;
4. chamar as regras de negócio;
5. converter o resultado em resposta HTTP;
6. escolher um código de status adequado.

As funções de tarefa continuam separadas para serem testadas e reutilizadas sem depender diretamente do servidor web.

## Conceito importante: `create_app`

O projeto usa uma função fábrica:

```python
create_app(caminho_dados)
```

Isso permite que os testes criem uma aplicação apontando para um arquivo temporário, sem alterar os dados reais do projeto.

## Como testar

```bash
python -m unittest conteudos.mini_sistemas.api_tarefas.test_app
```

Os testes verificam tanto regras quanto respostas HTTP.

## Checklist de revisão

- [ ] título vazio retorna `400`;
- [ ] prioridade inválida retorna `400`;
- [ ] criação retorna `201`;
- [ ] consulta existente retorna `200`;
- [ ] consulta inexistente retorna `404`;
- [ ] edição valida os campos;
- [ ] exclusão retorna `204`;
- [ ] filtro de status funciona;
- [ ] JSON inválido é rejeitado;
- [ ] persistência não interfere nos testes;
- [ ] todos os testes passam na CI.

## Desafios para quem está estudando

1. adicionar campo `descricao`;
2. adicionar data de criação;
3. adicionar prazo;
4. filtrar por prioridade;
5. criar paginação;
6. usar SQLite no lugar de JSON;
7. criar autenticação;
8. documentar a API com OpenAPI;
9. criar frontend consumindo os endpoints;
10. publicar a API em um ambiente de demonstração.

## Próximo sistema

**Mini Sistema 10 — Projeto Integrado**, reunindo conceitos dos projetos anteriores em uma aplicação maior e preparando a transição para o GitHub Student Dashboard.
