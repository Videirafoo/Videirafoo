import json
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).with_name("alunos.json")


def carregar_alunos(caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    if not caminho.exists():
        return []

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        raise ValueError("O arquivo de alunos precisa conter uma lista.")

    return dados


def salvar_alunos(alunos, caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(alunos, arquivo, ensure_ascii=False, indent=2)


def proximo_id(alunos):
    if not alunos:
        return 1

    return max(aluno["id"] for aluno in alunos) + 1


def encontrar_por_matricula(alunos, matricula):
    matricula = str(matricula).strip().lower()

    for aluno in alunos:
        if aluno["matricula"].lower() == matricula:
            return aluno

    return None


def criar_aluno(alunos, nome, matricula):
    nome = nome.strip()
    matricula = str(matricula).strip()

    if not nome:
        raise ValueError("O nome do aluno não pode ficar vazio.")

    if not matricula:
        raise ValueError("A matrícula não pode ficar vazia.")

    if encontrar_por_matricula(alunos, matricula):
        raise ValueError("Já existe um aluno com essa matrícula.")

    aluno = {
        "id": proximo_id(alunos),
        "nome": nome,
        "matricula": matricula,
        "notas": [],
    }

    alunos.append(aluno)
    return aluno


def validar_nota(nota):
    try:
        nota = float(nota)
    except (TypeError, ValueError) as erro:
        raise ValueError("A nota precisa ser numérica.") from erro

    if nota < 0 or nota > 10:
        raise ValueError("A nota precisa estar entre 0 e 10.")

    return nota


def adicionar_nota(alunos, matricula, nota):
    aluno = encontrar_por_matricula(alunos, matricula)

    if not aluno:
        return None

    aluno["notas"].append(validar_nota(nota))
    return aluno


def calcular_media(aluno):
    notas = aluno.get("notas", [])

    if not notas:
        return None

    return sum(notas) / len(notas)


def calcular_situacao(aluno):
    media = calcular_media(aluno)

    if media is None:
        return "sem notas"
    if media >= 7:
        return "aprovado"
    if media >= 5:
        return "recuperacao"

    return "reprovado"


def buscar_alunos(alunos, termo):
    termo = termo.strip().lower()

    if not termo:
        return []

    return [
        aluno
        for aluno in alunos
        if termo in aluno["nome"].lower()
        or termo in aluno["matricula"].lower()
    ]


def excluir_aluno(alunos, matricula):
    aluno = encontrar_por_matricula(alunos, matricula)

    if not aluno:
        return None

    alunos.remove(aluno)
    return aluno


def gerar_relatorio(alunos):
    relatorio = []

    for aluno in alunos:
        media = calcular_media(aluno)
        relatorio.append(
            {
                "matricula": aluno["matricula"],
                "nome": aluno["nome"],
                "media": None if media is None else round(media, 2),
                "situacao": calcular_situacao(aluno),
            }
        )

    return relatorio


def exibir_relatorio(alunos):
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    for item in gerar_relatorio(alunos):
        media = "sem notas" if item["media"] is None else f"{item['media']:.2f}"
        print(
            f"{item['matricula']} - {item['nome']} | "
            f"Média: {media} | Situação: {item['situacao']}"
        )


def mostrar_menu():
    print("\n=== Cadastro de Alunos ===")
    print("1. Cadastrar aluno")
    print("2. Adicionar nota")
    print("3. Buscar aluno")
    print("4. Exibir relatório")
    print("5. Excluir aluno")
    print("0. Sair")


def main():
    alunos = carregar_alunos()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome: ")
            matricula = input("Matrícula: ")

            try:
                criar_aluno(alunos, nome, matricula)
                salvar_alunos(alunos)
                print("Aluno cadastrado com sucesso.")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "2":
            matricula = input("Matrícula: ")
            nota = input("Nota (0 a 10): ")

            try:
                aluno = adicionar_nota(alunos, matricula, nota)
                if aluno:
                    salvar_alunos(alunos)
                    print("Nota adicionada.")
                else:
                    print("Aluno não encontrado.")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "3":
            termo = input("Nome ou matrícula: ")
            encontrados = buscar_alunos(alunos, termo)
            exibir_relatorio(encontrados)

        elif opcao == "4":
            exibir_relatorio(alunos)

        elif opcao == "5":
            matricula = input("Matrícula: ")
            removido = excluir_aluno(alunos, matricula)

            if removido:
                salvar_alunos(alunos)
                print("Aluno excluído.")
            else:
                print("Aluno não encontrado.")

        elif opcao == "0":
            print("Até a próxima.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
