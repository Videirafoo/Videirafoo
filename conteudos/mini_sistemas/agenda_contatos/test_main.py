import json
import tempfile
import unittest
from pathlib import Path

from conteudos.mini_sistemas.agenda_contatos.main import (
    adicionar_contato,
    buscar_indice,
    carregar_contatos,
    criar_contato,
    salvar_contatos,
)


class AgendaContatosTest(unittest.TestCase):
    def test_criar_contato_valido(self):
        contato = criar_contato("Ana", "99999-0000", "ana@example.com")
        self.assertEqual(contato["nome"], "Ana")
        self.assertEqual(contato["telefone"], "99999-0000")

    def test_criar_contato_exige_nome(self):
        with self.assertRaises(ValueError):
            criar_contato("", "99999-0000")

    def test_busca_ignora_maiusculas_e_espacos(self):
        contatos = [{"nome": "Ana Maria", "telefone": "123", "email": ""}]
        self.assertEqual(buscar_indice(contatos, "  ana maria  "), 0)

    def test_nao_permite_nome_duplicado(self):
        contatos = [{"nome": "Ana", "telefone": "123", "email": ""}]
        with self.assertRaises(ValueError):
            adicionar_contato(contatos, criar_contato("ana", "456"))

    def test_salvar_e_carregar_json(self):
        contatos = [{"nome": "Ana", "telefone": "123", "email": ""}]

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "contatos.json"
            salvar_contatos(contatos, caminho)
            carregados = carregar_contatos(caminho)

        self.assertEqual(carregados, contatos)

    def test_json_invalido_retorna_lista_vazia(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "contatos.json"
            caminho.write_text("{invalido", encoding="utf-8")
            carregados = carregar_contatos(caminho)

        self.assertEqual(carregados, [])


if __name__ == "__main__":
    unittest.main()
