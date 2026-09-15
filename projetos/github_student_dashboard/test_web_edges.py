import unittest

from projetos.github_student_dashboard.github_client import GitHubApiError
from projetos.github_student_dashboard.web import create_app


class WebEdgeCasesTest(unittest.TestCase):
    def _client(self, **overrides):
        defaults = {
            "analisador": lambda _repo: {"ok": True},
            "analisador_perfil": lambda _usuario: {"ok": True},
            "analisador_readme": lambda _repo: {"ok": True},
            "comparador": lambda _a, _b: {"ok": True},
            "analisador_historico": lambda _repo, limite=5: {"ok": True, "limite": limite},
            "explicador": lambda _repo: {"ok": True},
            "gerador_competencias": lambda: {"competencias": []},
        }
        defaults.update(overrides)
        app = create_app(**defaults)
        app.config["TESTING"] = True
        return app.test_client()

    def test_status_generico_da_api_vira_502(self):
        def falha(_):
            raise GitHubApiError("falha upstream", status=500)

        resposta = self._client(analisador=falha).get("/api/analisar?repo=a/b")
        self.assertEqual(resposta.status_code, 502)

    def test_perfil_mapeia_value_error_e_erro_github(self):
        def invalido(_):
            raise ValueError("usuário inválido")

        resposta = self._client(analisador_perfil=invalido).get("/api/perfil?usuario=x")
        self.assertEqual(resposta.status_code, 400)

        def limite(_):
            raise GitHubApiError("limite", status=429)

        resposta = self._client(analisador_perfil=limite).get("/api/perfil?usuario=x")
        self.assertEqual(resposta.status_code, 429)

    def test_readme_mapeia_value_error_e_erro_github(self):
        def ausente(_):
            raise ValueError("README ausente")

        resposta = self._client(analisador_readme=ausente).get("/api/readme?repo=a/b")
        self.assertEqual(resposta.status_code, 400)

        def upstream(_):
            raise GitHubApiError("indisponível", status=503)

        resposta = self._client(analisador_readme=upstream).get("/api/readme?repo=a/b")
        self.assertEqual(resposta.status_code, 502)

    def test_comparacao_mapeia_value_error_e_erro_github(self):
        def invalido(_a, _b):
            raise ValueError("comparação inválida")

        resposta = self._client(comparador=invalido).get("/api/comparar?a=a/b&b=c/d")
        self.assertEqual(resposta.status_code, 400)

        def negado(_a, _b):
            raise GitHubApiError("negado", status=401)

        resposta = self._client(comparador=negado).get("/api/comparar?a=a/b&b=c/d")
        self.assertEqual(resposta.status_code, 429)

    def test_historico_rejeita_limite_nao_numerico(self):
        resposta = self._client().get("/api/historico?repo=a/b&limite=abc")
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("número inteiro", resposta.get_json()["erro"])

    def test_historico_mapeia_value_error_e_erro_github(self):
        def invalido(_repo, limite=5):
            raise ValueError("limite inválido")

        resposta = self._client(analisador_historico=invalido).get("/api/historico?repo=a/b&limite=3")
        self.assertEqual(resposta.status_code, 400)

        def upstream(_repo, limite=5):
            raise GitHubApiError("indisponível", status=503)

        resposta = self._client(analisador_historico=upstream).get("/api/historico?repo=a/b&limite=3")
        self.assertEqual(resposta.status_code, 502)

    def test_explicar_exige_repo_e_mapeia_erros(self):
        self.assertEqual(self._client().get("/api/explicar").status_code, 400)

        def invalido(_):
            raise ValueError("inválido")

        self.assertEqual(
            self._client(explicador=invalido).get("/api/explicar?repo=a/b").status_code,
            400,
        )

        def upstream(_):
            raise GitHubApiError("indisponível", status=503)

        self.assertEqual(
            self._client(explicador=upstream).get("/api/explicar?repo=a/b").status_code,
            502,
        )

    def test_explicar_sucesso_e_pagina_publica(self):
        resposta = self._client(explicador=lambda repo: {"repositorio": repo, "modo": "local"}).get(
            "/api/explicar?repo=a/b"
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["modo"], "local")
        self.assertEqual(self._client().get("/explicar").status_code, 200)

    def test_favicon_e_resposta_json_nao_recebem_html_extra(self):
        self.assertEqual(self._client().get("/favicon.ico").status_code, 204)
        resposta = self._client().get("/healthz")
        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn(b"interactions.css", resposta.data)

    def test_api_trilha_e_competencias_injetadas(self):
        trilha = self._client().get("/api/trilha")
        self.assertEqual(trilha.status_code, 200)
        self.assertEqual(trilha.get_json()["total_niveis"], 6)

        competencias = self._client(gerador_competencias=lambda: {"resumo": {"forte": 2}}).get(
            "/api/competencias"
        )
        self.assertEqual(competencias.status_code, 200)
        self.assertEqual(competencias.get_json()["resumo"]["forte"], 2)


if __name__ == "__main__":
    unittest.main()
