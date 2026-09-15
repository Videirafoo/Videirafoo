import tempfile
import unittest
from pathlib import Path

from conteudos.mini_sistemas.lista_tarefas.app import (
    buscar_tarefas,
    carregar_tarefas,
    concluir_tarefa,
    criar_tarefa,
    excluir_tarefa,
    filtrar_tarefas,
    salvar_tarefas,
)


class ListaTarefasTest(unittest.TestCase):
    def setUp(self):
        self.tarefas = []

    def test_criar_tarefa(self):
        tarefa = criar_tarefa(self.tarefas, "Estudar Python", "alta")

        self.assertEqual(tarefa["id"], 1)
        self.assertEqual(tarefa["titulo"], "Estudar Python")
        self.assertEqual(tarefa["prioridade"], "alta")
        self.assertFalse(tarefa["concluida"])

    def test_criar_tarefa_rejeita_titulo_vazio(self):
        with self.assertRaises(ValueError):
            criar_tarefa(self.tarefas, "   ")

    def test_criar_tarefa_rejeita_prioridade_invalida(self):
        with self.assertRaises(ValueError):
            criar_tarefa(self.tarefas, "Estudar", "urgente")

    def test_buscar_tarefas_ignora_maiusculas(self):
        criar_tarefa(self.tarefas, "Estudar Python")
        criar_tarefa(self.tarefas, "Fazer exercício")

        resultado = buscar_tarefas(self.tarefas, "PYTHON")

        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["titulo"], "Estudar Python")

    def test_concluir_e_filtrar_tarefas(self):
        primeira = criar_tarefa(self.tarefas, "Tarefa 1")
        criar_tarefa(self.tarefas, "Tarefa 2")

        concluir_tarefa(self.tarefas, primeira["id"])

        self.assertEqual(len(filtrar_tarefas(self.tarefas, "concluidas")), 1)
        self.assertEqual(len(filtrar_tarefas(self.tarefas, "pendentes")), 1)

    def test_excluir_tarefa(self):
        tarefa = criar_tarefa(self.tarefas, "Excluir esta")

        removida = excluir_tarefa(self.tarefas, tarefa["id"])

        self.assertEqual(removida["titulo"], "Excluir esta")
        self.assertEqual(self.tarefas, [])

    def test_salvar_e_carregar_json(self):
        criar_tarefa(self.tarefas, "Persistir tarefa", "baixa")

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "tarefas.json"
            salvar_tarefas(self.tarefas, caminho)
            carregadas = carregar_tarefas(caminho)

        self.assertEqual(carregadas, self.tarefas)


if __name__ == "__main__":
    unittest.main()
