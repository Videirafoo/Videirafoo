"""Regression tests for educational algorithms and link verification."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


alg = load('alg', ROOT / 'conteudos/python-para-iniciantes/algoritmos_exemplos.py')
links = load('links', ROOT / 'scripts/check_links.py')


class EducationalTests(unittest.TestCase):
    def test_searches(self):
        self.assertEqual(alg.busca_sequencial([8, 3, 8], 3), 1)
        self.assertEqual(alg.busca_sequencial([], 3), -1)
        self.assertEqual(alg.busca_binaria([1, 3, 5, 7], 5), 2)
        self.assertEqual(alg.busca_binaria([1, 3, 5], 2), -1)

    def test_sort_does_not_mutate_input(self):
        original = [4, 2, 2, 1]
        self.assertEqual(alg.ordenacao_bolha(original), [1, 2, 2, 4])
        self.assertEqual(original, [4, 2, 2, 1])

    def test_broken_relative_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('[missing](missing.md)')
            self.assertEqual(len(links.validate(root)), 1)
            (root / 'missing.md').write_text('ok')
            self.assertEqual(links.validate(root), [])


if __name__ == '__main__':
    unittest.main()
