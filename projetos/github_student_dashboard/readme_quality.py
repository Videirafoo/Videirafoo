import base64
import re

from projetos.github_student_dashboard.engine import normalizar_referencia
from projetos.github_student_dashboard.github_client import GitHubApiError, GitHubClient


def _tem_heading(texto, termos):
    padrao = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE | re.IGNORECASE)
    headings = [match.group(1).strip().lower() for match in padrao.finditer(texto)]
    return any(any(termo in heading for termo in termos) for heading in headings)


def _contar_headings(texto):
    return len(re.findall(r"^#{1,6}\s+.+$", texto, re.MULTILINE))


def _contar_blocos_codigo(texto):
    return len(re.findall(r"```", texto)) // 2


def _contar_links(texto):
    markdown = len(re.findall(r"\[[^\]]+\]\(([^)]+)\)", texto))
    html = len(re.findall(r"href=[\"'][^\"']+[\"']", texto, re.IGNORECASE))
    return markdown + html


def _criterio(passou, observado, impacto, acao):
    return {
        "passou": bool(passou),
        "observado": observado,
        "impacto": impacto,
        "acao": acao,
    }


def _criterios_perfil(texto):
    headings = _contar_headings(texto)
    links = _contar_links(texto)
    tamanho = len(texto.strip())

    return {
        "titulo": _criterio(
            bool(re.search(r"^#\s+.+$", texto, re.MULTILINE)),
            "Título principal encontrado." if re.search(r"^#\s+.+$", texto, re.MULTILINE) else "Nenhum título H1 foi encontrado.",
            "Um título principal deixa a identidade do perfil clara logo no início.",
            "Manter um único H1 claro com nome ou posicionamento profissional.",
        ),
        "sobre": _criterio(
            _tem_heading(texto, ["sobre", "about"]),
            "Seção de apresentação pessoal encontrada." if _tem_heading(texto, ["sobre", "about"]) else "Seção Sobre/About não encontrada.",
            "A apresentação ajuda visitantes a entenderem rapidamente quem é a pessoa e o que ela está construindo.",
            "Adicionar uma seção curta de apresentação, foco e objetivos.",
        ),
        "stack": _criterio(
            _tem_heading(texto, ["stack", "tecnolog", "skills", "habilidades"]),
            "Seção de stack/habilidades encontrada." if _tem_heading(texto, ["stack", "tecnolog", "skills", "habilidades"]) else "Seção de stack/habilidades não encontrada.",
            "Tecnologias bem organizadas facilitam leitura por estudantes, recrutadores e colaboradores.",
            "Organizar as principais tecnologias por área ou objetivo de estudo.",
        ),
        "projetos": _criterio(
            _tem_heading(texto, ["projet", "project"]),
            "Seção de projetos encontrada." if _tem_heading(texto, ["projet", "project"]) else "Seção de projetos não encontrada.",
            "Projetos demonstram aplicação prática do aprendizado.",
            "Destacar poucos projetos com objetivo, tecnologia e link direto.",
        ),
        "aprendizado": _criterio(
            _tem_heading(texto, ["estud", "aprend", "learning", "study", "trilha"]),
            "Seção de aprendizado/trilha encontrada." if _tem_heading(texto, ["estud", "aprend", "learning", "study", "trilha"]) else "Seção de aprendizado/trilha não encontrada.",
            "Mostrar o que está sendo estudado torna a evolução transparente e ajuda outros iniciantes a acompanhar a trajetória.",
            "Registrar estudos atuais ou uma trilha de evolução de forma objetiva.",
        ),
        "navegacao": _criterio(
            links >= 3,
            f"{links} link(s) detectado(s) no README.",
            "Links úteis reduzem atrito para quem quer abrir projetos, guias e conteúdos relacionados.",
            "Manter links diretos para projetos, guias e materiais principais.",
        ),
        "estrutura": _criterio(
            headings >= 4 and tamanho >= 600,
            f"{headings} heading(s) e {tamanho} caracteres de conteúdo.",
            "Estrutura suficiente evita um perfil vazio, mas também deve continuar fácil de percorrer.",
            "Usar seções curtas e hierarquia consistente, evitando blocos excessivamente longos.",
        ),
    }


