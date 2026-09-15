"""Matriz de competências baseada em evidências públicas verificáveis.

A matriz não tenta adivinhar domínio pessoal. Ela mede apenas se existem
artefatos públicos que sustentam determinada competência: código, testes,
CI, deploy, documentação e contribuição open source.
"""

from datetime import datetime, timezone
import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from projetos.github_student_dashboard.github_client import GitHubApiError, GitHubClient


OWNER = "Videirafoo"
PROFILE_REPO = "Videirafoo"
PRODUCTION_HEALTH_URL = "https://github-student-dashboard-videirafoo.onrender.com/healthz"
CACHE_SECONDS = 600

_CACHE = {"expires_at": 0.0, "value": None}


COMPETENCIAS = [
    {
        "id": "fundamentos-python",
        "nivel": 1,
        "titulo": "Fundamentos em Python",
        "descricao": "Entrada, saída, condições, laços, funções e programas pequenos explicáveis.",
        "proximo_passo": "Continuar resolvendo exercícios sem copiar respostas e explicar o fluxo antes de executar.",
    },
    {
        "id": "algoritmos-busca",
        "nivel": 2,
        "titulo": "Algoritmos e busca",
        "descricao": "Busca sequencial/binária, organização de dados e raciocínio passo a passo.",
        "proximo_passo": "Comparar custo e comportamento dos algoritmos com entradas maiores e casos-limite.",
    },
    {
        "id": "recursividade",
        "nivel": 2,
        "titulo": "Recursividade",
        "descricao": "Caso-base, chamadas recursivas e rastreamento de execução.",
        "proximo_passo": "Adicionar testes de borda e comparar solução recursiva com uma versão iterativa.",
    },
    {
        "id": "mini-sistemas",
        "nivel": 3,
        "titulo": "Mini sistemas e regras de negócio",
        "descricao": "CRUD, validação, persistência, estado e regras executáveis em projetos pequenos.",
        "proximo_passo": "Evoluir um mini sistema com uma regra nova, teste correspondente e documentação da decisão.",
    },
    {
        "id": "backend-api",
        "nivel": 4,
        "titulo": "Backend e APIs HTTP",
        "descricao": "Rotas Flask, endpoints JSON, métodos HTTP, validação e códigos de resposta.",
        "proximo_passo": "Adicionar persistência real e autenticação em um projeto separado quando a base HTTP estiver consolidada.",
    },
    {
        "id": "qualidade-ci",
        "nivel": 5,
        "titulo": "Testes, cobertura e CI",
        "descricao": "Testes automatizados, cobertura, regressão e execução verificável no GitHub Actions.",
        "proximo_passo": "Aumentar cobertura útil das branches ainda descobertas sem perseguir 100% apenas por aparência.",
    },
    {
        "id": "deploy-operacao",
        "nivel": 5,
        "titulo": "Deploy e operação",
        "descricao": "Aplicação pública, healthcheck e documentação reproduzível de execução.",
        "proximo_passo": "Adicionar observabilidade e sinais operacionais somente quando houver uma necessidade real do produto.",
    },
    {
        "id": "documentacao",
        "nivel": 5,
        "titulo": "Documentação técnica",
        "descricao": "README, guia de estudos, padrão de ensino, evidências de qualidade e changelog.",
        "proximo_passo": "Manter documentação alinhada ao comportamento real e remover números que ficarem desatualizados.",
    },
    {
        "id": "open-source",
        "nivel": 5,
        "titulo": "Contribuição open source",
        "descricao": "Branch focada, commit pequeno, Pull Request público e revisão externa.",
        "proximo_passo": "Aguardar review/merge do PR externo e registrar aceitação somente se o merge público acontecer.",
    },
    {
        "id": "ia-aplicada",
        "nivel": 6,
        "titulo": "IA aplicada com evidência",
        "descricao": "Explicação por IA separada de checks determinísticos, com fallback e testes.",
        "proximo_passo": "Adicionar avaliações de qualidade da explicação antes de aumentar autonomia ou ferramentas.",
    },
]


def _agora_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _paths_da_arvore(payload):
    return {
        item.get("path", "")
        for item in payload.get("tree", [])
        if isinstance(item, dict) and item.get("path")
    }


def _tem_python(paths):
    return any(path.endswith(".py") for path in paths)


def _tem_prefixo(paths, prefixo):
    return any(path == prefixo or path.startswith(f"{prefixo}/") for path in paths)


def _evidencia(titulo, estado, detalhe, url):
    return {
        "titulo": titulo,
        "estado": estado,
        "detalhe": detalhe,
        "url": url,
    }


