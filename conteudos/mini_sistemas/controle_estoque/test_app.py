import tempfile
import unittest
from pathlib import Path

from conteudos.mini_sistemas.controle_estoque.app import (
    buscar_produtos,
    carregar_produtos,
    criar_produto,
    entrada_estoque,
    excluir_produto,
    produtos_com_estoque_baixo,
    saida_estoque,
    salvar_produtos,
)


class ControleEstoqueTest(unittest.TestCase):
    def setUp(self):
        self.produtos = []

    def test_criar_produto(self):
        produto = criar_produto(self.produtos, "P001", "Teclado", 10, 2)

        self.assertEqual(produto["id"], 1)
        self.assertEqual(produto["codigo"], "P001")
        self.assertEqual(produto["quantidade"], 10)
        self.assertEqual(produto["estoque_minimo"], 2)

    def test_rejeita_codigo_duplicado(self):
        criar_produto(self.produtos, "P001", "Teclado")

        with self.assertRaises(ValueError):
            criar_produto(self.produtos, "p001", "Outro produto")

    def test_rejeita_quantidade_negativa(self):
        with self.assertRaises(ValueError):
            criar_produto(self.produtos, "P001", "Teclado", -1)

    def test_entrada_estoque(self):
        criar_produto(self.produtos, "P001", "Teclado", 5)

        produto = entrada_estoque(self.produtos, "P001", 3)

        self.assertEqual(produto["quantidade"], 8)

    def test_saida_estoque(self):
        criar_produto(self.produtos, "P001", "Teclado", 5)

        produto = saida_estoque(self.produtos, "P001", 2)

        self.assertEqual(produto["quantidade"], 3)

    def test_rejeita_saida_maior_que_estoque(self):
        criar_produto(self.produtos, "P001", "Teclado", 2)

        with self.assertRaises(ValueError):
            saida_estoque(self.produtos, "P001", 3)

    def test_detecta_estoque_baixo(self):
        criar_produto(self.produtos, "P001", "Teclado", 2, 2)
        criar_produto(self.produtos, "P002", "Mouse", 8, 2)

        baixos = produtos_com_estoque_baixo(self.produtos)

        self.assertEqual(len(baixos), 1)
        self.assertEqual(baixos[0]["codigo"], "P001")

    def test_busca_por_nome_ou_codigo(self):
        criar_produto(self.produtos, "P001", "Teclado Mecânico")
        criar_produto(self.produtos, "P002", "Mouse")

        por_nome = buscar_produtos(self.produtos, "MECÂNICO")
        por_codigo = buscar_produtos(self.produtos, "p002")

        self.assertEqual(por_nome[0]["codigo"], "P001")
        self.assertEqual(por_codigo[0]["nome"], "Mouse")

    def test_excluir_produto(self):
        criar_produto(self.produtos, "P001", "Teclado")

        removido = excluir_produto(self.produtos, "P001")

        self.assertEqual(removido["nome"], "Teclado")
        self.assertEqual(self.produtos, [])

    def test_salvar_e_carregar_json(self):
        criar_produto(self.produtos, "P001", "Teclado", 10, 2)

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "estoque.json"
            salvar_produtos(self.produtos, caminho)
            carregados = carregar_produtos(caminho)

        self.assertEqual(carregados, self.produtos)


if __name__ == "__main__":
    unittest.main()
