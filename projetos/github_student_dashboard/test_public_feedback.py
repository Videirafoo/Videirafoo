import unittest

from projetos.github_student_dashboard.web import create_app


class StudentDashboardPublicFeedbackTest(unittest.TestCase):
    def test_home_expoe_navegacao_e_feedback(self):
        app = create_app(lambda _: {}, lambda _: {}, lambda _: {})
        app.config["TESTING"] = True
        cliente = app.test_client()

        resposta = cliente.get("/")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"Qualidade do README", resposta.data)
        self.assertIn(b"Comparar", resposta.data)
        self.assertIn(b"Hist", resposta.data)
        self.assertIn(b"Explica", resposta.data)
        self.assertIn(b"Enviar feedback", resposta.data)
        self.assertIn(b"dashboard-feedback.yml", resposta.data)


if __name__ == "__main__":
    unittest.main()
