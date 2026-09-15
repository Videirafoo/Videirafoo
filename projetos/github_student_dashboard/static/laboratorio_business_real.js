(() => {
  "use strict";

  const moeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
  const hoje = new Date().toISOString().slice(0, 10);
  const CHAVES = {
    biblioteca: "videirafoo-lab-biblioteca-v1",
    caixa: "videirafoo-lab-caixa-v2",
    caixaAntigo: "videirafoo-lab-caixa-produtos-v1",
    financeiro: "videirafoo-lab-financeiro-v1",
    habitos: "videirafoo-lab-habitos-v1",
  };

  function carregar(chave, padrao) {
    try {
      const valor = JSON.parse(localStorage.getItem(chave));
      return valor ?? padrao;
    } catch (_erro) {
      return padrao;
    }
  }

  function salvar(chave, valor) {
    localStorage.setItem(chave, JSON.stringify(valor));
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

  async function requisicao(url, corpo) {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(corpo),
    });
    return { response, corpo: await lerJson(response) };
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

  function mensagemErro(alvo, resultado, padrao) {
    alvo.textContent = resultado?.corpo?.erro || padrao;
  }

  // 05 — Biblioteca
  const bibliotecaCard = document.querySelector("#biblioteca");
  if (bibliotecaCard) {
    const addLivro = clonarSemListeners("#bib-add-livro");
    const addUsuario = clonarSemListeners("#bib-add-usuario");
    const emprestar = clonarSemListeners("#bib-emprestar");
    const status = document.querySelector("#bib-status");
    const lista = document.querySelector("#bib-lista");
    const descricao = bibliotecaCard.querySelector(".muted");
    const isbn = document.querySelector("#bib-isbn");
    const titulo = document.querySelector("#bib-titulo");
    const documento = document.querySelector("#bib-doc");
    const usuario = document.querySelector("#bib-usuario");
    const emprestimoIsbn = document.querySelector("#bib-emprestimo-isbn");
    const emprestimoDoc = document.querySelector("#bib-emprestimo-doc");

    let autor = document.querySelector("#bib-autor");
    if (!autor && titulo?.parentElement) {
      autor = document.createElement("input");
      autor.id = "bib-autor";
      autor.placeholder = "Autor";
      titulo.parentElement.insertBefore(autor, addLivro);
    }

    if (descricao) {
      descricao.textContent = "Livros, usuários, empréstimos e devoluções processados pelas funções Python reais do Mini Sistema 05.";
    }

    const estadoBiblioteca = () => carregar(CHAVES.biblioteca, { livros: [], usuarios: [], emprestimos: [] });

    const renderBiblioteca = () => {
      if (!lista) return;
      const estado = estadoBiblioteca();
      const livros = Array.isArray(estado.livros) ? estado.livros : [];
      const emprestimos = Array.isArray(estado.emprestimos) ? estado.emprestimos : [];
      lista.replaceChildren();

      if (!livros.length) {
        const vazio = document.createElement("li");
        vazio.className = "muted";
        vazio.textContent = "Nenhum livro cadastrado.";
        lista.appendChild(vazio);
        return;
      }

      livros.forEach((livro) => {
        const ativo = emprestimos.find((item) => item.isbn === livro.isbn && !item.devolvido);
        const li = document.createElement("li");
        li.className = "item";
        const texto = document.createElement("span");
        texto.textContent = ativo
          ? `${livro.titulo} — ${livro.autor} — emprestado para ${ativo.documento}`
          : `${livro.titulo} — ${livro.autor} — disponível`;

        if (ativo) {
          li.append(texto, criarBotao("Devolver", "secondary", async () => {
            try {
              const resultado = await requisicao("/api/laboratorio/biblioteca", {
                estado: estadoBiblioteca(),
                acao: "devolver",
                dados: { isbn: livro.isbn },
              });
              if (!resultado.response.ok) return mensagemErro(status, resultado, "Não foi possível devolver o livro.");
              salvar(CHAVES.biblioteca, resultado.corpo.estado);
              status.textContent = `${livro.titulo} devolvido pelo backend Python.`;
              renderBiblioteca();
            } catch (_erro) {
              status.textContent = "Backend indisponível no momento.";
            }
          }));
        } else {
          li.append(texto);
        }
        lista.appendChild(li);
      });
    };

    addLivro?.addEventListener("click", async () => {
      try {
        const resultado = await requisicao("/api/laboratorio/biblioteca", {
          estado: estadoBiblioteca(),
          acao: "cadastrar_livro",
          dados: { isbn: isbn?.value || "", titulo: titulo?.value || "", autor: autor?.value || "" },
        });
        if (!resultado.response.ok) return mensagemErro(status, resultado, "Não foi possível cadastrar o livro.");
        salvar(CHAVES.biblioteca, resultado.corpo.estado);
        status.textContent = `Livro ${resultado.corpo.resultado.titulo} cadastrado pelo Python.`;
        renderBiblioteca();
      } catch (_erro) {
        status.textContent = "Backend indisponível no momento.";
      }
    });

    addUsuario?.addEventListener("click", async () => {
      try {
        const resultado = await requisicao("/api/laboratorio/biblioteca", {
          estado: estadoBiblioteca(),
          acao: "cadastrar_usuario",
          dados: { nome: usuario?.value || "", documento: documento?.value || "" },
        });
        if (!resultado.response.ok) return mensagemErro(status, resultado, "Não foi possível cadastrar o usuário.");
        salvar(CHAVES.biblioteca, resultado.corpo.estado);
        status.textContent = `Usuário ${resultado.corpo.resultado.nome} cadastrado pelo Python.`;
      } catch (_erro) {
        status.textContent = "Backend indisponível no momento.";
      }
    });

    emprestar?.addEventListener("click", async () => {
      try {
        const resultado = await requisicao("/api/laboratorio/biblioteca", {
          estado: estadoBiblioteca(),
          acao: "emprestar",
          dados: { isbn: emprestimoIsbn?.value || "", documento: emprestimoDoc?.value || "" },
        });
        if (!resultado.response.ok) return mensagemErro(status, resultado, "Não foi possível registrar o empréstimo.");
        salvar(CHAVES.biblioteca, resultado.corpo.estado);
        status.textContent = "Empréstimo registrado pelo backend Python.";
        renderBiblioteca();
      } catch (_erro) {
        status.textContent = "Backend indisponível no momento.";
      }
    });

    renderBiblioteca();
  }

  // 06 — Caixa de mercado
  const caixaCard = document.querySelector("#caixa");
  if (caixaCard) {
    const cadastrar = clonarSemListeners("#cx-cadastrar");
    const adicionar = clonarSemListeners("#cx-adicionar");
    const fechar = clonarSemListeners("#cx-fechar");
    const desconto = clonarSemListeners("#cx-desconto");
    const selecao = document.querySelector("#cx-selecao");
    const carrinhoLista = document.querySelector("#cx-carrinho");
    const resumo = document.querySelector("#cx-resumo");
    const descricao = caixaCard.querySelector(".muted");

    if (descricao) {
      descricao.textContent = "Catálogo, carrinho, estoque, desconto e fechamento executados pelas funções Python reais do Mini Sistema 06.";
    }

    if (!localStorage.getItem(CHAVES.caixa)) {
      const antigos = carregar(CHAVES.caixaAntigo, []);
      const produtos = Array.isArray(antigos)
        ? antigos.map((item, indice) => ({
            id: indice + 1,
            codigo: item.codigo || `LAB-${indice + 1}`,
            nome: item.nome || `Produto ${indice + 1}`,
            preco: Number(item.preco) || 0,
            estoque: Number(item.estoque) || 0,
          }))
        : [];
      salvar(CHAVES.caixa, { produtos, carrinho: [], vendas: [] });
    }

    const estadoCaixa = () => carregar(CHAVES.caixa, { produtos: [], carrinho: [], vendas: [] });

    const renderCaixa = (mensagem = null) => {
      const estado = estadoCaixa();
      const produtos = Array.isArray(estado.produtos) ? estado.produtos : [];
      const carrinho = Array.isArray(estado.carrinho) ? estado.carrinho : [];
      selecao?.replaceChildren();
      produtos.forEach((produto) => {
        const opcao = document.createElement("option");
        opcao.value = produto.codigo;
        opcao.textContent = `${produto.nome} — ${moeda.format(produto.preco)} — estoque ${produto.estoque}`;
        selecao?.appendChild(opcao);
      });
      if (!produtos.length && selecao) {
        const opcao = document.createElement("option");
        opcao.value = "";
        opcao.textContent = "Cadastre um produto primeiro";
        selecao.appendChild(opcao);
      }

      carrinhoLista?.replaceChildren();
      carrinho.forEach((item) => {
        const li = document.createElement("li");
        li.className = "item";
        const texto = document.createElement("span");
        texto.textContent = `${item.nome}: ${item.quantidade} × ${moeda.format(item.preco_unitario)} = ${moeda.format(item.subtotal)}`;
        li.append(texto, criarBotao("Remover", "danger", async () => {
          try {
            const resultado = await requisicao("/api/laboratorio/caixa", {
              estado: estadoCaixa(), acao: "remover_carrinho", dados: { codigo: item.codigo },
            });
            if (!resultado.response.ok) return mensagemErro(resumo, resultado, "Não foi possível remover o item.");
            salvar(CHAVES.caixa, resultado.corpo.estado);
            renderCaixa("Item removido pelo backend Python.");
          } catch (_erro) {
            resumo.textContent = "Backend indisponível no momento.";
          }
        }));
        carrinhoLista?.appendChild(li);
      });

      const subtotal = carrinho.reduce((soma, item) => soma + Number(item.subtotal || 0), 0);
      const percentual = Math.min(100, Math.max(0, Number(desconto?.value) || 0));
      const total = subtotal * (1 - percentual / 100);
      resumo.textContent = mensagem || (carrinho.length
        ? `Subtotal: ${moeda.format(subtotal)}\nDesconto: ${percentual.toFixed(0)}%\nTotal previsto: ${moeda.format(total)}`
        : "Carrinho vazio.");
    };

    cadastrar?.addEventListener("click", async () => {
      try {
        const resultado = await requisicao("/api/laboratorio/caixa", {
          estado: estadoCaixa(),
          acao: "cadastrar_produto",
          dados: {
            nome: document.querySelector("#cx-produto")?.value || "",
            preco: document.querySelector("#cx-preco")?.value || "",
            estoque: document.querySelector("#cx-estoque")?.value || "",
          },
        });
        if (!resultado.response.ok) return mensagemErro(resumo, resultado, "Não foi possível cadastrar o produto.");
        salvar(CHAVES.caixa, resultado.corpo.estado);
        renderCaixa(`Produto ${resultado.corpo.resultado.nome} cadastrado pelo Python.`);
      } catch (_erro) {
        resumo.textContent = "Backend indisponível no momento.";
      }
    });

    adicionar?.addEventListener("click", async () => {
      try {
        const resultado = await requisicao("/api/laboratorio/caixa", {
          estado: estadoCaixa(),
          acao: "adicionar_carrinho",
          dados: { codigo: selecao?.value || "", quantidade: document.querySelector("#cx-qtd")?.value || "" },
        });
        if (!resultado.response.ok) return mensagemErro(resumo, resultado, "Não foi possível adicionar ao carrinho.");
        salvar(CHAVES.caixa, resultado.corpo.estado);
        renderCaixa("Item validado e adicionado pelo backend Python.");
      } catch (_erro) {
        resumo.textContent = "Backend indisponível no momento.";
      }
    });

    desconto?.addEventListener("input", () => renderCaixa());

    fechar?.addEventListener("click", async () => {
      try {
        const resultado = await requisicao("/api/laboratorio/caixa", {
          estado: estadoCaixa(),
          acao: "fechar_venda",
          dados: { desconto: desconto?.value || 0 },
        });
        if (!resultado.response.ok) return mensagemErro(resumo, resultado, "Não foi possível fechar a venda.");
        salvar(CHAVES.caixa, resultado.corpo.estado);
        renderCaixa(`Venda #${resultado.corpo.resultado.id} fechada pelo Python. Total: ${moeda.format(resultado.corpo.resultado.total)}.`);
      } catch (_erro) {
        resumo.textContent = "Backend indisponível no momento.";
      }
    });

    renderCaixa();
  }

  // 07 — Controle financeiro
  const financeiroCard = document.querySelector("#financeiro");
  if (financeiroCard) {
    const adicionar = clonarSemListeners("#fin-adicionar");
    const lista = document.querySelector("#fin-lista");
    const receitasEl = document.querySelector("#fin-receitas");
    const despesasEl = document.querySelector("#fin-despesas");
    const saldoEl = document.querySelector("#fin-saldo");
    const descricaoCard = financeiroCard.querySelector(".muted");

    if (descricaoCard) {
      descricaoCard.textContent = "Receitas, despesas, exclusões e totais validados pelas funções Python reais do Mini Sistema 07.";
    }

    const estadoFinanceiro = () => {
      const valor = carregar(CHAVES.financeiro, []);
      return Array.isArray(valor) ? valor : [];
    };

    const renderFinanceiro = (mensagem = null) => {
      const lancamentos = estadoFinanceiro();
      lista?.replaceChildren();
      let receitas = 0;
      let despesas = 0;
      lancamentos.forEach((item) => {
        if (item.tipo === "receita") receitas += Number(item.valor || 0);
        else despesas += Number(item.valor || 0);
        const li = document.createElement("li");
        li.className = "item";
        const sinal = item.tipo === "receita" ? "+" : "-";
        const texto = document.createElement("span");
        texto.textContent = `${sinal} ${moeda.format(item.valor)} — ${item.categoria} — ${item.descricao}`;
        li.append(texto, criarBotao("Excluir", "danger", async () => {
          try {
            const resultado = await requisicao("/api/laboratorio/financeiro", {
              estado: estadoFinanceiro(), acao: "excluir", dados: { id: item.id },
            });
            if (!resultado.response.ok) return;
            salvar(CHAVES.financeiro, resultado.corpo.lancamentos);
            renderFinanceiro();
          } catch (_erro) {
            // Mantém o estado atual quando o backend estiver indisponível.
          }
        }));
        lista?.appendChild(li);
      });
      if (!lancamentos.length && lista) {
        const vazio = document.createElement("li");
        vazio.className = "muted";
        vazio.textContent = mensagem || "Nenhum lançamento.";
        lista.appendChild(vazio);
      }
      receitasEl.textContent = moeda.format(receitas);
      despesasEl.textContent = moeda.format(despesas);
      saldoEl.textContent = moeda.format(receitas - despesas);
    };

    adicionar?.addEventListener("click", async () => {
      try {
        const resultado = await requisicao("/api/laboratorio/financeiro", {
          estado: estadoFinanceiro(),
          acao: "adicionar",
          dados: {
            tipo: document.querySelector("#fin-tipo")?.value || "",
            descricao: document.querySelector("#fin-descricao")?.value || "",
            valor: document.querySelector("#fin-valor")?.value || "",
            categoria: document.querySelector("#fin-categoria")?.value || "",
            data: hoje,
          },
        });
        if (!resultado.response.ok) return;
        salvar(CHAVES.financeiro, resultado.corpo.lancamentos);
        renderFinanceiro();
      } catch (_erro) {
        // Mantém a interface utilizável sem corromper o estado local.
      }
    });

    renderFinanceiro();
  }

  // 08 — Gerenciador de hábitos
  const habitosCard = document.querySelector("#habitos");
  if (habitosCard) {
    const adicionar = clonarSemListeners("#hab-adicionar");
    const lista = document.querySelector("#hab-lista");
    const descricaoCard = habitosCard.querySelector(".muted");

    if (descricaoCard) {
      descricaoCard.textContent = "Criação, conclusão diária, sequência e progresso usam as funções Python reais do Mini Sistema 08.";
    }

    const estadoHabitos = () => {
      const valor = carregar(CHAVES.habitos, []);
      return Array.isArray(valor) ? valor : [];
    };

    function inicioSemanaISO() {
      const data = new Date(`${hoje}T12:00:00`);
      const dia = data.getDay() || 7;
      data.setDate(data.getDate() - dia + 1);
      return data.toISOString().slice(0, 10);
    }

    const renderHabitos = () => {
      const habitos = estadoHabitos();
      lista?.replaceChildren();
      const inicio = inicioSemanaISO();
      habitos.forEach((habito) => {
        const registros = Array.isArray(habito.registros) ? habito.registros : [];
        const meta = Number(habito.meta_semanal ?? habito.meta ?? 7);
        const feitos = registros.filter((data) => data >= inicio && data <= hoje).length;
        const percentual = Math.min(100, Math.round((feitos / meta) * 100));
        const concluiuHoje = registros.includes(hoje);
        const li = document.createElement("li");
        li.className = "item";
        const texto = document.createElement("span");
        texto.textContent = `${habito.nome} — ${feitos}/${meta} nesta semana (${percentual}%)`;
        const acoes = document.createElement("div");
        acoes.append(
          criarBotao(concluiuHoje ? "Desmarcar hoje" : "Concluir hoje", "secondary", async () => {
            try {
              const resultado = await requisicao("/api/laboratorio/habitos", {
                estado: estadoHabitos(),
                acao: concluiuHoje ? "desmarcar_hoje" : "marcar_hoje",
                dados: { id: habito.id, data: hoje },
              });
              if (!resultado.response.ok) return;
              salvar(CHAVES.habitos, resultado.corpo.habitos);
              renderHabitos();
            } catch (_erro) {
              // Mantém o estado atual.
            }
          }),
          criarBotao("Excluir", "danger", async () => {
            try {
              const resultado = await requisicao("/api/laboratorio/habitos", {
                estado: estadoHabitos(), acao: "excluir", dados: { id: habito.id },
              });
              if (!resultado.response.ok) return;
              salvar(CHAVES.habitos, resultado.corpo.habitos);
              renderHabitos();
            } catch (_erro) {
              // Mantém o estado atual.
            }
          })
        );
        li.append(texto, acoes);
        lista?.appendChild(li);
      });
      if (!habitos.length && lista) {
        const vazio = document.createElement("li");
        vazio.className = "muted";
        vazio.textContent = "Crie o primeiro hábito.";
        lista.appendChild(vazio);
      }
    };

    adicionar?.addEventListener("click", async () => {
      try {
        const resultado = await requisicao("/api/laboratorio/habitos", {
          estado: estadoHabitos(),
          acao: "criar",
          dados: {
            nome: document.querySelector("#hab-nome")?.value || "",
            meta: Number(document.querySelector("#hab-meta")?.value || 0),
          },
        });
        if (!resultado.response.ok) return;
        salvar(CHAVES.habitos, resultado.corpo.habitos);
        renderHabitos();
      } catch (_erro) {
        // Mantém o estado atual.
      }
    });

    renderHabitos();
  }
})();
