import base64
import unittest

from projetos.github_student_dashboard.readme_quality import (
    analisar_readme_remoto,
    analisar_readme_texto,
)


class ClienteReadmeFalso:
    def __init__(self, texto):
        self.texto = texto

    def get_json(self, path):
        return {
            "path": "README.md",
            "encoding": "base64",
            "content": base64.b64encode(self.texto.encode("utf-8")).decode("ascii"),
        }

    def buscar_repositorio(self, owner, repo):
        return {
            "full_name": f"{owner}/{repo}",
            "default_branch": "main",
        }

    def buscar_arvore(self, owner, repo, ref):
        caminhos = [
            "README.md",
            "docs",
            "docs/guia.md",
            "src",
            "src/app.py",
        ]
        return {
            "truncated": False,
            "tree": [
                {"path": caminho, "type": "tree" if "." not in caminho.rsplit("/", 1)[-1] else "blob"}
                for caminho in caminhos
            ],
        }


class ReadmeQualityTest(unittest.TestCase):
    def test_detecta_readme_de_perfil(self):
        texto = """# Fernando Videira

## Sobre mim
Texto de apresentação com conteúdo suficiente para explicar a trajetória e objetivos profissionais.

## Stack
Python, Java, Flutter e GitHub.

## Projetos
- [Projeto 1](https://github.com/exemplo/1)
- [Projeto 2](https://github.com/exemplo/2)

## Atualmente estudando
Algoritmos, APIs e IA.

## Links
- [Guia](https://github.com/exemplo/guia)

Conteúdo complementar para manter o README útil, estruturado e fácil de percorrer por estudantes e visitantes interessados em acompanhar a evolução do perfil.
"""
        relatorio = analisar_readme_texto(texto, "Videirafoo", "Videirafoo")

        self.assertEqual(relatorio["tipo_detectado"], "perfil_github")
        self.assertGreaterEqual(relatorio["cobertura_documental"]["aprovados"], 6)
        self.assertTrue(relatorio["criterios"]["sobre"]["passou"])
        self.assertTrue(relatorio["criterios"]["projetos"]["passou"])

    def test_detecta_readme_de_projeto(self):
        texto = """# Projeto Exemplo

## Objetivo
Explicar um projeto de estudo.

## Requisitos e instalação
```bash
pip install -r requirements.txt
```

## Como executar
```bash
python app.py
```

## Testes
```bash
python -m unittest
```

## Como contribuir
Abra uma issue e envie um pull request.

## Licença
MIT. Veja LICENSE.
"""
        relatorio = analisar_readme_texto(texto, "aluno", "projeto")

        self.assertEqual(relatorio["tipo_detectado"], "projeto")
        self.assertTrue(relatorio["criterios"]["instalacao"]["passou"])
        self.assertTrue(relatorio["criterios"]["execucao"]["passou"])
        self.assertTrue(relatorio["criterios"]["testes"]["passou"])
        self.assertTrue(relatorio["criterios"]["licenca"]["passou"])

    def test_readme_incompleto_expoe_lacunas(self):
        relatorio = analisar_readme_texto("# Projeto\n\nPouco conteúdo.", "aluno", "projeto")

        self.assertFalse(relatorio["criterios"]["instalacao"]["passou"])
        self.assertFalse(relatorio["criterios"]["execucao"]["passou"])
        self.assertLess(relatorio["cobertura_documental"]["percentual"], 50)

    def test_verifica_links_internos_sem_consultar_urls_externas(self):
        texto = """# Projeto

- [Guia](./docs/guia.md)
- [Pasta](docs)
- [Ausente](docs/ausente.md)
- [Site](https://example.com)
- [Seção](#projeto)
"""
        caminhos = {"README.md", "docs", "docs/guia.md", "src", "src/app.py"}

        relatorio = analisar_readme_texto(texto, "aluno", "projeto", caminhos=caminhos)
        links = relatorio["links_internos"]

        self.assertTrue(links["verificados"])
        self.assertEqual(links["total"], 3)
        self.assertEqual(links["validos"], 2)
        self.assertEqual(links["quebrados"], ["docs/ausente.md"])

    def test_sem_arvore_nao_inventa_link_quebrado(self):
        relatorio = analisar_readme_texto("# Projeto\n\n[Guia](docs/guia.md)", "aluno", "projeto")

        self.assertFalse(relatorio["links_internos"]["verificados"])
        self.assertEqual(relatorio["links_internos"]["quebrados"], [])

    def test_analise_remota_decodifica_base64_e_verifica_links(self):
        cliente = ClienteReadmeFalso("# Perfil\n\n## Sobre mim\nTexto\n\n[Guia](docs/guia.md)")

        relatorio = analisar_readme_remoto("Videirafoo/Videirafoo", client=cliente)

        self.assertEqual(relatorio["repositorio"], "Videirafoo/Videirafoo")
        self.assertEqual(relatorio["arquivo"], "README.md")
        self.assertEqual(relatorio["tipo_detectado"], "perfil_github")
        self.assertTrue(relatorio["links_internos"]["verificados"])
        self.assertEqual(relatorio["links_internos"]["validos"], 1)
        self.assertEqual(relatorio["links_internos"]["quebrados"], [])


if __name__ == "__main__":
    unittest.main()
