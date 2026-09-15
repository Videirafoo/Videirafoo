import unittest

from projetos.github_student_dashboard.engine import (
    analisar_perfil_remoto,
    analisar_perfil_snapshot,
    analisar_repositorio_remoto,
    analisar_snapshot,
    arquivos_de_testes,
    normalizar_referencia,
    normalizar_usuario,
    resumir_status_ci,
)


class ClienteFalso:
    def __init__(self):
        self.chamadas = []

    def buscar_usuario(self, usuario):
        self.chamadas.append(("usuario", usuario))
        return {
            "login": usuario,
            "html_url": f"https://github.com/{usuario}",
            "name": "Fernando Videira",
            "bio": "Estudante de Engenharia de Software",
            "followers": 10,
            "following": 5,
            "public_repos": 2,
        }

    def buscar_repositorios_usuario(self, usuario):
        self.chamadas.append(("repositorios", usuario))
        return [
            {
                "name": usuario,
                "html_url": f"https://github.com/{usuario}/{usuario}",
                "description": "Perfil educacional",
                "language": "Python",
                "fork": False,
                "stargazers_count": 2,
                "forks_count": 1,
                "topics": ["education"],
                "license": {"spdx_id": "MIT"},
                "updated_at": "2026-09-15T00:00:00Z",
            },
            {
                "name": "projeto",
                "html_url": f"https://github.com/{usuario}/projeto",
                "description": None,
                "language": "Python",
                "fork": False,
                "stargazers_count": 1,
                "forks_count": 0,
                "topics": [],
                "license": None,
                "updated_at": "2026-09-14T00:00:00Z",
            },
        ]

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
            "projetos/app/requirements.txt",
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

    def buscar_workflow_runs(self, owner, repo, branch=None, limite=1):
        self.chamadas.append(("workflow_runs", owner, repo, branch, limite))
        return {
            "total_count": 1,
            "workflow_runs": [
                {
                    "name": "CI",
                    "status": "completed",
                    "conclusion": "success",
                    "html_url": f"https://github.com/{owner}/{repo}/actions/runs/1",
                    "updated_at": "2026-09-15T00:00:00Z",
                }
            ],
        }


