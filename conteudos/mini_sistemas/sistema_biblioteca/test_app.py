import tempfile
import unittest
from pathlib import Path

from conteudos.mini_sistemas.sistema_biblioteca.app import (
    buscar_livros,
    cadastrar_livro,
    cadastrar_usuario,
    carregar_dados,
    devolver_livro,
    emprestar_livro,
    listar_emprestimos_ativos,
    novo_estado,
    salvar_dados,
)


class SistemaBibliotecaTest(unittest.TestCase):
    def setUp(self):
        self.dados = novo_estado()

    def test_cadastrar_livro(self):
        livro = cadastrar_livro(self.dados, "978-1", "Python Básico", "Ana")

        self.assertEqual(livro["id"], 1)
        self.assertEqual(livro["isbn"], "978-1")
        self.assertTrue(livro["disponivel"])

    def test_rejeita_isbn_duplicado(self):
        cadastrar_livro(self.dados, "978-1", "Python", "Ana")

        with self.assertRaises(ValueError):
            cadastrar_livro(self.dados, "978-1", "Outro", "Bruno")

    def test_cadastrar_usuario(self):
        usuario = cadastrar_usuario(self.dados, "Carlos", "DOC1")

        self.assertEqual(usuario["id"], 1)
        self.assertEqual(usuario["documento"], "DOC1")

    def test_rejeita_usuario_duplicado(self):
        cadastrar_usuario(self.dados, "Carlos", "DOC1")

        with self.assertRaises(ValueError):
            cadastrar_usuario(self.dados, "Marina", "doc1")

    def test_emprestar_livro(self):
        livro = cadastrar_livro(self.dados, "978-1", "Python", "Ana")
        cadastrar_usuario(self.dados, "Carlos", "DOC1")

        emprestimo = emprestar_livro(self.dados, "978-1", "DOC1")

        self.assertFalse(livro["disponivel"])
        self.assertFalse(emprestimo["devolvido"])
        self.assertEqual(len(listar_emprestimos_ativos(self.dados)), 1)

    def test_bloqueia_emprestimo_de_livro_indisponivel(self):
        cadastrar_livro(self.dados, "978-1", "Python", "Ana")
        cadastrar_usuario(self.dados, "Carlos", "DOC1")
        cadastrar_usuario(self.dados, "Marina", "DOC2")
        emprestar_livro(self.dados, "978-1", "DOC1")

        with self.assertRaises(ValueError):
            emprestar_livro(self.dados, "978-1", "DOC2")

    def test_devolver_livro(self):
        livro = cadastrar_livro(self.dados, "978-1", "Python", "Ana")
        cadastrar_usuario(self.dados, "Carlos", "DOC1")
        emprestar_livro(self.dados, "978-1", "DOC1")

        emprestimo = devolver_livro(self.dados, "978-1")

        self.assertTrue(livro["disponivel"])
        self.assertTrue(emprestimo["devolvido"])
        self.assertEqual(listar_emprestimos_ativos(self.dados), [])

    def test_buscar_livro_por_titulo_autor_ou_isbn(self):
        cadastrar_livro(self.dados, "978-1", "Python Básico", "Ana Souza")
        cadastrar_livro(self.dados, "978-2", "Algoritmos", "Bruno Lima")

        por_titulo = buscar_livros(self.dados, "PYTHON")
        por_autor = buscar_livros(self.dados, "bruno")
        por_isbn = buscar_livros(self.dados, "978-1")

        self.assertEqual(por_titulo[0]["isbn"], "978-1")
        self.assertEqual(por_autor[0]["isbn"], "978-2")
        self.assertEqual(por_isbn[0]["titulo"], "Python Básico")

    def test_salvar_e_carregar_json(self):
        cadastrar_livro(self.dados, "978-1", "Python", "Ana")
        cadastrar_usuario(self.dados, "Carlos", "DOC1")
        emprestar_livro(self.dados, "978-1", "DOC1")

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "biblioteca.json"
            salvar_dados(self.dados, caminho)
            carregados = carregar_dados(caminho)

        self.assertEqual(carregados, self.dados)


if __name__ == "__main__":
    unittest.main()
