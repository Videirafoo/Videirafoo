import unittest

from projetos.github_student_dashboard.lab_business import (
    MAX_ITENS_LAB as MAX_NEGOCIO,
    _limitar_lista,
    biblioteca_operacao_lab,
    caixa_operacao_lab,
    financeiro_operacao_lab,
    habito_operacao_lab,
    normalizar_biblioteca_lab,
    normalizar_caixa_lab,
    normalizar_financeiro_lab,
    normalizar_habitos_lab,
)
from projetos.github_student_dashboard.lab_systems import (
    MAX_ITENS_LAB as MAX_SISTEMAS,
    criar_produto_lab,
    excluir_produto_lab,
)
from projetos.github_student_dashboard.web import create_app


class LabBusinessEdgesTest(unittest.TestCase):
    def test_limites_de_lista_sao_validados(self):
        self.assertEqual(_limitar_lista(None, "Itens"), [])
        with self.assertRaisesRegex(ValueError, "precisa ser uma lista"):
            _limitar_lista({}, "Itens")
        with self.assertRaisesRegex(ValueError, "no máximo"):
            _limitar_lista([{}] * (MAX_NEGOCIO + 1), "Itens")

    def test_biblioteca_rejeita_estados_e_acoes_invalidas(self):
        with self.assertRaisesRegex(ValueError, "objeto JSON"):
            normalizar_biblioteca_lab([])
        with self.assertRaisesRegex(ValueError, "Cada livro"):
            normalizar_biblioteca_lab({"livros": ["x"], "usuarios": [], "emprestimos": []})
        with self.assertRaisesRegex(ValueError, "Cada usuário"):
            normalizar_biblioteca_lab({"livros": [], "usuarios": ["x"], "emprestimos": []})
        with self.assertRaisesRegex(ValueError, "Cada empréstimo"):
            normalizar_biblioteca_lab({"livros": [], "usuarios": [], "emprestimos": ["x"]})
        with self.assertRaisesRegex(ValueError, "dados da operação"):
            biblioteca_operacao_lab({}, "cadastrar_livro", [])
        with self.assertRaisesRegex(ValueError, "não reconhecida"):
            biblioteca_operacao_lab({}, "inexistente", {})

    def test_biblioteca_normaliza_autor_e_emprestimo_devolvido(self):
        estado = {
            "livros": [{"isbn": "1", "titulo": "Livro", "autor": ""}],
            "usuarios": [{"nome": "Aluno", "documento": "DOC"}],
            "emprestimos": [{"isbn": "1", "documento": "DOC", "devolvido": True}],
        }
        normalizado = normalizar_biblioteca_lab(estado)
        self.assertEqual(normalizado["livros"][0]["autor"], "Autor do laboratório")
        self.assertTrue(normalizado["livros"][0]["disponivel"])
        self.assertTrue(normalizado["emprestimos"][0]["devolvido"])

    def test_caixa_rejeita_estados_itens_e_acao_invalidos(self):
        with self.assertRaisesRegex(ValueError, "objeto JSON"):
            normalizar_caixa_lab([])
        with self.assertRaisesRegex(ValueError, "Cada produto"):
            normalizar_caixa_lab({"produtos": ["x"]})
        with self.assertRaisesRegex(ValueError, "Cada item do carrinho"):
            normalizar_caixa_lab({"produtos": [], "carrinho": ["x"]})
        with self.assertRaisesRegex(ValueError, "Cada venda"):
            normalizar_caixa_lab({"produtos": [], "carrinho": [], "vendas": ["x"]})
        with self.assertRaisesRegex(ValueError, "dados da operação"):
            caixa_operacao_lab({}, "cadastrar_produto", [])
        with self.assertRaisesRegex(ValueError, "não reconhecida"):
            caixa_operacao_lab({}, "inexistente", {})

    def test_caixa_aceita_produto_id_legado_e_remove_item(self):
        estado = {
            "produtos": [{"id": 1, "nome": "Café", "preco": 10, "estoque": 4}],
            "carrinho": [{"produtoId": 1, "quantidade": 2}],
            "vendas": [{"total": 5}],
        }
        normalizado = normalizar_caixa_lab(estado)
        self.assertEqual(normalizado["carrinho"][0]["codigo"], "LAB-1")
        self.assertEqual(normalizado["vendas"][0]["id"], 1)

        removido = caixa_operacao_lab(normalizado, "remover_carrinho", {"codigo": "LAB-1"})
        self.assertEqual(removido["estado"]["carrinho"], [])
        self.assertEqual(removido["resultado"]["quantidade"], 2)

        ausente = caixa_operacao_lab(removido["estado"], "remover_carrinho", {"codigo": "LAB-1"})
        self.assertIsNone(ausente)

    def test_financeiro_valida_estado_id_e_acao(self):
        with self.assertRaisesRegex(ValueError, "Cada lançamento"):
            normalizar_financeiro_lab(["x"])
        with self.assertRaisesRegex(ValueError, "dados da operação"):
            financeiro_operacao_lab([], "adicionar", [])
        with self.assertRaisesRegex(ValueError, "id inteiro positivo"):
            financeiro_operacao_lab([], "excluir", {"id": 0})
        self.assertIsNone(financeiro_operacao_lab([], "excluir", {"id": 1}))
        with self.assertRaisesRegex(ValueError, "não reconhecida"):
            financeiro_operacao_lab([], "inexistente", {})

    def test_habitos_validam_estado_id_recurso_e_acao(self):
        with self.assertRaisesRegex(ValueError, "Cada hábito"):
            normalizar_habitos_lab(["x"])
        with self.assertRaisesRegex(ValueError, "dados da operação"):
            habito_operacao_lab([], "criar", [])
        with self.assertRaisesRegex(ValueError, "id inteiro positivo"):
            habito_operacao_lab([], "marcar_hoje", {"id": 0})
        self.assertIsNone(habito_operacao_lab([], "marcar_hoje", {"id": 1}))

        criado = habito_operacao_lab([], "criar", {"nome": "Ler", "meta": 3, "data": "2026-09-15"})
        with self.assertRaisesRegex(ValueError, "não reconhecida"):
            habito_operacao_lab(
                criado["habitos"],
                "inexistente",
                {"id": 1, "data": "2026-09-15"},
            )


