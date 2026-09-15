import unittest

from projetos.github_student_dashboard.lab_business import (
    biblioteca_operacao_lab,
    caixa_operacao_lab,
    financeiro_operacao_lab,
    habito_operacao_lab,
)


class LabBusinessTest(unittest.TestCase):
    def test_biblioteca_cadastra_empresta_e_devolve(self):
        estado = {"livros": [], "usuarios": [], "emprestimos": []}

        resultado = biblioteca_operacao_lab(
            estado,
            "cadastrar_livro",
            {"isbn": "123", "titulo": "Python", "autor": "Ada"},
        )
        estado = resultado["estado"]
        self.assertTrue(estado["livros"][0]["disponivel"])

        resultado = biblioteca_operacao_lab(
            estado,
            "cadastrar_usuario",
            {"nome": "Fernando", "documento": "ABC"},
        )
        estado = resultado["estado"]

        resultado = biblioteca_operacao_lab(
            estado,
            "emprestar",
            {"isbn": "123", "documento": "ABC"},
        )
        estado = resultado["estado"]
        self.assertFalse(estado["livros"][0]["disponivel"])
        self.assertFalse(estado["emprestimos"][0]["devolvido"])

        resultado = biblioteca_operacao_lab(estado, "devolver", {"isbn": "123"})
        self.assertTrue(resultado["estado"]["livros"][0]["disponivel"])
        self.assertTrue(resultado["estado"]["emprestimos"][0]["devolvido"])

    def test_caixa_valida_estoque_e_fecha_venda(self):
        estado = {"produtos": [], "carrinho": [], "vendas": []}

        resultado = caixa_operacao_lab(
            estado,
            "cadastrar_produto",
            {"nome": "Café", "preco": 10, "estoque": 5},
        )
        estado = resultado["estado"]
        codigo = estado["produtos"][0]["codigo"]

        resultado = caixa_operacao_lab(
            estado,
            "adicionar_carrinho",
            {"codigo": codigo, "quantidade": 2},
        )
        estado = resultado["estado"]
        self.assertEqual(resultado["resumo"]["subtotal"], 20.0)

        resultado = caixa_operacao_lab(
            estado,
            "fechar_venda",
            {"desconto": 10},
        )
        self.assertEqual(resultado["resultado"]["total"], 18.0)
        self.assertEqual(resultado["estado"]["produtos"][0]["estoque"], 3)
        self.assertEqual(resultado["estado"]["carrinho"], [])

    def test_financeiro_calcula_totais_e_exclui(self):
        estado = []
        resultado = financeiro_operacao_lab(
            estado,
            "adicionar",
            {
                "tipo": "receita",
                "descricao": "Freela",
                "valor": 100,
                "categoria": "Trabalho",
                "data": "2026-09-15",
            },
        )
        estado = resultado["lancamentos"]

        resultado = financeiro_operacao_lab(
            estado,
            "adicionar",
            {
                "tipo": "despesa",
                "descricao": "Livro",
                "valor": 30,
                "categoria": "Estudo",
                "data": "2026-09-15",
            },
        )
        self.assertEqual(resultado["totais"]["saldo"], 70.0)

        estado = resultado["lancamentos"]
        removido_id = estado[1]["id"]
        resultado = financeiro_operacao_lab(estado, "excluir", {"id": removido_id})
        self.assertEqual(resultado["totais"]["saldo"], 100.0)

    def test_habitos_respeita_data_enviada_pelo_navegador(self):
        data_local = "2026-09-15"
        resultado = habito_operacao_lab(
            [],
            "criar",
            {"nome": "Estudar Python", "meta": 5, "data": data_local},
        )
        estado = resultado["habitos"]
        habito_id = estado[0]["id"]
        self.assertEqual(estado[0]["meta_semanal"], 5)

        resultado = habito_operacao_lab(
            estado,
            "marcar_hoje",
            {"id": habito_id, "data": data_local},
        )
        estado = resultado["habitos"]
        self.assertEqual(estado[0]["registros"], [data_local])
        self.assertEqual(resultado["resumos"][0]["concluidos_semana"], 1)

        resultado = habito_operacao_lab(
            estado,
            "desmarcar_hoje",
            {"id": habito_id, "data": data_local},
        )
        self.assertEqual(resultado["habitos"][0]["registros"], [])

        resultado = habito_operacao_lab(resultado["habitos"], "excluir", {"id": habito_id, "data": data_local})
        self.assertEqual(resultado["habitos"], [])


if __name__ == "__main__":
    unittest.main()
