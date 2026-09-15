(() => {
  "use strict";

  const STORAGE_KEY = "videirafoo-lab-api-v1";
  const resposta = document.querySelector("#api-resposta");
  const titulo = document.querySelector("#api-titulo");
  const prioridade = document.querySelector("#api-prioridade");
  const card = document.querySelector("#api-tarefas");

  if (!resposta || !titulo || !prioridade || !card) return;

  const descricao = card.querySelector(".muted");
  const nota = card.querySelector(".code-note");
  if (descricao) {
    descricao.textContent = "Executa GET, POST, PATCH e DELETE no backend Flask usando as regras Python reais do Mini Sistema 09.";
  }
  if (nota) {
    nota.textContent = "O estado fica no seu navegador, mas validação e regras de negócio são processadas no servidor pelo mesmo módulo Python versionado no GitHub.";
  }

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

  function mostrar(status, corpo) {
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
    try {
      const response = await fetch(url, {
        headers: { "Content-Type": "application/json", ...(opcoes.headers || {}) },
        ...opcoes,
      });
      const corpo = await lerJson(response);
      return { response, corpo };
    } catch (_erro) {
      mostrar("indisponível", { erro: "Não foi possível alcançar o backend do laboratório." });
      return null;
    }
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

  interceptar("#api-post", async () => {
    const tarefas = carregar();
    const resultado = await requisicao("/api/laboratorio/tarefas", {
      method: "POST",
      body: JSON.stringify({
        tarefas,
        titulo: titulo.value.trim(),
        prioridade: prioridade.value,
      }),
    });
    if (!resultado) return;
    if (resultado.response.ok && resultado.corpo?.tarefas) {
      salvar(resultado.corpo.tarefas);
      titulo.value = "";
    }
    mostrar(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
  });

  interceptar("#api-get", async () => {
    const estado = encodeURIComponent(JSON.stringify(carregar()));
    const resultado = await requisicao(`/api/laboratorio/tarefas?estado=${estado}`, { method: "GET" });
    if (!resultado) return;
    mostrar(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
  });

  interceptar("#api-patch", async () => {
    const tarefas = carregar();
    if (!tarefas.length) {
      mostrar("400", { erro: "Crie uma tarefa antes de executar PATCH." });
      return;
    }
    const primeira = tarefas[0];
    const resultado = await requisicao("/api/laboratorio/tarefas", {
      method: "PATCH",
      body: JSON.stringify({
        tarefas,
        id: primeira.id,
        dados: { concluida: !Boolean(primeira.concluida) },
      }),
    });
    if (!resultado) return;
    if (resultado.response.ok && resultado.corpo?.tarefas) salvar(resultado.corpo.tarefas);
    mostrar(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
  });

  interceptar("#api-delete", async () => {
    const tarefas = carregar();
    if (!tarefas.length) {
      mostrar("404", { erro: "Não há tarefa para excluir." });
      return;
    }
    const primeira = tarefas[0];
    const resultado = await requisicao("/api/laboratorio/tarefas", {
      method: "DELETE",
      body: JSON.stringify({ tarefas, id: primeira.id }),
    });
    if (!resultado) return;
    if (resultado.response.status === 204) {
      salvar(tarefas.filter((item) => item.id !== primeira.id));
    }
    mostrar(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
  });
})();
