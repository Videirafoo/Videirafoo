import json
from datetime import date
from pathlib import Path

ARQUIVO_PADRAO = Path(__file__).with_name("financeiro.json")
TIPOS = {"receita", "despesa"}


def carregar_dados(caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    if not caminho.exists():
        return {"lancamentos": []}

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, dict) or not isinstance(dados.get("lancamentos"), list):
        raise ValueError("O arquivo financeiro está em formato inválido.")

    return dados


def salvar_dados(dados, caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def proximo_id(lancamentos):
    if not lancamentos:
        return 1

    return max(lancamento["id"] for lancamento in lancamentos) + 1


def validar_data(data_texto):
    try:
        return date.fromisoformat(data_texto).isoformat()
    except ValueError as erro:
        raise ValueError("Use uma data válida no formato AAAA-MM-DD.") from erro


def adicionar_lancamento(
    dados,
    tipo,
    descricao,
    valor,
    categoria,
    data_lancamento=None,
):
    tipo = tipo.strip().lower()
    descricao = descricao.strip()
    categoria = categoria.strip()
    valor = float(valor)

    if tipo not in TIPOS:
        raise ValueError("O tipo deve ser receita ou despesa.")
    if not descricao:
        raise ValueError("A descrição não pode ficar vazia.")
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")
    if not categoria:
        raise ValueError("A categoria não pode ficar vazia.")

    if data_lancamento is None:
        data_lancamento = date.today().isoformat()
    else:
        data_lancamento = validar_data(data_lancamento)

    lancamento = {
        "id": proximo_id(dados["lancamentos"]),
        "tipo": tipo,
        "descricao": descricao,
        "valor": round(valor, 2),
        "categoria": categoria,
        "data": data_lancamento,
    }

    dados["lancamentos"].append(lancamento)
    return lancamento


def excluir_lancamento(dados, lancamento_id):
    for indice, lancamento in enumerate(dados["lancamentos"]):
        if lancamento["id"] == lancamento_id:
            return dados["lancamentos"].pop(indice)

    return None


def filtrar_lancamentos(dados, tipo=None, categoria=None, mes=None):
    resultado = list(dados["lancamentos"])

    if tipo:
        tipo = tipo.strip().lower()
        if tipo not in TIPOS:
            raise ValueError("Filtro de tipo inválido.")
        resultado = [item for item in resultado if item["tipo"] == tipo]

    if categoria:
        categoria_normalizada = categoria.strip().lower()
        resultado = [
            item
            for item in resultado
            if item["categoria"].strip().lower() == categoria_normalizada
        ]

    if mes:
        mes = mes.strip()
        if len(mes) != 7 or mes[4] != "-":
            raise ValueError("Use o mês no formato AAAA-MM.")

        try:
            ano_numero = int(mes[:4])
            mes_numero = int(mes[5:])
        except ValueError as erro:
            raise ValueError("Use o mês no formato AAAA-MM.") from erro

        if ano_numero < 1 or not 1 <= mes_numero <= 12:
            raise ValueError("Use um mês válido no formato AAAA-MM.")

        resultado = [item for item in resultado if item["data"].startswith(mes)]

    return resultado


def calcular_totais(lancamentos):
    receitas = sum(
        item["valor"] for item in lancamentos if item["tipo"] == "receita"
    )
    despesas = sum(
        item["valor"] for item in lancamentos if item["tipo"] == "despesa"
    )

    receitas = round(receitas, 2)
    despesas = round(despesas, 2)

    return {
        "receitas": receitas,
        "despesas": despesas,
        "saldo": round(receitas - despesas, 2),
    }


def resumo_por_categoria(lancamentos):
    resumo = {}

    for item in lancamentos:
        categoria = item["categoria"]

        if categoria not in resumo:
            resumo[categoria] = {"receitas": 0.0, "despesas": 0.0}

        chave = "receitas" if item["tipo"] == "receita" else "despesas"
        resumo[categoria][chave] += item["valor"]

    for valores in resumo.values():
        valores["receitas"] = round(valores["receitas"], 2)
        valores["despesas"] = round(valores["despesas"], 2)
        valores["saldo"] = round(valores["receitas"] - valores["despesas"], 2)

    return resumo


def exibir_lancamentos(lancamentos):
    if not lancamentos:
        print("Nenhum lançamento encontrado.")
        return

    for item in lancamentos:
        sinal = "+" if item["tipo"] == "receita" else "-"
        print(
            f"#{item['id']} | {item['data']} | {item['categoria']} | "
            f"{item['descricao']} | {sinal} R$ {item['valor']:.2f}"
        )


def exibir_resumo(lancamentos):
    totais = calcular_totais(lancamentos)

    print(f"Receitas: R$ {totais['receitas']:.2f}")
    print(f"Despesas: R$ {totais['despesas']:.2f}")
    print(f"Saldo: R$ {totais['saldo']:.2f}")


def ler_float(mensagem):
    try:
        return float(input(mensagem).replace(",", "."))
    except ValueError:
        print("Digite um valor numérico válido.")
        return None


def ler_int(mensagem):
    try:
        return int(input(mensagem))
    except ValueError:
        print("Digite um número inteiro válido.")
        return None


def mostrar_menu():
    print("\n=== Controle Financeiro Pessoal ===")
    print("1. Adicionar receita")
    print("2. Adicionar despesa")
    print("3. Listar lançamentos")
    print("4. Mostrar resumo")
    print("5. Filtrar por categoria")
    print("6. Filtrar por mês")
    print("7. Excluir lançamento")
    print("8. Resumo por categoria")
    print("0. Sair")


def registrar_pelo_terminal(dados, tipo):
    descricao = input("Descrição: ")
    categoria = input("Categoria: ")
    valor = ler_float("Valor: R$ ")

    if valor is None:
        return

    data_texto = input("Data (AAAA-MM-DD, Enter = hoje): ").strip() or None

    try:
        adicionar_lancamento(
            dados,
            tipo,
            descricao,
            valor,
            categoria,
            data_texto,
        )
        salvar_dados(dados)
        print("Lançamento salvo com sucesso.")
    except ValueError as erro:
        print(f"Erro: {erro}")


def main():
    dados = carregar_dados()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            registrar_pelo_terminal(dados, "receita")

        elif opcao == "2":
            registrar_pelo_terminal(dados, "despesa")

        elif opcao == "3":
            exibir_lancamentos(dados["lancamentos"])

        elif opcao == "4":
            exibir_resumo(dados["lancamentos"])

        elif opcao == "5":
            categoria = input("Categoria: ")
            exibir_lancamentos(filtrar_lancamentos(dados, categoria=categoria))

        elif opcao == "6":
            mes = input("Mês (AAAA-MM): ")
            try:
                exibir_lancamentos(filtrar_lancamentos(dados, mes=mes))
            except ValueError as erro:
                print(f"Erro: {erro}")

        elif opcao == "7":
            lancamento_id = ler_int("ID do lançamento: ")
            if lancamento_id is None:
                continue

            removido = excluir_lancamento(dados, lancamento_id)
            if removido:
                salvar_dados(dados)
                print("Lançamento excluído.")
            else:
                print("Lançamento não encontrado.")

        elif opcao == "8":
            resumo = resumo_por_categoria(dados["lancamentos"])
            if not resumo:
                print("Nenhuma categoria encontrada.")
            else:
                for categoria, valores in resumo.items():
                    print(
                        f"{categoria}: receitas R$ {valores['receitas']:.2f} | "
                        f"despesas R$ {valores['despesas']:.2f} | "
                        f"saldo R$ {valores['saldo']:.2f}"
                    )

        elif opcao == "0":
            print("Até a próxima.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
