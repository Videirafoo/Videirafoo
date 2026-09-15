import unittest

from projetos.github_student_dashboard.lab_api import (
    analisar_projeto_lab,
    atualizar_tarefa_lab,
    concluir_lista_tarefa_lab,
    criar_contato_lab,
    criar_lista_tarefa_lab,
    criar_tarefa_lab,
    excluir_contato_lab,
    excluir_lista_tarefa_lab,
    excluir_tarefa_lab,
    listar_tarefas_lab,
)


class LabApiTest(unittest.TestCase):
    def test_agenda_reutiliza_validacao_e_regra_de_duplicidade(self):
        criada = criar_contato_lab([], "Ana", "21999999999")
        contatos = criada["contatos"]

        self.assertEqual(criada["resultado"]["nome"], "Ana")
        self.assertEqual(len(contatos), 1)

        with self.assertRaisesRegex(ValueError, "Já existe"):
            criar_contato_lab(contatos, " ana ", "21888888888")

        removida = excluir_contato_lab(contatos, contatos[0]["id"])
        self.assertEqual(removida["contatos"], [])
        self.assertEqual(removida["resultado"]["nome"], "Ana")

    def test_lista_02_cria_conclui_reabre_e_exclui_com_codigo_original(self):
        criada = criar_lista_tarefa_lab([], "Revisar funções", "alta")
        tarefas = criada["tarefas"]

        self.assertEqual(criada["resultado"]["titulo"], "Revisar funções")
        self.assertFalse(criada["resultado"]["concluida"])

        concluida = concluir_lista_tarefa_lab(tarefas, 1, True)
        self.assertTrue(concluida["resultado"]["concluida"])

        reaberta = concluir_lista_tarefa_lab(concluida["tarefas"], 1, False)
        self.assertFalse(reaberta["resultado"]["concluida"])

        removida = excluir_lista_tarefa_lab(reaberta["tarefas"], 1)
        self.assertEqual(removida["tarefas"], [])

    def test_lista_02_migra_estado_antigo_do_navegador(self):
        antiga = [{"id": "uuid-antigo", "texto": "Tarefa antiga", "concluida": False}]
        criada = criar_lista_tarefa_lab(antiga, "Nova tarefa")

        self.assertEqual([item["id"] for item in criada["tarefas"]], [1, 2])
        self.assertEqual(criada["tarefas"][0]["titulo"], "Tarefa antiga")

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

    def test_projeto_integrado_reutiliza_analisador_original(self):
        relatorio = analisar_projeto_lab(
            {
                "readme": True,
                "gitignore": True,
                "licenca": False,
                "ci": True,
                "testes": False,
                "dependencias": True,
            }
        )

        self.assertEqual(relatorio["score"], 65)
        self.assertTrue(relatorio["checks"]["readme"])
        self.assertTrue(relatorio["checks"]["gitignore"])
        self.assertFalse(relatorio["checks"]["licenca"])
        self.assertTrue(relatorio["checks"]["ci"])
        self.assertFalse(relatorio["checks"]["testes"])
        self.assertTrue(relatorio["checks"]["dependencias"])
        self.assertEqual(relatorio["caminho"], "temporário e isolado")
        self.assertGreaterEqual(relatorio["evidencias"]["total_arquivos_analisados"], 5)

    def test_projeto_integrado_com_todos_checks_chega_a_cem(self):
        relatorio = analisar_projeto_lab(
            {
                "readme": True,
                "gitignore": True,
                "licenca": True,
                "ci": True,
                "testes": True,
                "dependencias": True,
            }
        )

        self.assertEqual(relatorio["score"], 100)
        self.assertTrue(all(relatorio["checks"].values()))

    def test_projeto_integrado_rejeita_check_desconhecido(self):
        with self.assertRaisesRegex(ValueError, "não reconhecidos"):
            analisar_projeto_lab({"readme": True, "inventado": True})


if __name__ == "__main__":
    unittest.main()
