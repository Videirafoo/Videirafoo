# Mini Sistema 04 — Controle de Estoque

Quarto projeto da coleção **Mini Sistemas Python** do `Videirafoo`.

## Objetivo

Construir um sistema simples de estoque com cadastro de produtos, entradas, saídas e alerta de estoque baixo.

## O que este projeto ensina

- funções;
- listas e dicionários;
- validação de números inteiros;
- regras de negócio;
- busca por nome e código;
- entrada e saída de estoque;
- prevenção de saldo negativo;
- estoque mínimo;
- persistência em JSON;
- testes automatizados;
- CI.

## Funcionalidades

- cadastrar produto;
- impedir código duplicado;
- registrar quantidade inicial;
- registrar estoque mínimo;
- adicionar entrada de estoque;
- registrar saída de estoque;
- bloquear saída maior que o saldo disponível;
- buscar produto por nome ou código;
- listar produtos;
- mostrar produtos com estoque baixo;
- excluir produto;
- persistir dados em JSON.

## Estrutura

```text
controle_estoque/
├── __init__.py
├── app.py
├── test_app.py
└── README.md
```

O arquivo `estoque.json` é criado automaticamente quando o programa salva os dados pela primeira vez.

## Como executar

```bash
python conteudos/mini_sistemas/controle_estoque/app.py
```

## Como testar

```bash
python -m unittest conteudos.mini_sistemas.controle_estoque.test_app
```

## Conceito importante: invariantes

Uma **invariante** é uma regra que deve continuar verdadeira em qualquer operação do sistema.

Neste projeto, algumas invariantes são:

- quantidade nunca pode ser negativa;
- estoque mínimo nunca pode ser negativo;
- código de produto não pode se repetir;
- uma saída nunca pode ser maior que o saldo disponível.

Essas regras são boas candidatas para testes automáticos porque podem ser verificadas de forma objetiva.

## Checklist de revisão

- [ ] código vazio é rejeitado;
- [ ] nome vazio é rejeitado;
- [ ] código duplicado é rejeitado;
- [ ] quantidade negativa é rejeitada;
- [ ] estoque mínimo negativo é rejeitado;
- [ ] entrada aumenta o estoque corretamente;
- [ ] saída diminui o estoque corretamente;
- [ ] saída maior que o saldo é bloqueada;
- [ ] estoque baixo é detectado;
- [ ] busca funciona por nome e código;
- [ ] JSON preserva os dados;
- [ ] testes passam na CI.

## Desafios para quem está estudando

Tente evoluir o sistema nesta ordem:

1. editar nome do produto;
2. editar estoque mínimo;
3. registrar histórico de movimentações;
4. ordenar por quantidade;
5. mostrar produto com maior estoque;
6. mostrar produtos zerados;
7. adicionar preço de custo e venda;
8. calcular valor total do estoque;
9. exportar relatório;
10. criar versão com banco de dados.

## Erros comuns

### Permitir saldo negativo

Isso quebra a regra principal do estoque. Valide antes de efetuar a saída.

### Usar nome como identificador

Nomes podem se repetir. O código do produto deve ser a chave de busca principal.

### Misturar regra de estoque com impressão

A função que altera quantidade deve cuidar da regra. A interface apenas apresenta mensagens.

## Próximo sistema

**Mini Sistema 05 — Sistema de Biblioteca**, introduzindo cadastro de livros, usuários, empréstimos e devoluções.
