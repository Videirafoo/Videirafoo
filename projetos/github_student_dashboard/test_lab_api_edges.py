import unittest

from projetos.github_student_dashboard.lab_api import (
    MAX_ITENS_LAB,
    MAX_TITULO,
    _normalizar_agenda,
    _normalizar_lista_tarefas,
    _normalizar_tarefas,
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


class LabApiEdgesTest(unittest.TestCase):
    def test_agenda_normaliza_none_e_valida_formato_e_limite(self):
        self.assertEqual(_normalizar_agenda(None), [])
        with self.assertRaisesRegex(ValueError, "agenda precisa ser uma lista"):
            _normalizar_agenda({})
        with self.assertRaisesRegex(ValueError, "no máximo"):
            _normalizar_agenda([{}] * (MAX_ITENS_LAB + 1))
        with self.assertRaisesRegex(ValueError, "Cada contato"):
            _normalizar_agenda(["x"])

    def test_agenda_preserva_id_e_exclusao_ausente_retorna_none(self):
        estado = [{"id": "fixo", "nome": "Ana", "telefone": "999", "email": "a@b.com"}]
        normalizado = _normalizar_agenda(estado)
        self.assertEqual(normalizado[0]["id"], "fixo")
        self.assertIsNone(excluir_contato_lab(normalizado, "outro"))

    def test_agenda_rejeita_duplicidade_pelas_regras_originais(self):
        primeiro = criar_contato_lab([], "Ana", "999")
        with self.assertRaises(ValueError):
            criar_contato_lab(primeiro["contatos"], "Ana", "999")

    def test_lista_tarefas_normaliza_none_e_valida_entradas(self):
        self.assertEqual(_normalizar_lista_tarefas(None), [])
        with self.assertRaisesRegex(ValueError, "precisa ser uma lista"):
            _normalizar_lista_tarefas({})
        with self.assertRaisesRegex(ValueError, "no máximo"):
            _normalizar_lista_tarefas([{}] * (MAX_ITENS_LAB + 1))
        with self.assertRaisesRegex(ValueError, "Cada tarefa"):
            _normalizar_lista_tarefas(["x"])
        with self.assertRaisesRegex(ValueError, "booleano"):
            _normalizar_lista_tarefas([{"titulo": "X", "concluida": "sim"}])

    def test_lista_tarefas_reabre_e_valida_ids(self):
        criado = criar_lista_tarefa_lab([], "Estudar", "alta")
        estado = criado["tarefas"]
        concluido = concluir_lista_tarefa_lab(estado, 1, True)
        self.assertTrue(concluido["resultado"]["concluida"])

        reaberto = concluir_lista_tarefa_lab(concluido["tarefas"], 1, False)
        self.assertFalse(reaberto["resultado"]["concluida"])
        self.assertIsNone(concluir_lista_tarefa_lab(reaberto["tarefas"], 99, False))

        with self.assertRaisesRegex(ValueError, "id inteiro positivo"):
            concluir_lista_tarefa_lab(estado, 0)
        with self.assertRaisesRegex(ValueError, "booleano"):
            concluir_lista_tarefa_lab(estado, 1, "sim")
        with self.assertRaisesRegex(ValueError, "id inteiro positivo"):
            excluir_lista_tarefa_lab(estado, 0)
        self.assertIsNone(excluir_lista_tarefa_lab(estado, 99))

    def test_lista_tarefas_bloqueia_novo_item_no_limite(self):
        estado = [
            {"id": i, "titulo": f"Tarefa {i}", "prioridade": "media", "concluida": False}
            for i in range(1, MAX_ITENS_LAB + 1)
        ]
        with self.assertRaisesRegex(ValueError, "no máximo"):
            criar_lista_tarefa_lab(estado, "Extra")

    def test_api_tarefas_normaliza_e_rejeita_estados_invalidos(self):
        self.assertEqual(_normalizar_tarefas(None), [])
        with self.assertRaisesRegex(ValueError, "precisa ser uma lista"):
            _normalizar_tarefas({})
        with self.assertRaisesRegex(ValueError, "no máximo"):
            _normalizar_tarefas([{}] * (MAX_ITENS_LAB + 1))
        with self.assertRaisesRegex(ValueError, "Cada tarefa"):
            _normalizar_tarefas(["x"])

        casos = (
            ([{"id": 0, "titulo": "X"}], "id inteiro positivo"),
            ([{"id": 1, "titulo": "X"}, {"id": 1, "titulo": "Y"}], "não podem se repetir"),
            ([{"id": 1, "titulo": ""}], "entre 1"),
            ([{"id": 1, "titulo": "X", "prioridade": "urgente"}], "prioridade"),
            ([{"id": 1, "titulo": "X", "concluida": "sim"}], "booleano"),
        )
        for estado, mensagem in casos:
            with self.subTest(mensagem=mensagem):
                with self.assertRaisesRegex(ValueError, mensagem):
                    _normalizar_tarefas(estado)

    def test_api_tarefas_filtra_cria_e_bloqueia_titulo_grande(self):
        estado = [
            {"id": 1, "titulo": "Feita", "prioridade": "baixa", "concluida": True},
            {"id": 2, "titulo": "Aberta", "prioridade": "alta", "concluida": False},
        ]
        concluidas = listar_tarefas_lab(estado, "concluidas")
        self.assertEqual([item["id"] for item in concluidas], [1])

        criado = criar_tarefa_lab([], "Nova", "media")
        self.assertEqual(criado["resultado"]["id"], 1)

        with self.assertRaisesRegex(ValueError, "no máximo"):
            criar_tarefa_lab(
                [{"id": i, "titulo": f"T{i}", "prioridade": "media", "concluida": False} for i in range(1, MAX_ITENS_LAB + 1)],
                "Extra",
            )
        with self.assertRaisesRegex(ValueError, "no máximo"):
            criar_tarefa_lab([], "x" * (MAX_TITULO + 1))

    def test_atualizacao_valida_e_aplica_campos_permitidos(self):
        estado = [{"id": 1, "titulo": "Antes", "prioridade": "baixa", "concluida": False}]
        with self.assertRaisesRegex(ValueError, "id inteiro positivo"):
            atualizar_tarefa_lab(estado, 0, {})
        with self.assertRaisesRegex(ValueError, "objeto JSON"):
            atualizar_tarefa_lab(estado, 1, [])
        self.assertIsNone(atualizar_tarefa_lab(estado, 99, {}))
        with self.assertRaisesRegex(ValueError, "no máximo"):
            atualizar_tarefa_lab(estado, 1, {"titulo": "x" * (MAX_TITULO + 1)})

        resultado = atualizar_tarefa_lab(
            estado,
            1,
            {"titulo": "Depois", "prioridade": "alta", "concluida": True, "ignorado": "x"},
        )
        self.assertEqual(resultado["resultado"]["titulo"], "Depois")
        self.assertEqual(resultado["resultado"]["prioridade"], "alta")
        self.assertTrue(resultado["resultado"]["concluida"])
        self.assertNotIn("ignorado", resultado["resultado"])

    def test_exclusao_api_valida_id_e_ausencia(self):
        estado = [{"id": 1, "titulo": "X", "prioridade": "media", "concluida": False}]
        with self.assertRaisesRegex(ValueError, "id inteiro positivo"):
            excluir_tarefa_lab(estado, 0)
        self.assertIsNone(excluir_tarefa_lab(estado, 99))
        removido = excluir_tarefa_lab(estado, 1)
        self.assertEqual(removido["tarefas"], [])

    def test_analisador_valida_tipo_nomes_e_booleanos(self):
        with self.assertRaisesRegex(ValueError, "objeto JSON"):
            analisar_projeto_lab([])
        with self.assertRaisesRegex(ValueError, "não reconhecidos"):
            analisar_projeto_lab({"inventado": True})
        with self.assertRaisesRegex(ValueError, "true ou false"):
            analisar_projeto_lab({"readme": "sim"})

    def test_analisador_executa_todos_checks_ligados_e_desligados(self):
        todos = {
            "readme": True,
            "gitignore": True,
            "licenca": True,
            "ci": True,
            "testes": True,
            "dependencias": True,
        }
        completo = analisar_projeto_lab(todos)
        self.assertEqual(completo["entrada_checks"], todos)
        self.assertEqual(completo["repositorio"], "projeto-laboratorio")
        self.assertEqual(completo["caminho"], "temporário e isolado")

        vazio = analisar_projeto_lab({})
        self.assertTrue(all(valor is False for valor in vazio["entrada_checks"].values()))


if __name__ == "__main__":
    unittest.main()
