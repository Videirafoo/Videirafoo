from copy import deepcopy
from datetime import date

from conteudos.mini_sistemas.caixa_mercado.app import (
    adicionar_ao_carrinho,
    cadastrar_produto,
    calcular_subtotal,
    calcular_total,
    fechar_venda,
    remover_do_carrinho,
)
from conteudos.mini_sistemas.controle_financeiro.app import (
    adicionar_lancamento,
    calcular_totais,
    excluir_lancamento,
)
from conteudos.mini_sistemas.gerenciador_habitos.app import (
    criar_habito,
    encontrar_habito,
    excluir_habito,
    registrar_conclusao,
    remover_conclusao,
    resumo_habito,
)
from conteudos.mini_sistemas.sistema_biblioteca.app import (
    cadastrar_livro,
    cadastrar_usuario,
    devolver_livro,
    emprestar_livro,
    novo_estado,
)


MAX_ITENS_LAB = 50


def _limitar_lista(valor, nome):
    if valor is None:
        return []
    if not isinstance(valor, list):
        raise ValueError(f"{nome} precisa ser uma lista.")
    if len(valor) > MAX_ITENS_LAB:
        raise ValueError(f"{nome} aceita no máximo {MAX_ITENS_LAB} itens no laboratório.")
    return valor


# 05 — Biblioteca

def normalizar_biblioteca_lab(estado):
    if estado is None:
        estado = {}
    if not isinstance(estado, dict):
        raise ValueError("O estado da biblioteca precisa ser um objeto JSON.")

    livros = _limitar_lista(estado.get("livros"), "Livros")
    usuarios = _limitar_lista(estado.get("usuarios"), "Usuários")
    emprestimos = _limitar_lista(estado.get("emprestimos"), "Empréstimos")

    dados = novo_estado()
    for item in livros:
        if not isinstance(item, dict):
            raise ValueError("Cada livro precisa ser um objeto JSON.")
        cadastrar_livro(
            dados,
            str(item.get("isbn", "")),
            str(item.get("titulo", "")),
            str(item.get("autor") or "Autor do laboratório"),
        )

    for item in usuarios:
        if not isinstance(item, dict):
            raise ValueError("Cada usuário precisa ser um objeto JSON.")
        cadastrar_usuario(
            dados,
            str(item.get("nome", "")),
            str(item.get("documento", "")),
        )

    for item in emprestimos:
        if not isinstance(item, dict):
            raise ValueError("Cada empréstimo precisa ser um objeto JSON.")
        emprestar_livro(dados, str(item.get("isbn", "")), str(item.get("documento", "")))
        if bool(item.get("devolvido", False)):
            devolver_livro(dados, str(item.get("isbn", "")))

    return dados


def biblioteca_operacao_lab(estado, acao, dados):
    biblioteca = normalizar_biblioteca_lab(estado)
    if not isinstance(dados, dict):
        raise ValueError("Os dados da operação precisam ser um objeto JSON.")

    if acao == "cadastrar_livro":
        resultado = cadastrar_livro(
            biblioteca,
            str(dados.get("isbn", "")),
            str(dados.get("titulo", "")),
            str(dados.get("autor", "")),
        )
    elif acao == "cadastrar_usuario":
        resultado = cadastrar_usuario(
            biblioteca,
            str(dados.get("nome", "")),
            str(dados.get("documento", "")),
        )
    elif acao == "emprestar":
        resultado = emprestar_livro(
            biblioteca,
            str(dados.get("isbn", "")),
            str(dados.get("documento", "")),
        )
    elif acao == "devolver":
        resultado = devolver_livro(biblioteca, str(dados.get("isbn", "")))
    else:
        raise ValueError("Ação de biblioteca não reconhecida.")

    return {"estado": biblioteca, "resultado": deepcopy(resultado)}


# 06 — Caixa de mercado

def normalizar_caixa_lab(estado):
    if estado is None:
        estado = {}
    if not isinstance(estado, dict):
        raise ValueError("O estado do caixa precisa ser um objeto JSON.")

    produtos_entrada = _limitar_lista(estado.get("produtos"), "Produtos")
    carrinho_entrada = _limitar_lista(estado.get("carrinho"), "Carrinho")
    vendas_entrada = _limitar_lista(estado.get("vendas"), "Vendas")

    produtos = []
    for indice, item in enumerate(produtos_entrada, start=1):
        if not isinstance(item, dict):
            raise ValueError("Cada produto precisa ser um objeto JSON.")
        codigo = str(item.get("codigo") or f"LAB-{indice}")
        cadastrar_produto(
            produtos,
            codigo,
            str(item.get("nome", "")),
            item.get("preco", 0),
            item.get("estoque", 0),
        )

    carrinho = []
    for item in carrinho_entrada:
        if not isinstance(item, dict):
            raise ValueError("Cada item do carrinho precisa ser um objeto JSON.")
        codigo = item.get("codigo")
        if not codigo and item.get("produtoId") is not None:
            produto = next(
                (produto for produto in produtos if str(produto["id"]) == str(item.get("produtoId"))),
                None,
            )
            codigo = produto["codigo"] if produto else ""
        adicionar_ao_carrinho(carrinho, produtos, str(codigo or ""), item.get("quantidade", 0))

    vendas = []
    for indice, item in enumerate(vendas_entrada, start=1):
        if not isinstance(item, dict):
            raise ValueError("Cada venda precisa ser um objeto JSON.")
        copia = deepcopy(item)
        copia["id"] = int(copia.get("id") or indice)
        vendas.append(copia)

    return {"produtos": produtos, "carrinho": carrinho, "vendas": vendas}