class GitHubStudentDashboardEngineTest(unittest.TestCase):
    def test_normaliza_owner_repo(self):
        self.assertEqual(normalizar_referencia("Videirafoo/projeto"), ("Videirafoo", "projeto"))

    def test_normaliza_url_github(self):
        self.assertEqual(
            normalizar_referencia("https://github.com/Videirafoo/projeto.git"),
            ("Videirafoo", "projeto"),
        )

    def test_normaliza_usuario(self):
        self.assertEqual(normalizar_usuario("Videirafoo"), "Videirafoo")
        self.assertEqual(normalizar_usuario("https://github.com/Videirafoo"), "Videirafoo")

    def test_rejeita_referencia_invalida(self):
        with self.assertRaises(ValueError):
            normalizar_referencia("somente-um-nome")

    def test_detecta_testes_em_varias_stacks_sem_falso_positivo_simples(self):
        caminhos = {
            "python/test_app.py",
            "web/Button.test.tsx",
            "web/Card.spec.jsx",
            "go/user_test.go",
            "flutter/test/widget_test.dart",
            "java/src/test/java/AppTest.java",
            "ruby/spec/model_spec.rb",
            "dotnet/ServiceTests.cs",
            "php/UserTest.php",
            "src/contest.py",
            "src/latest.ts",
        }

        encontrados = arquivos_de_testes(caminhos)

        self.assertIn("python/test_app.py", encontrados)
        self.assertIn("web/Button.test.tsx", encontrados)
        self.assertIn("web/Card.spec.jsx", encontrados)
        self.assertIn("go/user_test.go", encontrados)
        self.assertIn("flutter/test/widget_test.dart", encontrados)
        self.assertIn("java/src/test/java/AppTest.java", encontrados)
        self.assertIn("ruby/spec/model_spec.rb", encontrados)
        self.assertIn("dotnet/ServiceTests.cs", encontrados)
        self.assertIn("php/UserTest.php", encontrados)
        self.assertNotIn("src/contest.py", encontrados)
        self.assertNotIn("src/latest.ts", encontrados)

    def test_resumir_ci_success(self):
        resumo = resumir_status_ci(
            {
                "workflow_runs": [
                    {
                        "name": "CI",
                        "status": "completed",
                        "conclusion": "success",
                        "html_url": "https://github.com/exemplo/actions/runs/1",
                        "updated_at": "2026-09-15T00:00:00Z",
                    }
                ]
            }
        )
        self.assertEqual(resumo["estado"], "success")
        self.assertEqual(resumo["workflow"], "CI")

    def test_resumir_ci_sem_execucao(self):
        resumo = resumir_status_ci({"workflow_runs": []})
        self.assertEqual(resumo["estado"], "sem_execucao")

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
                    {"path": "projetos/dashboard/requirements.txt", "type": "blob"},
                    {"path": "test_app.py", "type": "blob"},
                    {"path": ".github/workflows/ci.yml", "type": "blob"},
                ],
            },
            "linguagens": {"Python": 1000},
            "workflow_runs": {
                "workflow_runs": [
                    {
                        "name": "CI",
                        "status": "completed",
                        "conclusion": "success",
                        "html_url": "https://github.com/Videirafoo/projeto/actions/runs/1",
                        "updated_at": "2026-09-15T00:00:00Z",
                    }
                ]
            },
        }

        relatorio = analisar_snapshot(snapshot)

        self.assertEqual(relatorio["score"], 100)
        self.assertTrue(all(relatorio["checks"].values()))
        self.assertEqual(relatorio["recomendacoes"], [])
        self.assertEqual(
            relatorio["evidencias"]["arquivos_dependencias"],
            ["projetos/dashboard/requirements.txt"],
        )
        self.assertTrue(relatorio["detalhes_checks"]["readme"]["passou"])
        self.assertIn("README.md", relatorio["detalhes_checks"]["readme"]["observado"])
        self.assertIn("success", relatorio["detalhes_checks"]["ci"]["observado"])
        self.assertEqual(relatorio["ci_execucao"]["estado"], "success")

    def test_snapshot_incompleto_gera_recomendacoes_e_evidencias(self):
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
            "workflow_runs": None,
        }

        relatorio = analisar_snapshot(snapshot)

        self.assertEqual(relatorio["score"], 0)
        self.assertEqual(len(relatorio["recomendacoes"]), 8)
        self.assertFalse(relatorio["checks"]["readme"])
        self.assertFalse(relatorio["checks"]["ci"])
        self.assertEqual(relatorio["ci_execucao"]["estado"], "sem_workflow")
        self.assertIn("vazio", relatorio["detalhes_checks"]["descricao"]["observado"])
        self.assertIn("Nenhum topic", relatorio["detalhes_checks"]["topics"]["observado"])
        self.assertIn("Nenhum workflow", relatorio["detalhes_checks"]["ci"]["observado"])

    def test_analise_remota_usa_cliente_injetado(self):
        cliente = ClienteFalso()

        relatorio = analisar_repositorio_remoto("Videirafoo/projeto", client=cliente)

        self.assertEqual(relatorio["score"], 100)
        self.assertEqual(relatorio["ci_execucao"]["estado"], "success")
        self.assertIn(("repo", "Videirafoo", "projeto"), cliente.chamadas)
        self.assertIn(("tree", "Videirafoo", "projeto", "main"), cliente.chamadas)
        self.assertIn(("languages", "Videirafoo", "projeto"), cliente.chamadas)
        self.assertIn(("workflow_runs", "Videirafoo", "projeto", "main", 1), cliente.chamadas)

    def test_perfil_snapshot_calcula_cobertura_sem_nota_arbitraria(self):
        cliente = ClienteFalso()
        usuario = cliente.buscar_usuario("Videirafoo")
        repositorios = cliente.buscar_repositorios_usuario("Videirafoo")

        relatorio = analisar_perfil_snapshot(usuario, repositorios)

        self.assertEqual(relatorio["repositorios_analisados"], 2)
        self.assertEqual(relatorio["cobertura"]["descricao"]["percentual"], 50.0)
        self.assertEqual(relatorio["engajamento"]["stars_recebidos"], 3)
        self.assertTrue(relatorio["repositorio_perfil_existe"])
        self.assertNotIn("score", relatorio)

    def test_analise_perfil_remoto_usa_cliente_injetado(self):
        cliente = ClienteFalso()

        relatorio = analisar_perfil_remoto("Videirafoo", client=cliente)

        self.assertEqual(relatorio["usuario"], "Videirafoo")
        self.assertIn(("usuario", "Videirafoo"), cliente.chamadas)
        self.assertIn(("repositorios", "Videirafoo"), cliente.chamadas)


if __name__ == "__main__":
    unittest.main()
