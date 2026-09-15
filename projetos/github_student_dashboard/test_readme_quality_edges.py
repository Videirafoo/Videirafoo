import base64
import unittest

from projetos.github_student_dashboard.github_client import GitHubApiError
from projetos.github_student_dashboard.readme_quality import (
    _normalizar_link_interno,
    analisar_readme_remoto,
)


class ClienteReadmeEdge:
    def __init__(self, resposta=None, erro_readme=None, erro_arvore=None):
        self.resposta = resposta or {
            "path": "README.md",
            "encoding": "base64",
            "content": base64.b64encode(b"# Projeto\n").decode("ascii"),
        }
        self.erro_readme = erro_readme
        self.erro_arvore = erro_arvore

    def get_json(self, path):
        if self.erro_readme:
            raise self.erro_readme
        return self.resposta

    def buscar_repositorio(self, owner, repo):
        return {"default_branch": "main"}

    def buscar_arvore(self, owner, repo, ref):
        if self.erro_arvore:
            raise self.erro_arvore
        return {"tree": [{"path": "README.md"}]}


class ReadmeQualityEdgeCasesTest(unittest.TestCase):
    def test_normalizador_ignora_destinos_nao_verificaveis(self):
        self.assertIsNone(_normalizar_link_interno("#secao"))
        self.assertIsNone(_normalizar_link_interno("//cdn.exemplo.com/a"))
        self.assertIsNone(_normalizar_link_interno("https://example.com/a"))
        self.assertIsNone(_normalizar_link_interno("?modo=1"))
        self.assertIsNone(_normalizar_link_interno("/"))

    def test_normalizador_decodifica_url_interna(self):
        self.assertEqual(_normalizar_link_interno("docs/guia%20rapido.md#uso"), "docs/guia rapido.md")

    def test_readme_404_vira_erro_amigavel(self):
        cliente = ClienteReadmeEdge(erro_readme=GitHubApiError("não encontrado", status=404))
        with self.assertRaisesRegex(ValueError, "README não encontrado"):
            analisar_readme_remoto("aluno/projeto", client=cliente)

    def test_erro_github_diferente_de_404_e_propagado(self):
        erro = GitHubApiError("limite", status=403)
        cliente = ClienteReadmeEdge(erro_readme=erro)
        with self.assertRaises(GitHubApiError):
            analisar_readme_remoto("aluno/projeto", client=cliente)

    def test_rejeita_encoding_nao_suportado(self):
        cliente = ClienteReadmeEdge(resposta={"encoding": "utf-8", "content": "# Projeto"})
        with self.assertRaisesRegex(ValueError, "Formato de README"):
            analisar_readme_remoto("aluno/projeto", client=cliente)

    def test_rejeita_conteudo_base64_que_nao_e_utf8(self):
        cliente = ClienteReadmeEdge(
            resposta={"encoding": "base64", "content": base64.b64encode(b"\xff\xfe").decode("ascii")}
        )
        with self.assertRaisesRegex(ValueError, "decodificar"):
            analisar_readme_remoto("aluno/projeto", client=cliente)

    def test_falha_na_arvore_nao_inventa_links_quebrados(self):
        texto = b"# Projeto\n\n[Guia](docs/guia.md)"
        cliente = ClienteReadmeEdge(
            resposta={"encoding": "base64", "content": base64.b64encode(texto).decode("ascii")},
            erro_arvore=GitHubApiError("indisponível", status=503),
        )
        relatorio = analisar_readme_remoto("aluno/projeto", client=cliente)
        self.assertFalse(relatorio["links_internos"]["verificados"])
        self.assertEqual(relatorio["links_internos"]["quebrados"], [])

    def test_metadata_invalido_nao_quebra_analise(self):
        class Cliente(ClienteReadmeEdge):
            def buscar_repositorio(self, owner, repo):
                return None

        relatorio = analisar_readme_remoto("aluno/projeto", client=Cliente())
        self.assertFalse(relatorio["links_internos"]["verificados"])


if __name__ == "__main__":
    unittest.main()