class LabSystemsEdgesTest(unittest.TestCase):
    def test_estoque_rejeita_estado_formato_limite_e_preco_nao_numerico(self):
        with self.assertRaisesRegex(ValueError, "precisa ser uma lista"):
            criar_produto_lab({}, "Produto", 1, 1)
        with self.assertRaisesRegex(ValueError, "no máximo"):
            criar_produto_lab([{}] * (MAX_SISTEMAS + 1), "Produto", 1, 1)
        with self.assertRaisesRegex(ValueError, "Cada produto"):
            criar_produto_lab(["x"], "Produto", 1, 1)
        with self.assertRaisesRegex(ValueError, "numérico"):
            criar_produto_lab([], "Produto", 1, "abc")

    def test_estoque_rejeita_novo_item_quando_ja_esta_no_limite(self):
        estado = [
            {
                "id": indice,
                "codigo": f"P-{indice}",
                "nome": f"Produto {indice}",
                "quantidade": 1,
                "estoque_minimo": 0,
                "preco": 1,
            }
            for indice in range(1, MAX_SISTEMAS + 1)
        ]
        with self.assertRaisesRegex(ValueError, "no máximo"):
            criar_produto_lab(estado, "Extra", 1, 1)

    def test_exclusao_de_estoque_valida_id_e_recurso_ausente(self):
        with self.assertRaisesRegex(ValueError, "id inteiro positivo"):
            excluir_produto_lab([], 0)
        self.assertIsNone(excluir_produto_lab([], 1))


class LabHttpEdgesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(lambda _: {}, lambda _: {}, lambda _: {})
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_endpoints_post_rejeitam_corpo_nao_json(self):
        rotas = (
            "/api/laboratorio/agenda",
            "/api/laboratorio/lista-tarefas",
            "/api/laboratorio/aluno-media",
            "/api/laboratorio/estoque",
            "/api/laboratorio/biblioteca",
            "/api/laboratorio/caixa",
            "/api/laboratorio/financeiro",
            "/api/laboratorio/habitos",
            "/api/laboratorio/tarefas",
            "/api/laboratorio/analisar",
        )
        for rota in rotas:
            with self.subTest(rota=rota):
                resposta = self.client.post(rota, data="nao-json", content_type="text/plain")
                self.assertEqual(resposta.status_code, 400)
                self.assertIn("JSON válido", resposta.json["erro"])
                resposta.close()

    def test_agenda_delete_cobre_404_e_sucesso(self):
        ausente = self.client.delete("/api/laboratorio/agenda", json={"contatos": [], "id": "x"})
        self.assertEqual(ausente.status_code, 404)
        ausente.close()

        criado = self.client.post(
            "/api/laboratorio/agenda",
            json={"contatos": [], "nome": "Ana", "telefone": "9999"},
        )
        contato = criado.json["resultado"]
        estado = criado.json["contatos"]
        criado.close()

        removido = self.client.delete(
            "/api/laboratorio/agenda",
            json={"contatos": estado, "id": contato["id"]},
        )
        self.assertEqual(removido.status_code, 200)
        self.assertEqual(removido.json["contatos"], [])
        removido.close()

    def test_lista_tarefas_cobre_patch_delete_e_404(self):
        criado = self.client.post(
            "/api/laboratorio/lista-tarefas",
            json={"tarefas": [], "titulo": "Estudar", "prioridade": "alta"},
        )
        estado = criado.json["tarefas"]
        criado.close()

        alterado = self.client.patch(
            "/api/laboratorio/lista-tarefas",
            json={"tarefas": estado, "id": 1, "concluida": True},
        )
        self.assertEqual(alterado.status_code, 200)
        estado = alterado.json["tarefas"]
        self.assertTrue(estado[0]["concluida"])
        alterado.close()

        ausente = self.client.patch(
            "/api/laboratorio/lista-tarefas",
            json={"tarefas": estado, "id": 99, "concluida": True},
        )
        self.assertEqual(ausente.status_code, 404)
        ausente.close()

        removido = self.client.delete(
            "/api/laboratorio/lista-tarefas",
            json={"tarefas": estado, "id": 1},
        )
        self.assertEqual(removido.status_code, 200)
        self.assertEqual(removido.json["tarefas"], [])
        removido.close()

    def test_estoque_delete_cobre_404_e_sucesso(self):
        ausente = self.client.delete("/api/laboratorio/estoque", json={"produtos": [], "id": 1})
        self.assertEqual(ausente.status_code, 404)
        ausente.close()

        criado = self.client.post(
            "/api/laboratorio/estoque",
            json={"produtos": [], "nome": "Caneta", "quantidade": 2, "preco": 3},
        )
        estado = criado.json["produtos"]
        criado.close()
        removido = self.client.delete("/api/laboratorio/estoque", json={"produtos": estado, "id": 1})
        self.assertEqual(removido.status_code, 200)
        self.assertEqual(removido.json["produtos"], [])
        removido.close()

    def test_business_endpoints_cobrem_404_e_erros_de_acao(self):
        casos_404 = (
            (
                "/api/laboratorio/caixa",
                {"estado": {"produtos": [], "carrinho": [], "vendas": []}, "acao": "remover_carrinho", "dados": {"codigo": "X"}},
            ),
            (
                "/api/laboratorio/financeiro",
                {"estado": [], "acao": "excluir", "dados": {"id": 1}},
            ),
            (
                "/api/laboratorio/habitos",
                {"estado": [], "acao": "excluir", "dados": {"id": 1, "data": "2026-09-15"}},
            ),
        )
        for rota, corpo in casos_404:
            with self.subTest(rota=rota):
                resposta = self.client.post(rota, json=corpo)
                self.assertEqual(resposta.status_code, 404)
                resposta.close()

        resposta = self.client.post(
            "/api/laboratorio/biblioteca",
            json={"estado": {}, "acao": "inexistente", "dados": {}},
        )
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("não reconhecida", resposta.json["erro"])
        resposta.close()

    def test_api_tarefas_cobre_get_invalido_limite_patch_delete_e_404(self):
        invalido = self.client.get("/api/laboratorio/tarefas?estado=%7B")
        self.assertEqual(invalido.status_code, 400)
        invalido.close()

        grande = self.client.get("/api/laboratorio/tarefas?estado=" + ("x" * 20001))
        self.assertEqual(grande.status_code, 400)
        grande.close()

        criado = self.client.post(
            "/api/laboratorio/tarefas",
            json={"tarefas": [], "titulo": "Tarefa", "prioridade": "media"},
        )
        estado = criado.json["tarefas"]
        criado.close()

        alterado = self.client.patch(
            "/api/laboratorio/tarefas",
            json={"tarefas": estado, "id": 1, "dados": {"concluida": True}},
        )
        self.assertEqual(alterado.status_code, 200)
        estado = alterado.json["tarefas"]
        alterado.close()

        ausente = self.client.patch(
            "/api/laboratorio/tarefas",
            json={"tarefas": estado, "id": 99, "dados": {"concluida": True}},
        )
        self.assertEqual(ausente.status_code, 404)
        ausente.close()

        removido = self.client.delete(
            "/api/laboratorio/tarefas",
            json={"tarefas": estado, "id": 1},
        )
        self.assertEqual(removido.status_code, 204)
        removido.close()

        ausente_delete = self.client.delete(
            "/api/laboratorio/tarefas",
            json={"tarefas": [], "id": 1},
        )
        self.assertEqual(ausente_delete.status_code, 404)
        ausente_delete.close()

    def test_analisador_rejeita_check_desconhecido(self):
        resposta = self.client.post(
            "/api/laboratorio/analisar",
            json={"checks": {"inventado": True}},
        )
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("não reconhecidos", resposta.json["erro"])
        resposta.close()


if __name__ == "__main__":
    unittest.main()
