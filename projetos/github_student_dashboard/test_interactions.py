import unittest

from projetos.github_student_dashboard.web import create_app


class StudentDashboardInteractionsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(lambda _: {}, lambda _: {}, lambda _: {})
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_css_compartilhado_e_injetado_em_todas_as_paginas(self):
        for path in ("/", "/readme", "/comparar", "/historico", "/explicar"):
            with self.subTest(path=path):
                response = self.client.get(path)
                try:
                    self.assertEqual(response.status_code, 200)
                    self.assertIn(b'/static/interactions.css', response.data)
                finally:
                    response.close()

    def test_css_respeita_touch_teclado_e_reduced_motion(self):
        response = self.client.get("/static/interactions.css")
        try:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"@media (hover: hover) and (pointer: fine)", response.data)
            self.assertIn(b"@media (hover: none), (pointer: coarse)", response.data)
            self.assertIn(b":focus-visible", response.data)
            self.assertIn(b"prefers-reduced-motion: reduce", response.data)
        finally:
            response.close()


if __name__ == "__main__":
    unittest.main()
