import json
from collections import Counter
from pathlib import Path

EXTENSOES_LINGUAGENS = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript/React",
    ".java": "Java",
    ".dart": "Dart",
    ".html": "HTML",
    ".css": "CSS",
}

ARQUIVOS_DEPENDENCIAS = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "pubspec.yaml",
}

PASTAS_IGNORADAS = {".git", ".venv", "venv", "node_modules", "__pycache__"}

PESOS = {
    "readme": 20,
    "gitignore": 10,
    "licenca": 15,
    "ci": 20,
    "testes": 20,
    "dependencias": 15,
}


def listar_arquivos(caminho):
    caminho = Path(caminho)
    arquivos = []

    for item in caminho.rglob("*"):
        if not item.is_file():
            continue

        if any(parte in PASTAS_IGNORADAS for parte in item.parts):
            continue

        arquivos.append(item)

    return arquivos


def possui_arquivo_raiz(caminho, nomes):
    caminho = Path(caminho)
    existentes = {item.name.lower() for item in caminho.iterdir() if item.is_file()}
    return any(nome.lower() in existentes for nome in nomes)


def detectar_readme(caminho):
    return possui_arquivo_raiz(caminho, {"README.md", "README.rst", "README.txt", "README"})


def detectar_licenca(caminho):
    return possui_arquivo_raiz(
        caminho,
        {"LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "LICENCE.md"},
    )


def detectar_gitignore(caminho):
    return Path(caminho, ".gitignore").is_file()


def detectar_ci(caminho):
    pasta = Path(caminho, ".github", "workflows")

    if not pasta.is_dir():
        return False

    return any(
        arquivo.is_file() and arquivo.suffix.lower() in {".yml", ".yaml"}
        for arquivo in pasta.iterdir()
    )


def detectar_testes(caminho, arquivos=None):
    caminho = Path(caminho)
    arquivos = arquivos or listar_arquivos(caminho)

    if any(Path(caminho, nome).is_dir() for nome in ["tests", "test"]):
        return True

    for arquivo in arquivos:
        nome = arquivo.name.lower()
        if nome.startswith("test_") or nome.endswith("_test.py"):
            return True

    return False


def detectar_dependencias(caminho):
    return possui_arquivo_raiz(caminho, ARQUIVOS_DEPENDENCIAS)


def contar_linguagens(arquivos):
    contador = Counter()

    for arquivo in arquivos:
        linguagem = EXTENSOES_LINGUAGENS.get(arquivo.suffix.lower())
        if linguagem:
            contador[linguagem] += 1

    return dict(sorted(contador.items(), key=lambda item: (-item[1], item[0])))


def calcular_score(checks):
    return sum(PESOS[chave] for chave, presente in checks.items() if presente)


def gerar_recomendacoes(checks):
    recomendacoes = []

    if not checks["readme"]:
        recomendacoes.append(
            "Adicionar README com objetivo, como executar, exemplos e próximos passos."
        )
    if not checks["gitignore"]:
        recomendacoes.append(
            "Adicionar .gitignore adequado à tecnologia para evitar arquivos desnecessários."
        )
    if not checks["licenca"]:
        recomendacoes.append(
            "Definir uma licença quando o projeto for destinado a reutilização pública."
        )
    if not checks["ci"]:
        recomendacoes.append(
            "Adicionar CI para validar automaticamente sintaxe, testes ou build."
        )
    if not checks["testes"]:
        recomendacoes.append(
            "Adicionar testes automatizados para comportamentos importantes."
        )
    if not checks["dependencias"]:
        recomendacoes.append(
            "Registrar dependências em um arquivo padrão da tecnologia usada."
        )

    if not recomendacoes:
        recomendacoes.append(
            "A base está completa para estes checks. Próximo passo: revisar qualidade da documentação e cobertura dos testes."
        )

    return recomendacoes


def analisar_repositorio(caminho):
    caminho = Path(caminho).expanduser().resolve()

    if not caminho.exists():
        raise ValueError("O caminho informado não existe.")
    if not caminho.is_dir():
        raise ValueError("O caminho informado precisa ser uma pasta.")

    arquivos = listar_arquivos(caminho)

    checks = {
        "readme": detectar_readme(caminho),
        "gitignore": detectar_gitignore(caminho),
        "licenca": detectar_licenca(caminho),
        "ci": detectar_ci(caminho),
        "testes": detectar_testes(caminho, arquivos),
        "dependencias": detectar_dependencias(caminho),
    }

    linguagens = contar_linguagens(arquivos)

    return {
        "repositorio": caminho.name,
        "caminho": str(caminho),
        "score": calcular_score(checks),
        "checks": checks,
        "evidencias": {
            "total_arquivos_analisados": len(arquivos),
            "linguagens_estimadas": linguagens,
        },
        "recomendacoes": gerar_recomendacoes(checks),
    }


def salvar_relatorio(relatorio, destino):
    destino = Path(destino)

    with destino.open("w", encoding="utf-8") as arquivo:
        json.dump(relatorio, arquivo, ensure_ascii=False, indent=2)


def exibir_relatorio(relatorio):
    print(f"\n=== Diagnóstico: {relatorio['repositorio']} ===")
    print(f"Score: {relatorio['score']}/100")

    print("\nChecks:")
    for nome, presente in relatorio["checks"].items():
        marcador = "OK" if presente else "FALTA"
        print(f"- {nome}: {marcador}")

    print("\nLinguagens estimadas:")
    linguagens = relatorio["evidencias"]["linguagens_estimadas"]
    if linguagens:
        for nome, quantidade in linguagens.items():
            print(f"- {nome}: {quantidade} arquivo(s)")
    else:
        print("- nenhuma linguagem reconhecida pelos checks atuais")

    print("\nRecomendações:")
    for recomendacao in relatorio["recomendacoes"]:
        print(f"- {recomendacao}")


def main():
    caminho = input("Caminho do repositório/pasta que deseja analisar: ").strip()

    try:
        relatorio = analisar_repositorio(caminho)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return

    exibir_relatorio(relatorio)

    resposta = input("\nSalvar relatório em JSON? [s/n]: ").strip().lower()
    if resposta == "s":
        destino = input("Nome do arquivo [relatorio.json]: ").strip() or "relatorio.json"
        salvar_relatorio(relatorio, destino)
        print(f"Relatório salvo em {destino}.")


if __name__ == "__main__":
    main()
