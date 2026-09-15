import unittest

from projetos.github_student_dashboard.ai_explainer import (
    AIProviderError,
    explicar_repositorio_remoto,
    gerar_explicacao,
    montar_pacote_evidencias,
)


RELATORIO = {
    "repositorio": "Videirafoo/exemplo",
    "score": 80,
    "branch_padrao": "main",
    "checks": {
        "readme": True,
        "descricao": False,
        "licenca": True,
        "gitignore": True,
        "topics": False,
        "ci": True,
        "testes": True,
        "dependencias": True,
    },
    "ci_execucao": {"estado": "success", "workflow": "CI"},
    "detalhes_checks": {
        "descricao": {
            "passou": False,
            "observado": "Descrição vazia.",
            "impacto": "Reduz contexto.",
            "acao": "Adicionar descrição.",
        }
    },
    "recomendacoes": [
        {"check": "descricao", "prioridade": "media", "acao": "Adicionar descrição."},
        {"check": "topics", "prioridade": "media", "acao": "Adicionar topics."},
    ],
    "campo_que_nao_deve_ir": "segredo ou ruído",
}


class ProviderIndisponivel:
    disponivel = False
    model = "teste"


class ProviderFake:
    disponivel = True
    model = "modelo-teste"

    def __init__(self):
        self.pacote = None

    def explicar(self, pacote):
        self.pacote = pacote
        return "Explicação pedagógica baseada somente nas evidências."


class ProviderComErro:
    disponivel = True
    model = "modelo-teste"

    def explicar(self, pacote):
        raise AIProviderError("falha simulada")


class AIExplainerTest(unittest.TestCase):
    def test_pacote_limita_dados_enviados_para_ia(self):
        pacote = montar_pacote_evidencias(RELATORIO)

        self.assertEqual(pacote["score"], 80)
        self.assertIn("checks", pacote)
        self.assertNotIn("campo_que_nao_deve_ir", pacote)

    def test_sem_provider_externo_usa_modo_local_transparente(self):
        resultado = gerar_explicacao(RELATORIO, provider=ProviderIndisponivel())

        self.assertEqual(resultado["modo"], "local")
        self.assertEqual(resultado["score"], 80)
        self.assertEqual(resultado["ci_estado"], "success")
        self.assertEqual(resultado["checks_falhos"], ["descricao", "topics"])
        self.assertIn("nenhuma chamada externa", resultado["aviso"])

    def test_provider_ia_recebe_apenas_pacote_e_preserva_fatos(self):
        provider = ProviderFake()
        resultado = gerar_explicacao(RELATORIO, provider=provider)

        self.assertEqual(resultado["modo"], "ia")
        self.assertEqual(resultado["modelo"], "modelo-teste")
        self.assertEqual(resultado["score"], 80)
        self.assertNotIn("campo_que_nao_deve_ir", provider.pacote)
        self.assertIn("Explicação pedagógica", resultado["texto"])

    def test_falha_da_ia_nao_quebra_dashboard(self):
        resultado = gerar_explicacao(RELATORIO, provider=ProviderComErro())

        self.assertEqual(resultado["modo"], "local")
        self.assertIn("falha simulada", resultado["aviso"])
        self.assertIn("80/100", resultado["texto"])

    def test_explicacao_remota_primeiro_executa_analisador_deterministico(self):
        chamadas = []

        def analisador(ref):
            chamadas.append(ref)
            return RELATORIO

        resultado = explicar_repositorio_remoto(
            "Videirafoo/exemplo",
            analisador=analisador,
            provider=ProviderIndisponivel(),
        )

        self.assertEqual(chamadas, ["Videirafoo/exemplo"])
        self.assertEqual(resultado["fonte"], "relatorio_deterministico")


if __name__ == "__main__":
    unittest.main()
