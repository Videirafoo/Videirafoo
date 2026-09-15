import json
import unittest

from projetos.github_student_dashboard.web import create_app


class LabWebApiTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(lambda _: {}, lambda _: {}, lambda _: {})
        self.app.config["TESTING"] = True
        self.cliente = self.app.test_client()

    def test_pagina_laboratorio_carrega_integracao_backend_real(self):
        resposta = self.cliente.get("/laboratorio")
        conteudo = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("/static/laboratorio_api_real.js", conteudo)

    def test_fluxo_http_criar_listar_atualizar_excluir(self):
        criada = self.cliente.post(
            "/api/laboratorio/tarefas",
            json={"tarefas": [], "titulo": "Estudar Flask", "prioridade": "alta"},
        )
        self.assertEqual(criada.status_code, 201)
        tarefas = criada.get_json()["tarefas"]
        self.assertEqual(tarefas[0]["titulo"], "Estudar Flask")

        listada = self.cliente.get(
            "/api/laboratorio/tarefas",
            query_string={"estado": json.dumps(tarefas)},
        )
        self.assertEqual(listada.status_code, 200)
        self.assertEqual(len(listada.get_json()["tarefas"]), 1)

        atualizada = self.cliente.patch(
            "/api/laboratorio/tarefas",
            json={
                "tarefas": tarefas,
                "id": tarefas[0]["id"],
                "dados": {"concluida": True},
            },
        )
        self.assertEqual(atualizada.status_code, 200)
        tarefas_atualizadas = atualizada.get_json()["tarefas"]
        self.assertTrue(tarefas_atualizadas[0]["concluida"])

        excluida = self.cliente.delete(
            "/api/laboratorio/tarefas",
            json={"tarefas": tarefas_atualizadas, "id": tarefas[0]["id"]},
        )
        self.assertEqual(excluida.status_code, 204)

    def test_post_rejeita_prioridade_invalida(self):
        resposta = self.cliente.post(
            "/api/laboratorio/tarefas",
            json={"tarefas": [], "titulo": "Teste", "prioridade": "urgente"},
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("prioridade", resposta.get_json()["erro"])

    def test_patch_retorna_404_para_id_inexistente(self):
        tarefas = [
            {"id": 1, "titulo": "Teste", "prioridade": "media", "concluida": False}
        ]
        resposta = self.cliente.patch(
            "/api/laboratorio/tarefas",
            json={"tarefas": tarefas, "id": 99, "dados": {"concluida": True}},
        )

        self.assertEqual(resposta.status_code, 404)

    def test_get_rejeita_estado_json_invalido(self):
        resposta = self.cliente.get(
            "/api/laboratorio/tarefas",
            query_string={"estado": "{invalido"},
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("JSON", resposta.get_json()["erro"])

    def test_projeto_integrado_executa_analisador_python_real(self):
        resposta = self.cliente.post(
            "/api/laboratorio/analisar",
            json={
                "checks": {
                    "readme": True,
                    "gitignore": True,
                    "licenca": False,
                    "ci": True,
                    "testes": True,
                    "dependencias": True,
                }
            },
        )

        self.assertEqual(resposta.status_code, 200)
        relatorio = resposta.get_json()
        self.assertEqual(relatorio["score"], 85)
        self.assertEqual(relatorio["repositorio"], "projeto-laboratorio")
        self.assertEqual(relatorio["caminho"], "temporário e isolado")
        self.assertTrue(relatorio["checks"]["testes"])
        self.assertFalse(relatorio["checks"]["licenca"])

    def test_projeto_integrado_rejeita_payload_invalido(self):
        resposta = self.cliente.post(
            "/api/laboratorio/analisar",
            json={"checks": {"readme": "sim"}},
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("true ou false", resposta.get_json()["erro"])


if __name__ == "__main__":
    unittest.main()
