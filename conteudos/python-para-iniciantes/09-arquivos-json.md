# 09 — Arquivos e JSON

## O que você vai aprender

- ler e escrever arquivos;
- usar `with open()`;
- guardar dados em JSON;
- tratar arquivo inexistente;
- transformar dados em persistência simples.

## Texto simples

```python
with open("mensagem.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write("Olá, arquivo!")
```

Leitura:

```python
with open("mensagem.txt", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
    print(conteudo)
```

## JSON

```python
import json

contatos = [
    {"nome": "Ana", "telefone": "99999-0000"}
]

with open("contatos.json", "w", encoding="utf-8") as arquivo:
    json.dump(contatos, arquivo, ensure_ascii=False, indent=2)
```

Carregando:

```python
import json

try:
    with open("contatos.json", "r", encoding="utf-8") as arquivo:
        contatos = json.load(arquivo)
except FileNotFoundError:
    contatos = []
```

## Exercício guiado — agenda persistente

Crie uma lista de contatos, salve em `contatos.json`, encerre o programa e confirme que os dados continuam disponíveis ao executar novamente.

## Tente sozinho

Adicione funções:

- `carregar_contatos()`;
- `salvar_contatos(contatos)`;
- `adicionar_contato(contatos)`;
- `listar_contatos(contatos)`.

## Erros comuns

- esquecer `encoding="utf-8"`;
- sobrescrever um arquivo sem carregar os dados anteriores;
- assumir que o arquivo sempre existe;
- gravar dados em formato diferente do que o programa espera ler.

## Desafio extra

Implemente edição e exclusão de contatos.

## Próximo passo

Agora vamos organizar melhor o sistema, tratar falhas e introduzir testes automatizados.
