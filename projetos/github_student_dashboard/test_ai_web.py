import unittest

from projetos.github_student_dashboard.web import create_app


class AIExplainerWebTest(unittest.TestCase):
    def test_pagina_explicar_renderiza_interface(self):
        app = create_app(explicador=lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/explicar")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"IA explicativa", resposta.data)
        self.assertIn(b"Explicar diagn", resposta.data)

    def test_api_explicar_exige_repositorio(self):
        app = create_app(explicador=lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/explicar")

        self.assertEqual(resposta.status_code, 400)

    def test_api_explicar_retorna_resultado(self):
        def explicador(ref):
            return {
                "repositorio": ref,
                "score": 80,
                "modo": "local",
                "modelo": None,
                "checks_falhos": ["descricao", "topics"],
                "ci_estado": "success",
                "fonte": "relatorio_deterministico",
                "texto": "Explicação baseada em evidências.",
                "aviso": "Sem chamada externa.",
            }

        app = create_app(explicador=explicador)
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/api/explicar?repo=Videirafoo/Videirafoo")
        dados = resposta.get_json()

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(dados["score"], 80)
        self.assertEqual(dados["modo"], "local")
        self.assertEqual(dados["fonte"], "relatorio_deterministico")


if __name__ == "__main__":
    unittest.main()
