(() => {
  "use strict";

  const CHAVES = {
    agenda: "videirafoo-lab-agenda-v1",
    lista: "videirafoo-lab-tarefas-v1",
    api: "videirafoo-lab-api-v1",
  };

  function carregarArray(chave) {
    try {
      const valor = JSON.parse(localStorage.getItem(chave) || "[]");
      return Array.isArray(valor) ? valor : [];
    } catch (_erro) {
      return [];
    }
  }

  function salvarArray(chave, valor) {
    localStorage.setItem(chave, JSON.stringify(valor));
  }

  function clonarSemListeners(seletor) {
    const atual = document.querySelector(seletor);
    if (!atual) return null;
    const clone = atual.cloneNode(true);
    atual.replaceWith(clone);
    return clone;
  }

  function criarBotao(rotulo, classe, handler) {
    const botao = document.createElement("button");
    botao.type = "button";
    botao.className = classe;
    botao.textContent = rotulo;
    botao.addEventListener("click", () => void handler());
    return botao;
  }

  function garantirStatus(container, id) {
    let status = document.querySelector(`#${id}`);
    if (status) return status;
    status = document.createElement("div");
    status.id = id;
    status.className = "output";
    status.style.marginTop = "8px";
    container.appendChild(status);
    return status;
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

  // 01 — Agenda de contatos: UI local, regras Python reais no servidor.
  const agendaCard = document.querySelector("#agenda");
  if (agendaCard) {
    const form = clonarSemListeners("#agenda-form");
    const busca = clonarSemListeners("#agenda-busca");
    const lista = document.querySelector("#agenda-lista");
    const app = agendaCard.querySelector(".app");
    const descricao = agendaCard.querySelector(".muted");
    const status = app ? garantirStatus(app, "agenda-status-real") : null;

    if (descricao) {
      descricao.textContent = "Cadastro e exclusão executados pelo backend Flask usando as funções Python reais da Agenda de Contatos.";
    }
    if (status) {
      status.textContent = "Dados ficam neste navegador; regras de cadastro e duplicidade são validadas pelo Python.";
    }

    const renderAgenda = () => {
      if (!lista || !busca) return;
      const contatos = carregarArray(CHAVES.agenda);
      const termo = busca.value.trim().toLocaleLowerCase("pt-BR");
      const filtrados = contatos.filter((contato) =>
        `${contato.nome || ""} ${contato.telefone || ""}`.toLocaleLowerCase("pt-BR").includes(termo)
      );

      lista.replaceChildren();
      if (!filtrados.length) {
        const vazio = document.createElement("li");
        vazio.className = "muted";
        vazio.textContent = contatos.length ? "Nenhum contato encontrado." : "Nenhum contato cadastrado.";
        lista.appendChild(vazio);
        return;
      }

      filtrados.forEach((contato) => {
        const li = document.createElement("li");
        li.className = "item";
        const texto = document.createElement("span");
        texto.textContent = `${contato.nome} — ${contato.telefone}`;
        const excluir = criarBotao("Excluir", "danger", async () => {
          try {
            const resultado = await requisicao("/api/laboratorio/agenda", {
              method: "DELETE",
              body: JSON.stringify({ contatos: carregarArray(CHAVES.agenda), id: contato.id }),
            });
            if (!resultado.response.ok) {
              if (status) status.textContent = resultado.corpo?.erro || "Não foi possível excluir o contato.";
              return;
            }
            salvarArray(CHAVES.agenda, resultado.corpo.contatos);
            if (status) status.textContent = `Contato ${resultado.corpo.resultado.nome} excluído pelo Python.`;
            renderAgenda();
          } catch (_erro) {
            if (status) status.textContent = "Backend indisponível no momento.";
          }
        });
        li.append(texto, excluir);
        lista.appendChild(li);
      });
    };

    if (form) {
      const nome = form.querySelector("#agenda-nome");
      const telefone = form.querySelector("#agenda-telefone");
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
          const resultado = await requisicao("/api/laboratorio/agenda", {
            method: "POST",
            body: JSON.stringify({
              contatos: carregarArray(CHAVES.agenda),
              nome: nome?.value || "",
              telefone: telefone?.value || "",
            }),
          });
          if (!resultado.response.ok) {
            if (status) status.textContent = resultado.corpo?.erro || "Não foi possível cadastrar o contato.";
            return;
          }
          salvarArray(CHAVES.agenda, resultado.corpo.contatos);
          form.reset();
          if (status) status.textContent = `Contato ${resultado.corpo.resultado.nome} validado e criado pelo Python.`;
          renderAgenda();
          nome?.focus();
        } catch (_erro) {
          if (status) status.textContent = "Backend indisponível no momento.";
        }
      });
    }
    busca?.addEventListener("input", renderAgenda);
    renderAgenda();
  }

  // 02 — Lista de tarefas: UI local, regras Python reais no servidor.
  const listaCard = document.querySelector("#tarefas");
  if (listaCard) {
    const form = clonarSemListeners("#tarefas-form");
    const lista = document.querySelector("#tarefas-lista");
    const app = listaCard.querySelector(".app");
    const descricao = listaCard.querySelector(".muted");
    const status = app ? garantirStatus(app, "tarefas-status-real") : null;

    if (descricao) {
      descricao.textContent = "Criação, conclusão e exclusão processadas pelas funções Python reais do Mini Sistema 02.";
    }
    if (status) {
      status.textContent = "Estado privado no navegador; operações passam pelo backend Python.";
    }

    const renderLista = () => {
      if (!lista) return;
      const tarefas = carregarArray(CHAVES.lista);
      lista.replaceChildren();
      if (!tarefas.length) {
        const vazio = document.createElement("li");
        vazio.className = "muted";
        vazio.textContent = "Nenhuma tarefa. Adicione a primeira.";
        lista.appendChild(vazio);
        return;
      }

      tarefas.forEach((tarefa) => {
        const li = document.createElement("li");
        li.className = "item";
        const principal = document.createElement("div");
        principal.className = "item-main";
        const check = document.createElement("input");
        check.type = "checkbox";
        check.checked = Boolean(tarefa.concluida);
        const texto = document.createElement("span");
        texto.textContent = tarefa.titulo || tarefa.texto || "Tarefa";
        if (tarefa.concluida) texto.className = "done";

        check.addEventListener("change", async () => {
          try {
            const resultado = await requisicao("/api/laboratorio/lista-tarefas", {
              method: "PATCH",
              body: JSON.stringify({
                tarefas: carregarArray(CHAVES.lista),
                id: tarefa.id,
                concluida: check.checked,
              }),
            });
            if (!resultado.response.ok) {
              check.checked = !check.checked;
              if (status) status.textContent = resultado.corpo?.erro || "Não foi possível atualizar a tarefa.";
              return;
            }
            salvarArray(CHAVES.lista, resultado.corpo.tarefas);
            if (status) status.textContent = `Tarefa #${resultado.corpo.resultado.id} atualizada pelo Python.`;
            renderLista();
          } catch (_erro) {
            check.checked = !check.checked;
            if (status) status.textContent = "Backend indisponível no momento.";
          }
        });

        const excluir = criarBotao("Excluir", "danger", async () => {
          try {
            const resultado = await requisicao("/api/laboratorio/lista-tarefas", {
              method: "DELETE",
              body: JSON.stringify({ tarefas: carregarArray(CHAVES.lista), id: tarefa.id }),
            });
            if (!resultado.response.ok) {
              if (status) status.textContent = resultado.corpo?.erro || "Não foi possível excluir a tarefa.";
              return;
            }
            salvarArray(CHAVES.lista, resultado.corpo.tarefas);
            if (status) status.textContent = `Tarefa #${resultado.corpo.resultado.id} excluída pelo Python.`;
            renderLista();
          } catch (_erro) {
            if (status) status.textContent = "Backend indisponível no momento.";
          }
        });

        principal.append(check, texto);
        li.append(principal, excluir);
        lista.appendChild(li);
      });
    };

    if (form) {
      const campo = form.querySelector("#tarefa-texto");
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
          const resultado = await requisicao("/api/laboratorio/lista-tarefas", {
            method: "POST",
            body: JSON.stringify({
              tarefas: carregarArray(CHAVES.lista),
              titulo: campo?.value || "",
              prioridade: "media",
            }),
          });
          if (!resultado.response.ok) {
            if (status) status.textContent = resultado.corpo?.erro || "Não foi possível criar a tarefa.";
            return;
          }
          salvarArray(CHAVES.lista, resultado.corpo.tarefas);
          form.reset();
          if (status) status.textContent = `Tarefa #${resultado.corpo.resultado.id} criada pelo Python.`;
          renderLista();
          campo?.focus();
        } catch (_erro) {
          if (status) status.textContent = "Backend indisponível no momento.";
        }
      });
    }
    renderLista();
  }

  // 09 — API de tarefas real.
  const resposta = document.querySelector("#api-resposta");
  const titulo = document.querySelector("#api-titulo");
  const prioridade = document.querySelector("#api-prioridade");
  const card = document.querySelector("#api-tarefas");

  function mostrarApi(status, corpo) {
    if (!resposta) return;
    const texto = corpo === undefined || corpo === null || corpo === ""
      ? "(sem corpo de resposta)"
      : JSON.stringify(corpo, null, 2);
    resposta.textContent = `HTTP ${status}\n${texto}`;
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
        const tarefas = carregarArray(CHAVES.api);
        const resultado = await requisicao("/api/laboratorio/tarefas", {
          method: "POST",
          body: JSON.stringify({ tarefas, titulo: titulo.value.trim(), prioridade: prioridade.value }),
        });
        if (resultado.response.ok && resultado.corpo?.tarefas) {
          salvarArray(CHAVES.api, resultado.corpo.tarefas);
          titulo.value = "";
        }
        mostrarApi(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
      } catch (_erro) {
        mostrarApi("indisponível", { erro: "Não foi possível alcançar o backend do laboratório." });
      }
    });

    interceptar("#api-get", async () => {
      try {
        const estado = encodeURIComponent(JSON.stringify(carregarArray(CHAVES.api)));
        const resultado = await requisicao(`/api/laboratorio/tarefas?estado=${estado}`, { method: "GET" });
        mostrarApi(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
      } catch (_erro) {
        mostrarApi("indisponível", { erro: "Não foi possível alcançar o backend do laboratório." });
      }
    });

    interceptar("#api-patch", async () => {
      const tarefas = carregarArray(CHAVES.api);
      if (!tarefas.length) {
        mostrarApi("400", { erro: "Crie uma tarefa antes de executar PATCH." });
        return;
      }
      try {
        const primeira = tarefas[0];
        const resultado = await requisicao("/api/laboratorio/tarefas", {
          method: "PATCH",
          body: JSON.stringify({ tarefas, id: primeira.id, dados: { concluida: !Boolean(primeira.concluida) } }),
        });
        if (resultado.response.ok && resultado.corpo?.tarefas) salvarArray(CHAVES.api, resultado.corpo.tarefas);
        mostrarApi(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
      } catch (_erro) {
        mostrarApi("indisponível", { erro: "Não foi possível alcançar o backend do laboratório." });
      }
    });

    interceptar("#api-delete", async () => {
      const tarefas = carregarArray(CHAVES.api);
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
          salvarArray(CHAVES.api, tarefas.filter((item) => item.id !== primeira.id));
        }
        mostrarApi(`${resultado.response.status} ${resultado.response.statusText}`, resultado.corpo);
      } catch (_erro) {
        mostrarApi("indisponível", { erro: "Não foi possível alcançar o backend do laboratório." });
      }
    });
  }

  // 10 — Projeto integrado real.
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
      const checks = Object.fromEntries(repoChecks.map((checkbox, indice) => [nomes[indice], checkbox.checked]));

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
