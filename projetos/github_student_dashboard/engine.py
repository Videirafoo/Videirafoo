from urllib.parse import urlparse

from projetos.github_student_dashboard.github_client import GitHubClient

PESOS = {
    "readme": 15,
    "descricao": 10,
    "licenca": 10,
    "gitignore": 10,
    "topics": 10,
    "ci": 15,
    "testes": 20,
    "dependencias": 10,
}

ARQUIVOS_DEPENDENCIAS = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "pubspec.yaml",
    "go.mod",
    "cargo.toml",
}


def normalizar_referencia(referencia):
    referencia = referencia.strip()

    if referencia.startswith("http://") or referencia.startswith("https://"):
        url = urlparse(referencia)
        if url.netloc.lower() != "github.com":
            raise ValueError("A URL precisa ser do github.com.")
        partes = [parte for parte in url.path.split("/") if parte]
    else:
        partes = [parte for parte in referencia.split("/") if parte]

    if len(partes) < 2:
        raise ValueError("Use o formato usuario/repositorio.")

    owner = partes[0].strip()
    repo = partes[1].strip()

    if repo.endswith(".git"):
        repo = repo[:-4]

    if not owner or not repo:
        raise ValueError("Use o formato usuario/repositorio.")

    return owner, repo


def caminhos_da_arvore(arvore):
    return {
        item.get("path", "")
        for item in arvore.get("tree", [])
        if item.get("type") == "blob" and item.get("path")
    }


def detectar_readme(caminhos):
    nomes = {caminho.lower() for caminho in caminhos if "/" not in caminho}
    return any(
        nome == "readme" or nome.startswith("readme.")
        for nome in nomes
    )


def detectar_gitignore(caminhos):
    return ".gitignore" in caminhos


def detectar_licenca(metadata, caminhos):
    if metadata.get("license"):
        return True

    nomes = {caminho.lower() for caminho in caminhos if "/" not in caminho}
    return any(
        nome == "license"
        or nome.startswith("license.")
        or nome == "licence"
        or nome.startswith("licence.")
        for nome in nomes
    )


def detectar_ci(caminhos):
    return any(
        caminho.startswith(".github/workflows/")
        and caminho.lower().endswith((".yml", ".yaml"))
        for caminho in caminhos
    )


def detectar_testes(caminhos):
    for caminho in caminhos:
        partes = caminho.lower().split("/")
        nome = partes[-1]

        if "tests" in partes or "test" in partes:
            return True
        if nome.startswith("test_"):
            return True
        if nome.endswith("_test.py"):
            return True
        if nome.endswith((".test.js", ".test.ts", ".test.tsx", ".spec.js", ".spec.ts", ".spec.tsx")):
            return True

    return False


def detectar_dependencias(caminhos):
    raiz = {caminho.lower() for caminho in caminhos if "/" not in caminho}
    return any(nome in raiz for nome in ARQUIVOS_DEPENDENCIAS)


def calcular_score(checks):
    return sum(PESOS[nome] for nome, passou in checks.items() if passou)


def gerar_recomendacoes(checks):
    regras = {
        "readme": (
            "alta",
            "Adicionar README com objetivo, execução, exemplos e próximos passos.",
        ),
        "descricao": (
            "media",
            "Adicionar uma descrição curta e específica ao repositório no GitHub.",
        ),
        "licenca": (
            "media",
            "Definir uma licença adequada quando o projeto for destinado a reutilização pública.",
        ),
        "gitignore": (
            "media",
            "Adicionar .gitignore adequado à stack para evitar arquivos gerados e segredos locais.",
        ),
        "topics": (
            "media",
            "Adicionar topics relevantes para melhorar descoberta e contexto do projeto.",
        ),
        "ci": (
            "alta",
            "Adicionar CI para validar automaticamente testes, sintaxe ou build.",
        ),
        "testes": (
            "alta",
            "Adicionar testes automatizados para os comportamentos mais importantes.",
        ),
        "dependencias": (
            "media",
            "Registrar dependências em um arquivo padrão da tecnologia usada.",
        ),
    }

    recomendacoes = []
    for nome, passou in checks.items():
        if passou:
            continue

        prioridade, acao = regras[nome]
        recomendacoes.append(
            {
                "check": nome,
                "prioridade": prioridade,
                "acao": acao,
            }
        )

    return recomendacoes


def montar_snapshot(client, owner, repo):
    metadata = client.buscar_repositorio(owner, repo)
    branch = metadata.get("default_branch") or "main"
    arvore = client.buscar_arvore(owner, repo, branch)
    linguagens = client.buscar_linguagens(owner, repo)

    return {
        "metadata": metadata,
        "arvore": arvore,
        "linguagens": linguagens,
    }


def analisar_snapshot(snapshot):
    metadata = snapshot["metadata"]
    arvore = snapshot["arvore"]
    linguagens = snapshot.get("linguagens", {})
    caminhos = caminhos_da_arvore(arvore)

    checks = {
        "readme": detectar_readme(caminhos),
        "descricao": bool((metadata.get("description") or "").strip()),
        "licenca": detectar_licenca(metadata, caminhos),
        "gitignore": detectar_gitignore(caminhos),
        "topics": bool(metadata.get("topics")),
        "ci": detectar_ci(caminhos),
        "testes": detectar_testes(caminhos),
        "dependencias": detectar_dependencias(caminhos),
    }

    return {
        "repositorio": metadata.get("full_name"),
        "url": metadata.get("html_url"),
        "branch_padrao": metadata.get("default_branch"),
        "score": calcular_score(checks),
        "checks": checks,
        "evidencias": {
            "arquivos_encontrados": len(caminhos),
            "topics": metadata.get("topics", []),
            "linguagens_bytes": linguagens,
            "arvore_truncada": bool(arvore.get("truncated")),
        },
        "recomendacoes": gerar_recomendacoes(checks),
    }


def analisar_repositorio_remoto(referencia, client=None):
    owner, repo = normalizar_referencia(referencia)
    client = client or GitHubClient()
    snapshot = montar_snapshot(client, owner, repo)
    return analisar_snapshot(snapshot)
