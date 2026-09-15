import unittest
from unittest.mock import patch

import projetos.github_student_dashboard.competency_matrix as matrix_module
from projetos.github_student_dashboard.github_client import GitHubApiError
from projetos.github_student_dashboard.test_competency_matrix import FakeGitHubClient


class CompetencyMatrixEdgeCasesTest(unittest.TestCase):
    def setUp(self):
        matrix_module._CACHE["value"] = None
        matrix_module._CACHE["expires_at"] = 0.0

    def _gerar(self, client):
        return matrix_module.gerar_matriz_competencias(
            client=client,
            health_checker=lambda: (True, "ok"),
        )

    def test_falha_em_fundamentos_fica_indisponivel(self):
        resultado = self._gerar(FakeGitHubClient(fail_repo="Lista-01-segundo-periodo"))
        item = next(c for c in resultado["competencias"] if c["id"] == "fundamentos-python")
        self.assertEqual(item["estado_evidencia"], "indisponivel")

    def test_falha_em_recursividade_fica_indisponivel(self):
        resultado = self._gerar(FakeGitHubClient(fail_repo="lista-04-segundo-periodo"))
        item = next(c for c in resultado["competencias"] if c["id"] == "recursividade")
        self.assertEqual(item["estado_evidencia"], "indisponivel")

    def test_falha_no_repositorio_de_perfil_preserva_matriz(self):
        resultado = self._gerar(FakeGitHubClient(fail_repo="Videirafoo"))
        ids = {"mini-sistemas", "backend-api", "documentacao", "ia-aplicada"}
        afetadas = [c for c in resultado["competencias"] if c["id"] in ids]
        self.assertTrue(afetadas)
        self.assertTrue(all(c["estado_evidencia"] == "indisponivel" for c in afetadas))
        qualidade = next(c for c in resultado["competencias"] if c["id"] == "qualidade-ci")
        self.assertEqual(qualidade["estado_evidencia"], "parcial")

    def test_ci_concluida_com_falha_permanece_parcial(self):
        resultado = self._gerar(
            FakeGitHubClient(workflow_status="completed", workflow_conclusion="failure")
        )
        qualidade = next(c for c in resultado["competencias"] if c["id"] == "qualidade-ci")
        self.assertEqual(qualidade["evidencias"][1]["estado"], "parcial")
        self.assertIn("failure", qualidade["evidencias"][1]["detalhe"])

    def test_pr_com_value_error_fica_indisponivel(self):
        class Client(FakeGitHubClient):
            def buscar_pull_request(self, owner, repo, numero):
                raise ValueError("resposta inválida")

        resultado = self._gerar(Client())
        item = next(c for c in resultado["competencias"] if c["id"] == "open-source")
        self.assertEqual(item["estado_evidencia"], "indisponivel")

    def test_cache_so_e_usado_sem_cliente_injetado(self):
        fake = FakeGitHubClient()
        with patch.object(matrix_module, "GitHubClient", return_value=fake):
            primeiro = matrix_module.gerar_matriz_competencias(
                health_checker=lambda: (True, "ok"),
                usar_cache=False,
            )

        self.assertIs(matrix_module._CACHE["value"], primeiro)
        self.assertGreater(matrix_module._CACHE["expires_at"], 0)

        with patch.object(matrix_module, "GitHubClient", side_effect=AssertionError("cache deveria evitar cliente")):
            segundo = matrix_module.gerar_matriz_competencias()
        self.assertIs(segundo, primeiro)

    def test_estado_indisponivel_sem_sinal_positivo(self):
        estado = matrix_module._estado_competencia([{"estado": "indisponivel"}])
        self.assertEqual(estado, "indisponivel")

    def test_estado_parcial_tem_prioridade_sobre_indisponivel(self):
        estado = matrix_module._estado_competencia(
            [{"estado": "indisponivel"}, {"estado": "parcial"}]
        )
        self.assertEqual(estado, "parcial")


if __name__ == "__main__":
    unittest.main()
