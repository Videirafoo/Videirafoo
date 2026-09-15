from copy import deepcopy

from conteudos.mini_sistemas.api_tarefas.app import (
    atualizar_tarefa,
    criar_tarefa,
    excluir_tarefa,
    filtrar_tarefas,
)


MAX_TAREFAS = 50
MAX_TITULO = 120


def _normalizar_tarefas(valor):
    if valor is None:
        return []
    if not isinstance(valor, list):
        raise ValueError("O estado de tarefas precisa ser uma lista.")
    if len(valor) > MAX_TAREFAS:
        raise ValueError(f"O laboratório aceita no máximo {MAX_TAREFAS} tarefas por vez.")

    tarefas = []
    ids = set()
    for item in valor:
        if not isinstance(item, dict):
            raise ValueError("Cada tarefa precisa ser um objeto JSON.")

        tarefa_id = item.get("id")
        titulo = str(item.get("titulo", "")).strip()
        prioridade = str(item.get("prioridade", "media")).strip().lower()
        concluida = item.get("concluida", False)

        if not isinstance(tarefa_id, int) or tarefa_id <= 0:
            raise ValueError("Cada tarefa precisa ter um id inteiro positivo.")
        if tarefa_id in ids:
            raise ValueError("IDs de tarefas não podem se repetir.")
        if not titulo or len(titulo) > MAX_TITULO:
            raise ValueError(f"O título precisa ter entre 1 e {MAX_TITULO} caracteres.")
        if prioridade not in {"baixa", "media", "alta"}:
            raise ValueError("A prioridade deve ser baixa, media ou alta.")
        if not isinstance(concluida, bool):
            raise ValueError("O campo concluida precisa ser booleano.")

        ids.add(tarefa_id)
        tarefas.append(
            {
                "id": tarefa_id,
                "titulo": titulo,
                "prioridade": prioridade,
                "concluida": concluida,
            }
        )

    return tarefas


def listar_tarefas_lab(estado, status=None):
    tarefas = _normalizar_tarefas(estado)
    return filtrar_tarefas(tarefas, status)


def criar_tarefa_lab(estado, titulo, prioridade="media"):
    tarefas = _normalizar_tarefas(estado)
    if len(tarefas) >= MAX_TAREFAS:
        raise ValueError(f"O laboratório aceita no máximo {MAX_TAREFAS} tarefas por vez.")

    titulo = str(titulo).strip()
    if len(titulo) > MAX_TITULO:
        raise ValueError(f"O título pode ter no máximo {MAX_TITULO} caracteres.")

    criada = criar_tarefa(tarefas, titulo, prioridade)
    return {"tarefas": tarefas, "resultado": deepcopy(criada)}


def atualizar_tarefa_lab(estado, tarefa_id, dados):
    tarefas = _normalizar_tarefas(estado)
    if not isinstance(tarefa_id, int) or tarefa_id <= 0:
        raise ValueError("Informe um id inteiro positivo.")
    if not isinstance(dados, dict):
        raise ValueError("Envie um objeto JSON com os campos que deseja alterar.")

    tarefa = next((item for item in tarefas if item["id"] == tarefa_id), None)
    if tarefa is None:
        return None

    dados_permitidos = {}
    if "titulo" in dados:
        titulo = str(dados["titulo"]).strip()
        if len(titulo) > MAX_TITULO:
            raise ValueError(f"O título pode ter no máximo {MAX_TITULO} caracteres.")
        dados_permitidos["titulo"] = titulo
    if "prioridade" in dados:
        dados_permitidos["prioridade"] = dados["prioridade"]
    if "concluida" in dados:
        dados_permitidos["concluida"] = dados["concluida"]

    atualizada = atualizar_tarefa(tarefa, dados_permitidos)
    return {"tarefas": tarefas, "resultado": deepcopy(atualizada)}


def excluir_tarefa_lab(estado, tarefa_id):
    tarefas = _normalizar_tarefas(estado)
    if not isinstance(tarefa_id, int) or tarefa_id <= 0:
        raise ValueError("Informe um id inteiro positivo.")

    removida = excluir_tarefa(tarefas, tarefa_id)
    if removida is None:
        return None

    return {"tarefas": tarefas, "resultado": deepcopy(removida)}
