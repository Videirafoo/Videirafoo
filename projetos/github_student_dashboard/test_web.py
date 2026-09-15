import unittest

from projetos.github_student_dashboard.github_client import GitHubApiError
from projetos.github_student_dashboard.web import create_app


class StudentDashboardWebTest(unittest.TestCase):
    def test_home_renderiza_interface(self):
        app = create_app(lambda _: {}, lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"GitHub Student Dashboard", resposta.data)
        self.assertIn(b"Analisar perfil", resposta.data)

    def test_api_exige_repositorio(self):
        app = create_app(lambda _: {}, lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/analisar")

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("erro", resposta.get_json())

    def test_api_retorna_relatorio(self):
        def analisador(_):
            return {
                "repositorio": "Videirafoo/exemplo",
                "score": 80,
                "checks": {"readme": True, "testes": False},
                "evidencias": {},
                "recomendacoes": [
                    {
                        "check": "testes",
                        "prioridade": "alta",
                        "acao": "Adicionar testes.",
                    }
                ],
            }

        app = create_app(analisador, lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/analisar?repo=Videirafoo/exemplo")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["score"], 80)

    def test_api_perfil_exige_usuario(self):
        app = create_app(lambda _: {}, lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/perfil")

        self.assertEqual(resposta.status_code, 400)

    def test_api_perfil_retorna_relatorio(self):
        def analisador_perfil(_):
            return {
                "usuario": "Videirafoo",
                "repositorios_analisados": 7,
                "repositorio_perfil_existe": True,
                "cobertura": {
                    "descricao": {"quantidade": 2, "percentual": 28.6},
                    "topics": {"quantidade": 1, "percentual": 14.3},
                    "licenca": {"quantidade": 1, "percentual": 14.3},
                },
                "engajamento": {"stars_recebidos": 2, "forks_recebidos": 0},
                "linguagens_principais": [],
                "repositorios_destaque": [],
                "lacunas_objetivas": [],
            }

        app = create_app(lambda _: {}, analisador_perfil)
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/perfil?usuario=Videirafoo")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["usuario"], "Videirafoo")

    def test_api_rejeita_referencia_invalida(self):
        def analisador(_):
            raise ValueError("Use o formato usuario/repositorio.")

        app = create_app(analisador, lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/analisar?repo=invalido")

        self.assertEqual(resposta.status_code, 400)

    def test_api_mapeia_repositorio_nao_encontrado(self):
        def analisador(_):
            raise GitHubApiError("Não encontrado.", status=404)

        app = create_app(analisador, lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/analisar?repo=usuario/inexistente")

        self.assertEqual(resposta.status_code, 404)

    def test_api_mapeia_limite_da_api(self):
        def analisador(_):
            raise GitHubApiError("Limite atingido.", status=403)

        app = create_app(analisador, lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/analisar?repo=usuario/projeto")

        self.assertEqual(resposta.status_code, 429)


if __name__ == "__main__":
    unittest.main()
