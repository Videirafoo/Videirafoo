import unittest

from projetos.github_student_dashboard.web import create_app


class LaboratorioWebTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(lambda _: {}, lambda _: {}, lambda _: {})
        self.app.config["TESTING"] = True
        self.cliente = self.app.test_client()

    def test_pagina_laboratorio_renderiza_projetos_executaveis(self):
        resposta = self.cliente.get("/laboratorio")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Laboratório de Projetos".encode("utf-8"), resposta.data)
        self.assertIn(b"Lista de tarefas", resposta.data)
        self.assertIn(b"Controle de estoque", resposta.data)
        self.assertIn("Busca binária visual".encode("utf-8"), resposta.data)
        self.assertIn(b"/static/laboratorio.js", resposta.data)

    def test_laboratorio_aponta_para_codigo_real(self):
        resposta = self.cliente.get("/laboratorio")

        self.assertIn(b"conteudos/mini_sistemas/lista_tarefas", resposta.data)
        self.assertIn(b"conteudos/mini_sistemas/cadastro_alunos", resposta.data)
        self.assertIn(b"conteudos/mini_sistemas/controle_estoque", resposta.data)
        self.assertIn(b"test_app.py", resposta.data)

    def test_sitemap_inclui_laboratorio(self):
        resposta = self.cliente.get("/sitemap.xml")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"/laboratorio", resposta.data)


if __name__ == "__main__":
    unittest.main()
