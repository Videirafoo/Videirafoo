import json
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).with_name("biblioteca.json")


def novo_estado():
    return {
        "livros": [],
        "usuarios": [],
        "emprestimos": [],
    }


def carregar_dados(caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    if not caminho.exists():
        return novo_estado()

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, dict):
        raise ValueError("O arquivo da biblioteca precisa conter um objeto JSON.")

    for chave in ("livros", "usuarios", "emprestimos"):
        if chave not in dados or not isinstance(dados[chave], list):
            raise ValueError(f"A chave '{chave}' precisa conter uma lista.")

    return dados


def salvar_dados(dados, caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def proximo_id(itens):
    if not itens:
        return 1

    return max(item["id"] for item in itens) + 1


def encontrar_livro(dados, isbn):
    isbn = str(isbn).strip().lower()

    for livro in dados["livros"]:
        if livro["isbn"].lower() == isbn:
            return livro

    return None


def encontrar_usuario(dados, documento):
    documento = str(documento).strip().lower()

    for usuario in dados["usuarios"]:
        if usuario["documento"].lower() == documento:
            return usuario

    return None


def cadastrar_livro(dados, isbn, titulo, autor):
    isbn = str(isbn).strip()
    titulo = titulo.strip()
    autor = autor.strip()

    if not isbn:
        raise ValueError("O ISBN não pode ficar vazio.")
    if not titulo:
        raise ValueError("O título não pode ficar vazio.")
    if not autor:
        raise ValueError("O autor não pode ficar vazio.")
    if encontrar_livro(dados, isbn):
        raise ValueError("Já existe um livro com esse ISBN.")

    livro = {
        "id": proximo_id(dados["livros"]),
        "isbn": isbn,
        "titulo": titulo,
        "autor": autor,
        "disponivel": True,
    }

    dados["livros"].append(livro)
    return livro


def cadastrar_usuario(dados, nome, documento):
    nome = nome.strip()
    documento = str(documento).strip()

    if not nome:
        raise ValueError("O nome do usuário não pode ficar vazio.")
    if not documento:
        raise ValueError("O documento não pode ficar vazio.")
    if encontrar_usuario(dados, documento):
        raise ValueError("Já existe um usuário com esse documento.")

    usuario = {
        "id": proximo_id(dados["usuarios"]),
        "nome": nome,
        "documento": documento,
    }

    dados["usuarios"].append(usuario)
    return usuario


def encontrar_emprestimo_ativo(dados, isbn):
    isbn = str(isbn).strip().lower()

    for emprestimo in dados["emprestimos"]:
        if emprestimo["isbn"].lower() == isbn and not emprestimo["devolvido"]:
            return emprestimo

    return None


def emprestar_livro(dados, isbn, documento):
    livro = encontrar_livro(dados, isbn)
    usuario = encontrar_usuario(dados, documento)

    if not livro:
        raise ValueError("Livro não encontrado.")
    if not usuario:
        raise ValueError("Usuário não encontrado.")
    if not livro["disponivel"]:
        raise ValueError("Livro indisponível para empréstimo.")

    emprestimo = {
        "id": proximo_id(dados["emprestimos"]),
        "isbn": livro["isbn"],
        "documento": usuario["documento"],
        "devolvido": False,
    }

    dados["emprestimos"].append(emprestimo)
    livro["disponivel"] = False
    return emprestimo


def devolver_livro(dados, isbn):
    livro = encontrar_livro(dados, isbn)

    if not livro:
        raise ValueError("Livro não encontrado.")

    emprestimo = encontrar_emprestimo_ativo(dados, isbn)

    if not emprestimo:
        raise ValueError("Não existe empréstimo ativo para esse livro.")

    emprestimo["devolvido"] = True
    livro["disponivel"] = True
    return emprestimo


def buscar_livros(dados, termo):
    termo = termo.strip().lower()

    if not termo:
        return []

    return [
        livro
        for livro in dados["livros"]
        if termo in livro["titulo"].lower()
        or termo in livro["autor"].lower()
        or termo in livro["isbn"].lower()
    ]


def listar_emprestimos_ativos(dados):
    return [
        emprestimo
        for emprestimo in dados["emprestimos"]
        if not emprestimo["devolvido"]
    ]


def exibir_livros(livros):
    if not livros:
        print("Nenhum livro encontrado.")
        return

    for livro in livros:
        status = "disponível" if livro["disponivel"] else "emprestado"
        print(f"{livro['isbn']} - {livro['titulo']} | {livro['autor']} | {status}")


def exibir_emprestimos(dados):
    emprestimos = listar_emprestimos_ativos(dados)

    if not emprestimos:
        print("Nenhum empréstimo ativo.")
        return

    for emprestimo in emprestimos:
        livro = encontrar_livro(dados, emprestimo["isbn"])
        usuario = encontrar_usuario(dados, emprestimo["documento"])
        print(
            f"#{emprestimo['id']} - {livro['titulo']} -> "
            f"{usuario['nome']} ({usuario['documento']})"
        )


def mostrar_menu():
    print("\n=== Sistema de Biblioteca ===")
    print("1. Cadastrar livro")
    print("2. Cadastrar usuário")
    print("3. Emprestar livro")
    print("4. Devolver livro")
    print("5. Buscar livros")
    print("6. Listar livros")
    print("7. Listar empréstimos ativos")
    print("0. Sair")


def main():
    dados = carregar_dados()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                isbn = input("ISBN: ")
                titulo = input("Título: ")
                autor = input("Autor: ")
                cadastrar_livro(dados, isbn, titulo, autor)
                salvar_dados(dados)
                print("Livro cadastrado.")

            elif opcao == "2":
                nome = input("Nome: ")
                documento = input("Documento: ")
                cadastrar_usuario(dados, nome, documento)
                salvar_dados(dados)
                print("Usuário cadastrado.")

            elif opcao == "3":
                isbn = input("ISBN do livro: ")
                documento = input("Documento do usuário: ")
                emprestar_livro(dados, isbn, documento)
                salvar_dados(dados)
                print("Empréstimo registrado.")

            elif opcao == "4":
                isbn = input("ISBN do livro: ")
                devolver_livro(dados, isbn)
                salvar_dados(dados)
                print("Devolução registrada.")

            elif opcao == "5":
                termo = input("Título, autor ou ISBN: ")
                exibir_livros(buscar_livros(dados, termo))

            elif opcao == "6":
                exibir_livros(dados["livros"])

            elif opcao == "7":
                exibir_emprestimos(dados)

            elif opcao == "0":
                print("Até a próxima.")
                break

            else:
                print("Opção inválida.")

        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
