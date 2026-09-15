import json

from flask import jsonify, request

from projetos.github_student_dashboard.lab_api import (
    analisar_projeto_lab,
    atualizar_tarefa_lab,
    concluir_lista_tarefa_lab,
    criar_contato_lab,
    criar_lista_tarefa_lab,
    criar_tarefa_lab,
    excluir_contato_lab,
    excluir_lista_tarefa_lab,
    excluir_tarefa_lab,
    listar_tarefas_lab,
)
from projetos.github_student_dashboard.lab_systems import (
    calcular_aluno_lab,
    criar_produto_lab,
    excluir_produto_lab,
)


def register_lab_routes(app):
    @app.route("/api/laboratorio/agenda", methods=["POST", "DELETE"])
    def laboratorio_agenda():
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie um objeto JSON válido."}), 400
        try:
            estado = dados.get("contatos", [])
            if request.method == "POST":
                resultado = criar_contato_lab(
                    estado,
                    dados.get("nome", ""),
                    dados.get("telefone", ""),
                    dados.get("email", ""),
                )
                return jsonify(resultado), 201

            resultado = excluir_contato_lab(estado, dados.get("id"))
            if resultado is None:
                return jsonify({"erro": "Contato não encontrado."}), 404
            return jsonify(resultado), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    @app.route("/api/laboratorio/lista-tarefas", methods=["POST", "PATCH", "DELETE"])
    def laboratorio_lista_tarefas():
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie um objeto JSON válido."}), 400
        try:
            estado = dados.get("tarefas", [])
            if request.method == "POST":
                resultado = criar_lista_tarefa_lab(
                    estado,
                    dados.get("titulo", ""),
                    dados.get("prioridade", "media"),
                )
                return jsonify(resultado), 201

            tarefa_id = dados.get("id")
            if request.method == "PATCH":
                resultado = concluir_lista_tarefa_lab(
                    estado,
                    tarefa_id,
                    dados.get("concluida", True),
                )
                if resultado is None:
                    return jsonify({"erro": "Tarefa não encontrada."}), 404
                return jsonify(resultado), 200

            resultado = excluir_lista_tarefa_lab(estado, tarefa_id)
            if resultado is None:
                return jsonify({"erro": "Tarefa não encontrada."}), 404
            return jsonify(resultado), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    @app.post("/api/laboratorio/aluno-media")
    def laboratorio_aluno_media():
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie um objeto JSON válido."}), 400
        try:
            resultado = calcular_aluno_lab(
                dados.get("nome", ""),
                dados.get("notas", []),
            )
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        return jsonify(resultado), 200

    @app.route("/api/laboratorio/estoque", methods=["POST", "DELETE"])
    def laboratorio_estoque():
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie um objeto JSON válido."}), 400
        try:
            estado = dados.get("produtos", [])
            if request.method == "POST":
                resultado = criar_produto_lab(
                    estado,
                    dados.get("nome", ""),
                    dados.get("quantidade", 0),
                    dados.get("preco", 0),
                )
                return jsonify(resultado), 201

            resultado = excluir_produto_lab(estado, dados.get("id"))
            if resultado is None:
                return jsonify({"erro": "Produto não encontrado."}), 404
            return jsonify(resultado), 200
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    @app.route("/api/laboratorio/tarefas", methods=["GET", "POST", "PATCH", "DELETE"])
    def laboratorio_tarefas():
        try:
            if request.method == "GET":
                estado_texto = request.args.get("estado") or "[]"
                if len(estado_texto) > 20000:
                    raise ValueError("O estado enviado é grande demais para o laboratório.")
                try:
                    estado = json.loads(estado_texto)
                except json.JSONDecodeError as erro:
                    raise ValueError("O estado enviado não é um JSON válido.") from erro
                tarefas = listar_tarefas_lab(estado, request.args.get("status"))
                return jsonify({"tarefas": tarefas, "resultado": tarefas}), 200

            dados = request.get_json(silent=True)
            if not isinstance(dados, dict):
                return jsonify({"erro": "Envie um objeto JSON válido."}), 400

            estado = dados.get("tarefas", [])
            if request.method == "POST":
                resultado = criar_tarefa_lab(
                    estado,
                    dados.get("titulo", ""),
                    dados.get("prioridade", "media"),
                )
                return jsonify(resultado), 201

            tarefa_id = dados.get("id")
            if request.method == "PATCH":
                resultado = atualizar_tarefa_lab(estado, tarefa_id, dados.get("dados", {}))
                if resultado is None:
                    return jsonify({"erro": "Tarefa não encontrada."}), 404
                return jsonify(resultado), 200

            resultado = excluir_tarefa_lab(estado, tarefa_id)
            if resultado is None:
                return jsonify({"erro": "Tarefa não encontrada."}), 404
            return "", 204
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    @app.post("/api/laboratorio/analisar")
    def laboratorio_analisar():
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie um objeto JSON válido."}), 400
        try:
            relatorio = analisar_projeto_lab(dados.get("checks", {}))
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        return jsonify(relatorio), 200
