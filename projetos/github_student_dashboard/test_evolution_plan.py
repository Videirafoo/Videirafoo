import unittest

from projetos.github_student_dashboard.evolution_plan import gerar_plano_evolucao
from projetos.github_student_dashboard.web import create_app


def matriz_com(*competencias):
    return {
        "gerado_em": "2026-09-15T20:00:00+00:00",
        "competencias": list(competencias),
    }


def competencia(identificador, estado, titulo="Competência de teste", nivel=1):
    return {
        "id": identificador,
        "titulo": titulo,
        "nivel": nivel,
        "estado_evidencia": estado,
    }


class EvolutionPlanTests(unittest.TestCase):
    def test_forte_vira_aprofundamento_sem_certificacao(self):
        plano = gerar_plano_evolucao(matriz_com(competencia("fundamentos-python", "forte")))
        item = plano["itens"][0]
        self.assertEqual(item["acao"]["missao_id"], "n1-funcao")
        self.assertEqual(item["acao"]["objetivo"], "Aprofundar sem certificar domínio")
        self.assertEqual(item["acao"]["origem"], "trilha:n1-funcao")

    def test_parcial_recebe_missao_real_para_evoluir(self):
        plano = gerar_plano_evolucao(matriz_com(competencia("open-source", "parcial")))
        item = plano["itens"][0]
        self.assertEqual(item["acao"]["missao_id"], "n5-pr")
        self.assertEqual(item["acao"]["tipo"], "contribuicao")
        self.assertTrue(item["acao"]["url"].startswith("https://"))

    def test_sem_evidencia_recebe_proxima_acao_concreta(self):
        plano = gerar_plano_evolucao(matriz_com(competencia("backend-api", "sem_evidencia")))
        item = plano["itens"][0]
        self.assertEqual(item["acao"]["missao_id"], "n4-http")
        self.assertEqual(item["acao"]["url"], "/laboratorio#api-tarefas")

    def test_indisponivel_nao_inventa_recomendacao(self):
        plano = gerar_plano_evolucao(matriz_com(competencia("qualidade-ci", "indisponivel")))
        item = plano["itens"][0]
        self.assertIsNone(item["acao"])
        self.assertIn("indisponível", item["motivo_sem_acao"])

    def test_competencia_sem_mapeamento_nao_inventa_missao(self):
        plano = gerar_plano_evolucao(matriz_com(competencia("desconhecida", "parcial")))
        item = plano["itens"][0]
        self.assertIsNone(item["acao"])
        self.assertIn("Nenhuma missão real", item["motivo_sem_acao"])

    def test_resumo_conta_acoes_e_bloqueios(self):
        plano = gerar_plano_evolucao(
            matriz_com(
                competencia("fundamentos-python", "forte"),
                competencia("backend-api", "parcial"),
                competencia("qualidade-ci", "indisponivel"),
            )
        )
        self.assertEqual(plano["resumo"], {"total": 3, "com_acao": 2, "sem_acao": 1})


class EvolutionPlanWebTests(unittest.TestCase):
    def test_endpoint_calcula_plano_a_partir_da_matriz_injetada(self):
        matriz = matriz_com(competencia("ia-aplicada", "parcial", nivel=6))
        client = create_app(gerador_competencias=lambda: matriz).test_client()

        response = client.get("/api/plano-evolucao")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["itens"][0]["acao"]["missao_id"], "n6-deterministico")
        self.assertEqual(data["resumo"]["com_acao"], 1)

    def test_endpoint_aceita_gerador_de_plano_injetado(self):
        esperado = {"itens": [], "resumo": {"total": 0, "com_acao": 0, "sem_acao": 0}}
        client = create_app(gerador_plano=lambda: esperado).test_client()

        response = client.get("/api/plano-evolucao")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), esperado)


if __name__ == "__main__":
    unittest.main()