def _estado_competencia(evidencias):
    estados = [item["estado"] for item in evidencias]
    if estados and all(estado == "verificada" for estado in estados):
        return "forte"
    if any(estado in {"verificada", "parcial"} for estado in estados):
        return "parcial"
    if any(estado == "indisponivel" for estado in estados):
        return "indisponivel"
    return "sem_evidencia"


def _healthcheck_publico(timeout=4):
    requisicao = Request(
        PRODUCTION_HEALTH_URL,
        headers={"User-Agent": "Videirafoo-Competency-Matrix"},
    )
    try:
        with urlopen(requisicao, timeout=timeout) as resposta:
            if resposta.status != 200:
                return False, f"Healthcheck respondeu HTTP {resposta.status}."
            payload = json.loads(resposta.read().decode("utf-8"))
            if payload.get("status") == "ok":
                return True, "Healthcheck público respondeu status=ok."
            return False, "Healthcheck respondeu, mas sem status=ok."
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as erro:
        return False, f"Healthcheck indisponível nesta consulta: {erro.__class__.__name__}."


def _arvore_segura(client, repo):
    try:
        return _paths_da_arvore(client.buscar_arvore(OWNER, repo, "main")), None
    except GitHubApiError as erro:
        return set(), str(erro)


def _obter_arvores(client):
    repos = [
        PROFILE_REPO,
        "Lista-01-segundo-periodo",
        "Lista-03-segundo-periodo",
        "lista-04-segundo-periodo",
    ]
    return {repo: _arvore_segura(client, repo) for repo in repos}


def _avaliar_fundamentos(arvores):
    paths, erro = arvores["Lista-01-segundo-periodo"]
    if erro:
        return [_evidencia("Lista acadêmica com Python", "indisponivel", erro, f"https://github.com/{OWNER}/Lista-01-segundo-periodo")]
    ok = _tem_python(paths) and "README.md" in paths
    return [_evidencia(
        "Lista acadêmica com Python e README",
        "verificada" if ok else "ausente",
        "Repositório contém código Python e instruções de leitura." if ok else "Código Python ou README não foi localizado na árvore pública.",
        f"https://github.com/{OWNER}/Lista-01-segundo-periodo",
    )]


def _avaliar_algoritmos(arvores):
    paths, erro = arvores["Lista-03-segundo-periodo"]
    if erro:
        return [_evidencia("Lista de buscas", "indisponivel", erro, f"https://github.com/{OWNER}/Lista-03-segundo-periodo")]
    arquivos_python = sum(1 for path in paths if path.endswith(".py"))
    ok = arquivos_python >= 2
    return [_evidencia(
        "Exercícios versionados de busca",
        "verificada" if ok else "ausente",
        f"{arquivos_python} arquivos Python detectados na árvore pública." if ok else "Pouca ou nenhuma evidência Python foi detectada.",
        f"https://github.com/{OWNER}/Lista-03-segundo-periodo",
    )]


def _avaliar_recursividade(arvores):
    paths, erro = arvores["lista-04-segundo-periodo"]
    if erro:
        return [_evidencia("Lista de recursividade", "indisponivel", erro, f"https://github.com/{OWNER}/lista-04-segundo-periodo")]
    ok = _tem_python(paths)
    return [_evidencia(
        "Código Python de recursividade",
        "verificada" if ok else "ausente",
        "A árvore pública contém exercícios Python versionados." if ok else "Nenhum arquivo Python foi localizado.",
        f"https://github.com/{OWNER}/lista-04-segundo-periodo",
    )]


def _avaliar_mini_sistemas(arvores):
    paths, erro = arvores[PROFILE_REPO]
    url = f"https://github.com/{OWNER}/{PROFILE_REPO}/tree/main/conteudos/mini_sistemas"
    if erro:
        return [_evidencia("Coleção de mini sistemas", "indisponivel", erro, url)]
    prefixos = [
        "agenda_contatos",
        "lista_tarefas",
        "cadastro_alunos",
        "controle_estoque",
        "sistema_biblioteca",
        "caixa_mercado",
        "controle_financeiro",
        "gerenciador_habitos",
        "api_tarefas",
        "projeto_integrado",
    ]
    presentes = sum(
        1
        for nome in prefixos
        if _tem_prefixo(paths, f"conteudos/mini_sistemas/{nome}")
    )
    testes = sum(
        1
        for path in paths
        if path.startswith("conteudos/mini_sistemas/") and path.endswith(".py") and "/test_" in path
    )
    return [
        _evidencia(
            "10 mini sistemas versionados",
            "verificada" if presentes == 10 else "parcial" if presentes else "ausente",
            f"{presentes} de 10 diretórios esperados encontrados.",
            url,
        ),
        _evidencia(
            "Testes nos mini sistemas",
            "verificada" if testes >= 8 else "parcial" if testes else "ausente",
            f"{testes} arquivos de teste detectados dentro da coleção.",
            url,
        ),
    ]


