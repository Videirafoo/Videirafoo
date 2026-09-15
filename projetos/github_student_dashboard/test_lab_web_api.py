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
        self.assertIn("/static/laboratorio_systems_real.js", conteudo)
        self.assertIn("/static/laboratorio_api_real.js", conteudo)

    def test_agenda_cria_e_exclui_contato_no_backend_real(self):
        criada = self.cliente.post(
            "/api/laboratorio/agenda",
            json={"contatos": [], "nome": "Ana", "telefone": "21999999999"},
        )
        self.assertEqual(criada.status_code, 201)
        contatos = criada.get_json()["contatos"]
        self.assertEqual(contatos[0]["nome"], "Ana")

        duplicada = self.cliente.post(
            "/api/laboratorio/agenda",
            json={"contatos": contatos, "nome": " ana ", "telefone": "21888888888"},
        )
        self.assertEqual(duplicada.status_code, 400)

        excluida = self.cliente.delete(
            "/api/laboratorio/agenda",
            json={"contatos": contatos, "id": contatos[0]["id"]},
        )
        self.assertEqual(excluida.status_code, 200)
        self.assertEqual(excluida.get_json()["contatos"], [])

    def test_lista_02_cria_conclui_reabre_e_exclui(self):
        criada = self.cliente.post(
            "/api/laboratorio/lista-tarefas",
            json={"tarefas": [], "titulo": "Revisar Python", "prioridade": "alta"},
        )
        self.assertEqual(criada.status_code, 201)
        tarefas = criada.get_json()["tarefas"]
        self.assertEqual(tarefas[0]["id"], 1)

        concluida = self.cliente.patch(
            "/api/laboratorio/lista-tarefas",
            json={"tarefas": tarefas, "id": 1, "concluida": True},
        )
        self.assertEqual(concluida.status_code, 200)
        tarefas = concluida.get_json()["tarefas"]
        self.assertTrue(tarefas[0]["concluida"])

        reaberta = self.cliente.patch(
            "/api/laboratorio/lista-tarefas",
            json={"tarefas": tarefas, "id": 1, "concluida": False},
        )
        self.assertEqual(reaberta.status_code, 200)
        tarefas = reaberta.get_json()["tarefas"]
        self.assertFalse(tarefas[0]["concluida"])

        excluida = self.cliente.delete(
            "/api/laboratorio/lista-tarefas",
            json={"tarefas": tarefas, "id": 1},
        )
        self.assertEqual(excluida.status_code, 200)
        self.assertEqual(excluida.get_json()["tarefas"], [])

    def test_aluno_media_executa_regras_python_reais(self):
        resposta = self.cliente.post(
            "/api/laboratorio/aluno-media",
            json={"nome": "Fernando", "notas": [8, 7, 9]},
        )

        self.assertEqual(resposta.status_code, 200)
        dados = resposta.get_json()
        self.assertEqual(dados["media"], 8.0)
        self.assertEqual(dados["situacao"], "aprovado")

        invalida = self.cliente.post(
            "/api/laboratorio/aluno-media",
            json={"nome": "Fernando", "notas": [8, 11, 9]},
        )
        self.assertEqual(invalida.status_code, 400)

    def test_estoque_cria_e_exclui_produto_no_backend_real(self):
        criada = self.cliente.post(
            "/api/laboratorio/estoque",
            json={"produtos": [], "nome": "Caderno", "quantidade": 2, "preco": 15.5},
        )
        self.assertEqual(criada.status_code, 201)
        dados = criada.get_json()
        produtos = dados["produtos"]
        self.assertEqual(produtos[0]["codigo"], "LAB-1")
        self.assertEqual(dados["valor_total"], 31.0)

        excluida = self.cliente.delete(
            "/api/laboratorio/estoque",
            json={"produtos": produtos, "id": produtos[0]["id"]},
        )
        self.assertEqual(excluida.status_code, 200)
        self.assertEqual(excluida.get_json()["produtos"], [])

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
