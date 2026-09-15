from projetos.github_student_dashboard.engine import analisar_repositorio_remoto
from projetos.github_student_dashboard.readme_quality import analisar_readme_remoto


def _resumir_repo(relatorio, readme):
    ci = relatorio.get("evidencias", {}).get("ci_status") or {}
    return {
        "repositorio": relatorio.get("repositorio"),
        "url": relatorio.get("url"),
        "score": relatorio.get("score", 0),
        "checks": relatorio.get("checks", {}),
        "ci_real": {
            "estado": ci.get("estado"),
            "workflow": ci.get("workflow"),
            "url": ci.get("url"),
        },
        "readme": {
            "tipo": readme.get("tipo_detectado"),
            "cobertura_percentual": readme.get("cobertura_documental", {}).get("percentual", 0),
            "criterios": readme.get("criterios", {}),
        },
    }


def comparar_relatorios(relatorio_a, readme_a, relatorio_b, readme_b):
    a = _resumir_repo(relatorio_a, readme_a)
    b = _resumir_repo(relatorio_b, readme_b)

    nomes_checks = sorted(set(a["checks"]) | set(b["checks"]))
    checks = []
    vantagens_a = []
    vantagens_b = []

    for nome in nomes_checks:
        valor_a = bool(a["checks"].get(nome))
        valor_b = bool(b["checks"].get(nome))
        checks.append({"nome": nome, "a": valor_a, "b": valor_b})
        if valor_a and not valor_b:
            vantagens_a.append(nome)
        elif valor_b and not valor_a:
            vantagens_b.append(nome)

    cobertura_a = a["readme"]["cobertura_percentual"]
    cobertura_b = b["readme"]["cobertura_percentual"]

    diferencas = {
        "score": a["score"] - b["score"],
        "readme_cobertura": round(cobertura_a - cobertura_b, 1),
        "checks_exclusivos_a": vantagens_a,
        "checks_exclusivos_b": vantagens_b,
    }

    return {
        "repositorio_a": a,
        "repositorio_b": b,
        "comparacao_checks": checks,
        "diferencas_objetivas": diferencas,
        "observacao": (
            "A comparação mostra diferenças verificáveis entre os repositórios. "
            "Ela não declara um vencedor geral nem substitui contexto sobre finalidade, maturidade ou público do projeto."
        ),
    }


def comparar_repositorios_remotos(
    referencia_a,
    referencia_b,
    analisador_repo=analisar_repositorio_remoto,
    analisador_readme=analisar_readme_remoto,
):
    if referencia_a.strip().lower() == referencia_b.strip().lower():
        raise ValueError("Informe dois repositórios diferentes para comparar.")

    relatorio_a = analisador_repo(referencia_a)
    relatorio_b = analisador_repo(referencia_b)
    readme_a = analisador_readme(referencia_a)
    readme_b = analisador_readme(referencia_b)

    return comparar_relatorios(relatorio_a, readme_a, relatorio_b, readme_b)
