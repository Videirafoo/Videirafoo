import unittest

from projetos.github_student_dashboard.lab_api import (
    atualizar_tarefa_lab,
    criar_tarefa_lab,
    excluir_tarefa_lab,
    listar_tarefas_lab,
)


class LabApiTest(unittest.TestCase):
    def test_cria_lista_atualiza_e_exclui_tarefa(self):
        criada = criar_tarefa_lab([], "Estudar Flask", "alta")
        tarefas = criada["tarefas"]

        self.assertEqual(criada["resultado"]["titulo"], "Estudar Flask")
        self.assertEqual(criada["resultado"]["prioridade"], "alta")
        self.assertFalse(criada["resultado"]["concluida"])

        listadas = listar_tarefas_lab(tarefas)
        self.assertEqual(len(listadas), 1)

        atualizada = atualizar_tarefa_lab(
            tarefas,
            tarefas[0]["id"],
            {"concluida": True},
        )
        self.assertTrue(atualizada["resultado"]["concluida"])

        removida = excluir_tarefa_lab(
            atualizada["tarefas"],
            tarefas[0]["id"],
        )
        self.assertEqual(removida["tarefas"], [])

    def test_reutiliza_validacao_de_prioridade_do_mini_sistema(self):
        with self.assertRaisesRegex(ValueError, "prioridade"):
            criar_tarefa_lab([], "Teste", "urgente")

    def test_rejeita_estado_invalido(self):
        with self.assertRaisesRegex(ValueError, "lista"):
            listar_tarefas_lab({"id": 1})

    def test_rejeita_mais_de_cinquenta_tarefas(self):
        tarefas = [
            {
                "id": indice + 1,
                "titulo": f"Tarefa {indice + 1}",
                "prioridade": "media",
                "concluida": False,
            }
            for indice in range(51)
        ]

        with self.assertRaisesRegex(ValueError, "50"):
            listar_tarefas_lab(tarefas)

    def test_filtro_reutiliza_regra_do_mini_sistema(self):
        tarefas = [
            {"id": 1, "titulo": "A", "prioridade": "media", "concluida": False},
            {"id": 2, "titulo": "B", "prioridade": "alta", "concluida": True},
        ]

        pendentes = listar_tarefas_lab(tarefas, "pendentes")
        concluidas = listar_tarefas_lab(tarefas, "concluidas")

        self.assertEqual([item["id"] for item in pendentes], [1])
        self.assertEqual([item["id"] for item in concluidas], [2])


if __name__ == "__main__":
    unittest.main()
