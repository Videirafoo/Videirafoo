import json
from pathlib import Path

ARQUIVO_DADOS = Path(__file__).with_name("contatos.json")


def carregar_contatos(caminho=ARQUIVO_DADOS):
    caminho = Path(caminho)

    if not caminho.exists():
        return []

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        return []

    return dados if isinstance(dados, list) else []


def salvar_contatos(contatos, caminho=ARQUIVO_DADOS):
    caminho = Path(caminho)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(contatos, arquivo, ensure_ascii=False, indent=2)


def normalizar(texto):
    return texto.strip().casefold()


def buscar_indice(contatos, nome):
    nome_normalizado = normalizar(nome)

    for indice, contato in enumerate(contatos):
        if normalizar(contato.get("nome", "")) == nome_normalizado:
            return indice

    return -1


def criar_contato(nome, telefone, email=""):
    nome = nome.strip()
    telefone = telefone.strip()
    email = email.strip()

    if not nome:
        raise ValueError("O nome é obrigatório.")

    if not telefone:
        raise ValueError("O telefone é obrigatório.")

    return {
        "nome": nome,
        "telefone": telefone,
        "email": email,
    }


def adicionar_contato(contatos, contato):
    if buscar_indice(contatos, contato["nome"]) != -1:
        raise ValueError("Já existe um contato com esse nome.")

    contatos.append(contato)


def listar_contatos(contatos):
    if not contatos:
        print("Nenhum contato cadastrado.")
        return

    for numero, contato in enumerate(contatos, start=1):
        email = contato.get("email") or "não informado"
        print(
            f"{numero}. {contato['nome']} | "
            f"{contato['telefone']} | {email}"
        )


def cadastrar_interativo(contatos):
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("E-mail (opcional): ")

    try:
        contato = criar_contato(nome, telefone, email)
        adicionar_contato(contatos, contato)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return False

    print("Contato cadastrado.")
    return True


def buscar_interativo(contatos):
    nome = input("Nome para buscar: ")
    indice = buscar_indice(contatos, nome)

    if indice == -1:
        print("Contato não encontrado.")
        return

    contato = contatos[indice]
    print(f"Nome: {contato['nome']}")
    print(f"Telefone: {contato['telefone']}")
    print(f"E-mail: {contato.get('email') or 'não informado'}")


def editar_interativo(contatos):
    nome = input("Nome do contato que deseja editar: ")
    indice = buscar_indice(contatos, nome)

    if indice == -1:
        print("Contato não encontrado.")
        return False

    atual = contatos[indice]
    novo_nome = input(f"Nome [{atual['nome']}]: ").strip() or atual["nome"]
    novo_telefone = (
        input(f"Telefone [{atual['telefone']}]: ").strip()
        or atual["telefone"]
    )
    novo_email = (
        input(f"E-mail [{atual.get('email', '')}]: ").strip()
        or atual.get("email", "")
    )

    try:
        novo_contato = criar_contato(novo_nome, novo_telefone, novo_email)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return False

    indice_existente = buscar_indice(contatos, novo_nome)
    if indice_existente not in (-1, indice):
        print("Já existe outro contato com esse nome.")
        return False

    contatos[indice] = novo_contato
    print("Contato atualizado.")
    return True


def excluir_interativo(contatos):
    nome = input("Nome do contato que deseja excluir: ")
    indice = buscar_indice(contatos, nome)

    if indice == -1:
        print("Contato não encontrado.")
        return False

    removido = contatos.pop(indice)
    print(f"Contato '{removido['nome']}' excluído.")
    return True


def mostrar_menu():
    print("\n=== Agenda de Contatos ===")
    print("1 - Cadastrar")
    print("2 - Listar")
    print("3 - Buscar")
    print("4 - Editar")
    print("5 - Excluir")
    print("0 - Sair")


def main():
    contatos = carregar_contatos()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        alterou_dados = False

        if opcao == "1":
            alterou_dados = cadastrar_interativo(contatos)
        elif opcao == "2":
            listar_contatos(contatos)
        elif opcao == "3":
            buscar_interativo(contatos)
        elif opcao == "4":
            alterou_dados = editar_interativo(contatos)
        elif opcao == "5":
            alterou_dados = excluir_interativo(contatos)
        elif opcao == "0":
            salvar_contatos(contatos)
            print("Dados salvos. Até a próxima.")
            break
        else:
            print("Opção inválida.")

        if alterou_dados:
            salvar_contatos(contatos)


if __name__ == "__main__":
    main()
