from flask import Flask, jsonify, render_template, request

from projetos.github_student_dashboard.engine import analisar_repositorio_remoto
from projetos.github_student_dashboard.github_client import GitHubApiError


def create_app(analisador=analisar_repositorio_remoto):
    app = Flask(__name__)

    @app.get("/")
    def inicio():
        return render_template("index.html")

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
            if erro.status == 404:
                status = 404
            elif erro.status in {401, 403, 429}:
                status = 429
            else:
                status = 502
            return jsonify({"erro": str(erro)}), status

        return jsonify(relatorio), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
