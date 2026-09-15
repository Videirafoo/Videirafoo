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


def arquivos_de_testes(caminhos):
    encontrados = []
    for caminho in caminhos:
        partes = caminho.lower().split("/")
        nome = partes[-1]
        if (
            "tests" in partes
            or "test" in partes
            or nome.startswith("test_")
            or nome.endswith("_test.py")
            or nome.endswith((".test.js", ".test.ts", ".test.tsx", ".spec.js", ".spec.ts", ".spec.tsx"))
        ):
            encontrados.append(caminho)
    return sorted(encontrados)


def detectar_testes(caminhos):
    return bool(arquivos_de_testes(caminhos))


def arquivos_de_dependencias(caminhos):
    encontrados = []
    for caminho in caminhos:
        nome = caminho.rsplit("/", 1)[-1].lower()
        if nome in ARQUIVOS_DEPENDENCIAS:
            encontrados.append(caminho)
    return sorted(encontrados)


def detectar_dependencias(caminhos):
    return bool(arquivos_de_dependencias(caminhos))


def arquivos_de_ci(caminhos):
    return sorted(
        caminho
        for caminho in caminhos
        if caminho.startswith(".github/workflows/")
        and caminho.lower().endswith((".yml", ".yaml"))
    )


def arquivo_readme(caminhos):
    for caminho in sorted(caminhos):
        if "/" in caminho:
            continue
        nome = caminho.lower()
        if nome == "readme" or nome.startswith("readme."):
            return caminho
    return None


def arquivo_licenca(caminhos):
    for caminho in sorted(caminhos):
        if "/" in caminho:
            continue
        nome = caminho.lower()
        if nome == "license" or nome.startswith("license.") or nome == "licence" or nome.startswith("licence."):
            return caminho
    return None


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


def gerar_detalhes_checks(metadata, caminhos, checks):
    readme = arquivo_readme(caminhos)
    licenca_arquivo = arquivo_licenca(caminhos)
    workflows = arquivos_de_ci(caminhos)
    testes = arquivos_de_testes(caminhos)
    dependencias = arquivos_de_dependencias(caminhos)
    topics = metadata.get("topics") or []
    licenca_api = metadata.get("license") or {}
    licenca_nome = licenca_api.get("spdx_id") or licenca_api.get("name")
    descricao = (metadata.get("description") or "").strip()

    return {
        "readme": {
            "passou": checks["readme"],
            "observado": f"README encontrado: {readme}." if readme else "Nenhum README foi encontrado na raiz do repositório.",
            "impacto": "O README é a principal porta de entrada para entender objetivo, execução e uso do projeto.",
            "acao": "Manter o README atualizado e orientado a quem chega pela primeira vez." if readme else "Criar README com objetivo, instalação, execução, exemplos e próximos passos.",
        },
        "descricao": {
            "passou": checks["descricao"],
            "observado": f"Descrição pública: {descricao}" if descricao else "O campo Description do repositório está vazio.",
            "impacto": "A descrição ajuda pessoas e mecanismos de busca do GitHub a entenderem rapidamente o projeto.",
            "acao": "Manter a descrição curta, específica e coerente com o projeto." if descricao else "Preencher uma descrição curta e específica na área About do GitHub.",
        },
        "licenca": {
            "passou": checks["licenca"],
            "observado": (
                f"Licença declarada pela API: {licenca_nome}."
                if licenca_nome
                else f"Arquivo de licença encontrado: {licenca_arquivo}."
                if licenca_arquivo
                else "Nenhuma licença declarada foi encontrada."
            ),
            "impacto": "A licença deixa claro como outras pessoas podem usar, estudar e reutilizar o código.",
            "acao": "Manter a licença compatível com o objetivo do projeto." if checks["licenca"] else "Escolher e adicionar uma licença adequada antes de incentivar reutilização pública.",
        },
        "gitignore": {
            "passou": checks["gitignore"],
            "observado": "Arquivo .gitignore encontrado na raiz." if checks["gitignore"] else "Arquivo .gitignore não encontrado na raiz.",
            "impacto": "Um .gitignore adequado reduz o risco de versionar arquivos temporários, ambientes locais e segredos.",
            "acao": "Revisar o .gitignore quando novas ferramentas forem adicionadas." if checks["gitignore"] else "Adicionar .gitignore adequado às tecnologias usadas.",
        },
        "topics": {
            "passou": checks["topics"],
            "observado": f"Topics encontrados: {', '.join(topics)}." if topics else "Nenhum topic público foi encontrado.",
            "impacto": "Topics melhoram contexto e descoberta do repositório dentro do GitHub.",
            "acao": "Manter apenas topics realmente relacionados ao conteúdo." if topics else "Adicionar topics de linguagem, domínio e finalidade do projeto.",
        },
        "ci": {
            "passou": checks["ci"],
            "observado": f"Workflows encontrados: {', '.join(workflows)}." if workflows else "Nenhum workflow em .github/workflows foi encontrado.",
            "impacto": "CI ajuda a detectar regressões automaticamente a cada mudança.",
            "acao": "Na próxima etapa, verificar também o status real da execução mais recente." if workflows else "Adicionar workflow de CI para testes, sintaxe ou build.",
        },
        "testes": {
            "passou": checks["testes"],
            "observado": f"Arquivos de teste encontrados: {', '.join(testes[:8])}." if testes else "Nenhum arquivo de teste reconhecido foi encontrado.",
            "impacto": "Testes automatizados ajudam a provar comportamentos importantes e evitam regressões.",
            "acao": "Manter testes alinhados às regras de negócio mais importantes." if testes else "Adicionar testes automatizados para os principais comportamentos.",
        },
        "dependencias": {
            "passou": checks["dependencias"],
            "observado": f"Arquivos de dependências encontrados: {', '.join(dependencias)}." if dependencias else "Nenhum arquivo padrão de dependências foi encontrado.",
            "impacto": "Dependências declaradas tornam o projeto reproduzível em outras máquinas e ambientes de CI.",
            "acao": "Manter versões e dependências compatíveis com o projeto." if dependencias else "Registrar dependências em arquivo padrão da tecnologia usada.",
        },
    }


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
        "detalhes_checks": gerar_detalhes_checks(metadata, caminhos, checks),
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
