import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from projetos.github_student_dashboard import cli
from projetos.github_student_dashboard.github_client import GitHubApiError


RELATORIO = {
    "repositorio": "Videirafoo/exemplo",
    "score": 75,
    "checks": {"readme": True, "topics": False},
    "recomendacoes": [
        {"prioridade": "media", "acao": "Adicionar topics relevantes."},
    ],
}


class CliTest(unittest.TestCase):
    def executar(self, argumentos, relatorio=None, erro=None):
        saida = io.StringIO()
        with patch.object(sys, "argv", ["dashboard", *argumentos]):
            with patch.object(
                cli,
                "analisar_repositorio_remoto",
                return_value=relatorio,
                side_effect=erro,
            ):
                with redirect_stdout(saida):
                    if erro is not None:
                        with self.assertRaises(SystemExit) as contexto:
                            cli.main()
                        return saida.getvalue(), contexto.exception.code
                    cli.main()
        return saida.getvalue(), 0

    def test_saida_textual_mostra_score_checks_e_recomendacoes(self):
        saida, codigo = self.executar(["Videirafoo/exemplo"], relatorio=RELATORIO)

        self.assertEqual(codigo, 0)
        self.assertIn("=== Videirafoo/exemplo ===", saida)
        self.assertIn("Score: 75/100", saida)
        self.assertIn("readme: OK", saida)
        self.assertIn("topics: FALTA", saida)
        self.assertIn("[media] Adicionar topics relevantes.", saida)

    def test_saida_textual_sem_recomendacoes_informa_ausencia(self):
        relatorio = {**RELATORIO, "checks": {"readme": True}, "recomendacoes": []}
        saida, codigo = self.executar(["Videirafoo/exemplo"], relatorio=relatorio)

        self.assertEqual(codigo, 0)
        self.assertIn("Nenhuma ausência encontrada nos checks atuais.", saida)

    def test_saida_json_entrega_relatorio_completo(self):
        saida, codigo = self.executar(
            ["Videirafoo/exemplo", "--json"],
            relatorio=RELATORIO,
        )

        self.assertEqual(codigo, 0)
        self.assertEqual(json.loads(saida), RELATORIO)

    def test_erro_de_validacao_encerra_com_codigo_um(self):
        saida, codigo = self.executar(
            ["invalido"],
            erro=ValueError("referência inválida"),
        )

        self.assertEqual(codigo, 1)
        self.assertIn("Erro: referência inválida", saida)

    def test_erro_da_api_encerra_com_codigo_um(self):
        saida, codigo = self.executar(
            ["Videirafoo/exemplo"],
            erro=GitHubApiError("rate limit", status=403),
        )

        self.assertEqual(codigo, 1)
        self.assertIn("Erro: rate limit", saida)


if __name__ == "__main__":
    unittest.main()
