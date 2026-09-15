import unittest

from projetos.github_student_dashboard.lab_systems import (
    calcular_aluno_lab,
    criar_produto_lab,
    excluir_produto_lab,
)


class LabSystemsTest(unittest.TestCase):
    def test_calculo_de_aluno_reutiliza_regras_originais(self):
        resultado = calcular_aluno_lab("Fernando", [8, 7, 9])

        self.assertEqual(resultado["nome"], "Fernando")
        self.assertEqual(resultado["media"], 8.0)
        self.assertEqual(resultado["situacao"], "aprovado")
        self.assertEqual(resultado["notas"], [8.0, 7.0, 9.0])

    def test_calculo_de_aluno_rejeita_nota_fora_do_intervalo(self):
        with self.assertRaisesRegex(ValueError, "entre 0 e 10"):
            calcular_aluno_lab("Fernando", [8, 12, 9])

    def test_estoque_cria_calcula_valor_e_exclui(self):
        primeiro = criar_produto_lab([], "Caderno", 2, 15.5)
        produtos = primeiro["produtos"]

        self.assertEqual(produtos[0]["codigo"], "LAB-1")
        self.assertEqual(produtos[0]["quantidade"], 2)
        self.assertEqual(primeiro["valor_total"], 31.0)

        segundo = criar_produto_lab(produtos, "Caneta", 3, 4)
        self.assertEqual(segundo["valor_total"], 43.0)

        removido = excluir_produto_lab(segundo["produtos"], 1)
        self.assertEqual(len(removido["produtos"]), 1)
        self.assertEqual(removido["produtos"][0]["nome"], "Caneta")
        self.assertEqual(removido["valor_total"], 12.0)

    def test_estoque_rejeita_quantidade_e_preco_invalidos(self):
        with self.assertRaisesRegex(ValueError, "quantidade"):
            criar_produto_lab([], "Caderno", -1, 10)

        with self.assertRaisesRegex(ValueError, "preço"):
            criar_produto_lab([], "Caderno", 1, -10)


if __name__ == "__main__":
    unittest.main()
