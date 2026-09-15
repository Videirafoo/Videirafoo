import tempfile
import unittest
from pathlib import Path

from conteudos.mini_sistemas.api_tarefas.app import create_app


class ApiTarefasTest(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.caminho = Path(self.pasta.name) / "tarefas.json"
        self.app = create_app(self.caminho)
        self.app.config["TESTING"] = True
        self.cliente = self.app.test_client()

    def tearDown(self):
        self.pasta.cleanup()

    def test_inicio(self):
        resposta = self.cliente.get("/")

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["projeto"], "API de Tarefas")

    def test_criar_e_listar_tarefa(self):
        criada = self.cliente.post(
            "/tarefas",
            json={"titulo": "Estudar Flask", "prioridade": "alta"},
        )

        self.assertEqual(criada.status_code, 201)
        self.assertEqual(criada.get_json()["titulo"], "Estudar Flask")

        lista = self.cliente.get("/tarefas")
        self.assertEqual(lista.status_code, 200)
        self.assertEqual(len(lista.get_json()), 1)

    def test_rejeita_titulo_vazio(self):
        resposta = self.cliente.post("/tarefas", json={"titulo": "   "})

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("erro", resposta.get_json())

    def test_rejeita_prioridade_invalida(self):
        resposta = self.cliente.post(
            "/tarefas",
            json={"titulo": "Estudar", "prioridade": "urgente"},
        )

        self.assertEqual(resposta.status_code, 400)

    def test_detalhar_tarefa_inexistente_retorna_404(self):
        resposta = self.cliente.get("/tarefas/999")

        self.assertEqual(resposta.status_code, 404)

    def test_editar_tarefa(self):
        criada = self.cliente.post("/tarefas", json={"titulo": "Ler"}).get_json()

        resposta = self.cliente.patch(
            f"/tarefas/{criada['id']}",
            json={"titulo": "Ler documentação", "concluida": True},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["titulo"], "Ler documentação")
        self.assertTrue(resposta.get_json()["concluida"])

    def test_filtro_por_status(self):
        primeira = self.cliente.post("/tarefas", json={"titulo": "Tarefa 1"}).get_json()
        self.cliente.post("/tarefas", json={"titulo": "Tarefa 2"})
        self.cliente.patch(f"/tarefas/{primeira['id']}", json={"concluida": True})

        concluidas = self.cliente.get("/tarefas?status=concluidas")
        pendentes = self.cliente.get("/tarefas?status=pendentes")

        self.assertEqual(len(concluidas.get_json()), 1)
        self.assertEqual(len(pendentes.get_json()), 1)

    def test_status_invalido_retorna_400(self):
        resposta = self.cliente.get("/tarefas?status=todas")

        self.assertEqual(resposta.status_code, 400)

    def test_excluir_tarefa(self):
        criada = self.cliente.post("/tarefas", json={"titulo": "Excluir"}).get_json()

        resposta = self.cliente.delete(f"/tarefas/{criada['id']}")

        self.assertEqual(resposta.status_code, 204)
        self.assertEqual(self.cliente.get("/tarefas").get_json(), [])

    def test_json_invalido_retorna_400(self):
        resposta = self.cliente.post(
            "/tarefas",
            data="texto",
            content_type="text/plain",
        )

        self.assertEqual(resposta.status_code, 400)


if __name__ == "__main__":
    unittest.main()
