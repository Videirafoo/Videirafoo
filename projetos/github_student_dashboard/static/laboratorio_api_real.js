(() => {
  "use strict";

  const STORAGE_KEY = "videirafoo-lab-api-v1";
  const resposta = document.querySelector("#api-resposta");
  const titulo = document.querySelector("#api-titulo");
  const prioridade = document.querySelector("#api-prioridade");
  const card = document.querySelector("#api-tarefas");

  function carregar() {
    try {
      const valor = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      return Array.isArray(valor) ? valor : [];
    } catch (_erro) {
      return [];
    }
  }

  function salvar(tarefas) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tarefas));
  }

  function mostrarApi(status, corpo) {
    if (!resposta) return;
    const texto = corpo === undefined || corpo === null || corpo === ""
      ? "(sem corpo de resposta)"
      : JSON.stringify(corpo, null, 2);
    resposta.textContent = `HTTP ${status}\n${texto}`;
  }

  async function lerJson(response) {
    const texto = await response.text();
    if (!texto) return null;
    try {
      return JSON.parse(texto);
    } catch (_erro) {
      return { erro: texto };
    }
  }

  async function requisicao(url, opcoes = {}) {
    const response = await fetch(url, {
      headers: { "Content-Type": "application/json", ...(opcoes.headers || {}) },
      ...opcoes,
    });
    const corpo = await lerJson(response);
    return { response, corpo };
  }

  function interceptar(id, handler) {
    const elemento = document.querySelector(id);
    if (!elemento) return;
    elemento.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopImmediatePropagation();
      void handler();
    }, true);
  }

  if (resposta && titulo && prioridade && card) {
    const descricao = card.querySelector(".muted");
    const nota = card.querySelector(".code-note");
    if (descricao) {
      descricao.textContent = "Executa GET, POST, PATCH e DELETE no backend Flask usando as regras Python reais do Mini Sistema 09.";
    }
    if (nota) {
      nota.textContent = "O estado fica no seu navegador, mas validação e regras de negócio são processadas no servidor pelo mesmo módulo Python versionado no GitHub.";
    }

    interceptar("#api-post", async () => {
      try {
        const tarefas = carregar();
        const resultado = await requisicao("/api/laboratorio/tarefas", {
          method: "POST",
          body: JSON.stringify({
            tarefas,
            titulo: titulo.value.trim(),
            prioridade: prioridade.value,
          }),
        });
        if (resultado.response.ok && resultado.corpo?.tarefas) {
          salvar(resultado.corpo.tarefas);
          titulo.value = "";
        }
        mostrarApi(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
      } catch (_erro) {
        mostrarApi("indisponível", { erro: "Não foi possível alcançar o backend do laboratório." });
      }
    });

    interceptar("#api-get", async () => {
      try {
        const estado = encodeURIComponent(JSON.stringify(carregar()));
        const resultado = await requisicao(`/api/laboratorio/tarefas?estado=${estado}`, { method: "GET" });
        mostrarApi(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
      } catch (_erro) {
        mostrarApi("indisponível", { erro: "Não foi possível alcançar o backend do laboratório." });
      }
    });

    interceptar("#api-patch", async () => {
      const tarefas = carregar();
      if (!tarefas.length) {
        mostrarApi("400", { erro: "Crie uma tarefa antes de executar PATCH." });
        return;
      }
      try {
        const primeira = tarefas[0];
        const resultado = await requisicao("/api/laboratorio/tarefas", {
          method: "PATCH",
          body: JSON.stringify({
            tarefas,
            id: primeira.id,
            dados: { concluida: !Boolean(primeira.concluida) },
          }),
        });
        if (resultado.response.ok && resultado.corpo?.tarefas) salvar(resultado.corpo.tarefas);
        mostrarApi(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
      } catch (_erro) {
        mostrarApi("indisponível", { erro: "Não foi possível alcançar o backend do laboratório." });
      }
    });

    interceptar("#api-delete", async () => {
      const tarefas = carregar();
      if (!tarefas.length) {
        mostrarApi("404", { erro: "Não há tarefa para excluir." });
        return;
      }
      try {
        const primeira = tarefas[0];
        const resultado = await requisicao("/api/laboratorio/tarefas", {
          method: "DELETE",
          body: JSON.stringify({ tarefas, id: primeira.id }),
        });
        if (resultado.response.status === 204) {
          salvar(tarefas.filter((item) => item.id !== primeira.id));
        }
        mostrarApi(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
      } catch (_erro) {
        mostrarApi("indisponível", { erro: "Não foi possível alcançar o backend do laboratório." });
      }
    });
  }

  const repoCard = document.querySelector("#analisador-local");
  const repoResultado = document.querySelector("#repo-resultado");
  const repoChecks = Array.from(document.querySelectorAll(".repo-check"));

  if (repoCard && repoResultado && repoChecks.length === 6) {
    const descricao = repoCard.querySelector(".muted");
    if (descricao) {
      descricao.textContent = "Monta um repositório temporário isolado e executa o analisar_repositorio() original do Mini Sistema 10 no backend Python.";
    }

    interceptar("#repo-calcular", async () => {
      const nomes = ["readme", "gitignore", "licenca", "ci", "testes", "dependencias"];
      const checks = Object.fromEntries(
        repoChecks.map((checkbox, indice) => [nomes[indice], checkbox.checked])
      );

      repoResultado.textContent = "Executando analisador Python no servidor...";
      try {
        const resultado = await requisicao("/api/laboratorio/analisar", {
          method: "POST",
          body: JSON.stringify({ checks }),
        });
        if (!resultado.response.ok) {
          repoResultado.textContent = resultado.corpo?.erro || "Não foi possível analisar o projeto.";
          return;
        }

        const relatorio = resultado.corpo;
        const linhasChecks = Object.entries(relatorio.checks)
          .map(([nome, presente]) => `- ${nome}: ${presente ? "OK" : "FALTA"}`)
          .join("\n");
        const recomendacoes = relatorio.recomendacoes.map((item) => `- ${item}`).join("\n");
        repoResultado.textContent = [
          `Score real: ${relatorio.score}/100`,
          "",
          "Checks executados pelo Python:",
          linhasChecks,
          "",
          `Arquivos temporários analisados: ${relatorio.evidencias.total_arquivos_analisados}`,
          "",
          "Recomendações:",
          recomendacoes,
        ].join("\n");
      } catch (_erro) {
        repoResultado.textContent = "Não foi possível alcançar o backend do laboratório.";
      }
    });
  }
})();
