import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from projetos.github_student_dashboard.ai_explainer import (
    AIProviderError,
    OpenAIResponsesExplainer,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        if isinstance(self.payload, bytes):
            return self.payload
        if isinstance(self.payload, str):
            return self.payload.encode("utf-8")
        return json.dumps(self.payload).encode("utf-8")


class OpenAIResponsesExplainerTest(unittest.TestCase):
    def test_disponibilidade_depende_da_chave(self):
        self.assertFalse(OpenAIResponsesExplainer(api_key="").disponivel)
        self.assertTrue(OpenAIResponsesExplainer(api_key="chave").disponivel)

    def test_extrai_output_text_direto(self):
        provider = OpenAIResponsesExplainer(api_key="chave")
        self.assertEqual(provider._extrair_texto({"output_text": " resposta "}), "resposta")

    def test_extrai_texto_de_mensagens_aninhadas(self):
        provider = OpenAIResponsesExplainer(api_key="chave")
        resposta = {
            "output": [
                {"type": "reasoning", "content": []},
                {
                    "type": "message",
                    "content": [
                        {"type": "output_text", "text": "Linha 1"},
                        {"type": "text", "text": "Linha 2"},
                    ],
                },
            ]
        }
        self.assertEqual(provider._extrair_texto(resposta), "Linha 1\nLinha 2")

    def test_resposta_sem_texto_dispara_erro(self):
        provider = OpenAIResponsesExplainer(api_key="chave")
        with self.assertRaisesRegex(AIProviderError, "sem texto utilizável"):
            provider._extrair_texto({"output": []})

    def test_explicar_sem_chave_falha_antes_da_rede(self):
        provider = OpenAIResponsesExplainer(api_key="")
        with self.assertRaisesRegex(AIProviderError, "OPENAI_API_KEY"):
            provider.explicar({"score": 80})

    @patch("projetos.github_student_dashboard.ai_explainer.urlopen")
    def test_explicar_envia_evidencias_e_retorna_texto(self, urlopen_mock):
        urlopen_mock.return_value = FakeResponse({"output_text": "Explicação pronta"})
        provider = OpenAIResponsesExplainer(
            api_key="chave",
            model="modelo-teste",
            base_url="https://ia.exemplo/v1/",
            timeout=9,
        )

        texto = provider.explicar({"repositorio": "Videirafoo/exemplo", "score": 80})

        self.assertEqual(texto, "Explicação pronta")
        requisicao = urlopen_mock.call_args.args[0]
        self.assertEqual(requisicao.full_url, "https://ia.exemplo/v1/responses")
        self.assertEqual(urlopen_mock.call_args.kwargs["timeout"], 9)
        corpo = json.loads(requisicao.data.decode("utf-8"))
        self.assertEqual(corpo["model"], "modelo-teste")
        self.assertIn("Videirafoo/exemplo", corpo["input"])
        self.assertIn("SOMENTE EVIDÊNCIAS", corpo["input"])

    @patch("projetos.github_student_dashboard.ai_explainer.urlopen")
    def test_http_error_inclui_detalhe_do_provider(self, urlopen_mock):
        erro_http = HTTPError(
            "https://ia.exemplo/v1/responses",
            429,
            "Too Many Requests",
            hdrs={},
            fp=io.BytesIO(b'{"error":{"message":"limite excedido"}}'),
        )
        urlopen_mock.side_effect = erro_http
        provider = OpenAIResponsesExplainer(api_key="chave", base_url="https://ia.exemplo/v1")

        with self.assertRaises(AIProviderError) as contexto:
            provider.explicar({"score": 80})

        self.assertIn("HTTP 429", str(contexto.exception))
        self.assertIn("limite excedido", str(contexto.exception))

    @patch("projetos.github_student_dashboard.ai_explainer.urlopen")
    def test_http_error_com_corpo_invalido_preserva_status(self, urlopen_mock):
        erro_http = HTTPError(
            "https://ia.exemplo/v1/responses",
            500,
            "Erro",
            hdrs={},
            fp=io.BytesIO(b"nao-json"),
        )
        urlopen_mock.side_effect = erro_http
        provider = OpenAIResponsesExplainer(api_key="chave", base_url="https://ia.exemplo/v1")

        with self.assertRaisesRegex(AIProviderError, "HTTP 500"):
            provider.explicar({"score": 80})

    @patch(
        "projetos.github_student_dashboard.ai_explainer.urlopen",
        side_effect=URLError("offline"),
    )
    def test_erro_de_rede_vira_erro_de_provider(self, _urlopen_mock):
        provider = OpenAIResponsesExplainer(api_key="chave")
        with self.assertRaisesRegex(AIProviderError, "Não foi possível conectar"):
            provider.explicar({"score": 80})

    @patch("projetos.github_student_dashboard.ai_explainer.urlopen")
    def test_json_invalido_vira_erro_de_provider(self, urlopen_mock):
        urlopen_mock.return_value = FakeResponse("nao-json")
        provider = OpenAIResponsesExplainer(api_key="chave")

        with self.assertRaisesRegex(AIProviderError, "JSON inválido"):
            provider.explicar({"score": 80})


if __name__ == "__main__":
    unittest.main()
