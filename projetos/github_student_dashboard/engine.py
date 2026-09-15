from collections import Counter
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


def normalizar_usuario(usuario):
    usuario = usuario.strip()

    if usuario.startswith("http://") or usuario.startswith("https://"):
        url = urlparse(usuario)
        if url.netloc.lower() != "github.com":
            raise ValueError("A URL precisa ser do github.com.")
        partes = [parte for parte in url.path.split("/") if parte]
        if not partes:
            raise ValueError("Informe um usuário do GitHub.")
        usuario = partes[0]

    usuario = usuario.strip().strip("/")
    if not usuario or "/" in usuario:
        raise ValueError("Informe apenas o usuário do GitHub.")

    return usuario


def caminhos_da_arvore(arvore):
    return {
        item.get("path", "")
        for item in arvore.get("tree", [])
        if item.get("type") == "blob" and item.get("path")
    }


def detectar_readme(caminhos):
    nomes = {caminho.lower() for caminho in caminhos if "/" not in caminho}
    return any(nome == "readme" or nome.startswith("readme.") for nome in nomes)


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


def arquivos_de_dependencias(caminhos):
    encontrados = []
    for caminho in caminhos:
        nome = caminho.rsplit("/", 1)[-1].lower()
        if nome in ARQUIVOS_DEPENDENCIAS:
            encontrados.append(caminho)
    return sorted(encontrados)


def detectar_dependencias(caminhos):
    return bool(arquivos_de_dependencias(caminhos))


def calcular_score(checks):
    return sum(PESOS[nome] for nome, passou in checks.items() if passou)


def gerar_recomendacoes(checks):
    regras = {
        "readme": ("alta", "Adicionar README com objetivo, execução, exemplos e próximos passos."),
        "descricao": ("media", "Adicionar uma descrição curta e específica ao repositório no GitHub."),
        "licenca": ("media", "Definir uma licença adequada quando o projeto for destinado a reutilização pública."),
        "gitignore": ("media", "Adicionar .gitignore adequado à stack para evitar arquivos gerados e segredos locais."),
        "topics": ("media", "Adicionar topics relevantes para melhorar descoberta e contexto do projeto."),
        "ci": ("alta", "Adicionar CI para validar automaticamente testes, sintaxe ou build."),
        "testes": ("alta", "Adicionar testes automatizados para os comportamentos mais importantes."),
        "dependencias": ("media", "Registrar dependências em um arquivo padrão da tecnologia usada."),
    }

    recomendacoes = []
    for nome, passou in checks.items():
        if passou:
            continue

        prioridade, acao = regras[nome]
        recomendacoes.append({"check": nome, "prioridade": prioridade, "acao": acao})

    return recomendacoes


def montar_snapshot(client, owner, repo):
    metadata = client.buscar_repositorio(owner, repo)
    branch = metadata.get("default_branch") or "main"
    arvore = client.buscar_arvore(owner, repo, branch)
    linguagens = client.buscar_linguagens(owner, repo)

    return {"metadata": metadata, "arvore": arvore, "linguagens": linguagens}


def analisar_snapshot(snapshot):
    metadata = snapshot["metadata"]
    arvore = snapshot["arvore"]
    linguagens = snapshot.get("linguagens", {})
    caminhos = caminhos_da_arvore(arvore)
    dependencias_encontradas = arquivos_de_dependencias(caminhos)

    checks = {
        "readme": detectar_readme(caminhos),
        "descricao": bool((metadata.get("description") or "").strip()),
        "licenca": detectar_licenca(metadata, caminhos),
        "gitignore": detectar_gitignore(caminhos),
        "topics": bool(metadata.get("topics")),
        "ci": detectar_ci(caminhos),
        "testes": detectar_testes(caminhos),
        "dependencias": bool(dependencias_encontradas),
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
            "arquivos_dependencias": dependencias_encontradas,
            "tem_descricao": checks["descricao"],
            "tem_licenca": checks["licenca"],
            "tem_gitignore": checks["gitignore"],
            "tem_ci": checks["ci"],
            "tem_testes": checks["testes"],
        },
        "recomendacoes": gerar_recomendacoes(checks),
    }


