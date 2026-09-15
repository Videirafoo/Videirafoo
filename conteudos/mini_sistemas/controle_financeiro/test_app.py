import tempfile
import unittest
from pathlib import Path

from conteudos.mini_sistemas.controle_financeiro.app import (
    adicionar_lancamento,
    calcular_totais,
    carregar_dados,
    excluir_lancamento,
    filtrar_lancamentos,
    resumo_por_categoria,
    salvar_dados,
)


class ControleFinanceiroTest(unittest.TestCase):
    def setUp(self):
        self.dados = {"lancamentos": []}

    def test_adicionar_receita(self):
        lancamento = adicionar_lancamento(
            self.dados,
            "receita",
            "Salário",
            2500,
            "Renda",
            "2026-09-01",
        )

        self.assertEqual(lancamento["id"], 1)
        self.assertEqual(lancamento["tipo"], "receita")
        self.assertEqual(lancamento["valor"], 2500.0)

    def test_rejeita_tipo_invalido(self):
        with self.assertRaises(ValueError):
            adicionar_lancamento(
                self.dados,
                "transferencia",
                "Teste",
                10,
                "Outros",
                "2026-09-01",
            )

    def test_rejeita_valor_zero_ou_negativo(self):
        with self.assertRaises(ValueError):
            adicionar_lancamento(
                self.dados,
                "despesa",
                "Conta",
                0,
                "Casa",
                "2026-09-01",
            )

        with self.assertRaises(ValueError):
            adicionar_lancamento(
                self.dados,
                "despesa",
                "Conta",
                -20,
                "Casa",
                "2026-09-01",
            )

    def test_calcular_totais_e_saldo(self):
        adicionar_lancamento(
            self.dados, "receita", "Freelance", 1000, "Renda", "2026-09-01"
        )
        adicionar_lancamento(
            self.dados, "despesa", "Internet", 120, "Casa", "2026-09-02"
        )
        adicionar_lancamento(
            self.dados, "despesa", "Mercado", 300, "Alimentação", "2026-09-03"
        )

        totais = calcular_totais(self.dados["lancamentos"])

        self.assertEqual(totais["receitas"], 1000.0)
        self.assertEqual(totais["despesas"], 420.0)
        self.assertEqual(totais["saldo"], 580.0)

    def test_filtrar_por_tipo_categoria_e_mes(self):
        adicionar_lancamento(
            self.dados, "receita", "Salário", 2000, "Renda", "2026-09-01"
        )
        adicionar_lancamento(
            self.dados, "despesa", "Mercado", 250, "Alimentação", "2026-09-05"
        )
        adicionar_lancamento(
            self.dados, "despesa", "Cinema", 50, "Lazer", "2026-08-20"
        )

        self.assertEqual(
            len(filtrar_lancamentos(self.dados, tipo="despesa")),
            2,
        )
        self.assertEqual(
            len(filtrar_lancamentos(self.dados, categoria="alimentação")),
            1,
        )
        self.assertEqual(
            len(filtrar_lancamentos(self.dados, mes="2026-09")),
            2,
        )

    def test_resumo_por_categoria(self):
        adicionar_lancamento(
            self.dados, "receita", "Salário", 3000, "Renda", "2026-09-01"
        )
        adicionar_lancamento(
            self.dados, "despesa", "Curso", 200, "Educação", "2026-09-02"
        )
        adicionar_lancamento(
            self.dados, "despesa", "Livro", 80, "Educação", "2026-09-03"
        )

        resumo = resumo_por_categoria(self.dados["lancamentos"])

        self.assertEqual(resumo["Renda"]["receitas"], 3000.0)
        self.assertEqual(resumo["Educação"]["despesas"], 280.0)
        self.assertEqual(resumo["Educação"]["saldo"], -280.0)

    def test_excluir_lancamento(self):
        lancamento = adicionar_lancamento(
            self.dados, "despesa", "Teste", 10, "Outros", "2026-09-01"
        )

        removido = excluir_lancamento(self.dados, lancamento["id"])

        self.assertEqual(removido["descricao"], "Teste")
        self.assertEqual(self.dados["lancamentos"], [])

    def test_salvar_e_carregar_json(self):
        adicionar_lancamento(
            self.dados,
            "receita",
            "Venda",
            150,
            "Extra",
            "2026-09-10",
        )

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "financeiro.json"
            salvar_dados(self.dados, caminho)
            carregados = carregar_dados(caminho)

        self.assertEqual(carregados, self.dados)


if __name__ == "__main__":
    unittest.main()
