import unittest

from projetos.github_student_dashboard.engine import (
    analisar_repositorio_remoto,
    analisar_snapshot,
    normalizar_referencia,
)


class ClienteFalso:
    def __init__(self):
        self.chamadas = []

    def buscar_repositorio(self, owner, repo):
        self.chamadas.append(("repo", owner, repo))
        return {
            "full_name": f"{owner}/{repo}",
            "html_url": f"https://github.com/{owner}/{repo}",
            "default_branch": "main",
            "description": "Projeto de exemplo",
            "license": {"spdx_id": "MIT"},
            "topics": ["python", "education"],
        }

    def buscar_arvore(self, owner, repo, ref):
        self.chamadas.append(("tree", owner, repo, ref))
        caminhos = [
            "README.md",
            ".gitignore",
            "requirements.txt",
            "app.py",
            "test_app.py",
            ".github/workflows/ci.yml",
        ]
        return {
            "truncated": False,
            "tree": [{"path": caminho, "type": "blob"} for caminho in caminhos],
        }

    def buscar_linguagens(self, owner, repo):
        self.chamadas.append(("languages", owner, repo))
        return {"Python": 1200}


class GitHubStudentDashboardEngineTest(unittest.TestCase):
    def test_normaliza_owner_repo(self):
        self.assertEqual(normalizar_referencia("Videirafoo/projeto"), ("Videirafoo", "projeto"))

    def test_normaliza_url_github(self):
        self.assertEqual(
            normalizar_referencia("https://github.com/Videirafoo/projeto.git"),
            ("Videirafoo", "projeto"),
        )

    def test_rejeita_referencia_invalida(self):
        with self.assertRaises(ValueError):
            normalizar_referencia("somente-um-nome")

    def test_snapshot_completo_recebe_score_100(self):
        snapshot = {
            "metadata": {
                "full_name": "Videirafoo/projeto",
                "html_url": "https://github.com/Videirafoo/projeto",
                "default_branch": "main",
                "description": "Projeto completo",
                "license": {"spdx_id": "MIT"},
                "topics": ["python"],
            },
            "arvore": {
                "truncated": False,
                "tree": [
                    {"path": "README.md", "type": "blob"},
                    {"path": ".gitignore", "type": "blob"},
                    {"path": "requirements.txt", "type": "blob"},
                    {"path": "test_app.py", "type": "blob"},
                    {"path": ".github/workflows/ci.yml", "type": "blob"},
                ],
            },
            "linguagens": {"Python": 1000},
        }

        relatorio = analisar_snapshot(snapshot)

        self.assertEqual(relatorio["score"], 100)
        self.assertTrue(all(relatorio["checks"].values()))
        self.assertEqual(relatorio["recomendacoes"], [])

    def test_snapshot_incompleto_gera_recomendacoes(self):
        snapshot = {
            "metadata": {
                "full_name": "Videirafoo/incompleto",
                "html_url": "https://github.com/Videirafoo/incompleto",
                "default_branch": "main",
                "description": None,
                "license": None,
                "topics": [],
            },
            "arvore": {
                "truncated": False,
                "tree": [{"path": "main.py", "type": "blob"}],
            },
            "linguagens": {"Python": 300},
        }

        relatorio = analisar_snapshot(snapshot)

        self.assertEqual(relatorio["score"], 0)
        self.assertEqual(len(relatorio["recomendacoes"]), 8)
        self.assertFalse(relatorio["checks"]["readme"])
        self.assertFalse(relatorio["checks"]["ci"])

    def test_analise_remota_usa_cliente_injetado(self):
        cliente = ClienteFalso()

        relatorio = analisar_repositorio_remoto("Videirafoo/projeto", client=cliente)

        self.assertEqual(relatorio["score"], 100)
        self.assertIn(("repo", "Videirafoo", "projeto"), cliente.chamadas)
        self.assertIn(("tree", "Videirafoo", "projeto", "main"), cliente.chamadas)
        self.assertIn(("languages", "Videirafoo", "projeto"), cliente.chamadas)


if __name__ == "__main__":
    unittest.main()
