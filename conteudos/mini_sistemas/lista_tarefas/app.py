import json
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).with_name("tarefas.json")
PRIORIDADES = {"baixa", "media", "alta"}


def carregar_tarefas(caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    if not caminho.exists():
        return []

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        raise ValueError("O arquivo de tarefas precisa conter uma lista.")

    return dados


def salvar_tarefas(tarefas, caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)


def proximo_id(tarefas):
    if not tarefas:
        return 1

    return max(tarefa["id"] for tarefa in tarefas) + 1


def criar_tarefa(tarefas, titulo, prioridade="media"):
    titulo = titulo.strip()
    prioridade = prioridade.strip().lower()

    if not titulo:
        raise ValueError("O título da tarefa não pode ficar vazio.")

    if prioridade not in PRIORIDADES:
        raise ValueError("A prioridade deve ser baixa, media ou alta.")

    tarefa = {
        "id": proximo_id(tarefas),
        "titulo": titulo,
        "prioridade": prioridade,
        "concluida": False,
    }

    tarefas.append(tarefa)
    return tarefa


def buscar_tarefas(tarefas, termo):
    termo = termo.strip().lower()

    if not termo:
        return []

    return [
        tarefa
        for tarefa in tarefas
        if termo in tarefa["titulo"].lower()
    ]


def concluir_tarefa(tarefas, tarefa_id):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            tarefa["concluida"] = True
            return tarefa

    return None


def excluir_tarefa(tarefas, tarefa_id):
    for indice, tarefa in enumerate(tarefas):
        if tarefa["id"] == tarefa_id:
            return tarefas.pop(indice)

    return None


def filtrar_tarefas(tarefas, status="todas"):
    status = status.lower()

    if status == "todas":
        return list(tarefas)
    if status == "pendentes":
        return [tarefa for tarefa in tarefas if not tarefa["concluida"]]
    if status == "concluidas":
        return [tarefa for tarefa in tarefas if tarefa["concluida"]]

    raise ValueError("Status inválido.")


def exibir_tarefas(tarefas):
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return

    for tarefa in tarefas:
        marcador = "x" if tarefa["concluida"] else " "
        print(
            f"[{marcador}] #{tarefa['id']} - {tarefa['titulo']} "
            f"({tarefa['prioridade']})"
        )


def ler_id(mensagem):
    try:
        return int(input(mensagem))
    except ValueError:
        print("Digite um número inteiro válido.")
        return None


def mostrar_menu():
    print("\n=== Lista de Tarefas ===")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Buscar tarefa")
    print("4. Concluir tarefa")
    print("5. Excluir tarefa")
    print("6. Listar pendentes")
    print("7. Listar concluídas")
    print("0. Sair")


def main():
    tarefas = carregar_tarefas()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            titulo = input("Título: ")
            prioridade = input("Prioridade (baixa/media/alta): ") or "media"

            try:
                criar_tarefa(tarefas, titulo, prioridade)
                salvar_tarefas(tarefas)
                print("Tarefa criada com sucesso.")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "2":
            exibir_tarefas(filtrar_tarefas(tarefas))

        elif opcao == "3":
            termo = input("Buscar por: ")
            exibir_tarefas(buscar_tarefas(tarefas, termo))

        elif opcao == "4":
            tarefa_id = ler_id("ID da tarefa: ")
            if tarefa_id is None:
                continue

            tarefa = concluir_tarefa(tarefas, tarefa_id)
            if tarefa:
                salvar_tarefas(tarefas)
                print("Tarefa concluída.")
            else:
                print("Tarefa não encontrada.")

        elif opcao == "5":
            tarefa_id = ler_id("ID da tarefa: ")
            if tarefa_id is None:
                continue

            tarefa = excluir_tarefa(tarefas, tarefa_id)
            if tarefa:
                salvar_tarefas(tarefas)
                print("Tarefa excluída.")
            else:
                print("Tarefa não encontrada.")

        elif opcao == "6":
            exibir_tarefas(filtrar_tarefas(tarefas, "pendentes"))

        elif opcao == "7":
            exibir_tarefas(filtrar_tarefas(tarefas, "concluidas"))

        elif opcao == "0":
            print("Até a próxima.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
