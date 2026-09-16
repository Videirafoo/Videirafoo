"""Plano de evolução ligado à Matriz Viva e à Trilha Educacional.

O plano não marca missões como concluídas e não certifica domínio. Ele apenas
transforma o estado atual das evidências em uma próxima ação verificável.
"""

from projetos.github_student_dashboard.learning_path import TRILHA_APRENDIZADO


MAPA_EVOLUCAO = {
    "fundamentos-python": {
        "evoluir": ("n1-explicar-fluxo", "exercicio"),
        "aprofundar": ("n1-funcao", "exercicio"),
    },
    "algoritmos-busca": {
        "evoluir": ("n2-comparar-buscas", "exercicio"),
        "aprofundar": ("n2-busca-binaria", "laboratorio"),
    },
    "recursividade": {
        "evoluir": ("n2-recursao", "exercicio"),
        "aprofundar": ("n2-recursao", "exercicio"),
    },
    "mini-sistemas": {
        "evoluir": ("n3-quebrar-validacao", "mini_sistema"),
        "aprofundar": ("n3-melhoria", "mini_sistema"),
    },
    "backend-api": {
        "evoluir": ("n4-http", "mini_sistema"),
        "aprofundar": ("n4-dashboard", "aplicacao"),
    },
    "qualidade-ci": {
        "evoluir": ("n5-quality", "documentacao"),
        "aprofundar": ("n3-melhoria", "teste"),
    },
    "deploy-operacao": {
        "evoluir": ("n4-health", "runtime"),
        "aprofundar": ("n4-health", "runtime"),
    },
    "documentacao": {
        "evoluir": ("n5-review", "documentacao"),
        "aprofundar": ("n5-quality", "documentacao"),
    },
    "open-source": {
        "evoluir": ("n5-pr", "contribuicao"),
        "aprofundar": ("n5-review", "contribuicao"),
    },
    "ia-aplicada": {
        "evoluir": ("n6-deterministico", "aplicacao"),
        "aprofundar": ("n6-proveniencia", "verificacao"),
    },
}


def _indice_missoes():
    return {
        missao["id"]: {**missao, "nivel": nivel["nivel"], "nivel_titulo": nivel["titulo"]}
        for nivel in TRILHA_APRENDIZADO
        for missao in nivel["missoes"]
    }


def _acao_para_competencia(competencia, indice):
    estado = competencia.get("estado_evidencia")
    if estado == "indisponivel":
        return None, "A fonte de evidência está indisponível; nenhuma recomendação foi inventada."

    mapeamento = MAPA_EVOLUCAO.get(competencia.get("id"))
    if not mapeamento:
        return None, "Nenhuma missão real foi mapeada para esta competência."

    chave = "aprofundar" if estado == "forte" else "evoluir"
    missao_id, tipo = mapeamento[chave]
    missao = indice.get(missao_id)
    if missao is None:
        return None, f"A missão {missao_id} não existe na Trilha Educacional atual."

    objetivo = "Aprofundar sem certificar domínio" if estado == "forte" else "Fortalecer a evidência disponível"
    return {
        "tipo": tipo,
        "objetivo": objetivo,
        "missao_id": missao_id,
        "titulo": missao["titulo"],
        "descricao": missao["evidencia"],
        "url": missao["url"],
        "nivel": missao["nivel"],
        "nivel_titulo": missao["nivel_titulo"],
        "origem": f"trilha:{missao_id}",
    }, None


def gerar_plano_evolucao(matriz):
    """Converte uma Matriz Viva já calculada em próximas ações determinísticas."""
    indice = _indice_missoes()
    itens = []

    for competencia in matriz.get("competencias", []):
        acao, motivo = _acao_para_competencia(competencia, indice)
        itens.append({
            "competencia_id": competencia.get("id"),
            "competencia": competencia.get("titulo"),
            "nivel": competencia.get("nivel"),
            "estado_evidencia": competencia.get("estado_evidencia"),
            "acao": acao,
            "motivo_sem_acao": motivo,
            "regra": "orientação baseada em evidência; não marca conclusão e não certifica domínio",
        })

    return {
        "gerado_em": matriz.get("gerado_em"),
        "metodologia": "competência → missão real da Trilha Educacional",
        "itens": itens,
        "resumo": {
            "total": len(itens),
            "com_acao": sum(item["acao"] is not None for item in itens),
            "sem_acao": sum(item["acao"] is None for item in itens),
        },
    }
