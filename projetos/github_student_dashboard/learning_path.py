"""Trilha educacional pública do Videirafoo.

A estrutura combina progressão por etapas, competências por nível e missões
práticas ligadas a evidências reais do próprio repositório.
"""

TRILHA_APRENDIZADO = [
    {
        "nivel": 1,
        "slug": "fundamentos",
        "titulo": "Fundamentos",
        "objetivo": "Entender lógica de programação e escrever programas pequenos sem depender de copiar respostas.",
        "competencias": [
            "variáveis, tipos e entrada/saída",
            "operadores e expressões",
            "condicionais",
            "laços",
            "funções e decomposição simples",
        ],
        "missoes": [
            {
                "id": "n1-explicar-fluxo",
                "titulo": "Explique um programa linha por linha",
                "evidencia": "Use uma das listas acadêmicas e consiga explicar entrada, processamento e saída.",
                "url": "https://github.com/Videirafoo/Lista-01-segundo-periodo",
            },
            {
                "id": "n1-alterar-regra",
                "titulo": "Altere uma regra e teste",
                "evidencia": "Mude uma condição simples e teste pelo menos três entradas diferentes.",
                "url": "/laboratorio#alunos",
            },
            {
                "id": "n1-funcao",
                "titulo": "Transforme repetição em função",
                "evidencia": "Pegue um exercício repetitivo e extraia uma função com nome claro.",
                "url": "https://github.com/Videirafoo/Videirafoo/tree/main/conteudos/python-para-iniciantes",
            },
        ],
    },
    {
        "nivel": 2,
        "slug": "estruturas-algoritmos",
        "titulo": "Estruturas e Algoritmos",
        "objetivo": "Escolher estruturas adequadas, percorrer dados e entender custo básico de algoritmos.",
        "competencias": [
            "listas, dicionários, tuplas e strings",
            "busca sequencial e binária",
            "ordenação",
            "recursividade",
            "Big O em nível introdutório",
        ],
        "missoes": [
            {
                "id": "n2-busca-binaria",
                "titulo": "Visualize uma busca binária",
                "evidencia": "Use o simulador e explique inicio, meio, fim e por que a lista precisa estar ordenada.",
                "url": "/laboratorio#busca-binaria",
            },
            {
                "id": "n2-comparar-buscas",
                "titulo": "Compare busca sequencial e binária",
                "evidencia": "Conte comparações em exemplos pequenos e descreva quando cada abordagem faz sentido.",
                "url": "https://github.com/Videirafoo/Lista-03-segundo-periodo",
            },
            {
                "id": "n2-recursao",
                "titulo": "Resolva e trace uma recursão",
                "evidencia": "Desenhe as chamadas de uma função recursiva até o caso-base e depois execute o código.",
                "url": "https://github.com/Videirafoo/lista-04-segundo-periodo",
            },
        ],
    },
    {
        "nivel": 3,
        "slug": "mini-sistemas",
        "titulo": "Mini Sistemas",
        "objetivo": "Sair do exercício isolado e construir software pequeno com CRUD, validação, estado e testes.",
        "competencias": [
            "CRUD",
            "validação de entrada",
            "arquivos e JSON",
            "regras de negócio",
            "testes automatizados",
        ],
        "missoes": [
            {
                "id": "n3-quebrar-validacao",
                "titulo": "Quebre uma validação de propósito",
                "evidencia": "Use um mini sistema, envie uma entrada inválida, observe o erro e encontre a regra no Python.",
                "url": "/laboratorio",
            },
            {
                "id": "n3-ler-teste",
                "titulo": "Leia o teste antes do código",
                "evidencia": "Escolha um mini sistema, preveja o comportamento pelo teste e só depois abra a implementação.",
                "url": "https://github.com/Videirafoo/Videirafoo/tree/main/conteudos/mini_sistemas",
            },
            {
                "id": "n3-melhoria",
                "titulo": "Implemente uma melhoria pequena",
                "evidencia": "Adicione uma regra, escreva ou ajuste teste e confirme a suíte verde.",
                "url": "https://github.com/Videirafoo/Videirafoo/tree/main/conteudos/mini_sistemas",
            },
        ],
    },
    {
        "nivel": 4,
        "slug": "aplicacoes-reais",
        "titulo": "Aplicações Reais",
        "objetivo": "Conectar frontend, backend, APIs, deploy e comportamento observável em uma aplicação pública.",
        "competencias": [
            "HTTP e REST",
            "Flask e rotas",
            "integração com API externa",
            "frontend consumindo backend",
            "deploy e healthcheck",
        ],
        "missoes": [
            {
                "id": "n4-http",
                "titulo": "Teste métodos HTTP reais",
                "evidencia": "Use o Mini Sistema 09 e diferencie GET, POST, PATCH, DELETE e seus códigos de resposta.",
                "url": "/laboratorio#api-tarefas",
            },
            {
                "id": "n4-dashboard",
                "titulo": "Analise um repositório público",
                "evidencia": "Execute o Dashboard, leia as evidências e confirme no GitHub pelo menos dois checks apresentados.",
                "url": "/",
            },
            {
                "id": "n4-health",
                "titulo": "Verifique produção",
                "evidencia": "Abra o healthcheck e explique por que uma aplicação pública precisa de uma rota simples de saúde.",
                "url": "/healthz",
            },
        ],
    },
    {
        "nivel": 5,
        "slug": "engenharia",
        "titulo": "Engenharia de Software",
        "objetivo": "Proteger comportamento com testes, CI, revisão, documentação e contribuições rastreáveis.",
        "competencias": [
            "Git, branches e pull requests",
            "testes e cobertura",
            "CI/CD",
            "documentação e manutenção",
            "segurança e dependências",
        ],
        "missoes": [
            {
                "id": "n5-quality",
                "titulo": "Leia uma evidência de qualidade",
                "evidencia": "Abra QUALITY.md e identifique quantidade de testes, cobertura, gate e limite da auditoria.",
                "url": "https://github.com/Videirafoo/Videirafoo/blob/main/QUALITY.md",
            },
            {
                "id": "n5-pr",
                "titulo": "Faça uma contribuição pequena",
                "evidencia": "Crie branch, commit focado e pull request que outra pessoa consiga revisar sem contexto escondido.",
                "url": "https://github.com/Videirafoo/Videirafoo/blob/main/OPEN_SOURCE_START.md",
            },
            {
                "id": "n5-review",
                "titulo": "Revise usando evidências",
                "evidencia": "Para uma mudança, registre observado, impacto e ação antes de sugerir correção.",
                "url": "https://github.com/Videirafoo/Videirafoo/blob/main/REFERENCIAS_OPEN_SOURCE.md",
            },
        ],
    },
    {
        "nivel": 6,
        "slug": "ia-aplicada",
        "titulo": "IA Aplicada",
        "objetivo": "Usar IA depois dos fundamentos, mantendo fatos verificáveis separados de explicação e julgamento.",
        "competencias": [
            "consumo de APIs de modelos",
            "prompt e contexto",
            "RAG e ferramentas",
            "avaliação e fallback",
            "segurança, proveniência e limites",
        ],
        "missoes": [
            {
                "id": "n6-deterministico",
                "titulo": "Separe fato de explicação",
                "evidencia": "Compare um check determinístico do Dashboard com a explicação opcional da IA e identifique quem calcula cada parte.",
                "url": "/explicar",
            },
            {
                "id": "n6-fallback",
                "titulo": "Entenda o fallback local",
                "evidencia": "Leia como o projeto continua funcionando quando a IA externa está desativada ou indisponível.",
                "url": "https://github.com/Videirafoo/Videirafoo/blob/main/projetos/github_student_dashboard/README.md",
            },
            {
                "id": "n6-proveniencia",
                "titulo": "Cheque a fonte antes de aceitar a resposta",
                "evidencia": "Escolha uma recomendação da IA e confirme manualmente a evidência no repositório analisado.",
                "url": "/",
            },
        ],
    },
]


def resumo_trilha():
    """Retorna a trilha e contagens úteis para a API e a interface."""
    total_missoes = sum(len(nivel["missoes"]) for nivel in TRILHA_APRENDIZADO)
    return {
        "niveis": TRILHA_APRENDIZADO,
        "total_niveis": len(TRILHA_APRENDIZADO),
        "total_missoes": total_missoes,
        "regra": "progresso deve ser ligado a evidência prática, não apenas leitura concluída",
    }
