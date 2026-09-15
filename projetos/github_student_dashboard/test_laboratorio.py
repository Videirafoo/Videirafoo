import unittest
from pathlib import Path

from projetos.github_student_dashboard.web import create_app


class LaboratorioWebTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(lambda _: {}, lambda _: {}, lambda _: {})
        self.app.config["TESTING"] = True
        self.cliente = self.app.test_client()

    def test_pagina_laboratorio_renderiza_dez_mini_sistemas(self):
        resposta = self.cliente.get("/laboratorio")

        self.assertEqual(resposta.status_code, 200)
        conteudo = resposta.get_data(as_text=True)

        esperados = [
            "01 — Agenda de Contatos",
            "02 — Lista de tarefas",
            "03 — Cadastro de aluno",
            "04 — Controle de estoque",
            "05 — Sistema de Biblioteca",
            "06 — Caixa de Mercado",
            "07 — Controle financeiro",
            "08 — Gerenciador de hábitos",
            "09 — API de Tarefas",
            "10 — Projeto Integrado",
        ]

        for titulo in esperados:
            with self.subTest(titulo=titulo):
                self.assertIn(titulo, conteudo)

        self.assertIn("Busca binária visual", conteudo)
        self.assertIn("/static/laboratorio.js", conteudo)

    def test_laboratorio_aponta_para_codigo_e_testes_reais(self):
        resposta = self.cliente.get("/laboratorio")
        conteudo = resposta.get_data(as_text=True)

        caminhos = [
            "conteudos/mini_sistemas/agenda_contatos/main.py",
            "conteudos/mini_sistemas/lista_tarefas",
            "conteudos/mini_sistemas/cadastro_alunos",
            "conteudos/mini_sistemas/controle_estoque",
            "conteudos/mini_sistemas/sistema_biblioteca/test_app.py",
            "conteudos/mini_sistemas/caixa_mercado/app.py",
            "conteudos/mini_sistemas/controle_financeiro/test_app.py",
            "conteudos/mini_sistemas/gerenciador_habitos/app.py",
            "conteudos/mini_sistemas/api_tarefas/test_app.py",
            "conteudos/mini_sistemas/projeto_integrado/app.py",
        ]

        for caminho in caminhos:
            with self.subTest(caminho=caminho):
                self.assertIn(caminho, conteudo)

    def test_javascript_do_laboratorio_cobre_primeiro_e_decimo_sistema(self):
        caminho = Path(__file__).with_name("static") / "laboratorio.js"

        self.assertTrue(caminho.exists())
        conteudo = caminho.read_text(encoding="utf-8")
        self.assertIn("// 01 — Agenda de contatos", conteudo)
        self.assertIn("// 10 — Analisador local de repositórios", conteudo)

    def test_sitemap_inclui_laboratorio(self):
        resposta = self.cliente.get("/sitemap.xml")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"/laboratorio", resposta.data)


if __name__ == "__main__":
    unittest.main()
