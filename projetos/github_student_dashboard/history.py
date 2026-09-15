from projetos.github_student_dashboard.engine import (
    arquivos_de_dependencias,
    caminhos_da_arvore,
    detectar_ci,
    detectar_gitignore,
    detectar_readme,
    detectar_testes,
    normalizar_referencia,
)
from projetos.github_student_dashboard.github_client import GitHubClient


CHECKS_VERSIONADOS = ("readme", "gitignore", "ci", "testes", "dependencias")


def analisar_estado_versionado(arvore):
    caminhos = caminhos_da_arvore(arvore)
    checks = {
        "readme": detectar_readme(caminhos),
        "gitignore": detectar_gitignore(caminhos),
        "ci": detectar_ci(caminhos),
        "testes": detectar_testes(caminhos),
        "dependencias": bool(arquivos_de_dependencias(caminhos)),
    }
    aprovados = sum(checks.values())
    total = len(checks)

    return {
        "checks": checks,
        "cobertura_versionada": {
            "aprovados": aprovados,
            "total": total,
            "percentual": round((aprovados / total) * 100, 1) if total else 0,
        },
        "arquivos_encontrados": len(caminhos),
    }


def _dados_commit(item):
    commit = item.get("commit") or {}
    autor = commit.get("author") or {}
    committer = commit.get("committer") or {}
    mensagem = (commit.get("message") or "").splitlines()[0].strip()

    return {
        "sha": item.get("sha"),
        "sha_curto": (item.get("sha") or "")[:7],
        "mensagem": mensagem,
        "autor": autor.get("name") or committer.get("name") or "Desconhecido",
        "data": autor.get("date") or committer.get("date"),
        "url": item.get("html_url"),
    }


def construir_evolucao(snapshots):
    cronologico = list(reversed(snapshots))
    anterior = None

    for snapshot in cronologico:
        checks = snapshot["estado"]["checks"]
        if anterior is None:
            snapshot["mudancas"] = {
                "adicionados": [],
                "removidos": [],
                "observacao": "Primeiro ponto da janela analisada.",
            }
        else:
            adicionados = [
                nome for nome in CHECKS_VERSIONADOS
                if checks.get(nome) and not anterior.get(nome)
            ]
            removidos = [
                nome for nome in CHECKS_VERSIONADOS
                if anterior.get(nome) and not checks.get(nome)
            ]
            snapshot["mudancas"] = {
                "adicionados": adicionados,
                "removidos": removidos,
                "observacao": "Comparação com o commit anterior dentro da janela analisada.",
            }
        anterior = checks

    return cronologico


def analisar_historico_remoto(referencia, client=None, limite=5):
    owner, repo = normalizar_referencia(referencia)
    client = client or GitHubClient()
    limite = max(2, min(int(limite), 10))

    commits = client.buscar_commits(owner, repo, limite=limite)
    snapshots = []

    for item in commits:
        sha = item.get("sha")
        if not sha:
            continue
        arvore = client.buscar_arvore(owner, repo, sha)
        snapshots.append({
            "commit": _dados_commit(item),
            "estado": analisar_estado_versionado(arvore),
        })

    evolucao = construir_evolucao(snapshots)

    return {
        "repositorio": f"{owner}/{repo}",
        "commits_analisados": len(evolucao),
        "checks_versionados": list(CHECKS_VERSIONADOS),
        "evolucao": evolucao,
        "observacao": (
            "O histórico reconstrói apenas sinais presentes nos arquivos versionados em cada commit. "
            "Descrição, topics e outros metadados atuais do GitHub não são retroativamente inferidos."
        ),
    }
