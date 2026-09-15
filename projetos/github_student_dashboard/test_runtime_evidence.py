import unittest
from unittest.mock import patch

from projetos.github_student_dashboard.web import (
    PUBLIC_BASE_URL,
    PUBLIC_HOST,
    _evidencia_runtime_publico,
    create_app,
)


class RuntimeEvidenceTests(unittest.TestCase):
    def test_host_publico_e_evidencia_de_runtime(self):
        app = create_app(gerador_competencias=lambda: {})
        with app.test_request_context("/api/competencias", base_url=PUBLIC_BASE_URL):
            ok, detalhe = _evidencia_runtime_publico()

        self.assertTrue(ok)
        self.assertIn("host público", detalhe)

    def test_host_publico_continua_valido_quando_proxy_entrega_http_interno(self):
        app = create_app(gerador_competencias=lambda: {})
        with app.test_request_context(
            "/api/competencias",
            base_url=f"http://{PUBLIC_HOST}",
        ):
            ok, detalhe = _evidencia_runtime_publico()

        self.assertTrue(ok)
        self.assertIn("host público", detalhe)

    def test_execucao_local_nao_e_promovida_a_producao(self):
        app = create_app(gerador_competencias=lambda: {})
        with app.test_request_context("/api/competencias", base_url="http://localhost:5000"):
            ok, detalhe = _evidencia_runtime_publico()

        self.assertFalse(ok)
        self.assertIn("não é inferida", detalhe)

    @patch("projetos.github_student_dashboard.web.gerar_matriz_competencias")
    def test_api_padrao_injeta_evidencia_do_runtime_sem_chamar_healthz(self, gerador_mock):
        def gerar(**kwargs):
            ok, detalhe = kwargs["health_checker"]()
            return {
                "resumo": {"forte": 1 if ok else 0},
                "runtime": detalhe,
            }

        gerador_mock.side_effect = gerar
        app = create_app()
        response = app.test_client().get("/api/competencias", base_url=PUBLIC_BASE_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["resumo"]["forte"], 1)
        gerador_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
