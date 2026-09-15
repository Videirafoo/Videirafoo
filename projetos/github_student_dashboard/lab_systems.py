from copy import deepcopy

from conteudos.mini_sistemas.cadastro_alunos.app import (
    adicionar_nota,
    calcular_media,
    calcular_situacao,
    criar_aluno,
)
from conteudos.mini_sistemas.controle_estoque.app import (
    criar_produto,
    excluir_produto,
)


MAX_ITENS_LAB = 50


def calcular_aluno_lab(nome, notas):
    if not isinstance(notas, list) or len(notas) != 3:
        raise ValueError("Informe exatamente três notas.")

    alunos = []
    aluno = criar_aluno(alunos, str(nome), "LAB-001")
    for nota in notas:
        adicionar_nota(alunos, aluno["matricula"], nota)

    media = calcular_media(aluno)
    return {
        "nome": aluno["nome"],
        "matricula": aluno["matricula"],
        "notas": list(aluno["notas"]),
        "media": round(media, 2),
        "situacao": calcular_situacao(aluno),
    }


def _validar_preco(valor):
    try:
        preco = float(valor)
    except (TypeError, ValueError) as erro:
        raise ValueError("O preço precisa ser numérico.") from erro
    if preco < 0:
        raise ValueError("O preço não pode ser negativo.")
    return preco


def _normalizar_estoque(valor):
    if valor is None:
        return []
    if not isinstance(valor, list):
        raise ValueError("O estado do estoque precisa ser uma lista.")
    if len(valor) > MAX_ITENS_LAB:
        raise ValueError(f"O laboratório aceita no máximo {MAX_ITENS_LAB} produtos por vez.")

    produtos = []
    for indice, item in enumerate(valor, start=1):
        if not isinstance(item, dict):
            raise ValueError("Cada produto precisa ser um objeto JSON.")
        codigo = str(item.get("codigo") or f"LAB-{indice}")
        produto = criar_produto(
            produtos,
            codigo,
            str(item.get("nome", "")),
            item.get("quantidade", 0),
            item.get("estoque_minimo", 0),
        )
        produto["preco"] = _validar_preco(item.get("preco", 0))
    return produtos


def criar_produto_lab(estado, nome, quantidade, preco):
    produtos = _normalizar_estoque(estado)
    if len(produtos) >= MAX_ITENS_LAB:
        raise ValueError(f"O laboratório aceita no máximo {MAX_ITENS_LAB} produtos por vez.")

    proximo = max((produto["id"] for produto in produtos), default=0) + 1
    produto = criar_produto(produtos, f"LAB-{proximo}", str(nome), quantidade, 0)
    produto["preco"] = _validar_preco(preco)
    return {
        "produtos": produtos,
        "resultado": deepcopy(produto),
        "valor_total": round(valor_total_estoque_lab(produtos), 2),
    }


def excluir_produto_lab(estado, produto_id):
    produtos = _normalizar_estoque(estado)
    if not isinstance(produto_id, int) or produto_id <= 0:
        raise ValueError("Informe um id inteiro positivo.")

    alvo = next((produto for produto in produtos if produto["id"] == produto_id), None)
    if alvo is None:
        return None

    removido = excluir_produto(produtos, alvo["codigo"])
    return {
        "produtos": produtos,
        "resultado": deepcopy(removido),
        "valor_total": round(valor_total_estoque_lab(produtos), 2),
    }


def valor_total_estoque_lab(produtos):
    return sum(produto["quantidade"] * produto.get("preco", 0) for produto in produtos)
