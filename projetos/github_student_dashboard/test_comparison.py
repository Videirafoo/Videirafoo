import unittest

from projetos.github_student_dashboard.comparison import (
    comparar_relatorios,
    comparar_repositorios_remotos,
)


class ComparisonTest(unittest.TestCase):
    def test_compara_diferencas_objetivas(self):
        relatorio_a = {
            "repositorio": "org/a",
            "url": "https://github.com/org/a",
            "score": 90,
            "checks": {
                "readme": True,
                "descricao": True,
                "licenca": True,
                "gitignore": True,
                "topics": True,
                "ci": True,
                "testes": True,
                "dependencias": False,
            },
            "evidencias": {
                "ci_status": {"estado": "success", "workflow": "CI", "url": "https://example.com/a"}
            },
        }
        relatorio_b = {
            "repositorio": "org/b",
            "url": "https://github.com/org/b",
            "score": 70,
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
            "evidencias": {
                "ci_status": {"estado": "failure", "workflow": "CI", "url": "https://example.com/b"}
            },
        }
        readme_a = {
            "tipo_detectado": "projeto",
            "cobertura_documental": {"percentual": 88.9},
            "criterios": {},
        }
        readme_b = {
            "tipo_detectado": "projeto",
            "cobertura_documental": {"percentual": 66.7},
            "criterios": {},
        }

        resultado = comparar_relatorios(relatorio_a, readme_a, relatorio_b, readme_b)

        self.assertEqual(resultado["diferencas_objetivas"]["score"], 20)
        self.assertEqual(resultado["diferencas_objetivas"]["readme_cobertura"], 22.2)
        self.assertIn("descricao", resultado["diferencas_objetivas"]["checks_exclusivos_a"])
        self.assertIn("topics", resultado["diferencas_objetivas"]["checks_exclusivos_a"])
        self.assertIn("dependencias", resultado["diferencas_objetivas"]["checks_exclusivos_b"])
        self.assertEqual(resultado["repositorio_a"]["ci_real"]["estado"], "success")

    def test_rejeita_comparacao_do_mesmo_repositorio(self):
        with self.assertRaises(ValueError):
            comparar_repositorios_remotos(
                "Videirafoo/projeto",
                "videirafoo/PROJETO",
                analisador_repo=lambda _: {},
                analisador_readme=lambda _: {},
            )

    def test_usa_analisadores_injetados(self):
        chamadas = []

        def repo(ref):
            chamadas.append(("repo", ref))
            return {
                "repositorio": ref,
                "url": f"https://github.com/{ref}",
                "score": 100,
                "checks": {"readme": True},
                "evidencias": {"ci_status": {"estado": "success"}},
            }

        def readme(ref):
            chamadas.append(("readme", ref))
            return {
                "tipo_detectado": "projeto",
                "cobertura_documental": {"percentual": 100.0},
                "criterios": {},
            }

        resultado = comparar_repositorios_remotos(
            "Videirafoo/a",
            "Videirafoo/b",
            analisador_repo=repo,
            analisador_readme=readme,
        )

        self.assertEqual(resultado["repositorio_a"]["repositorio"], "Videirafoo/a")
        self.assertEqual(len(chamadas), 4)


if __name__ == "__main__":
    unittest.main()
