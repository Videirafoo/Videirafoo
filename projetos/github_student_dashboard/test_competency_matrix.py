import unittest
from unittest.mock import patch
from urllib.error import URLError

import projetos.github_student_dashboard.competency_matrix as matrix_module
from projetos.github_student_dashboard.competency_matrix import gerar_matriz_competencias
from projetos.github_student_dashboard.github_client import GitHubApiError
from projetos.github_student_dashboard.web import create_app


MINI_SISTEMAS = [
    "agenda_contatos",
    "lista_tarefas",
    "cadastro_alunos",
    "controle_estoque",
    "sistema_biblioteca",
    "caixa_mercado",
    "controle_financeiro",
    "gerenciador_habitos",
    "api_tarefas",
    "projeto_integrado",
]


def _tree(paths):
    return {"tree": [{"path": path} for path in sorted(paths)]}


class FakeHealthResponse:
    def __init__(self, status=200, body='{"status":"ok"}'):
        self.status = status
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self.body.encode("utf-8")


class FakeGitHubClient:
    def __init__(
        self,
        pr_state="open",
        pr_merged=False,
        fail_repo=None,
        workflow_status="completed",
        workflow_conclusion="success",
        include_workflow=True,
        workflow_error=False,
        pr_error=False,
    ):
        self.pr_state = pr_state
        self.pr_merged = pr_merged
        self.fail_repo = fail_repo
        self.workflow_status = workflow_status
        self.workflow_conclusion = workflow_conclusion
        self.include_workflow = include_workflow
        self.workflow_error = workflow_error
        self.pr_error = pr_error

        profile_paths = {
            ".github/workflows/student-dashboard.yml",
            "projetos/github_student_dashboard/.coveragerc",
            "projetos/github_student_dashboard/web.py",
            "projetos/github_student_dashboard/lab_web.py",
            "projetos/github_student_dashboard/ai_explainer.py",
            "projetos/github_student_dashboard/test_ai_explainer.py",
            "projetos/github_student_dashboard/test_ai_provider.py",
            "projetos/github_student_dashboard/engine.py",
            "projetos/github_student_dashboard/CHANGELOG.md",
            "conteudos/mini_sistemas/api_tarefas/app.py",
            "README.md",
            "GUIA_DE_ESTUDOS.md",
            "PADRAO_DE_ENSINO.md",
            "QUALITY.md",
        }
        for nome in MINI_SISTEMAS:
            profile_paths.add(f"conteudos/mini_sistemas/{nome}/app.py")
            profile_paths.add(f"conteudos/mini_sistemas/{nome}/test_app.py")

        self.trees = {
            "Videirafoo": _tree(profile_paths),
            "Lista-01-segundo-periodo": _tree({"README.md", "exercicio1.py"}),
            "Lista-03-segundo-periodo": _tree({"README.md", "busca1.py", "busca2.py"}),
            "lista-04-segundo-periodo": _tree({"README.md", "recursao.py"}),
        }

    def buscar_arvore(self, owner, repo, ref):
        if repo == self.fail_repo:
            raise GitHubApiError("falha simulada", status=502)
        return self.trees[repo]

    def buscar_workflow_runs(self, owner, repo, branch=None, limite=1):
        if self.workflow_error:
            raise GitHubApiError("workflow indisponível", status=502)
        if not self.include_workflow:
            return {"workflow_runs": []}
        return {
            "workflow_runs": [
                {
                    "name": "GitHub Student Dashboard CI",
                    "status": self.workflow_status,
                    "conclusion": self.workflow_conclusion,
                    "html_url": "https://github.com/Videirafoo/Videirafoo/actions/runs/1",
                }
            ]
        }

    def buscar_pull_request(self, owner, repo, numero):
        if self.pr_error:
            raise GitHubApiError("PR indisponível", status=502)
        return {
            "state": self.pr_state,
            "merged": self.pr_merged,
            "merged_at": "2026-09-15T18:00:00Z" if self.pr_merged else None,
            "html_url": "https://github.com/fork-commit-merge/fork-commit-merge/pull/8150",
        }


