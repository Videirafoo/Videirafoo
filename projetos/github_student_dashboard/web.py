from flask import Flask, jsonify, render_template, request

from projetos.github_student_dashboard.engine import (
    analisar_perfil_remoto,
    analisar_repositorio_remoto,
)
from projetos.github_student_dashboard.github_client import GitHubApiError
from projetos.github_student_dashboard.readme_quality import analisar_readme_remoto


def _status_para_erro_github(erro):
    if erro.status == 404:
        return 404
    if erro.status in {401, 403, 429}:
        return 429
    return 502


def create_app(
    analisador=analisar_repositorio_remoto,
    analisador_perfil=analisar_perfil_remoto,
    analisador_readme=analisar_readme_remoto,
):
    app = Flask(__name__)
    app.json.ensure_ascii = False

    @app.get("/")
    def inicio():
        return render_template("index.html")

    @app.get("/favicon.ico")
    def favicon():
        return "", 204

    @app.get("/api/analisar")
    def analisar():
        repositorio = (request.args.get("repo") or "").strip()

        if not repositorio:
            return jsonify({"erro": "Informe um repositório no formato usuario/repositorio."}), 400

        try:
            relatorio = analisador(repositorio)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except GitHubApiError as erro:
            return jsonify({"erro": str(erro)}), _status_para_erro_github(erro)

        return jsonify(relatorio), 200

    @app.get("/api/perfil")
    def analisar_perfil():
        usuario = (request.args.get("usuario") or "").strip()

        if not usuario:
            return jsonify({"erro": "Informe um usuário do GitHub."}), 400

        try:
            relatorio = analisador_perfil(usuario)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except GitHubApiError as erro:
            return jsonify({"erro": str(erro)}), _status_para_erro_github(erro)

        return jsonify(relatorio), 200

    @app.get("/api/readme")
    def analisar_readme():
        repositorio = (request.args.get("repo") or "").strip()

        if not repositorio:
            return jsonify({"erro": "Informe um repositório no formato usuario/repositorio."}), 400

        try:
            relatorio = analisador_readme(repositorio)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except GitHubApiError as erro:
            return jsonify({"erro": str(erro)}), _status_para_erro_github(erro)

        return jsonify(relatorio), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
