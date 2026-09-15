import unittest

from projetos.github_student_dashboard.learning_path import TRILHA_APRENDIZADO, resumo_trilha
from projetos.github_student_dashboard.web import create_app


class LearningPathDataTests(unittest.TestCase):
    def test_trilha_tem_seis_niveis_e_dezoito_missoes(self):
        resumo = resumo_trilha()
        self.assertEqual(resumo["total_niveis"], 6)
        self.assertEqual(resumo["total_missoes"], 18)

    def test_ids_de_missoes_sao_unicos(self):
        ids = [
            missao["id"]
            for nivel in TRILHA_APRENDIZADO
            for missao in nivel["missoes"]
        ]
        self.assertEqual(len(ids), len(set(ids)))

    def test_cada_nivel_tem_competencias_e_missoes(self):
        for nivel in TRILHA_APRENDIZADO:
            self.assertTrue(nivel["competencias"])
            self.assertTrue(nivel["missoes"])
            self.assertTrue(nivel["objetivo"])

    def test_urls_de_evidencia_sao_locais_ou_https(self):
        for nivel in TRILHA_APRENDIZADO:
            for missao in nivel["missoes"]:
                self.assertTrue(
                    missao["url"].startswith("/") or missao["url"].startswith("https://"),
                    missao["url"],
                )


class LearningPathWebTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_pagina_trilha_renderiza_niveis(self):
        response = self.app.get("/trilha")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Trilha Educacional", html)
        self.assertIn("Nível 1", html)
        self.assertIn("Nível 6", html)
        self.assertIn("/static/trilha.js", html)

    def test_api_trilha_retorna_dados_estruturados(self):
        response = self.app.get("/api/trilha")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total_niveis"], 6)
        self.assertEqual(data["total_missoes"], 18)
        self.assertEqual(data["niveis"][0]["titulo"], "Fundamentos")

    def test_sitemap_inclui_trilha(self):
        response = self.app.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("/trilha</loc>", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