class CompetencyMatrixTests(unittest.TestCase):
    def test_matriz_mede_evidencias_sem_certificar_dominio(self):
        resultado = gerar_matriz_competencias(
            client=FakeGitHubClient(),
            health_checker=lambda: (True, "ok"),
        )

        self.assertEqual(resultado["resumo"]["total_competencias"], 10)
        self.assertEqual(resultado["resumo"]["total_evidencias"], 13)
        self.assertEqual(resultado["resumo"]["evidencias_verificadas"], 12)
        self.assertEqual(resultado["resumo"]["forte"], 9)
        self.assertEqual(resultado["resumo"]["parcial"], 1)
        self.assertIn("não certifica domínio pessoal", resultado["metodologia"])

    def test_pr_aberto_e_parcial_ate_merge_publico(self):
        resultado = gerar_matriz_competencias(
            client=FakeGitHubClient(pr_state="open", pr_merged=False),
            health_checker=lambda: (True, "ok"),
        )
        open_source = next(item for item in resultado["competencias"] if item["id"] == "open-source")
        self.assertEqual(open_source["estado_evidencia"], "parcial")
        self.assertIn("ainda não aceita", open_source["evidencias"][0]["detalhe"])

    def test_pr_mergeado_torna_evidencia_open_source_forte(self):
        resultado = gerar_matriz_competencias(
            client=FakeGitHubClient(pr_state="closed", pr_merged=True),
            health_checker=lambda: (True, "ok"),
        )
        open_source = next(item for item in resultado["competencias"] if item["id"] == "open-source")
        self.assertEqual(open_source["estado_evidencia"], "forte")
        self.assertEqual(resultado["resumo"]["forte"], 10)
        self.assertEqual(resultado["resumo"]["evidencias_verificadas"], 13)

    def test_pr_fechado_sem_merge_permanece_parcial(self):
        resultado = gerar_matriz_competencias(
            client=FakeGitHubClient(pr_state="closed", pr_merged=False),
            health_checker=lambda: (True, "ok"),
        )
        open_source = next(item for item in resultado["competencias"] if item["id"] == "open-source")
        self.assertIn("fechado sem evidência de merge", open_source["evidencias"][0]["detalhe"])

    def test_pr_indisponivel_nao_vira_evidencia(self):
        resultado = gerar_matriz_competencias(
            client=FakeGitHubClient(pr_error=True),
            health_checker=lambda: (True, "ok"),
        )
        open_source = next(item for item in resultado["competencias"] if item["id"] == "open-source")
        self.assertEqual(open_source["estado_evidencia"], "indisponivel")

    def test_healthcheck_falho_nao_inventa_deploy_verificado(self):
        resultado = gerar_matriz_competencias(
            client=FakeGitHubClient(),
            health_checker=lambda: (False, "health indisponível"),
        )
        deploy = next(item for item in resultado["competencias"] if item["id"] == "deploy-operacao")
        self.assertEqual(deploy["estado_evidencia"], "parcial")
        self.assertEqual(deploy["evidencias"][0]["estado"], "parcial")

    def test_falha_da_api_em_um_repo_preserva_resto_da_matriz(self):
        resultado = gerar_matriz_competencias(
            client=FakeGitHubClient(fail_repo="Lista-03-segundo-periodo"),
            health_checker=lambda: (True, "ok"),
        )
        algoritmos = next(item for item in resultado["competencias"] if item["id"] == "algoritmos-busca")
        fundamentos = next(item for item in resultado["competencias"] if item["id"] == "fundamentos-python")
        self.assertEqual(algoritmos["estado_evidencia"], "indisponivel")
        self.assertEqual(fundamentos["estado_evidencia"], "forte")

    def test_ci_em_andamento_e_parcial(self):
        resultado = gerar_matriz_competencias(
            client=FakeGitHubClient(workflow_status="in_progress", workflow_conclusion=None),
            health_checker=lambda: (True, "ok"),
        )
        qualidade = next(item for item in resultado["competencias"] if item["id"] == "qualidade-ci")
        self.assertEqual(qualidade["estado_evidencia"], "parcial")
        self.assertIn("em andamento", qualidade["evidencias"][1]["detalhe"])

    def test_ci_sem_execucao_nao_inventa_resultado(self):
        resultado = gerar_matriz_competencias(
            client=FakeGitHubClient(include_workflow=False),
            health_checker=lambda: (True, "ok"),
        )
        qualidade = next(item for item in resultado["competencias"] if item["id"] == "qualidade-ci")
        self.assertEqual(qualidade["evidencias"][1]["estado"], "ausente")

    def test_ci_indisponivel_preserva_evidencia_versionada(self):
        resultado = gerar_matriz_competencias(
            client=FakeGitHubClient(workflow_error=True),
            health_checker=lambda: (True, "ok"),
        )
        qualidade = next(item for item in resultado["competencias"] if item["id"] == "qualidade-ci")
        self.assertEqual(qualidade["evidencias"][0]["estado"], "verificada")
        self.assertEqual(qualidade["evidencias"][1]["estado"], "indisponivel")
        self.assertEqual(qualidade["estado_evidencia"], "parcial")

    def test_estado_sem_evidencia_exige_ausencia_real(self):
        estado = matrix_module._estado_competencia([{"estado": "ausente"}])
        self.assertEqual(estado, "sem_evidencia")

    @patch("projetos.github_student_dashboard.competency_matrix.urlopen")
    def test_healthcheck_publico_ok(self, urlopen_mock):
        urlopen_mock.return_value = FakeHealthResponse()
        ok, detalhe = matrix_module._healthcheck_publico(timeout=1)
        self.assertTrue(ok)
        self.assertIn("status=ok", detalhe)

    @patch("projetos.github_student_dashboard.competency_matrix.urlopen")
    def test_healthcheck_publico_http_nao_200(self, urlopen_mock):
        urlopen_mock.return_value = FakeHealthResponse(status=503)
        ok, detalhe = matrix_module._healthcheck_publico(timeout=1)
        self.assertFalse(ok)
        self.assertIn("HTTP 503", detalhe)

    @patch("projetos.github_student_dashboard.competency_matrix.urlopen")
    def test_healthcheck_publico_sem_status_ok(self, urlopen_mock):
        urlopen_mock.return_value = FakeHealthResponse(body='{"status":"degraded"}')
        ok, detalhe = matrix_module._healthcheck_publico(timeout=1)
        self.assertFalse(ok)
        self.assertIn("sem status=ok", detalhe)

    @patch("projetos.github_student_dashboard.competency_matrix.urlopen", side_effect=URLError("offline"))
    def test_healthcheck_publico_trata_falha_de_rede(self, _urlopen_mock):
        ok, detalhe = matrix_module._healthcheck_publico(timeout=1)
        self.assertFalse(ok)
        self.assertIn("URLError", detalhe)