def resumo_caixa_lab(estado, desconto=0):
    subtotal = calcular_subtotal(estado["carrinho"])
    total = calcular_total(estado["carrinho"], desconto)
    return {
        "subtotal": subtotal,
        "desconto_percentual": float(desconto),
        "total": total,
    }


def caixa_operacao_lab(estado, acao, dados):
    caixa = normalizar_caixa_lab(estado)
    if not isinstance(dados, dict):
        raise ValueError("Os dados da operação precisam ser um objeto JSON.")

    if acao == "cadastrar_produto":
        proximo = len(caixa["produtos"]) + 1
        resultado = cadastrar_produto(
            caixa["produtos"],
            str(dados.get("codigo") or f"LAB-{proximo}"),
            str(dados.get("nome", "")),
            dados.get("preco", 0),
            dados.get("estoque", 0),
        )
    elif acao == "adicionar_carrinho":
        resultado = adicionar_ao_carrinho(
            caixa["carrinho"],
            caixa["produtos"],
            str(dados.get("codigo", "")),
            dados.get("quantidade", 0),
        )
    elif acao == "remover_carrinho":
        resultado = remover_do_carrinho(caixa["carrinho"], str(dados.get("codigo", "")))
        if resultado is None:
            return None
    elif acao == "fechar_venda":
        resultado = fechar_venda(
            caixa["produtos"],
            caixa["vendas"],
            caixa["carrinho"],
            dados.get("desconto", 0),
        )
    else:
        raise ValueError("Ação de caixa não reconhecida.")

    desconto = dados.get("desconto", 0)
    return {
        "estado": caixa,
        "resultado": deepcopy(resultado),
        "resumo": resumo_caixa_lab(caixa, desconto if caixa["carrinho"] else 0),
    }


# 07 — Controle financeiro

def normalizar_financeiro_lab(estado):
    lancamentos_entrada = _limitar_lista(estado, "Lançamentos")
    dados = {"lancamentos": []}
    for item in lancamentos_entrada:
        if not isinstance(item, dict):
            raise ValueError("Cada lançamento precisa ser um objeto JSON.")
        adicionar_lancamento(
            dados,
            str(item.get("tipo", "")),
            str(item.get("descricao", "")),
            item.get("valor", 0),
            str(item.get("categoria", "")),
            item.get("data") or date.today().isoformat(),
        )
    return dados


def financeiro_operacao_lab(estado, acao, dados):
    financeiro = normalizar_financeiro_lab(estado)
    if not isinstance(dados, dict):
        raise ValueError("Os dados da operação precisam ser um objeto JSON.")

    if acao == "adicionar":
        resultado = adicionar_lancamento(
            financeiro,
            str(dados.get("tipo", "")),
            str(dados.get("descricao", "")),
            dados.get("valor", 0),
            str(dados.get("categoria", "")),
            dados.get("data") or date.today().isoformat(),
        )
    elif acao == "excluir":
        lancamento_id = dados.get("id")
        if not isinstance(lancamento_id, int) or lancamento_id <= 0:
            raise ValueError("Informe um id inteiro positivo.")
        resultado = excluir_lancamento(financeiro, lancamento_id)
        if resultado is None:
            return None
    else:
        raise ValueError("Ação financeira não reconhecida.")

    return {
        "lancamentos": financeiro["lancamentos"],
        "resultado": deepcopy(resultado),
        "totais": calcular_totais(financeiro["lancamentos"]),
    }


# 08 — Gerenciador de hábitos

def normalizar_habitos_lab(estado):
    entrada = _limitar_lista(estado, "Hábitos")
    habitos = []
    for item in entrada:
        if not isinstance(item, dict):
            raise ValueError("Cada hábito precisa ser um objeto JSON.")
        meta = item.get("meta_semanal", item.get("meta", 7))
        habito = criar_habito(habitos, str(item.get("nome", "")), int(meta))
        for registro in _limitar_lista(item.get("registros"), "Registros do hábito"):
            registrar_conclusao(habito, str(registro))
    return habitos


def _resumos_habitos(habitos, data_referencia=None):
    return [resumo_habito(habito, data_referencia) for habito in habitos]


def habito_operacao_lab(estado, acao, dados):
    habitos = normalizar_habitos_lab(estado)
    if not isinstance(dados, dict):
        raise ValueError("Os dados da operação precisam ser um objeto JSON.")

    data_referencia = dados.get("data") or None

    if acao == "criar":
        resultado = criar_habito(
            habitos,
            str(dados.get("nome", "")),
            int(dados.get("meta", 7)),
        )
    else:
        habito_id = dados.get("id")
        if not isinstance(habito_id, int) or habito_id <= 0:
            raise ValueError("Informe um id inteiro positivo.")
        habito = encontrar_habito(habitos, habito_id)
        if habito is None:
            return None

        if acao == "marcar_hoje":
            resultado = registrar_conclusao(habito, data_referencia)
        elif acao == "desmarcar_hoje":
            resultado = remover_conclusao(habito, data_referencia)
        elif acao == "excluir":
            resultado = excluir_habito(habitos, habito_id)
        else:
            raise ValueError("Ação de hábito não reconhecida.")

    return {
        "habitos": habitos,
        "resultado": deepcopy(resultado),
        "resumos": _resumos_habitos(habitos, data_referencia),
    }
