import unittest

from projetos.github_student_dashboard.web import create_app


class LabBusinessWebTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(lambda _: {}, lambda _: {}, lambda _: {})
        self.app.config["TESTING"] = True
        self.cliente = self.app.test_client()

    def test_laboratorio_carrega_todas_integracoes_reais(self):
        resposta = self.cliente.get("/laboratorio")
        conteudo = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("/static/laboratorio_systems_real.js", conteudo)
        self.assertIn("/static/laboratorio_business_real.js", conteudo)
        self.assertIn("/static/laboratorio_api_real.js", conteudo)

    def test_endpoint_biblioteca_cadastra_livro(self):
        resposta = self.cliente.post(
            "/api/laboratorio/biblioteca",
            json={
                "estado": {"livros": [], "usuarios": [], "emprestimos": []},
                "acao": "cadastrar_livro",
                "dados": {"isbn": "123", "titulo": "Python", "autor": "Ada"},
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json["resultado"]["titulo"], "Python")

    def test_endpoint_caixa_cadastra_produto(self):
        resposta = self.cliente.post(
            "/api/laboratorio/caixa",
            json={
                "estado": {"produtos": [], "carrinho": [], "vendas": []},
                "acao": "cadastrar_produto",
                "dados": {"nome": "Café", "preco": 12.5, "estoque": 3},
            },
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json["resultado"]["nome"], "Café")
        self.assertEqual(resposta.json["estado"]["produtos"][0]["estoque"], 3)

    def test_endpoint_financeiro_rejeita_valor_invalido(self):
        resposta = self.cliente.post(
            "/api/laboratorio/financeiro",
            json={
                "estado": [],
                "acao": "adicionar",
                "dados": {
                    "tipo": "despesa",
                    "descricao": "Teste",
                    "valor": 0,
                    "categoria": "Estudo",
                    "data": "2026-09-15",
                },
            },
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("maior que zero", resposta.json["erro"])

    def test_endpoint_habitos_cria_habito(self):
        resposta = self.cliente.post(
            "/api/laboratorio/habitos",
            json={"estado": [], "acao": "criar", "dados": {"nome": "Ler", "meta": 4}},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json["habitos"][0]["nome"], "Ler")
        self.assertEqual(resposta.json["habitos"][0]["meta_semanal"], 4)


if __name__ == "__main__":
    unittest.main()
