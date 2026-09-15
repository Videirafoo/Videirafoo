(() => {
  "use strict";

  const CHAVES = {
    lista: "videirafoo-lab-tarefas-v1",
    estoque: "videirafoo-lab-estoque-v1",
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

  function migrarEstadosAntigos() {
    const tarefas = carregarArray(CHAVES.lista);
    if (tarefas.some((item) => !Number.isInteger(item?.id) || !("titulo" in item))) {
      salvarArray(
        CHAVES.lista,
        tarefas.map((item, indice) => ({
          id: indice + 1,
          titulo: item?.titulo || item?.texto || `Tarefa ${indice + 1}`,
          prioridade: item?.prioridade || "media",
          concluida: Boolean(item?.concluida),
        }))
      );
    }

    const produtos = carregarArray(CHAVES.estoque);
    if (produtos.some((item) => !Number.isInteger(item?.id) || !("codigo" in item))) {
      salvarArray(
        CHAVES.estoque,
        produtos.map((item, indice) => ({
          id: indice + 1,
          codigo: `LAB-${indice + 1}`,
          nome: item?.nome || `Produto ${indice + 1}`,
          quantidade: Number(item?.quantidade) || 0,
          estoque_minimo: Number(item?.estoque_minimo) || 0,
          preco: Number(item?.preco) || 0,
        }))
      );
    }
  }

  migrarEstadosAntigos();

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
    return { response, corpo: await lerJson(response) };
  }

  // 03 — Cadastro de alunos: cálculo e situação pelo Python real.
  const alunoCard = document.querySelector("#alunos");
  if (alunoCard) {
    const botao = clonarSemListeners("#calcular-media");
    const nome = document.querySelector("#aluno-nome");
    const camposNotas = ["#nota-1", "#nota-2", "#nota-3"].map((id) => document.querySelector(id));
    const resultado = document.querySelector("#media-resultado");
    const descricao = alunoCard.querySelector(".muted");

    if (descricao) {
      descricao.textContent = "Validação das notas, média e situação acadêmica executadas pelas funções Python reais do Mini Sistema 03.";
    }

    botao?.addEventListener("click", async () => {
      if (!resultado) return;
      resultado.textContent = "Calculando pelo backend Python...";
      try {
        const resposta = await requisicao("/api/laboratorio/aluno-media", {
          method: "POST",
          body: JSON.stringify({
            nome: nome?.value || "",
            notas: camposNotas.map((campo) => campo?.value ?? ""),
          }),
        });
        if (!resposta.response.ok) {
          resultado.textContent = resposta.corpo?.erro || "Não foi possível calcular a média.";
          return;
        }
        const dados = resposta.corpo;
        const situacao = {
          aprovado: "Aprovado",
          recuperacao: "Recuperação",
          reprovado: "Reprovado",
        }[dados.situacao] || dados.situacao;
        resultado.textContent = `${dados.nome}: média ${Number(dados.media).toFixed(2)} — ${situacao}. Calculado pelo Python.`;
      } catch (_erro) {
        resultado.textContent = "Backend indisponível no momento.";
      }
    });
  }

  // 04 — Controle de estoque: cadastro e exclusão pelo Python real.
  const estoqueCard = document.querySelector("#estoque");
  if (estoqueCard) {
    const form = clonarSemListeners("#estoque-form");
    const lista = document.querySelector("#estoque-lista");
    const total = document.querySelector("#estoque-total");
    const descricao = estoqueCard.querySelector(".muted");

    if (descricao) {
      descricao.textContent = "Cadastro, quantidade e exclusão usam as regras Python reais do Mini Sistema 04; preço continua como extensão didática do card.";
    }

    const moeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

    const renderEstoque = () => {
      if (!lista || !total) return;
      const produtos = carregarArray(CHAVES.estoque);
      lista.replaceChildren();
      if (!produtos.length) {
        const vazio = document.createElement("li");
        vazio.className = "muted";
        vazio.textContent = "Estoque vazio.";
        lista.appendChild(vazio);
      }

      produtos.forEach((produto) => {
        const li = document.createElement("li");
        li.className = "item";
        const texto = document.createElement("span");
        texto.textContent = `${produto.nome} — ${produto.quantidade} × ${moeda.format(produto.preco || 0)}`;
        const excluir = criarBotao("Excluir", "danger", async () => {
          try {
            const resposta = await requisicao("/api/laboratorio/estoque", {
              method: "DELETE",
              body: JSON.stringify({ produtos: carregarArray(CHAVES.estoque), id: produto.id }),
            });
            if (!resposta.response.ok) {
              total.textContent = resposta.corpo?.erro || "Não foi possível excluir o produto.";
              return;
            }
            salvarArray(CHAVES.estoque, resposta.corpo.produtos);
            renderEstoque();
          } catch (_erro) {
            total.textContent = "Backend indisponível no momento.";
          }
        });
        li.append(texto, excluir);
        lista.appendChild(li);
      });

      const valor = produtos.reduce(
        (soma, produto) => soma + Number(produto.quantidade || 0) * Number(produto.preco || 0),
        0
      );
      total.textContent = `Valor do estoque: ${moeda.format(valor)} — regras validadas pelo Python.`;
    };

    if (form) {
      const nome = form.querySelector("#produto-nome");
      const quantidade = form.querySelector("#produto-qtd");
      const preco = form.querySelector("#produto-preco");
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
          const resposta = await requisicao("/api/laboratorio/estoque", {
            method: "POST",
            body: JSON.stringify({
              produtos: carregarArray(CHAVES.estoque),
              nome: nome?.value || "",
              quantidade: quantidade?.value || "",
              preco: preco?.value || "",
            }),
          });
          if (!resposta.response.ok) {
            if (total) total.textContent = resposta.corpo?.erro || "Não foi possível cadastrar o produto.";
            return;
          }
          salvarArray(CHAVES.estoque, resposta.corpo.produtos);
          form.reset();
          renderEstoque();
          nome?.focus();
        } catch (_erro) {
          if (total) total.textContent = "Backend indisponível no momento.";
        }
      });
    }

    renderEstoque();
  }
})();
