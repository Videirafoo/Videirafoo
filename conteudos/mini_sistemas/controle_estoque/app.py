import json
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).with_name("estoque.json")


def carregar_produtos(caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    if not caminho.exists():
        return []

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        raise ValueError("O arquivo de estoque precisa conter uma lista.")

    return dados


def salvar_produtos(produtos, caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=2)


def proximo_id(produtos):
    if not produtos:
        return 1

    return max(produto["id"] for produto in produtos) + 1


def encontrar_por_codigo(produtos, codigo):
    codigo = str(codigo).strip().lower()

    for produto in produtos:
        if produto["codigo"].lower() == codigo:
            return produto

    return None


def validar_inteiro_nao_negativo(valor, campo):
    try:
        valor = int(valor)
    except (TypeError, ValueError) as erro:
        raise ValueError(f"{campo} precisa ser um número inteiro.") from erro

    if valor < 0:
        raise ValueError(f"{campo} não pode ser negativo.")

    return valor


def criar_produto(produtos, codigo, nome, quantidade=0, estoque_minimo=0):
    codigo = str(codigo).strip()
    nome = nome.strip()

    if not codigo:
        raise ValueError("O código do produto não pode ficar vazio.")

    if not nome:
        raise ValueError("O nome do produto não pode ficar vazio.")

    if encontrar_por_codigo(produtos, codigo):
        raise ValueError("Já existe um produto com esse código.")

    quantidade = validar_inteiro_nao_negativo(quantidade, "A quantidade")
    estoque_minimo = validar_inteiro_nao_negativo(estoque_minimo, "O estoque mínimo")

    produto = {
        "id": proximo_id(produtos),
        "codigo": codigo,
        "nome": nome,
        "quantidade": quantidade,
        "estoque_minimo": estoque_minimo,
    }

    produtos.append(produto)
    return produto


def entrada_estoque(produtos, codigo, quantidade):
    produto = encontrar_por_codigo(produtos, codigo)

    if not produto:
        return None

    quantidade = validar_inteiro_nao_negativo(quantidade, "A quantidade")

    if quantidade == 0:
        raise ValueError("A entrada precisa ser maior que zero.")

    produto["quantidade"] += quantidade
    return produto


def saida_estoque(produtos, codigo, quantidade):
    produto = encontrar_por_codigo(produtos, codigo)

    if not produto:
        return None

    quantidade = validar_inteiro_nao_negativo(quantidade, "A quantidade")

    if quantidade == 0:
        raise ValueError("A saída precisa ser maior que zero.")

    if quantidade > produto["quantidade"]:
        raise ValueError("Estoque insuficiente para essa saída.")

    produto["quantidade"] -= quantidade
    return produto


def buscar_produtos(produtos, termo):
    termo = termo.strip().lower()

    if not termo:
        return []

    return [
        produto
        for produto in produtos
        if termo in produto["nome"].lower()
        or termo in produto["codigo"].lower()
    ]


def produtos_com_estoque_baixo(produtos):
    return [
        produto
        for produto in produtos
        if produto["quantidade"] <= produto["estoque_minimo"]
    ]


def excluir_produto(produtos, codigo):
    produto = encontrar_por_codigo(produtos, codigo)

    if not produto:
        return None

    produtos.remove(produto)
    return produto


def exibir_produtos(produtos):
    if not produtos:
        print("Nenhum produto encontrado.")
        return

    for produto in produtos:
        alerta = " | ESTOQUE BAIXO" if produto["quantidade"] <= produto["estoque_minimo"] else ""
        print(
            f"{produto['codigo']} - {produto['nome']} | "
            f"Quantidade: {produto['quantidade']} | "
            f"Mínimo: {produto['estoque_minimo']}{alerta}"
        )


def mostrar_menu():
    print("\n=== Controle de Estoque ===")
    print("1. Cadastrar produto")
    print("2. Entrada de estoque")
    print("3. Saída de estoque")
    print("4. Buscar produto")
    print("5. Listar produtos")
    print("6. Mostrar estoque baixo")
    print("7. Excluir produto")
    print("0. Sair")


def main():
    produtos = carregar_produtos()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                codigo = input("Código: ")
                nome = input("Nome: ")
                quantidade = input("Quantidade inicial: ") or "0"
                estoque_minimo = input("Estoque mínimo: ") or "0"
                criar_produto(produtos, codigo, nome, quantidade, estoque_minimo)
                salvar_produtos(produtos)
                print("Produto cadastrado com sucesso.")

            elif opcao == "2":
                codigo = input("Código: ")
                quantidade = input("Quantidade de entrada: ")
                produto = entrada_estoque(produtos, codigo, quantidade)
                if produto:
                    salvar_produtos(produtos)
                    print("Entrada registrada.")
                else:
                    print("Produto não encontrado.")

            elif opcao == "3":
                codigo = input("Código: ")
                quantidade = input("Quantidade de saída: ")
                produto = saida_estoque(produtos, codigo, quantidade)
                if produto:
                    salvar_produtos(produtos)
                    print("Saída registrada.")
                else:
                    print("Produto não encontrado.")

            elif opcao == "4":
                termo = input("Nome ou código: ")
                exibir_produtos(buscar_produtos(produtos, termo))

            elif opcao == "5":
                exibir_produtos(produtos)

            elif opcao == "6":
                exibir_produtos(produtos_com_estoque_baixo(produtos))

            elif opcao == "7":
                codigo = input("Código: ")
                removido = excluir_produto(produtos, codigo)
                if removido:
                    salvar_produtos(produtos)
                    print("Produto excluído.")
                else:
                    print("Produto não encontrado.")

            elif opcao == "0":
                print("Até a próxima.")
                break

            else:
                print("Opção inválida.")

        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
