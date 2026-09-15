import tempfile
import unittest
from datetime import date
from pathlib import Path

from conteudos.mini_sistemas.gerenciador_habitos.app import (
    buscar_habitos,
    calcular_sequencia,
    carregar_habitos,
    criar_habito,
    excluir_habito,
    progresso_semanal,
    registrar_conclusao,
    remover_conclusao,
    salvar_habitos,
)


class GerenciadorHabitosTest(unittest.TestCase):
    def setUp(self):
        self.habitos = []

    def test_criar_habito(self):
        habito = criar_habito(self.habitos, "Estudar Python", 5)

        self.assertEqual(habito["id"], 1)
        self.assertEqual(habito["nome"], "Estudar Python")
        self.assertEqual(habito["meta_semanal"], 5)
        self.assertEqual(habito["registros"], [])

    def test_rejeita_nome_vazio(self):
        with self.assertRaises(ValueError):
            criar_habito(self.habitos, "   ", 5)

    def test_rejeita_meta_fora_do_intervalo(self):
        with self.assertRaises(ValueError):
            criar_habito(self.habitos, "Ler", 0)

        with self.assertRaises(ValueError):
            criar_habito(self.habitos, "Ler", 8)

    def test_rejeita_nome_duplicado_ignorando_maiusculas(self):
        criar_habito(self.habitos, "Ler", 4)

        with self.assertRaises(ValueError):
            criar_habito(self.habitos, "ler", 4)

    def test_registro_do_mesmo_dia_nao_duplica(self):
        habito = criar_habito(self.habitos, "Caminhar", 7)

        registrar_conclusao(habito, "2026-09-14")
        registrar_conclusao(habito, "2026-09-14")

        self.assertEqual(habito["registros"], ["2026-09-14"])

    def test_calcula_sequencia_consecutiva(self):
        habito = criar_habito(self.habitos, "Estudar", 7)
        for dia in ["2026-09-13", "2026-09-14", "2026-09-15"]:
            registrar_conclusao(habito, dia)

        sequencia = calcular_sequencia(habito, date(2026, 9, 15))

        self.assertEqual(sequencia, 3)

    def test_sequencia_zero_quando_hoje_nao_foi_registrado(self):
        habito = criar_habito(self.habitos, "Meditar", 7)
        registrar_conclusao(habito, "2026-09-14")

        self.assertEqual(calcular_sequencia(habito, "2026-09-15"), 0)

    def test_progresso_semanal(self):
        habito = criar_habito(self.habitos, "Exercício", 4)
        for dia in ["2026-09-14", "2026-09-15", "2026-09-16"]:
            registrar_conclusao(habito, dia)

        progresso = progresso_semanal(habito, "2026-09-16")

        self.assertEqual(progresso["concluidos"], 3)
        self.assertEqual(progresso["meta"], 4)
        self.assertEqual(progresso["percentual"], 75.0)

    def test_remover_conclusao(self):
        habito = criar_habito(self.habitos, "Água", 7)
        registrar_conclusao(habito, "2026-09-15")

        removido = remover_conclusao(habito, "2026-09-15")

        self.assertTrue(removido)
        self.assertEqual(habito["registros"], [])

    def test_busca_e_exclusao(self):
        primeiro = criar_habito(self.habitos, "Estudar Python", 5)
        criar_habito(self.habitos, "Caminhar", 4)

        encontrados = buscar_habitos(self.habitos, "PYTHON")
        removido = excluir_habito(self.habitos, primeiro["id"])

        self.assertEqual(len(encontrados), 1)
        self.assertEqual(removido["nome"], "Estudar Python")
        self.assertEqual(len(self.habitos), 1)

    def test_salvar_e_carregar_json(self):
        habito = criar_habito(self.habitos, "Ler", 5)
        registrar_conclusao(habito, "2026-09-15")

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "habitos.json"
            salvar_habitos(self.habitos, caminho)
            carregados = carregar_habitos(caminho)

        self.assertEqual(carregados, self.habitos)


if __name__ == "__main__":
    unittest.main()
