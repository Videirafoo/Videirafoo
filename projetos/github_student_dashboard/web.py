import json

from flask import Flask, Response, jsonify, render_template, request

from projetos.github_student_dashboard.ai_explainer import explicar_repositorio_remoto
from projetos.github_student_dashboard.comparison import comparar_repositorios_remotos
from projetos.github_student_dashboard.engine import (
    analisar_perfil_remoto,
    analisar_repositorio_remoto,
)
from projetos.github_student_dashboard.github_client import GitHubApiError
from projetos.github_student_dashboard.history import analisar_historico_remoto
from projetos.github_student_dashboard.lab_api import (
    analisar_projeto_lab,
    atualizar_tarefa_lab,
    criar_tarefa_lab,
    excluir_tarefa_lab,
    listar_tarefas_lab,
)
from projetos.github_student_dashboard.readme_quality import analisar_readme_remoto


PUBLIC_BASE_URL = "https://github-student-dashboard-videirafoo.onrender.com"
PUBLIC_PAGES = ["/", "/laboratorio", "/readme", "/comparar", "/historico", "/explicar"]
INTERACTIONS_STYLESHEET = '<link rel="stylesheet" href="/static/interactions.css">'
LAB_REAL_SCRIPT = '<script src="/static/laboratorio_api_real.js" defer></script>'


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
    comparador=comparar_repositorios_remotos,
    analisador_historico=analisar_historico_remoto,
    explicador=explicar_repositorio_remoto,
):
    app = Flask(__name__)
    app.json.ensure_ascii = False

    @app.after_request
    def aplicar_microinteracoes(response):
        """Carrega os recursos compartilhados apenas em respostas HTML."""
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            return response

        html = response.get_data(as_text=True)
        if INTERACTIONS_STYLESHEET not in html and "</head>" in html:
            html = html.replace(
                "</head>",
                f"  {INTERACTIONS_STYLESHEET}\n</head>",
                1,
            )
        if request.path == "/laboratorio" and LAB_REAL_SCRIPT not in html and "</body>" in html:
            html = html.replace(
                "</body>",
                f"  {LAB_REAL_SCRIPT}\n</body>",
                1,
            )
        response.set_data(html)
        return response

    @app.get("/")
    def inicio():
        return render_template("index.html")

    @app.get("/laboratorio")
    def pagina_laboratorio():
        return render_template("laboratorio.html")

    @app.get("/readme")
    def pagina_readme():
        return render_template("readme.html")

    @app.get("/comparar")
    def pagina_comparar():
        return render_template("comparar.html")

    @app.get("/historico")
    def pagina_historico():
        return render_template("historico.html")

    @app.get("/explicar")
    def pagina_explicar():
        return render_template("explicar.html")

    @app.get("/favicon.ico")
    def favicon():
        return "", 204

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok", "service": "github-student-dashboard"}), 200

    @app.get("/robots.txt")
    def robots():
        conteudo = (
            "User-agent: *\n"
            "Allow: /\n"
            f"Sitemap: {PUBLIC_BASE_URL}/sitemap.xml\n"
        )
        return Response(conteudo, mimetype="text/plain")

    @app.get("/sitemap.xml")
    def sitemap():
        urls = "".join(
            f"<url><loc>{PUBLIC_BASE_URL}{path}</loc></url>" for path in PUBLIC_PAGES
        )
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"{urls}"
            "</urlset>"
        )
        return Response(xml, mimetype="application/xml")

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

    @app.get("/api/comparar")
    def comparar():
        repositorio_a = (request.args.get("a") or "").strip()
        repositorio_b = (request.args.get("b") or "").strip()
        if not repositorio_a or not repositorio_b:
            return jsonify({"erro": "Informe os dois repositórios para comparação."}), 400
        try:
            relatorio = comparador(repositorio_a, repositorio_b)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except GitHubApiError as erro:
            return jsonify({"erro": str(erro)}), _status_para_erro_github(erro)
        return jsonify(relatorio), 200

    @app.get("/api/historico")
    def historico():
        repositorio = (request.args.get("repo") or "").strip()
        limite_texto = (request.args.get("limite") or "5").strip()
        if not repositorio:
            return jsonify({"erro": "Informe um repositório no formato usuario/repositorio."}), 400
        try:
            limite = int(limite_texto)
        except ValueError:
            return jsonify({"erro": "O limite precisa ser um número inteiro entre 2 e 10."}), 400
        try:
            relatorio = analisador_historico(repositorio, limite=limite)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except GitHubApiError as erro:
            return jsonify({"erro": str(erro)}), _status_para_erro_github(erro)
        return jsonify(relatorio), 200

    @app.get("/api/explicar")
    def explicar():
        repositorio = (request.args.get("repo") or "").strip()
        if not repositorio:
            return jsonify({"erro": "Informe um repositório no formato usuario/repositorio."}), 400
        try:
            relatorio = explicador(repositorio)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400
        except GitHubApiError as erro:
            return jsonify({"erro": str(erro)}), _status_para_erro_github(erro)
        return jsonify(relatorio), 200

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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
