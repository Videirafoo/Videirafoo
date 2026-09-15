import json
from pathlib import Path

from flask import Flask, jsonify, request

ARQUIVO_PADRAO = Path(__file__).with_name("tarefas_api.json")
PRIORIDADES = {"baixa", "media", "alta"}


def carregar_tarefas(caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    if not caminho.exists():
        return []

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        raise ValueError("O arquivo da API precisa conter uma lista de tarefas.")

    return dados


def salvar_tarefas(tarefas, caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)


def proximo_id(tarefas):
    if not tarefas:
        return 1

    return max(tarefa["id"] for tarefa in tarefas) + 1


def validar_prioridade(prioridade):
    prioridade = str(prioridade).strip().lower()

    if prioridade not in PRIORIDADES:
        raise ValueError("A prioridade deve ser baixa, media ou alta.")

    return prioridade


def criar_tarefa(tarefas, titulo, prioridade="media"):
    titulo = str(titulo).strip()

    if not titulo:
        raise ValueError("O título não pode ficar vazio.")

    tarefa = {
        "id": proximo_id(tarefas),
        "titulo": titulo,
        "prioridade": validar_prioridade(prioridade),
        "concluida": False,
    }

    tarefas.append(tarefa)
    return tarefa


def encontrar_tarefa(tarefas, tarefa_id):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            return tarefa

    return None


def atualizar_tarefa(tarefa, dados):
    if "titulo" in dados:
        titulo = str(dados["titulo"]).strip()
        if not titulo:
            raise ValueError("O título não pode ficar vazio.")
        tarefa["titulo"] = titulo

    if "prioridade" in dados:
        tarefa["prioridade"] = validar_prioridade(dados["prioridade"])

    if "concluida" in dados:
        if not isinstance(dados["concluida"], bool):
            raise ValueError("O campo concluida precisa ser true ou false.")
        tarefa["concluida"] = dados["concluida"]

    return tarefa


def excluir_tarefa(tarefas, tarefa_id):
    for indice, tarefa in enumerate(tarefas):
        if tarefa["id"] == tarefa_id:
            return tarefas.pop(indice)

    return None


def filtrar_tarefas(tarefas, status=None):
    if status is None:
        return list(tarefas)

    status = status.strip().lower()

    if status == "pendentes":
        return [tarefa for tarefa in tarefas if not tarefa["concluida"]]
    if status == "concluidas":
        return [tarefa for tarefa in tarefas if tarefa["concluida"]]

    raise ValueError("Use status=pendentes ou status=concluidas.")


def create_app(caminho_dados=ARQUIVO_PADRAO):
    app = Flask(__name__)
    app.config["CAMINHO_DADOS"] = Path(caminho_dados)

    @app.get("/")
    def inicio():
        return jsonify(
            {
                "projeto": "API de Tarefas",
                "mensagem": "Use /tarefas para acessar os recursos.",
            }
        )

    @app.get("/tarefas")
    def listar_tarefas():
        tarefas = carregar_tarefas(app.config["CAMINHO_DADOS"])
        status = request.args.get("status")

        try:
            resultado = filtrar_tarefas(tarefas, status)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

        return jsonify(resultado), 200

    @app.post("/tarefas")
    def adicionar_tarefa():
        dados = request.get_json(silent=True)

        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie um objeto JSON válido."}), 400

        tarefas = carregar_tarefas(app.config["CAMINHO_DADOS"])

        try:
            tarefa = criar_tarefa(
                tarefas,
                dados.get("titulo", ""),
                dados.get("prioridade", "media"),
            )
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

        salvar_tarefas(tarefas, app.config["CAMINHO_DADOS"])
        return jsonify(tarefa), 201

    @app.get("/tarefas/<int:tarefa_id>")
    def detalhar_tarefa(tarefa_id):
        tarefas = carregar_tarefas(app.config["CAMINHO_DADOS"])
        tarefa = encontrar_tarefa(tarefas, tarefa_id)

        if tarefa is None:
            return jsonify({"erro": "Tarefa não encontrada."}), 404

        return jsonify(tarefa), 200

    @app.patch("/tarefas/<int:tarefa_id>")
    def editar_tarefa(tarefa_id):
        dados = request.get_json(silent=True)

        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie um objeto JSON válido."}), 400

        tarefas = carregar_tarefas(app.config["CAMINHO_DADOS"])
        tarefa = encontrar_tarefa(tarefas, tarefa_id)

        if tarefa is None:
            return jsonify({"erro": "Tarefa não encontrada."}), 404

        try:
            atualizar_tarefa(tarefa, dados)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

        salvar_tarefas(tarefas, app.config["CAMINHO_DADOS"])
        return jsonify(tarefa), 200

    @app.delete("/tarefas/<int:tarefa_id>")
    def remover_tarefa(tarefa_id):
        tarefas = carregar_tarefas(app.config["CAMINHO_DADOS"])
        removida = excluir_tarefa(tarefas, tarefa_id)

        if removida is None:
            return jsonify({"erro": "Tarefa não encontrada."}), 404

        salvar_tarefas(tarefas, app.config["CAMINHO_DADOS"])
        return "", 204

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
