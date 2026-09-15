# Mini Sistema 06 — Caixa de Mercado

Sexto projeto da coleção **Mini Sistemas Python** do GitHub `Videirafoo`.

## Objetivo

Construir um caixa simples que conecte catálogo de produtos, carrinho, estoque, desconto e registro de vendas.

O foco é ensinar como várias regras de negócio passam a depender umas das outras dentro do mesmo sistema.

## O que este projeto ensina

- catálogo de produtos;
- código único por produto;
- preço unitário;
- carrinho de compras;
- quantidade por item;
- subtotal por item;
- subtotal da compra;
- desconto percentual;
- total final;
- validação de estoque;
- fechamento de venda;
- redução automática do estoque;
- histórico de vendas;
- persistência em JSON;
- funções separadas da interface;
- testes automatizados;
- CI.

## Funcionalidades

- cadastrar produto;
- listar produtos;
- adicionar item ao carrinho;
- acumular quantidade quando o mesmo produto é adicionado novamente;
- impedir venda acima do estoque disponível;
- remover item do carrinho;
- calcular subtotal;
- aplicar desconto de 0% a 100%;
- calcular total final;
- fechar venda;
- baixar o estoque apenas no fechamento;
- registrar a venda no histórico;
- salvar catálogo e vendas em JSON.

## Estrutura

```text
caixa_mercado/
├── __init__.py
├── app.py
├── test_app.py
└── README.md
```

O arquivo `caixa.json` é criado automaticamente quando o sistema salva os dados pela primeira vez.

## Como executar

Na raiz do repositório:

```bash
python conteudos/mini_sistemas/caixa_mercado/app.py
```

## Como testar

```bash
python -m unittest conteudos.mini_sistemas.caixa_mercado.test_app
```

A CI geral da coleção também executa automaticamente todos os arquivos `test_*.py` dos mini sistemas.

## Conceito importante: reservar não é vender

Ao adicionar um item ao carrinho, o estoque real ainda não é alterado.

O sistema apenas verifica se a quantidade total reservada no carrinho cabe no estoque atual.

A baixa definitiva ocorre somente quando `fechar_venda()` é executada.

Isso evita um erro comum em sistemas simples: diminuir o estoque antes de a compra realmente ser concluída.

## Conceito importante: invariantes

Algumas regras precisam permanecer verdadeiras o tempo todo:

- preço não pode ser negativo;
- estoque não pode ser negativo;
- quantidade deve ser maior que zero;
- desconto deve ficar entre 0 e 100;
- não é possível fechar um carrinho vazio;
- não é possível vender mais do que existe em estoque.

Essas regras são validadas de forma determinística pelo código e pelos testes.

## Exemplo de cálculo

Se o carrinho possui:

```text
2 x Arroz a R$ 10,00 = R$ 20,00
1 x Feijão a R$ 8,50 = R$ 8,50
```

Subtotal:

```text
R$ 28,50
```

Com desconto de 10%:

```text
Desconto: R$ 2,85
Total: R$ 25,65
```

## Checklist de revisão

Antes de considerar uma alteração pronta:

- [ ] produtos com código duplicado são rejeitados;
- [ ] preço negativo é rejeitado;
- [ ] estoque negativo é rejeitado;
- [ ] quantidade zero ou negativa é rejeitada;
- [ ] carrinho nunca ultrapassa o estoque disponível;
- [ ] subtotal é calculado corretamente;
- [ ] desconto inválido é rejeitado;
- [ ] total final considera o desconto;
- [ ] fechamento reduz o estoque corretamente;
- [ ] carrinho é limpo depois da venda;
- [ ] venda é adicionada ao histórico;
- [ ] JSON salva e carrega corretamente;
- [ ] testes passam na CI.

## Desafios para quem está estudando

Tente evoluir o projeto nesta ordem:

1. alterar a quantidade de um item já no carrinho;
2. aplicar desconto por item;
3. adicionar categoria aos produtos;
4. permitir busca por nome;
5. adicionar forma de pagamento;
6. registrar data e hora da venda;
7. calcular troco;
8. gerar relatório de faturamento;
9. mostrar produtos mais vendidos;
10. integrar o caixa ao mini sistema de controle de estoque.

## Próximo sistema

**Mini Sistema 07 — Controle Financeiro Pessoal**, introduzindo receitas, despesas, categorias, saldo, filtros e relatórios simples.
