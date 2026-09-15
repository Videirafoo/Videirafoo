import json
import tempfile
import unittest
from pathlib import Path

from conteudos.mini_sistemas.projeto_integrado.app import (
    analisar_repositorio,
    salvar_relatorio,
)


class ProjetoIntegradoTest(unittest.TestCase):
    def criar_repo_completo(self, raiz):
        raiz = Path(raiz)
        (raiz / "README.md").write_text("# Projeto\n", encoding="utf-8")
        (raiz / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
        (raiz / "LICENSE").write_text("MIT\n", encoding="utf-8")
        (raiz / "requirements.txt").write_text("Flask\n", encoding="utf-8")
        (raiz / "app.py").write_text("print('ok')\n", encoding="utf-8")
        (raiz / "test_app.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
        workflows = raiz / ".github" / "workflows"
        workflows.mkdir(parents=True)
        (workflows / "ci.yml").write_text("name: CI\n", encoding="utf-8")

    def test_repo_completo_recebe_score_100(self):
        with tempfile.TemporaryDirectory() as pasta:
            self.criar_repo_completo(pasta)
            relatorio = analisar_repositorio(pasta)

        self.assertEqual(relatorio["score"], 100)
        self.assertTrue(all(relatorio["checks"].values()))

    def test_repo_incompleto_gera_recomendacoes(self):
        with tempfile.TemporaryDirectory() as pasta:
            Path(pasta, "main.py").write_text("print('oi')\n", encoding="utf-8")
            relatorio = analisar_repositorio(pasta)

        self.assertLess(relatorio["score"], 100)
        self.assertGreater(len(relatorio["recomendacoes"]), 1)
        self.assertFalse(relatorio["checks"]["readme"])

    def test_detecta_linguagens(self):
        with tempfile.TemporaryDirectory() as pasta:
            Path(pasta, "main.py").write_text("print('oi')\n", encoding="utf-8")
            Path(pasta, "index.html").write_text("<h1>Oi</h1>\n", encoding="utf-8")
            relatorio = analisar_repositorio(pasta)

        linguagens = relatorio["evidencias"]["linguagens_estimadas"]
        self.assertEqual(linguagens["Python"], 1)
        self.assertEqual(linguagens["HTML"], 1)

    def test_ignora_arquivos_de_venv(self):
        with tempfile.TemporaryDirectory() as pasta:
            venv = Path(pasta, ".venv")
            venv.mkdir()
            (venv / "interno.py").write_text("print('ignorar')\n", encoding="utf-8")
            Path(pasta, "main.py").write_text("print('ok')\n", encoding="utf-8")
            relatorio = analisar_repositorio(pasta)

        self.assertEqual(relatorio["evidencias"]["total_arquivos_analisados"], 1)

    def test_caminho_inexistente_rejeitado(self):
        with self.assertRaises(ValueError):
            analisar_repositorio("/caminho/que/nao/existe")

    def test_arquivo_em_vez_de_pasta_rejeitado(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta, "arquivo.txt")
            arquivo.write_text("x", encoding="utf-8")

            with self.assertRaises(ValueError):
                analisar_repositorio(arquivo)

    def test_salvar_relatorio_json(self):
        with tempfile.TemporaryDirectory() as pasta:
            Path(pasta, "README.md").write_text("# Projeto\n", encoding="utf-8")
            relatorio = analisar_repositorio(pasta)
            destino = Path(pasta, "relatorio.json")
            salvar_relatorio(relatorio, destino)
            carregado = json.loads(destino.read_text(encoding="utf-8"))

        self.assertEqual(carregado["repositorio"], relatorio["repositorio"])
        self.assertEqual(carregado["score"], relatorio["score"])


if __name__ == "__main__":
    unittest.main()
