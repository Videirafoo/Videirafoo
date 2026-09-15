import unittest

from projetos.github_student_dashboard.history import (
    analisar_estado_versionado,
    analisar_historico_remoto,
    construir_evolucao,
)


class ClienteHistoricoFalso:
    def __init__(self):
        self.chamadas = []

    def buscar_commits(self, owner, repo, limite=5):
        self.chamadas.append(("commits", owner, repo, limite))
        return [
            {
                "sha": "bbbbbbbbbbbb",
                "html_url": "https://github.com/org/repo/commit/b",
                "commit": {
                    "message": "feat: adiciona testes e CI\n\nDetalhes",
                    "author": {"name": "Aluno", "date": "2026-09-15T02:00:00Z"},
                },
            },
            {
                "sha": "aaaaaaaaaaaa",
                "html_url": "https://github.com/org/repo/commit/a",
                "commit": {
                    "message": "docs: cria README",
                    "author": {"name": "Aluno", "date": "2026-09-14T02:00:00Z"},
                },
            },
        ]

    def buscar_arvore(self, owner, repo, ref):
        self.chamadas.append(("tree", owner, repo, ref))
        if ref.startswith("b"):
            caminhos = [
                "README.md",
                ".gitignore",
                ".github/workflows/ci.yml",
                "test_app.py",
                "requirements.txt",
            ]
        else:
            caminhos = ["README.md", "app.py"]

        return {
            "truncated": False,
            "tree": [{"path": caminho, "type": "blob"} for caminho in caminhos],
        }


class HistoryTest(unittest.TestCase):
    def test_estado_versionado_mede_cinco_sinais(self):
        arvore = {
            "tree": [
                {"path": "README.md", "type": "blob"},
                {"path": ".gitignore", "type": "blob"},
                {"path": ".github/workflows/ci.yml", "type": "blob"},
                {"path": "test_app.py", "type": "blob"},
                {"path": "requirements.txt", "type": "blob"},
            ]
        }

        resultado = analisar_estado_versionado(arvore)

        self.assertEqual(resultado["cobertura_versionada"]["percentual"], 100.0)
        self.assertTrue(all(resultado["checks"].values()))

    def test_evolucao_detecta_checks_adicionados(self):
        snapshots = [
            {
                "commit": {"sha": "b"},
                "estado": {
                    "checks": {
                        "readme": True,
                        "gitignore": True,
                        "ci": True,
                        "testes": True,
                        "dependencias": True,
                    }
                },
            },
            {
                "commit": {"sha": "a"},
                "estado": {
                    "checks": {
                        "readme": True,
                        "gitignore": False,
                        "ci": False,
                        "testes": False,
                        "dependencias": False,
                    }
                },
            },
        ]

        evolucao = construir_evolucao(snapshots)

        self.assertEqual(evolucao[0]["commit"]["sha"], "a")
        self.assertEqual(
            set(evolucao[1]["mudancas"]["adicionados"]),
            {"gitignore", "ci", "testes", "dependencias"},
        )
        self.assertEqual(evolucao[1]["mudancas"]["removidos"], [])

    def test_historico_remoto_reconstroi_commits(self):
        cliente = ClienteHistoricoFalso()

        resultado = analisar_historico_remoto("org/repo", client=cliente, limite=5)

        self.assertEqual(resultado["commits_analisados"], 2)
        self.assertEqual(resultado["evolucao"][-1]["commit"]["sha_curto"], "bbbbbbb")
        self.assertEqual(resultado["evolucao"][-1]["estado"]["cobertura_versionada"]["percentual"], 100.0)
        self.assertIn(("commits", "org", "repo", 5), cliente.chamadas)


if __name__ == "__main__":
    unittest.main()