class CompetencyMatrixWebTests(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "gerado_em": "2026-09-15T18:00:00+00:00",
            "cache_segundos": 600,
            "metodologia": "mede evidências públicas; não certifica domínio pessoal",
            "resumo": {
                "total_competencias": 1,
                "total_evidencias": 1,
                "evidencias_verificadas": 1,
                "forte": 1,
                "parcial": 0,
                "sem_evidencia": 0,
                "indisponivel": 0,
            },
            "competencias": [
                {
                    "id": "teste",
                    "nivel": 1,
                    "titulo": "Teste",
                    "descricao": "Competência de teste",
                    "proximo_passo": "Continuar",
                    "estado_evidencia": "forte",
                    "verificadas": 1,
                    "total_evidencias": 1,
                    "evidencias": [
                        {
                            "titulo": "Evidência",
                            "estado": "verificada",
                            "detalhe": "ok",
                            "url": "https://github.com/Videirafoo/Videirafoo",
                        }
                    ],
                }
            ],
        }
        self.app = create_app(gerador_competencias=lambda: self.payload).test_client()

    def test_pagina_competencias_existe(self):
        response = self.app.get("/competencias")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Matriz Viva de Competências", html)
        self.assertIn("/static/competencias.js", html)

    def test_api_competencias_retorna_payload(self):
        response = self.app.get("/api/competencias")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["resumo"]["forte"], 1)

    def test_sitemap_inclui_competencias(self):
        response = self.app.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("/competencias</loc>", response.get_data(as_text=True))

    def test_dashboard_exibe_atalho_para_competencias(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('href="/competencias"', response.get_data(as_text=True))

    def test_laboratorio_exibe_atalho_para_competencias(self):
        response = self.app.get("/laboratorio")
        self.assertEqual(response.status_code, 200)
        self.assertIn('href="/competencias"', response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
