import unittest

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


class FakeGitHubClient:
    def __init__(self, pr_state="open", pr_merged=False, fail_repo=None):
        self.pr_state = pr_state
        self.pr_merged = pr_merged
        self.fail_repo = fail_repo

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
        return {
            "workflow_runs": [
                {
                    "name": "GitHub Student Dashboard CI",
                    "status": "completed",
                    "conclusion": "success",
                    "html_url": "https://github.com/Videirafoo/Videirafoo/actions/runs/1",
                }
            ]
        }

    def buscar_pull_request(self, owner, repo, numero):
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