def _criterios_projeto(texto):
    headings = _contar_headings(texto)
    blocos = _contar_blocos_codigo(texto)
    tamanho = len(texto.strip())

    return {
        "titulo": _criterio(
            bool(re.search(r"^#\s+.+$", texto, re.MULTILINE)),
            "Título principal encontrado." if re.search(r"^#\s+.+$", texto, re.MULTILINE) else "Nenhum título H1 foi encontrado.",
            "O título identifica rapidamente o projeto.",
            "Adicionar um único H1 claro com o nome do projeto.",
        ),
        "objetivo": _criterio(
            _tem_heading(texto, ["objetivo", "sobre", "overview", "introdu", "o que"]),
            "Seção de objetivo/apresentação encontrada." if _tem_heading(texto, ["objetivo", "sobre", "overview", "introdu", "o que"]) else "Não foi encontrada seção clara de objetivo/apresentação.",
            "Explicar o problema e o propósito evita que o visitante precise inferir o que o projeto faz.",
            "Adicionar uma explicação curta do problema, objetivo e público do projeto.",
        ),
        "instalacao": _criterio(
            _tem_heading(texto, ["instala", "requisit", "setup", "pré-requis", "pre-requis"]),
            "Seção de instalação/requisitos encontrada." if _tem_heading(texto, ["instala", "requisit", "setup", "pré-requis", "pre-requis"]) else "Seção de instalação/requisitos não encontrada.",
            "Requisitos explícitos ajudam outra pessoa a reproduzir o projeto.",
            "Documentar versões, dependências e passos mínimos de instalação.",
        ),
        "execucao": _criterio(
            _tem_heading(texto, ["execut", "como usar", "uso", "run", "quick start", "início rápido"]),
            "Seção de execução/uso encontrada." if _tem_heading(texto, ["execut", "como usar", "uso", "run", "quick start", "início rápido"]) else "Seção de execução/uso não encontrada.",
            "O visitante deve conseguir executar o projeto sem descobrir comandos por tentativa e erro.",
            "Adicionar comandos de execução e um primeiro exemplo funcional.",
        ),
        "comandos": _criterio(
            blocos >= 1,
            f"{blocos} bloco(s) de código/comando detectado(s).",
            "Exemplos copiáveis tornam a documentação prática.",
            "Adicionar exemplos de terminal ou código que possam ser reproduzidos.",
        ),
        "testes": _criterio(
            _tem_heading(texto, ["teste", "test"]),
            "Seção de testes encontrada." if _tem_heading(texto, ["teste", "test"]) else "Seção de testes não encontrada.",
            "Explicar como validar o projeto aumenta confiança e ajuda contribuidores.",
            "Documentar como executar os testes ou validações principais.",
        ),
        "contribuicao": _criterio(
            _tem_heading(texto, ["contrib", "contributing"]),
            "Orientação de contribuição encontrada." if _tem_heading(texto, ["contrib", "contributing"]) else "Orientação de contribuição não encontrada no README.",
            "Projetos open source ficam mais acessíveis quando a forma de contribuir é explícita.",
            "Adicionar uma seção curta de contribuição ou apontar para CONTRIBUTING.md.",
        ),
        "licenca": _criterio(
            _tem_heading(texto, ["licen", "license"]) or "LICENSE" in texto,
            "Referência à licença encontrada." if (_tem_heading(texto, ["licen", "license"]) or "LICENSE" in texto) else "README não menciona licença.",
            "A referência à licença ajuda usuários a entenderem as regras de reutilização.",
            "Indicar a licença no README quando o projeto for público e reutilizável.",
        ),
        "estrutura": _criterio(
            headings >= 3 and tamanho >= 350,
            f"{headings} heading(s) e {tamanho} caracteres de conteúdo.",
            "Uma estrutura mínima torna o README escaneável e útil para quem chega pela primeira vez.",
            "Organizar o README em seções curtas e em ordem de uso.",
        ),
    }


def analisar_readme_texto(texto, owner, repo):
    texto = texto or ""
    tipo = "perfil_github" if owner.lower() == repo.lower() else "projeto"
    criterios = _criterios_perfil(texto) if tipo == "perfil_github" else _criterios_projeto(texto)
    aprovados = sum(item["passou"] for item in criterios.values())
    total = len(criterios)

    return {
        "tipo_detectado": tipo,
        "criterios": criterios,
        "cobertura_documental": {
            "aprovados": aprovados,
            "total": total,
            "percentual": round((aprovados / total) * 100, 1) if total else 0,
        },
        "metricas": {
            "caracteres": len(texto.strip()),
            "headings": _contar_headings(texto),
            "blocos_codigo": _contar_blocos_codigo(texto),
            "links": _contar_links(texto),
        },
        "observacao": "A cobertura mede presença de elementos documentais verificáveis; não é uma nota subjetiva de qualidade textual.",
    }


def analisar_readme_remoto(referencia, client=None):
    owner, repo = normalizar_referencia(referencia)
    client = client or GitHubClient()

    try:
        resposta = client.get_json(f"/repos/{owner}/{repo}/readme")
    except GitHubApiError as erro:
        if erro.status == 404:
            raise ValueError("README não encontrado no repositório.") from erro
        raise

    conteudo = resposta.get("content") or ""
    encoding = (resposta.get("encoding") or "").lower()
    if encoding != "base64":
        raise ValueError("Formato de README não suportado pela análise.")

    try:
        texto = base64.b64decode(conteudo).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as erro:
        raise ValueError("Não foi possível decodificar o README em UTF-8.") from erro

    relatorio = analisar_readme_texto(texto, owner, repo)
    relatorio["repositorio"] = f"{owner}/{repo}"
    relatorio["arquivo"] = resposta.get("path") or "README.md"
    return relatorio
