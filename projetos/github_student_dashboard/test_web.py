import unittest

from projetos.github_student_dashboard.github_client import GitHubApiError
from projetos.github_student_dashboard.web import create_app


class StudentDashboardWebTest(unittest.TestCase):
    def test_home_renderiza_interface(self):
        app = create_app(lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"GitHub Student Dashboard", resposta.data)

    def test_api_exige_repositorio(self):
        app = create_app(lambda _: {})
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

        app = create_app(analisador)
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/analisar?repo=Videirafoo/exemplo")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["score"], 80)

    def test_api_rejeita_referencia_invalida(self):
        def analisador(_):
            raise ValueError("Use o formato usuario/repositorio.")

        app = create_app(analisador)
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/analisar?repo=invalido")

        self.assertEqual(resposta.status_code, 400)

    def test_api_mapeia_repositorio_nao_encontrado(self):
        def analisador(_):
            raise GitHubApiError("Não encontrado.", status=404)

        app = create_app(analisador)
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/analisar?repo=usuario/inexistente")

        self.assertEqual(resposta.status_code, 404)

    def test_api_mapeia_limite_da_api(self):
        def analisador(_):
            raise GitHubApiError("Limite atingido.", status=403)

        app = create_app(analisador)
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/analisar?repo=usuario/projeto")

        self.assertEqual(resposta.status_code, 429)


if __name__ == "__main__":
    unittest.main()
