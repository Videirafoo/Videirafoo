from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from conteudos.mini_sistemas.agenda_contatos.main import (
    adicionar_contato as agenda_adicionar_contato,
    buscar_indice as agenda_buscar_indice,
    criar_contato as agenda_criar_contato,
)
from conteudos.mini_sistemas.api_tarefas.app import (
    atualizar_tarefa as api_atualizar_tarefa,
    criar_tarefa as api_criar_tarefa,
    excluir_tarefa as api_excluir_tarefa,
    filtrar_tarefas as api_filtrar_tarefas,
)
from conteudos.mini_sistemas.lista_tarefas.app import (
    concluir_tarefa as lista_concluir_tarefa,
    criar_tarefa as lista_criar_tarefa,
    excluir_tarefa as lista_excluir_tarefa,
)
from conteudos.mini_sistemas.projeto_integrado.app import analisar_repositorio


MAX_ITENS_LAB = 50
MAX_TITULO = 120
CHECKS_PROJETO = {"readme", "gitignore", "licenca", "ci", "testes", "dependencias"}


def _normalizar_agenda(valor):
    if valor is None:
        return []
    if not isinstance(valor, list):
        raise ValueError("O estado da agenda precisa ser uma lista.")
    if len(valor) > MAX_ITENS_LAB:
        raise ValueError(f"O laboratório aceita no máximo {MAX_ITENS_LAB} contatos por vez.")

    contatos = []
    base_original = []
    for item in valor:
        if not isinstance(item, dict):
            raise ValueError("Cada contato precisa ser um objeto JSON.")
        contato = agenda_criar_contato(
            str(item.get("nome", "")),
            str(item.get("telefone", "")),
            str(item.get("email", "")),
        )
        agenda_adicionar_contato(base_original, contato)
        contatos.append(
            {
                "id": str(item.get("id") or uuid4()),
                **contato,
            }
        )
    return contatos


def criar_contato_lab(estado, nome, telefone, email=""):
    contatos = _normalizar_agenda(estado)
    base_original = [
        {"nome": item["nome"], "telefone": item["telefone"], "email": item.get("email", "")}
        for item in contatos
    ]
    contato = agenda_criar_contato(str(nome), str(telefone), str(email))
    agenda_adicionar_contato(base_original, contato)
    criado = {"id": str(uuid4()), **contato}
    contatos.append(criado)
    return {"contatos": contatos, "resultado": deepcopy(criado)}


def excluir_contato_lab(estado, contato_id):
    contatos = _normalizar_agenda(estado)
    alvo = next((item for item in contatos if item["id"] == str(contato_id)), None)
    if alvo is None:
        return None

    base_original = [
        {"nome": item["nome"], "telefone": item["telefone"], "email": item.get("email", "")}
        for item in contatos
    ]
    indice = agenda_buscar_indice(base_original, alvo["nome"])
    if indice == -1:
        return None

    removido = contatos.pop(indice)
    return {"contatos": contatos, "resultado": deepcopy(removido)}


def _normalizar_lista_tarefas(valor):
    if valor is None:
        return []
    if not isinstance(valor, list):
        raise ValueError("O estado da lista de tarefas precisa ser uma lista.")
    if len(valor) > MAX_ITENS_LAB:
        raise ValueError(f"O laboratório aceita no máximo {MAX_ITENS_LAB} tarefas por vez.")

    tarefas = []
    for item in valor:
        if not isinstance(item, dict):
            raise ValueError("Cada tarefa precisa ser um objeto JSON.")
        titulo = str(item.get("titulo", item.get("texto", "")))
        prioridade = str(item.get("prioridade", "media"))
        concluida = item.get("concluida", False)
        if not isinstance(concluida, bool):
            raise ValueError("O campo concluida precisa ser booleano.")
        criada = lista_criar_tarefa(tarefas, titulo, prioridade)
        criada["concluida"] = concluida
    return tarefas


def criar_lista_tarefa_lab(estado, titulo, prioridade="media"):
    tarefas = _normalizar_lista_tarefas(estado)
    if len(tarefas) >= MAX_ITENS_LAB:
        raise ValueError(f"O laboratório aceita no máximo {MAX_ITENS_LAB} tarefas por vez.")
    criada = lista_criar_tarefa(tarefas, str(titulo), str(prioridade))
    return {"tarefas": tarefas, "resultado": deepcopy(criada)}


def concluir_lista_tarefa_lab(estado, tarefa_id, concluida=True):
    tarefas = _normalizar_lista_tarefas(estado)
    if not isinstance(tarefa_id, int) or tarefa_id <= 0:
        raise ValueError("Informe um id inteiro positivo.")
    if not isinstance(concluida, bool):
        raise ValueError("O campo concluida precisa ser booleano.")

    if concluida:
        tarefa = lista_concluir_tarefa(tarefas, tarefa_id)
    else:
        tarefa = next((item for item in tarefas if item["id"] == tarefa_id), None)
        if tarefa is not None:
            tarefa["concluida"] = False
    if tarefa is None:
        return None
    return {"tarefas": tarefas, "resultado": deepcopy(tarefa)}


def excluir_lista_tarefa_lab(estado, tarefa_id):
    tarefas = _normalizar_lista_tarefas(estado)
    if not isinstance(tarefa_id, int) or tarefa_id <= 0:
        raise ValueError("Informe um id inteiro positivo.")
    removida = lista_excluir_tarefa(tarefas, tarefa_id)
    if removida is None:
        return None
    return {"tarefas": tarefas, "resultado": deepcopy(removida)}