def analisar_repositorio_remoto(referencia, client=None):
    owner, repo = normalizar_referencia(referencia)
    client = client or GitHubClient()
    snapshot = montar_snapshot(client, owner, repo)
    return analisar_snapshot(snapshot)


def _percentual(parte, total):
    if not total:
        return 0
    return round((parte / total) * 100, 1)


def analisar_perfil_snapshot(usuario, repositorios):
    login = usuario.get("login") or ""
    repositorios_proprios = [repo for repo in repositorios if not repo.get("fork")]
    total = len(repositorios_proprios)

    com_descricao = sum(bool((repo.get("description") or "").strip()) for repo in repositorios_proprios)
    com_topics = sum(bool(repo.get("topics")) for repo in repositorios_proprios)
    com_licenca = sum(bool(repo.get("license")) for repo in repositorios_proprios)
    stars = sum(int(repo.get("stargazers_count") or 0) for repo in repositorios_proprios)
    forks = sum(int(repo.get("forks_count") or 0) for repo in repositorios_proprios)

    linguagens = Counter(
        repo.get("language")
        for repo in repositorios_proprios
        if repo.get("language")
    )

    repo_perfil = next(
        (repo for repo in repositorios_proprios if (repo.get("name") or "").lower() == login.lower()),
        None,
    )

    repos_ordenados = sorted(
        repositorios_proprios,
        key=lambda repo: (
            int(repo.get("stargazers_count") or 0),
            int(repo.get("forks_count") or 0),
            repo.get("updated_at") or "",
        ),
        reverse=True,
    )

    lacunas = []
    if not (usuario.get("name") or "").strip():
        lacunas.append("nome_publico")
    if not (usuario.get("bio") or "").strip():
        lacunas.append("bio")
    if not repo_perfil:
        lacunas.append("repositorio_perfil")
    if total and com_descricao < total:
        lacunas.append("descricoes_repositorios")
    if total and com_topics < total:
        lacunas.append("topics_repositorios")
    if total and com_licenca < total:
        lacunas.append("licencas_repositorios")

    return {
        "usuario": login,
        "url": usuario.get("html_url"),
        "nome_publico": usuario.get("name"),
        "bio": usuario.get("bio"),
        "seguidores": int(usuario.get("followers") or 0),
        "seguindo": int(usuario.get("following") or 0),
        "repositorios_publicos_api": int(usuario.get("public_repos") or total),
        "repositorios_analisados": total,
        "repositorio_perfil_existe": bool(repo_perfil),
        "cobertura": {
            "descricao": {"quantidade": com_descricao, "percentual": _percentual(com_descricao, total)},
            "topics": {"quantidade": com_topics, "percentual": _percentual(com_topics, total)},
            "licenca": {"quantidade": com_licenca, "percentual": _percentual(com_licenca, total)},
        },
        "engajamento": {"stars_recebidos": stars, "forks_recebidos": forks},
        "linguagens_principais": [
            {"linguagem": linguagem, "repositorios": quantidade}
            for linguagem, quantidade in linguagens.most_common(5)
        ],
        "repositorios_destaque": [
            {
                "nome": repo.get("name"),
                "url": repo.get("html_url"),
                "descricao": repo.get("description"),
                "linguagem": repo.get("language"),
                "stars": int(repo.get("stargazers_count") or 0),
                "forks": int(repo.get("forks_count") or 0),
                "topics": repo.get("topics") or [],
            }
            for repo in repos_ordenados[:5]
        ],
        "lacunas_objetivas": lacunas,
        "observacao": "A análise de perfil usa metadados públicos e não atribui uma nota arbitrária de qualidade.",
    }


def analisar_perfil_remoto(usuario, client=None):
    usuario = normalizar_usuario(usuario)
    client = client or GitHubClient()
    metadata = client.buscar_usuario(usuario)
    repositorios = client.buscar_repositorios_usuario(usuario)
    return analisar_perfil_snapshot(metadata, repositorios)
