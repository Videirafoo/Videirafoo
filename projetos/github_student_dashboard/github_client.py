import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class GitHubApiError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status


class GitHubClient:
    def __init__(self, token=None, base_url="https://api.github.com", timeout=10):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _headers(self):
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "Videirafoo-GitHub-Student-Dashboard",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    def get_json(self, path):
        url = f"{self.base_url}{path}"
        requisicao = Request(url, headers=self._headers())

        try:
            with urlopen(requisicao, timeout=self.timeout) as resposta:
                conteudo = resposta.read().decode("utf-8")
                return json.loads(conteudo)
        except HTTPError as erro:
            mensagem = f"GitHub API retornou HTTP {erro.code}."
            try:
                corpo = json.loads(erro.read().decode("utf-8"))
                detalhe = corpo.get("message")
                if detalhe:
                    mensagem = f"{mensagem} {detalhe}"
            except (ValueError, UnicodeDecodeError):
                pass

            raise GitHubApiError(mensagem, status=erro.code) from erro
        except URLError as erro:
            raise GitHubApiError("Não foi possível conectar à GitHub API.") from erro
        except json.JSONDecodeError as erro:
            raise GitHubApiError("A GitHub API retornou JSON inválido.") from erro

    def buscar_usuario(self, usuario):
        usuario = quote(usuario, safe="")
        return self.get_json(f"/users/{usuario}")

    def buscar_repositorios_usuario(self, usuario, limite=100):
        usuario = quote(usuario, safe="")
        limite = max(1, min(int(limite), 100))
        return self.get_json(
            f"/users/{usuario}/repos?type=owner&sort=updated&direction=desc&per_page={limite}"
        )

    def buscar_repositorio(self, owner, repo):
        owner = quote(owner, safe="")
        repo = quote(repo, safe="")
        return self.get_json(f"/repos/{owner}/{repo}")

    def buscar_arvore(self, owner, repo, ref):
        owner = quote(owner, safe="")
        repo = quote(repo, safe="")
        ref = quote(ref, safe="")
        return self.get_json(f"/repos/{owner}/{repo}/git/trees/{ref}?recursive=1")

    def buscar_linguagens(self, owner, repo):
        owner = quote(owner, safe="")
        repo = quote(repo, safe="")
        return self.get_json(f"/repos/{owner}/{repo}/languages")
