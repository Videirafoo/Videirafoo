import io
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from projetos.github_student_dashboard.github_client import GitHubApiError, GitHubClient


class FakeResponse:
    def __init__(self, texto):
        self.texto = texto

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self.texto.encode("utf-8")


class GitHubClientTest(unittest.TestCase):
    def test_headers_incluem_token_quando_configurado(self):
        cliente = GitHubClient(token="segredo", base_url="https://api.exemplo/")
        headers = cliente._headers()

        self.assertEqual(cliente.base_url, "https://api.exemplo")
        self.assertEqual(headers["Authorization"], "Bearer segredo")
        self.assertEqual(headers["Accept"], "application/vnd.github+json")
        self.assertIn("User-Agent", headers)

    def test_token_pode_vir_do_ambiente(self):
        with patch.dict("os.environ", {"GITHUB_TOKEN": "ambiente"}, clear=False):
            cliente = GitHubClient()

        self.assertEqual(cliente.token, "ambiente")

    @patch("projetos.github_student_dashboard.github_client.urlopen")
    def test_get_json_retorna_payload_e_respeita_timeout(self, urlopen_mock):
        urlopen_mock.return_value = FakeResponse('{"ok": true}')
        cliente = GitHubClient(token="abc", base_url="https://api.exemplo", timeout=7)

        resultado = cliente.get_json("/teste")

        self.assertEqual(resultado, {"ok": True})
        requisicao = urlopen_mock.call_args.args[0]
        self.assertEqual(requisicao.full_url, "https://api.exemplo/teste")
        self.assertEqual(urlopen_mock.call_args.kwargs["timeout"], 7)

    @patch("projetos.github_student_dashboard.github_client.urlopen")
    def test_http_error_preserva_status_e_mensagem_da_api(self, urlopen_mock):
        erro_http = HTTPError(
            "https://api.exemplo/teste",
            403,
            "Forbidden",
            hdrs={},
            fp=io.BytesIO(b'{"message":"API rate limit exceeded"}'),
        )
        urlopen_mock.side_effect = erro_http

        with self.assertRaises(GitHubApiError) as contexto:
            GitHubClient(base_url="https://api.exemplo").get_json("/teste")

        self.assertEqual(contexto.exception.status, 403)
        self.assertIn("HTTP 403", str(contexto.exception))
        self.assertIn("API rate limit exceeded", str(contexto.exception))

    @patch("projetos.github_student_dashboard.github_client.urlopen")
    def test_http_error_com_corpo_invalido_mantem_mensagem_basica(self, urlopen_mock):
        erro_http = HTTPError(
            "https://api.exemplo/teste",
            500,
            "Server Error",
            hdrs={},
            fp=io.BytesIO(b"nao-json"),
        )
        urlopen_mock.side_effect = erro_http

        with self.assertRaises(GitHubApiError) as contexto:
            GitHubClient(base_url="https://api.exemplo").get_json("/teste")

        self.assertEqual(contexto.exception.status, 500)
        self.assertEqual(str(contexto.exception), "GitHub API retornou HTTP 500.")

    @patch("projetos.github_student_dashboard.github_client.urlopen", side_effect=URLError("offline"))
    def test_erro_de_rede_vira_erro_de_dominio(self, _urlopen_mock):
        with self.assertRaisesRegex(GitHubApiError, "Não foi possível conectar"):
            GitHubClient(base_url="https://api.exemplo").get_json("/teste")

    @patch("projetos.github_student_dashboard.github_client.urlopen")
    def test_json_invalido_vira_erro_de_dominio(self, urlopen_mock):
        urlopen_mock.return_value = FakeResponse("nao-json")

        with self.assertRaisesRegex(GitHubApiError, "JSON inválido"):
            GitHubClient(base_url="https://api.exemplo").get_json("/teste")

    def test_metodos_montam_rotas_com_encoding_e_limites(self):
        cliente = GitHubClient(base_url="https://api.exemplo")
        with patch.object(cliente, "get_json", return_value={}) as get_json:
            cliente.buscar_usuario("nome com espaço")
            cliente.buscar_repositorios_usuario("a/b", limite=0)
            cliente.buscar_repositorio("org x", "repo/y")
            cliente.buscar_arvore("org", "repo", "feature/x")
            cliente.buscar_linguagens("org", "repo")
            cliente.buscar_workflow_runs("org", "repo", branch="feat/x", limite=999)
            cliente.buscar_commits("org", "repo", limite=999)

        chamadas = [chamada.args[0] for chamada in get_json.call_args_list]
        self.assertIn("/users/nome%20com%20espa%C3%A7o", chamadas)
        self.assertIn("/users/a%2Fb/repos?type=owner&sort=updated&direction=desc&per_page=1", chamadas)
        self.assertIn("/repos/org%20x/repo%2Fy", chamadas)
        self.assertIn("/repos/org/repo/git/trees/feature%2Fx?recursive=1", chamadas)
        self.assertIn("/repos/org/repo/languages", chamadas)
        self.assertIn("/repos/org/repo/actions/runs?per_page=20&branch=feat%2Fx", chamadas)
        self.assertIn("/repos/org/repo/commits?per_page=10", chamadas)


if __name__ == "__main__":
    unittest.main()
