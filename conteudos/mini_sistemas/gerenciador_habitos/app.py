import json
from datetime import date, timedelta
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).with_name("habitos.json")


def carregar_habitos(caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    if not caminho.exists():
        return []

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        raise ValueError("O arquivo de hábitos precisa conter uma lista.")

    return dados


def salvar_habitos(habitos, caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(habitos, arquivo, ensure_ascii=False, indent=2)


def proximo_id(habitos):
    if not habitos:
        return 1

    return max(habito["id"] for habito in habitos) + 1


def criar_habito(habitos, nome, meta_semanal=7):
    nome = nome.strip()

    if not nome:
        raise ValueError("O nome do hábito não pode ficar vazio.")

    if not isinstance(meta_semanal, int) or not 1 <= meta_semanal <= 7:
        raise ValueError("A meta semanal deve ser um número inteiro entre 1 e 7.")

    if any(habito["nome"].lower() == nome.lower() for habito in habitos):
        raise ValueError("Já existe um hábito com esse nome.")

    habito = {
        "id": proximo_id(habitos),
        "nome": nome,
        "meta_semanal": meta_semanal,
        "registros": [],
    }

    habitos.append(habito)
    return habito


def encontrar_habito(habitos, habito_id):
    for habito in habitos:
        if habito["id"] == habito_id:
            return habito

    return None


def buscar_habitos(habitos, termo):
    termo = termo.strip().lower()

    if not termo:
        return []

    return [habito for habito in habitos if termo in habito["nome"].lower()]


def normalizar_data(data_registro=None):
    if data_registro is None:
        return date.today()

    if isinstance(data_registro, date):
        return data_registro

    try:
        return date.fromisoformat(str(data_registro))
    except ValueError as erro:
        raise ValueError("A data precisa estar no formato AAAA-MM-DD.") from erro


def registrar_conclusao(habito, data_registro=None):
    dia = normalizar_data(data_registro).isoformat()

    if dia not in habito["registros"]:
        habito["registros"].append(dia)
        habito["registros"].sort()

    return dia


def remover_conclusao(habito, data_registro=None):
    dia = normalizar_data(data_registro).isoformat()

    if dia in habito["registros"]:
        habito["registros"].remove(dia)
        return True

    return False


def calcular_sequencia(habito, data_referencia=None):
    referencia = normalizar_data(data_referencia)
    registros = {date.fromisoformat(valor) for valor in habito["registros"]}

    sequencia = 0
    atual = referencia

    while atual in registros:
        sequencia += 1
        atual -= timedelta(days=1)

    return sequencia


def progresso_semanal(habito, data_referencia=None):
    referencia = normalizar_data(data_referencia)
    inicio_semana = referencia - timedelta(days=referencia.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    total = 0
    for valor in habito["registros"]:
        dia = date.fromisoformat(valor)
        if inicio_semana <= dia <= fim_semana:
            total += 1

    meta = habito["meta_semanal"]
    percentual = min(100.0, (total / meta) * 100)

    return {
        "concluidos": total,
        "meta": meta,
        "percentual": round(percentual, 2),
    }


def resumo_habito(habito, data_referencia=None):
    progresso = progresso_semanal(habito, data_referencia)

    return {
        "id": habito["id"],
        "nome": habito["nome"],
        "sequencia": calcular_sequencia(habito, data_referencia),
        "concluidos_semana": progresso["concluidos"],
        "meta_semanal": progresso["meta"],
        "percentual": progresso["percentual"],
    }


def excluir_habito(habitos, habito_id):
    for indice, habito in enumerate(habitos):
        if habito["id"] == habito_id:
            return habitos.pop(indice)

    return None


def exibir_habitos(habitos):
    if not habitos:
        print("Nenhum hábito cadastrado.")
        return

    for habito in habitos:
        resumo = resumo_habito(habito)
        print(
            f"#{resumo['id']} - {resumo['nome']} | "
            f"sequência: {resumo['sequencia']} dia(s) | "
            f"semana: {resumo['concluidos_semana']}/{resumo['meta_semanal']} "
            f"({resumo['percentual']:.0f}%)"
        )


def ler_id(mensagem):
    try:
        return int(input(mensagem))
    except ValueError:
        print("Digite um número inteiro válido.")
        return None


def mostrar_menu():
    print("\n=== Gerenciador de Hábitos ===")
    print("1. Criar hábito")
    print("2. Listar hábitos")
    print("3. Buscar hábito")
    print("4. Registrar conclusão hoje")
    print("5. Remover conclusão de hoje")
    print("6. Excluir hábito")
    print("0. Sair")


def main():
    habitos = carregar_habitos()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do hábito: ")

            try:
                meta = int(input("Meta semanal (1 a 7): "))
                criar_habito(habitos, nome, meta)
                salvar_habitos(habitos)
                print("Hábito criado com sucesso.")
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "2":
            exibir_habitos(habitos)

        elif opcao == "3":
            termo = input("Buscar por: ")
            exibir_habitos(buscar_habitos(habitos, termo))

        elif opcao == "4":
            habito_id = ler_id("ID do hábito: ")
            if habito_id is None:
                continue

            habito = encontrar_habito(habitos, habito_id)
            if habito:
                registrar_conclusao(habito)
                salvar_habitos(habitos)
                print("Conclusão registrada.")
            else:
                print("Hábito não encontrado.")

        elif opcao == "5":
            habito_id = ler_id("ID do hábito: ")
            if habito_id is None:
                continue

            habito = encontrar_habito(habitos, habito_id)
            if habito and remover_conclusao(habito):
                salvar_habitos(habitos)
                print("Conclusão removida.")
            else:
                print("Nenhum registro de hoje encontrado para esse hábito.")

        elif opcao == "6":
            habito_id = ler_id("ID do hábito: ")
            if habito_id is None:
                continue

            removido = excluir_habito(habitos, habito_id)
            if removido:
                salvar_habitos(habitos)
                print("Hábito excluído.")
            else:
                print("Hábito não encontrado.")

        elif opcao == "0":
            print("Até a próxima.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