def _avaliar_backend(arvores):
    paths, erro = arvores[PROFILE_REPO]
    base = f"https://github.com/{OWNER}/{PROFILE_REPO}/tree/main"
    if erro:
        return [_evidencia("Backend Flask", "indisponivel", erro, base)]
    esperados = [
        "projetos/github_student_dashboard/web.py",
        "projetos/github_student_dashboard/lab_web.py",
        "conteudos/mini_sistemas/api_tarefas/app.py",
    ]
    presentes = sum(path in paths for path in esperados)
    testes_http = any(
        path.startswith("projetos/github_student_dashboard/test_") and path.endswith(".py")
        for path in paths
    )
    return [
        _evidencia(
            "Flask + API versionados",
            "verificada" if presentes == len(esperados) else "parcial" if presentes else "ausente",
            f"{presentes} de {len(esperados)} componentes esperados encontrados.",
            f"{base}/projetos/github_student_dashboard",
        ),
        _evidencia(
            "Testes do backend",
            "verificada" if testes_http else "ausente",
            "Arquivos de teste do Dashboard detectados." if testes_http else "Nenhum teste do Dashboard foi detectado.",
            f"{base}/projetos/github_student_dashboard",
        ),
    ]


def _avaliar_qualidade(client, arvores):
    paths, erro = arvores[PROFILE_REPO]
    evidencias = []
    url = f"https://github.com/{OWNER}/{PROFILE_REPO}/actions"
    if erro:
        evidencias.append(_evidencia("Workflow e configuração de cobertura", "indisponivel", erro, url))
    else:
        arquivos_ok = (
            ".github/workflows/student-dashboard.yml" in paths
            and "projetos/github_student_dashboard/.coveragerc" in paths
        )
        evidencias.append(_evidencia(
            "Workflow + gate de cobertura versionados",
            "verificada" if arquivos_ok else "ausente",
            "Workflow e configuração de cobertura encontrados." if arquivos_ok else "Workflow ou configuração de cobertura não encontrados.",
            url,
        ))
    try:
        runs = client.buscar_workflow_runs(OWNER, PROFILE_REPO, branch="main", limite=20).get("workflow_runs", [])
        dashboard_run = next((run for run in runs if run.get("name") == "GitHub Student Dashboard CI"), None)
        if dashboard_run is None:
            evidencias.append(_evidencia("Última CI do Dashboard", "ausente", "Nenhuma execução do workflow foi localizada entre as mais recentes.", url))
        else:
            status = dashboard_run.get("status")
            conclusion = dashboard_run.get("conclusion")
            html_url = dashboard_run.get("html_url") or url
            if status == "completed" and conclusion == "success":
                estado = "verificada"
                detalhe = "Última execução localizada terminou com success."
            elif status in {"queued", "in_progress", "waiting", "requested"}:
                estado = "parcial"
                detalhe = f"Execução atual ainda está em andamento: {status}."
            else:
                estado = "parcial"
                detalhe = f"Última execução localizada: status={status}, conclusion={conclusion}."
            evidencias.append(_evidencia("Última CI do Dashboard", estado, detalhe, html_url))
    except GitHubApiError as erro_api:
        evidencias.append(_evidencia("Última CI do Dashboard", "indisponivel", str(erro_api), url))
    return evidencias


def _avaliar_deploy(health_checker):
    ok, detalhe = health_checker()
    return [_evidencia(
        "Healthcheck público",
        "verificada" if ok else "parcial",
        detalhe,
        PRODUCTION_HEALTH_URL,
    )]


def _avaliar_documentacao(arvores):
    paths, erro = arvores[PROFILE_REPO]
    url = f"https://github.com/{OWNER}/{PROFILE_REPO}"
    if erro:
        return [_evidencia("Documentação canônica", "indisponivel", erro, url)]
    esperados = [
        "README.md",
        "GUIA_DE_ESTUDOS.md",
        "PADRAO_DE_ENSINO.md",
        "QUALITY.md",
        "projetos/github_student_dashboard/CHANGELOG.md",
    ]
    presentes = [path for path in esperados if path in paths]
    return [_evidencia(
        "Documentação canônica versionada",
        "verificada" if len(presentes) == len(esperados) else "parcial" if presentes else "ausente",
        f"{len(presentes)} de {len(esperados)} documentos esperados encontrados.",
        url,
    )]


