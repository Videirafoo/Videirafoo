import tempfile
import unittest
from pathlib import Path

from conteudos.mini_sistemas.caixa_mercado.app import (
    adicionar_ao_carrinho,
    buscar_produto,
    cadastrar_produto,
    calcular_desconto,
    calcular_subtotal,
    calcular_total,
    carregar_dados,
    fechar_venda,
    remover_do_carrinho,
    salvar_dados,
)


class CaixaMercadoTest(unittest.TestCase):
    def setUp(self):
        self.produtos = []
        self.vendas = []
        self.carrinho = []
        cadastrar_produto(self.produtos, "A1", "Arroz", 10.0, 5)
        cadastrar_produto(self.produtos, "F1", "Feijão", 8.5, 3)

    def test_cadastrar_produto(self):
        produto = buscar_produto(self.produtos, "a1")
        self.assertEqual(produto["nome"], "Arroz")
        self.assertEqual(produto["estoque"], 5)

    def test_rejeita_codigo_duplicado(self):
        with self.assertRaises(ValueError):
            cadastrar_produto(self.produtos, "A1", "Outro", 2, 1)

    def test_adicionar_ao_carrinho_calcula_subtotal(self):
        item = adicionar_ao_carrinho(self.carrinho, self.produtos, "A1", 2)
        self.assertEqual(item["quantidade"], 2)
        self.assertEqual(item["subtotal"], 20.0)
        self.assertEqual(calcular_subtotal(self.carrinho), 20.0)

    def test_adicionar_mesmo_produto_acumula_quantidade(self):
        adicionar_ao_carrinho(self.carrinho, self.produtos, "A1", 1)
        adicionar_ao_carrinho(self.carrinho, self.produtos, "A1", 2)
        self.assertEqual(len(self.carrinho), 1)
        self.assertEqual(self.carrinho[0]["quantidade"], 3)
        self.assertEqual(self.carrinho[0]["subtotal"], 30.0)

    def test_nao_permite_ultrapassar_estoque(self):
        with self.assertRaises(ValueError):
            adicionar_ao_carrinho(self.carrinho, self.produtos, "F1", 4)

    def test_calcular_desconto_e_total(self):
        adicionar_ao_carrinho(self.carrinho, self.produtos, "A1", 2)
        self.assertEqual(calcular_desconto(20, 10), 2.0)
        self.assertEqual(calcular_total(self.carrinho, 10), 18.0)

    def test_desconto_invalido(self):
        with self.assertRaises(ValueError):
            calcular_desconto(100, 101)

    def test_fechar_venda_baixa_estoque_e_limpa_carrinho(self):
        adicionar_ao_carrinho(self.carrinho, self.produtos, "A1", 2)
        venda = fechar_venda(self.produtos, self.vendas, self.carrinho, 10)

        self.assertEqual(venda["subtotal"], 20.0)
        self.assertEqual(venda["valor_desconto"], 2.0)
        self.assertEqual(venda["total"], 18.0)
        self.assertEqual(buscar_produto(self.produtos, "A1")["estoque"], 3)
        self.assertEqual(self.carrinho, [])
        self.assertEqual(len(self.vendas), 1)

    def test_fechar_venda_rejeita_carrinho_vazio(self):
        with self.assertRaises(ValueError):
            fechar_venda(self.produtos, self.vendas, self.carrinho)

    def test_remover_item_do_carrinho(self):
        adicionar_ao_carrinho(self.carrinho, self.produtos, "A1", 1)
        removido = remover_do_carrinho(self.carrinho, "A1")
        self.assertEqual(removido["nome"], "Arroz")
        self.assertEqual(self.carrinho, [])

    def test_salvar_e_carregar_json(self):
        dados = {"produtos": self.produtos, "vendas": self.vendas}

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "caixa.json"
            salvar_dados(dados, caminho)
            carregados = carregar_dados(caminho)

        self.assertEqual(carregados, dados)


if __name__ == "__main__":
    unittest.main()
