import unittest

from projetos.github_student_dashboard.engine import (
    analisar_perfil_snapshot,
    analisar_snapshot,
    normalizar_referencia,
    normalizar_usuario,
    resumir_status_ci,
)


class EngineEdgeCasesTest(unittest.TestCase):
    def test_rejeita_urls_fora_do_github(self):
        with self.assertRaises(ValueError):
            normalizar_referencia("https://example.com/owner/repo")
        with self.assertRaises(ValueError):
            normalizar_usuario("https://example.com/owner")

    def test_rejeita_usuario_vazio_ou_com_caminho(self):
        with self.assertRaises(ValueError):
            normalizar_usuario("https://github.com/")
        with self.assertRaises(ValueError):
            normalizar_usuario("owner/repo")

    def test_resumo_ci_cobre_estados_de_borda(self):
        self.assertEqual(resumir_status_ci(None)["estado"], "indisponivel")
        self.assertEqual(resumir_status_ci({"erro": "rate limit"})["erro"], "rate limit")
        self.assertEqual(
            resumir_status_ci({"workflow_runs": [{"status": "in_progress", "name": "CI"}]})["estado"],
            "in_progress",
        )
        self.assertEqual(
            resumir_status_ci({"workflow_runs": [{"status": "completed", "conclusion": None}]})["estado"],
            "completed",
        )

    def _snapshot(self, estado_ci):
        workflow_runs = {
            "workflow_runs": [
                {
                    "name": "CI",
                    "status": "completed" if estado_ci not in {"queued", "in_progress"} else estado_ci,
                    "conclusion": estado_ci if estado_ci not in {"queued", "in_progress", "sem_execucao"} else None,
                    "html_url": "https://github.com/exemplo/projeto/actions/runs/1",
                }
            ]
        }
        if estado_ci == "sem_execucao":
            workflow_runs = {"workflow_runs": []}
        return {
            "metadata": {
                "full_name": "exemplo/projeto",
                "html_url": "https://github.com/exemplo/projeto",
                "default_branch": "main",
                "description": "Projeto",
                "license": None,
                "topics": ["python"],
            },
            "arvore": {
                "truncated": False,
                "tree": [
                    {"path": "README.md", "type": "blob"},
                    {"path": "LICENSE", "type": "blob"},
                    {"path": ".gitignore", "type": "blob"},
                    {"path": "requirements.txt", "type": "blob"},
                    {"path": "tests/test_app.py", "type": "blob"},
                    {"path": ".github/workflows/ci.yml", "type": "blob"},
                ],
            },
            "linguagens": {"Python": 500},
            "workflow_runs": workflow_runs,
        }

    def test_detalhes_ci_failure(self):
        relatorio = analisar_snapshot(self._snapshot("failure"))
        self.assertIn("failure", relatorio["detalhes_checks"]["ci"]["observado"])
        self.assertIn("corrigir", relatorio["detalhes_checks"]["ci"]["acao"])

    def test_detalhes_ci_em_andamento(self):
        relatorio = analisar_snapshot(self._snapshot("queued"))
        self.assertIn("andamento", relatorio["detalhes_checks"]["ci"]["observado"])

    def test_detalhes_ci_sem_execucao(self):
        relatorio = analisar_snapshot(self._snapshot("sem_execucao"))
        self.assertIn("nenhuma execução", relatorio["detalhes_checks"]["ci"]["observado"].lower())

    def test_perfil_vazio_expoe_lacunas_sem_divisao_por_zero(self):
        usuario = {"login": "aluno", "name": "", "bio": "", "followers": 0, "following": 0, "public_repos": 0}
        relatorio = analisar_perfil_snapshot(usuario, [])
        self.assertEqual(relatorio["repositorios_analisados"], 0)
        self.assertEqual(relatorio["cobertura"]["descricao"]["percentual"], 0)
        self.assertIn("nome_publico", relatorio["lacunas_objetivas"])
        self.assertIn("bio", relatorio["lacunas_objetivas"])
        self.assertIn("repositorio_perfil", relatorio["lacunas_objetivas"])


if __name__ == "__main__":
    unittest.main()