def _avaliar_open_source(client):
    url = "https://github.com/fork-commit-merge/fork-commit-merge/pull/8150"
    try:
        pr = client.buscar_pull_request("fork-commit-merge", "fork-commit-merge", 8150)
    except (GitHubApiError, ValueError) as erro:
        return [_evidencia("PR externo #8150", "indisponivel", str(erro), url)]

    if pr.get("merged") or pr.get("merged_at"):
        estado = "verificada"
        detalhe = "Pull Request externo foi aceito por merge público."
    elif pr.get("state") == "open":
        estado = "parcial"
        detalhe = "Pull Request externo está aberto; contribuição enviada, ainda não aceita por merge."
    else:
        estado = "parcial"
        detalhe = "Pull Request externo foi fechado sem evidência de merge."

    return [_evidencia("PR externo #8150", estado, detalhe, pr.get("html_url") or url)]


def _avaliar_ia(arvores):
    paths, erro = arvores[PROFILE_REPO]
    base = f"https://github.com/{OWNER}/{PROFILE_REPO}/tree/main/projetos/github_student_dashboard"
    if erro:
        return [_evidencia("Camada de IA explicativa", "indisponivel", erro, base)]
    esperados = [
        "projetos/github_student_dashboard/ai_explainer.py",
        "projetos/github_student_dashboard/test_ai_explainer.py",
        "projetos/github_student_dashboard/test_ai_provider.py",
        "projetos/github_student_dashboard/engine.py",
    ]
    presentes = sum(path in paths for path in esperados)
    return [_evidencia(
        "IA separada do motor determinístico",
        "verificada" if presentes == len(esperados) else "parcial" if presentes else "ausente",
        f"{presentes} de {len(esperados)} componentes de implementação/teste encontrados.",
        base,
    )]


def _montar_competencia(definicao, evidencias):
    return {
        **definicao,
        "estado_evidencia": _estado_competencia(evidencias),
        "evidencias": evidencias,
        "verificadas": sum(item["estado"] == "verificada" for item in evidencias),
        "total_evidencias": len(evidencias),
    }


def gerar_matriz_competencias(client=None, health_checker=None, usar_cache=True):
    """Gera a matriz a partir de GitHub público + healthcheck fixo.

    O cache reduz chamadas à API pública. Quando um cliente é injetado em teste,
    o cache global não é utilizado para evitar acoplamento entre cenários.
    """
    agora = time.monotonic()
    cliente_injetado = client is not None
    if usar_cache and not cliente_injetado and _CACHE["value"] is not None and agora < _CACHE["expires_at"]:
        return _CACHE["value"]

    client = client or GitHubClient()
    health_checker = health_checker or _healthcheck_publico
    arvores = _obter_arvores(client)

    avaliadores = {
        "fundamentos-python": lambda: _avaliar_fundamentos(arvores),
        "algoritmos-busca": lambda: _avaliar_algoritmos(arvores),
        "recursividade": lambda: _avaliar_recursividade(arvores),
        "mini-sistemas": lambda: _avaliar_mini_sistemas(arvores),
        "backend-api": lambda: _avaliar_backend(arvores),
        "qualidade-ci": lambda: _avaliar_qualidade(client, arvores),
        "deploy-operacao": lambda: _avaliar_deploy(health_checker),
        "documentacao": lambda: _avaliar_documentacao(arvores),
        "open-source": lambda: _avaliar_open_source(client),
        "ia-aplicada": lambda: _avaliar_ia(arvores),
    }

    competencias = [
        _montar_competencia(definicao, avaliadores[definicao["id"]]())
        for definicao in COMPETENCIAS
    ]
    contagem = {
        "forte": sum(item["estado_evidencia"] == "forte" for item in competencias),
        "parcial": sum(item["estado_evidencia"] == "parcial" for item in competencias),
        "sem_evidencia": sum(item["estado_evidencia"] == "sem_evidencia" for item in competencias),
        "indisponivel": sum(item["estado_evidencia"] == "indisponivel" for item in competencias),
    }
    total_evidencias = sum(item["total_evidencias"] for item in competencias)
    verificadas = sum(item["verificadas"] for item in competencias)

    resultado = {
        "gerado_em": _agora_iso(),
        "cache_segundos": CACHE_SECONDS,
        "metodologia": "mede evidências públicas; não certifica domínio pessoal",
        "competencias": competencias,
        "resumo": {
            "total_competencias": len(competencias),
            "total_evidencias": total_evidencias,
            "evidencias_verificadas": verificadas,
            **contagem,
        },
    }

    if not cliente_injetado:
        _CACHE["value"] = resultado
        _CACHE["expires_at"] = agora + CACHE_SECONDS
    return resultado