def _normalizar_tarefas(valor):
    if valor is None:
        return []
    if not isinstance(valor, list):
        raise ValueError("O estado de tarefas precisa ser uma lista.")
    if len(valor) > MAX_ITENS_LAB:
        raise ValueError(f"O laboratório aceita no máximo {MAX_ITENS_LAB} tarefas por vez.")

    tarefas = []
    ids = set()
    for item in valor:
        if not isinstance(item, dict):
            raise ValueError("Cada tarefa precisa ser um objeto JSON.")

        tarefa_id = item.get("id")
        titulo = str(item.get("titulo", "")).strip()
        prioridade = str(item.get("prioridade", "media")).strip().lower()
        concluida = item.get("concluida", False)

        if not isinstance(tarefa_id, int) or tarefa_id <= 0:
            raise ValueError("Cada tarefa precisa ter um id inteiro positivo.")
        if tarefa_id in ids:
            raise ValueError("IDs de tarefas não podem se repetir.")
        if not titulo or len(titulo) > MAX_TITULO:
            raise ValueError(f"O título precisa ter entre 1 e {MAX_TITULO} caracteres.")
        if prioridade not in {"baixa", "media", "alta"}:
            raise ValueError("A prioridade deve ser baixa, media ou alta.")
        if not isinstance(concluida, bool):
            raise ValueError("O campo concluida precisa ser booleano.")

        ids.add(tarefa_id)
        tarefas.append(
            {
                "id": tarefa_id,
                "titulo": titulo,
                "prioridade": prioridade,
                "concluida": concluida,
            }
        )

    return tarefas


def listar_tarefas_lab(estado, status=None):
    tarefas = _normalizar_tarefas(estado)
    return api_filtrar_tarefas(tarefas, status)


def criar_tarefa_lab(estado, titulo, prioridade="media"):
    tarefas = _normalizar_tarefas(estado)
    if len(tarefas) >= MAX_ITENS_LAB:
        raise ValueError(f"O laboratório aceita no máximo {MAX_ITENS_LAB} tarefas por vez.")

    titulo = str(titulo).strip()
    if len(titulo) > MAX_TITULO:
        raise ValueError(f"O título pode ter no máximo {MAX_TITULO} caracteres.")

    criada = api_criar_tarefa(tarefas, titulo, prioridade)
    return {"tarefas": tarefas, "resultado": deepcopy(criada)}


def atualizar_tarefa_lab(estado, tarefa_id, dados):
    tarefas = _normalizar_tarefas(estado)
    if not isinstance(tarefa_id, int) or tarefa_id <= 0:
        raise ValueError("Informe um id inteiro positivo.")
    if not isinstance(dados, dict):
        raise ValueError("Envie um objeto JSON com os campos que deseja alterar.")

    tarefa = next((item for item in tarefas if item["id"] == tarefa_id), None)
    if tarefa is None:
        return None

    dados_permitidos = {}
    if "titulo" in dados:
        titulo = str(dados["titulo"]).strip()
        if len(titulo) > MAX_TITULO:
            raise ValueError(f"O título pode ter no máximo {MAX_TITULO} caracteres.")
        dados_permitidos["titulo"] = titulo
    if "prioridade" in dados:
        dados_permitidos["prioridade"] = dados["prioridade"]
    if "concluida" in dados:
        dados_permitidos["concluida"] = dados["concluida"]

    atualizada = api_atualizar_tarefa(tarefa, dados_permitidos)
    return {"tarefas": tarefas, "resultado": deepcopy(atualizada)}


def excluir_tarefa_lab(estado, tarefa_id):
    tarefas = _normalizar_tarefas(estado)
    if not isinstance(tarefa_id, int) or tarefa_id <= 0:
        raise ValueError("Informe um id inteiro positivo.")

    removida = api_excluir_tarefa(tarefas, tarefa_id)
    if removida is None:
        return None

    return {"tarefas": tarefas, "resultado": deepcopy(removida)}


def analisar_projeto_lab(checks):
    if not isinstance(checks, dict):
        raise ValueError("Envie os checks do projeto como objeto JSON.")

    desconhecidos = set(checks) - CHECKS_PROJETO
    if desconhecidos:
        raise ValueError("Há checks não reconhecidos no laboratório.")

    normalizados = {}
    for nome in CHECKS_PROJETO:
        valor = checks.get(nome, False)
        if not isinstance(valor, bool):
            raise ValueError("Cada check precisa ser true ou false.")
        normalizados[nome] = valor

    with TemporaryDirectory(prefix="videirafoo-lab-") as temporario:
        raiz = Path(temporario)
        Path(raiz, "app.py").write_text("print('laboratorio')\n", encoding="utf-8")

        if normalizados["readme"]:
            Path(raiz, "README.md").write_text("# Projeto de laboratório\n", encoding="utf-8")
        if normalizados["gitignore"]:
            Path(raiz, ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
        if normalizados["licenca"]:
            Path(raiz, "LICENSE").write_text("MIT\n", encoding="utf-8")
        if normalizados["ci"]:
            workflows = Path(raiz, ".github", "workflows")
            workflows.mkdir(parents=True)
            Path(workflows, "ci.yml").write_text("name: CI\n", encoding="utf-8")
        if normalizados["testes"]:
            Path(raiz, "test_app.py").write_text("def test_exemplo():\n    assert True\n", encoding="utf-8")
        if normalizados["dependencias"]:
            Path(raiz, "requirements.txt").write_text("flask>=3.1,<4\n", encoding="utf-8")

        relatorio = analisar_repositorio(raiz)

    relatorio["repositorio"] = "projeto-laboratorio"
    relatorio["caminho"] = "temporário e isolado"
    relatorio["entrada_checks"] = normalizados
    return relatorio
