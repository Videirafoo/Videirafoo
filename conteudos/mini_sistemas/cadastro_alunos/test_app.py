import tempfile
import unittest
from pathlib import Path

from conteudos.mini_sistemas.cadastro_alunos.app import (
    adicionar_nota,
    buscar_alunos,
    calcular_media,
    calcular_situacao,
    carregar_alunos,
    criar_aluno,
    excluir_aluno,
    gerar_relatorio,
    salvar_alunos,
)


class CadastroAlunosTest(unittest.TestCase):
    def setUp(self):
        self.alunos = []

    def test_criar_aluno(self):
        aluno = criar_aluno(self.alunos, "Ana Silva", "2026001")

        self.assertEqual(aluno["id"], 1)
        self.assertEqual(aluno["nome"], "Ana Silva")
        self.assertEqual(aluno["matricula"], "2026001")
        self.assertEqual(aluno["notas"], [])

    def test_rejeita_nome_vazio(self):
        with self.assertRaises(ValueError):
            criar_aluno(self.alunos, "   ", "2026001")

    def test_rejeita_matricula_duplicada(self):
        criar_aluno(self.alunos, "Ana", "ABC123")

        with self.assertRaises(ValueError):
            criar_aluno(self.alunos, "Bruno", "abc123")

    def test_adicionar_nota_e_calcular_media(self):
        criar_aluno(self.alunos, "Ana", "1")
        adicionar_nota(self.alunos, "1", 8)
        adicionar_nota(self.alunos, "1", 6)

        self.assertEqual(calcular_media(self.alunos[0]), 7)
        self.assertEqual(calcular_situacao(self.alunos[0]), "aprovado")

    def test_rejeita_nota_fora_do_intervalo(self):
        criar_aluno(self.alunos, "Ana", "1")

        with self.assertRaises(ValueError):
            adicionar_nota(self.alunos, "1", 11)

    def test_calcular_situacoes(self):
        aprovado = criar_aluno(self.alunos, "A", "1")
        recuperacao = criar_aluno(self.alunos, "B", "2")
        reprovado = criar_aluno(self.alunos, "C", "3")
        sem_notas = criar_aluno(self.alunos, "D", "4")

        aprovado["notas"] = [7, 8]
        recuperacao["notas"] = [5, 6]
        reprovado["notas"] = [3, 4]

        self.assertEqual(calcular_situacao(aprovado), "aprovado")
        self.assertEqual(calcular_situacao(recuperacao), "recuperacao")
        self.assertEqual(calcular_situacao(reprovado), "reprovado")
        self.assertEqual(calcular_situacao(sem_notas), "sem notas")

    def test_busca_por_nome_ou_matricula(self):
        criar_aluno(self.alunos, "Carlos Souza", "2026A")
        criar_aluno(self.alunos, "Marina Lima", "2026B")

        por_nome = buscar_alunos(self.alunos, "CARLOS")
        por_matricula = buscar_alunos(self.alunos, "2026b")

        self.assertEqual(len(por_nome), 1)
        self.assertEqual(por_nome[0]["nome"], "Carlos Souza")
        self.assertEqual(len(por_matricula), 1)
        self.assertEqual(por_matricula[0]["nome"], "Marina Lima")

    def test_excluir_aluno(self):
        criar_aluno(self.alunos, "Ana", "1")

        removido = excluir_aluno(self.alunos, "1")

        self.assertEqual(removido["nome"], "Ana")
        self.assertEqual(self.alunos, [])

    def test_gerar_relatorio(self):
        aluno = criar_aluno(self.alunos, "Ana", "1")
        aluno["notas"] = [8, 9]

        relatorio = gerar_relatorio(self.alunos)

        self.assertEqual(relatorio[0]["media"], 8.5)
        self.assertEqual(relatorio[0]["situacao"], "aprovado")

    def test_salvar_e_carregar_json(self):
        criar_aluno(self.alunos, "Ana", "1")

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "alunos.json"
            salvar_alunos(self.alunos, caminho)
            carregados = carregar_alunos(caminho)

        self.assertEqual(carregados, self.alunos)


if __name__ == "__main__":
    unittest.main()
