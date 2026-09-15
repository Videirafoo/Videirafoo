import json
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).with_name("caixa.json")


def carregar_dados(caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    if not caminho.exists():
        return {"produtos": [], "vendas": []}

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, dict):
        raise ValueError("O arquivo do caixa precisa conter um objeto JSON.")

    dados.setdefault("produtos", [])
    dados.setdefault("vendas", [])
    return dados


def salvar_dados(dados, caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def proximo_id(registros):
    if not registros:
        return 1
    return max(registro["id"] for registro in registros) + 1


def buscar_produto(produtos, codigo):
    codigo = codigo.strip().lower()
    for produto in produtos:
        if produto["codigo"].lower() == codigo:
            return produto
    return None


def cadastrar_produto(produtos, codigo, nome, preco, estoque=0):
    codigo = codigo.strip()
    nome = nome.strip()

    if not codigo:
        raise ValueError("O código não pode ficar vazio.")
    if not nome:
        raise ValueError("O nome não pode ficar vazio.")
    if buscar_produto(produtos, codigo):
        raise ValueError("Já existe um produto com esse código.")

    preco = float(preco)
    estoque = int(estoque)

    if preco < 0:
        raise ValueError("O preço não pode ser negativo.")
    if estoque < 0:
        raise ValueError("O estoque não pode ser negativo.")

    produto = {
        "id": proximo_id(produtos),
        "codigo": codigo,
        "nome": nome,
        "preco": round(preco, 2),
        "estoque": estoque,
    }
    produtos.append(produto)
    return produto


def quantidade_no_carrinho(carrinho, codigo):
    return sum(
        item["quantidade"]
        for item in carrinho
        if item["codigo"].lower() == codigo.lower()
    )


def adicionar_ao_carrinho(carrinho, produtos, codigo, quantidade):
    produto = buscar_produto(produtos, codigo)
    if produto is None:
        raise ValueError("Produto não encontrado.")

    quantidade = int(quantidade)
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    reservada = quantidade_no_carrinho(carrinho, produto["codigo"])
    if reservada + quantidade > produto["estoque"]:
        raise ValueError("Estoque insuficiente para essa quantidade.")

    for item in carrinho:
        if item["codigo"].lower() == produto["codigo"].lower():
            item["quantidade"] += quantidade
            item["subtotal"] = round(item["quantidade"] * item["preco_unitario"], 2)
            return item

    item = {
        "codigo": produto["codigo"],
        "nome": produto["nome"],
        "quantidade": quantidade,
        "preco_unitario": produto["preco"],
        "subtotal": round(quantidade * produto["preco"], 2),
    }
    carrinho.append(item)
    return item


def remover_do_carrinho(carrinho, codigo):
    for indice, item in enumerate(carrinho):
        if item["codigo"].lower() == codigo.strip().lower():
            return carrinho.pop(indice)
    return None


def calcular_subtotal(carrinho):
    return round(sum(item["subtotal"] for item in carrinho), 2)


def calcular_desconto(subtotal, desconto_percentual):
    desconto_percentual = float(desconto_percentual)
    if desconto_percentual < 0 or desconto_percentual > 100:
        raise ValueError("O desconto deve estar entre 0 e 100.")
    return round(subtotal * (desconto_percentual / 100), 2)


def calcular_total(carrinho, desconto_percentual=0):
    subtotal = calcular_subtotal(carrinho)
    desconto = calcular_desconto(subtotal, desconto_percentual)
    return round(subtotal - desconto, 2)


def fechar_venda(produtos, vendas, carrinho, desconto_percentual=0):
    if not carrinho:
        raise ValueError("O carrinho está vazio.")

    for item in carrinho:
        produto = buscar_produto(produtos, item["codigo"])
        if produto is None:
            raise ValueError(f"Produto {item['codigo']} não existe mais.")
        if item["quantidade"] > produto["estoque"]:
            raise ValueError(f"Estoque insuficiente para {produto['nome']}.")

    subtotal = calcular_subtotal(carrinho)
    valor_desconto = calcular_desconto(subtotal, desconto_percentual)
    total = round(subtotal - valor_desconto, 2)

    for item in carrinho:
        produto = buscar_produto(produtos, item["codigo"])
        produto["estoque"] -= item["quantidade"]

    venda = {
        "id": proximo_id(vendas),
        "itens": [dict(item) for item in carrinho],
        "subtotal": subtotal,
        "desconto_percentual": float(desconto_percentual),
        "valor_desconto": valor_desconto,
        "total": total,
    }
    vendas.append(venda)
    carrinho.clear()
    return venda


def exibir_produtos(produtos):
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        print(
            f"{produto['codigo']} - {produto['nome']} | "
            f"R$ {produto['preco']:.2f} | estoque: {produto['estoque']}"
        )


def exibir_carrinho(carrinho):
    if not carrinho:
        print("Carrinho vazio.")
        return

    for item in carrinho:
        print(
            f"{item['codigo']} - {item['nome']} | "
            f"{item['quantidade']} x R$ {item['preco_unitario']:.2f} = "
            f"R$ {item['subtotal']:.2f}"
        )
    print(f"Subtotal: R$ {calcular_subtotal(carrinho):.2f}")


def mostrar_menu():
    print("\n=== Caixa de Mercado ===")
    print("1. Cadastrar produto")
    print("2. Listar produtos")
    print("3. Adicionar item ao carrinho")
    print("4. Ver carrinho")
    print("5. Remover item do carrinho")
    print("6. Fechar venda")
    print("7. Listar vendas")
    print("0. Sair")


def main():
    dados = carregar_dados()
    produtos = dados["produtos"]
    vendas = dados["vendas"]
    carrinho = []

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                codigo = input("Código: ")
                nome = input("Nome: ")
                preco = float(input("Preço: "))
                estoque = int(input("Estoque inicial: "))
                cadastrar_produto(produtos, codigo, nome, preco, estoque)
                salvar_dados(dados)
                print("Produto cadastrado.")

            elif opcao == "2":
                exibir_produtos(produtos)

            elif opcao == "3":
                codigo = input("Código do produto: ")
                quantidade = int(input("Quantidade: "))
                adicionar_ao_carrinho(carrinho, produtos, codigo, quantidade)
                print("Item adicionado ao carrinho.")

            elif opcao == "4":
                exibir_carrinho(carrinho)

            elif opcao == "5":
                codigo = input("Código do item: ")
                removido = remover_do_carrinho(carrinho, codigo)
                print("Item removido." if removido else "Item não encontrado.")

            elif opcao == "6":
                desconto = float(input("Desconto em % (0 para nenhum): ") or 0)
                venda = fechar_venda(produtos, vendas, carrinho, desconto)
                salvar_dados(dados)
                print(f"Venda #{venda['id']} concluída. Total: R$ {venda['total']:.2f}")

            elif opcao == "7":
                if not vendas:
                    print("Nenhuma venda registrada.")
                for venda in vendas:
                    print(f"Venda #{venda['id']} - Total: R$ {venda['total']:.2f}")

            elif opcao == "0":
                print("Até a próxima.")
                break

            else:
                print("Opção inválida.")

        except (ValueError, TypeError) as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
