(() => {
  "use strict";

  const moeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
  const hoje = new Date().toISOString().slice(0, 10);

  const chaves = {
    agenda: "videirafoo-lab-agenda-v1",
    tarefas: "videirafoo-lab-tarefas-v1",
    estoque: "videirafoo-lab-estoque-v1",
    biblioteca: "videirafoo-lab-biblioteca-v1",
    caixaProdutos: "videirafoo-lab-caixa-produtos-v1",
    financeiro: "videirafoo-lab-financeiro-v1",
    habitos: "videirafoo-lab-habitos-v1",
    api: "videirafoo-lab-api-v1",
  };

  function carregar(chave, padrao = []) {
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

  function novoId() {
    return crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`;
  }

  function botao(rotulo, onClick, classe = "secondary") {
    const elemento = document.createElement("button");
    elemento.type = "button";
    elemento.className = classe;
    elemento.textContent = rotulo;
    elemento.addEventListener("click", onClick);
    return elemento;
  }

  function itemTexto(texto) {
    const span = document.createElement("span");
    span.textContent = texto;
    return span;
  }

  // 01 — Agenda de contatos
  let contatos = carregar(chaves.agenda);
  const agendaForm = document.querySelector("#agenda-form");
  const agendaNome = document.querySelector("#agenda-nome");
  const agendaTelefone = document.querySelector("#agenda-telefone");
  const agendaBusca = document.querySelector("#agenda-busca");
  const agendaLista = document.querySelector("#agenda-lista");

  function renderAgenda() {
    const termo = agendaBusca.value.trim().toLowerCase();
    const filtrados = contatos.filter((contato) =>
      `${contato.nome} ${contato.telefone}`.toLowerCase().includes(termo)
    );
    agendaLista.replaceChildren();
    if (!filtrados.length) {
      const vazio = document.createElement("li");
      vazio.className = "muted";
      vazio.textContent = contatos.length ? "Nenhum contato encontrado." : "Nenhum contato cadastrado.";
      agendaLista.appendChild(vazio);
      return;
    }
    filtrados.forEach((contato) => {
      const li = document.createElement("li");
      li.className = "item";
      li.append(
        itemTexto(`${contato.nome} — ${contato.telefone}`),
        botao("Excluir", () => {
          contatos = contatos.filter((item) => item.id !== contato.id);
          salvar(chaves.agenda, contatos);
          renderAgenda();
        }, "danger")
      );
      agendaLista.appendChild(li);
    });
  }

  agendaForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const nome = agendaNome.value.trim();
    const telefone = agendaTelefone.value.trim();
    if (!nome || !telefone) return;
    contatos.push({ id: novoId(), nome, telefone });
    salvar(chaves.agenda, contatos);
    agendaForm.reset();
    renderAgenda();
    agendaNome.focus();
  });
  agendaBusca.addEventListener("input", renderAgenda);
  renderAgenda();

  // 02 — Lista de tarefas
  let tarefas = carregar(chaves.tarefas);
  const tarefasForm = document.querySelector("#tarefas-form");
  const tarefaTexto = document.querySelector("#tarefa-texto");
  const tarefasLista = document.querySelector("#tarefas-lista");

  function renderTarefas() {
    tarefasLista.replaceChildren();
    if (!tarefas.length) {
      const vazio = document.createElement("li");
      vazio.className = "muted";
      vazio.textContent = "Nenhuma tarefa. Adicione a primeira.";
      tarefasLista.appendChild(vazio);
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
      check.setAttribute("aria-label", `Marcar ${tarefa.texto} como concluída`);
      const texto = itemTexto(tarefa.texto);
      if (tarefa.concluida) texto.className = "done";
      check.addEventListener("change", () => {
        tarefa.concluida = check.checked;
        salvar(chaves.tarefas, tarefas);
        renderTarefas();
      });
      principal.append(check, texto);
      li.append(principal, botao("Excluir", () => {
        tarefas = tarefas.filter((item) => item.id !== tarefa.id);
        salvar(chaves.tarefas, tarefas);
        renderTarefas();
      }, "danger"));
      tarefasLista.appendChild(li);
    });
  }

  tarefasForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const texto = tarefaTexto.value.trim();
    if (!texto) return;
    tarefas.push({ id: novoId(), texto, concluida: false });
    salvar(chaves.tarefas, tarefas);
    tarefaTexto.value = "";
    renderTarefas();
    tarefaTexto.focus();
  });
  renderTarefas();

  // 03 — Cadastro de aluno
  const alunoNome = document.querySelector("#aluno-nome");
  const notas = ["#nota-1", "#nota-2", "#nota-3"].map((seletor) => document.querySelector(seletor));
  const mediaResultado = document.querySelector("#media-resultado");
  document.querySelector("#calcular-media").addEventListener("click", () => {
    const nome = alunoNome.value.trim() || "Aluno";
    const valores = notas.map((campo) => Number(String(campo.value).replace(",", ".")));
    if (valores.some((nota) => !Number.isFinite(nota) || nota < 0 || nota > 10)) {
      mediaResultado.textContent = "Use três notas válidas entre 0 e 10.";
      return;
    }
    const media = valores.reduce((total, nota) => total + nota, 0) / valores.length;
    const situacao = media >= 7 ? "Aprovado" : media >= 5 ? "Recuperação" : "Reprovado";
    mediaResultado.textContent = `${nome}: média ${media.toFixed(2)} — ${situacao}.`;
  });

  // 04 — Controle de estoque
  let estoque = carregar(chaves.estoque);
  const estoqueForm = document.querySelector("#estoque-form");
  const produtoNome = document.querySelector("#produto-nome");
  const produtoQtd = document.querySelector("#produto-qtd");
  const produtoPreco = document.querySelector("#produto-preco");
  const estoqueLista = document.querySelector("#estoque-lista");
  const estoqueTotal = document.querySelector("#estoque-total");

  function renderEstoque() {
    estoqueLista.replaceChildren();
    if (!estoque.length) {
      const vazio = document.createElement("li");
      vazio.className = "muted";
      vazio.textContent = "Estoque vazio.";
      estoqueLista.appendChild(vazio);
    }
    estoque.forEach((produto) => {
      const li = document.createElement("li");
      li.className = "item";
      li.append(
        itemTexto(`${produto.nome} — ${produto.quantidade} × ${moeda.format(produto.preco)}`),
        botao("Excluir", () => {
          estoque = estoque.filter((item) => item.id !== produto.id);
          salvar(chaves.estoque, estoque);
          renderEstoque();
        }, "danger")
      );
      estoqueLista.appendChild(li);
    });
    const total = estoque.reduce((soma, produto) => soma + produto.quantidade * produto.preco, 0);
    estoqueTotal.textContent = `Valor do estoque: ${moeda.format(total)}`;
  }

  estoqueForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const nome = produtoNome.value.trim();
    const quantidade = Number(produtoQtd.value);
    const preco = Number(produtoPreco.value);
    if (!nome || !Number.isInteger(quantidade) || quantidade <= 0 || !Number.isFinite(preco) || preco < 0) return;
    estoque.push({ id: novoId(), nome, quantidade, preco });
    salvar(chaves.estoque, estoque);
    estoqueForm.reset();
    renderEstoque();
  });
  renderEstoque();

  // 05 — Biblioteca
  let biblioteca = carregar(chaves.biblioteca, { livros: [], usuarios: [], emprestimos: [] });
  if (!biblioteca || Array.isArray(biblioteca)) biblioteca = { livros: [], usuarios: [], emprestimos: [] };
  biblioteca.livros ||= [];
  biblioteca.usuarios ||= [];
  biblioteca.emprestimos ||= [];
  const bibStatus = document.querySelector("#bib-status");
  const bibLista = document.querySelector("#bib-lista");

  function salvarBiblioteca() {
    salvar(chaves.biblioteca, biblioteca);
    renderBiblioteca();
  }

  function renderBiblioteca() {
    bibLista.replaceChildren();
    biblioteca.livros.forEach((livro) => {
      const ativo = biblioteca.emprestimos.find((emp) => emp.isbn === livro.isbn && !emp.devolvido);
      const li = document.createElement("li");
      li.className = "item";
      const texto = ativo
        ? `${livro.titulo} (${livro.isbn}) — emprestado para ${ativo.documento}`
        : `${livro.titulo} (${livro.isbn}) — disponível`;
      const acoes = document.createElement("div");
      if (ativo) {
        acoes.appendChild(botao("Devolver", () => {
          ativo.devolvido = true;
          bibStatus.textContent = `Livro ${livro.titulo} devolvido.`;
          salvarBiblioteca();
        }));
      }
      li.append(itemTexto(texto), acoes);
      bibLista.appendChild(li);
    });
    if (!biblioteca.livros.length) {
      const vazio = document.createElement("li");
      vazio.className = "muted";
      vazio.textContent = "Nenhum livro cadastrado.";
      bibLista.appendChild(vazio);
    }
  }

  document.querySelector("#bib-add-livro").addEventListener("click", () => {
    const isbn = document.querySelector("#bib-isbn").value.trim();
    const titulo = document.querySelector("#bib-titulo").value.trim();
    if (!isbn || !titulo) return;
    if (biblioteca.livros.some((livro) => livro.isbn === isbn)) {
      bibStatus.textContent = "ISBN já cadastrado.";
      return;
    }
    biblioteca.livros.push({ isbn, titulo });
    bibStatus.textContent = `Livro ${titulo} cadastrado.`;
    salvarBiblioteca();
  });

  document.querySelector("#bib-add-usuario").addEventListener("click", () => {
    const documento = document.querySelector("#bib-doc").value.trim();
    const nome = document.querySelector("#bib-usuario").value.trim();
    if (!documento || !nome) return;
    if (biblioteca.usuarios.some((usuario) => usuario.documento === documento)) {
      bibStatus.textContent = "Documento já cadastrado.";
      return;
    }
    biblioteca.usuarios.push({ documento, nome });
    bibStatus.textContent = `Usuário ${nome} cadastrado.`;
    salvarBiblioteca();
  });

  document.querySelector("#bib-emprestar").addEventListener("click", () => {
    const isbn = document.querySelector("#bib-emprestimo-isbn").value.trim();
    const documento = document.querySelector("#bib-emprestimo-doc").value.trim();
    const livro = biblioteca.livros.find((item) => item.isbn === isbn);
    const usuario = biblioteca.usuarios.find((item) => item.documento === documento);
    const ativo = biblioteca.emprestimos.some((emp) => emp.isbn === isbn && !emp.devolvido);
    if (!livro) return void (bibStatus.textContent = "Livro não encontrado.");
    if (!usuario) return void (bibStatus.textContent = "Usuário não encontrado.");
    if (ativo) return void (bibStatus.textContent = "Livro já está emprestado.");
    biblioteca.emprestimos.push({ isbn, documento, devolvido: false });
    bibStatus.textContent = `${livro.titulo} emprestado para ${usuario.nome}.`;
    salvarBiblioteca();
  });
  renderBiblioteca();

  // 06 — Caixa de mercado
  let caixaProdutos = carregar(chaves.caixaProdutos);
  let carrinho = [];
  const cxSelecao = document.querySelector("#cx-selecao");
  const cxCarrinho = document.querySelector("#cx-carrinho");
  const cxResumo = document.querySelector("#cx-resumo");

  function salvarCaixa() {
    salvar(chaves.caixaProdutos, caixaProdutos);
    renderCaixa();
  }

  function renderCaixa() {
    cxSelecao.replaceChildren();
    caixaProdutos.forEach((produto) => {
      const option = document.createElement("option");
      option.value = produto.id;
      option.textContent = `${produto.nome} — ${moeda.format(produto.preco)} — estoque ${produto.estoque}`;
      cxSelecao.appendChild(option);
    });
    if (!caixaProdutos.length) {
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "Cadastre um produto primeiro";
      cxSelecao.appendChild(option);
    }

    cxCarrinho.replaceChildren();
    carrinho.forEach((item) => {
      const produto = caixaProdutos.find((p) => p.id === item.produtoId);
      if (!produto) return;
      const li = document.createElement("li");
      li.className = "item";
      li.append(
        itemTexto(`${produto.nome}: ${item.quantidade} × ${moeda.format(produto.preco)} = ${moeda.format(item.quantidade * produto.preco)}`),
        botao("Remover", () => {
          carrinho = carrinho.filter((c) => c.produtoId !== item.produtoId);
          renderCaixa();
        }, "danger")
      );
      cxCarrinho.appendChild(li);
    });

    const subtotal = carrinho.reduce((soma, item) => {
      const produto = caixaProdutos.find((p) => p.id === item.produtoId);
      return soma + (produto ? produto.preco * item.quantidade : 0);
    }, 0);
    const desconto = Math.min(100, Math.max(0, Number(document.querySelector("#cx-desconto").value) || 0));
    const total = subtotal * (1 - desconto / 100);
    cxResumo.textContent = carrinho.length
      ? `Subtotal: ${moeda.format(subtotal)}\nDesconto: ${desconto.toFixed(0)}%\nTotal: ${moeda.format(total)}`
      : "Carrinho vazio.";
  }

  document.querySelector("#cx-cadastrar").addEventListener("click", () => {
    const nome = document.querySelector("#cx-produto").value.trim();
    const preco = Number(document.querySelector("#cx-preco").value);
    const quantidade = Number(document.querySelector("#cx-estoque").value);
    if (!nome || !Number.isFinite(preco) || preco < 0 || !Number.isInteger(quantidade) || quantidade < 0) return;
    caixaProdutos.push({ id: novoId(), nome, preco, estoque: quantidade });
    salvarCaixa();
  });

  document.querySelector("#cx-adicionar").addEventListener("click", () => {
    const produtoId = cxSelecao.value;
    const quantidade = Number(document.querySelector("#cx-qtd").value);
    const produto = caixaProdutos.find((p) => p.id === produtoId);
    if (!produto || !Number.isInteger(quantidade) || quantidade <= 0) return;
    const existente = carrinho.find((item) => item.produtoId === produtoId);
    const totalReservado = (existente?.quantidade || 0) + quantidade;
    if (totalReservado > produto.estoque) {
      cxResumo.textContent = `Estoque insuficiente. Disponível: ${produto.estoque}.`;
      return;
    }
    if (existente) existente.quantidade = totalReservado;
    else carrinho.push({ produtoId, quantidade });
    renderCaixa();
  });

  document.querySelector("#cx-desconto").addEventListener("input", renderCaixa);
  document.querySelector("#cx-fechar").addEventListener("click", () => {
    if (!carrinho.length) return void (cxResumo.textContent = "Não é possível fechar um carrinho vazio.");
    carrinho.forEach((item) => {
      const produto = caixaProdutos.find((p) => p.id === item.produtoId);
      produto.estoque -= item.quantidade;
    });
    carrinho = [];
    salvarCaixa();
    cxResumo.textContent = "Venda fechada. O estoque foi atualizado.";
  });
  renderCaixa();

  // 07 — Controle financeiro
  let lancamentos = carregar(chaves.financeiro);
  const finLista = document.querySelector("#fin-lista");

  function renderFinanceiro() {
    finLista.replaceChildren();
    let receitas = 0;
    let despesas = 0;
    lancamentos.forEach((lancamento) => {
      if (lancamento.tipo === "receita") receitas += lancamento.valor;
      else despesas += lancamento.valor;
      const li = document.createElement("li");
      li.className = "item";
      const sinal = lancamento.tipo === "receita" ? "+" : "-";
      li.append(
        itemTexto(`${sinal} ${moeda.format(lancamento.valor)} — ${lancamento.categoria} — ${lancamento.descricao}`),
        botao("Excluir", () => {
          lancamentos = lancamentos.filter((item) => item.id !== lancamento.id);
          salvar(chaves.financeiro, lancamentos);
          renderFinanceiro();
        }, "danger")
      );
      finLista.appendChild(li);
    });
    if (!lancamentos.length) {
      const vazio = document.createElement("li");
      vazio.className = "muted";
      vazio.textContent = "Nenhum lançamento.";
      finLista.appendChild(vazio);
    }
    document.querySelector("#fin-receitas").textContent = moeda.format(receitas);
    document.querySelector("#fin-despesas").textContent = moeda.format(despesas);
    document.querySelector("#fin-saldo").textContent = moeda.format(receitas - despesas);
  }

  document.querySelector("#fin-adicionar").addEventListener("click", () => {
    const tipo = document.querySelector("#fin-tipo").value;
    const descricao = document.querySelector("#fin-descricao").value.trim();
    const valor = Number(document.querySelector("#fin-valor").value);
    const categoria = document.querySelector("#fin-categoria").value.trim();
    if (!descricao || !categoria || !Number.isFinite(valor) || valor <= 0) return;
    lancamentos.push({ id: novoId(), tipo, descricao, valor, categoria, data: hoje });
    salvar(chaves.financeiro, lancamentos);
    renderFinanceiro();
  });
  renderFinanceiro();

  // 08 — Hábitos
  let habitos = carregar(chaves.habitos);
  const habLista = document.querySelector("#hab-lista");

  function inicioSemanaISO() {
    const data = new Date(`${hoje}T12:00:00`);
    const dia = data.getDay() || 7;
    data.setDate(data.getDate() - dia + 1);
    return data.toISOString().slice(0, 10);
  }

  function registrosSemana(registros) {
    const inicio = inicioSemanaISO();
    return registros.filter((data) => data >= inicio && data <= hoje).length;
  }

  function renderHabitos() {
    habLista.replaceChildren();
    habitos.forEach((habito) => {
      const feitos = registrosSemana(habito.registros || []);
      const percentual = Math.min(100, Math.round((feitos / habito.meta) * 100));
      const concluiuHoje = (habito.registros || []).includes(hoje);
      const li = document.createElement("li");
      li.className = "item";
      const texto = itemTexto(`${habito.nome} — ${feitos}/${habito.meta} nesta semana (${percentual}%)`);
      const acoes = document.createElement("div");
      acoes.append(
        botao(concluiuHoje ? "Desmarcar hoje" : "Concluir hoje", () => {
          habito.registros ||= [];
          habito.registros = concluiuHoje
            ? habito.registros.filter((data) => data !== hoje)
            : [...habito.registros, hoje];
          salvar(chaves.habitos, habitos);
          renderHabitos();
        }),
        botao("Excluir", () => {
          habitos = habitos.filter((item) => item.id !== habito.id);
          salvar(chaves.habitos, habitos);
          renderHabitos();
        }, "danger")
      );
      li.append(texto, acoes);
      habLista.appendChild(li);
    });
    if (!habitos.length) {
      const vazio = document.createElement("li");
      vazio.className = "muted";
      vazio.textContent = "Crie o primeiro hábito.";
      habLista.appendChild(vazio);
    }
  }

  document.querySelector("#hab-adicionar").addEventListener("click", () => {
    const nome = document.querySelector("#hab-nome").value.trim();
    const meta = Number(document.querySelector("#hab-meta").value);
    if (!nome || !Number.isInteger(meta) || meta < 1 || meta > 7) return;
    if (habitos.some((habito) => habito.nome.toLowerCase() === nome.toLowerCase())) return;
    habitos.push({ id: novoId(), nome, meta, registros: [] });
    salvar(chaves.habitos, habitos);
    renderHabitos();
  });
  renderHabitos();

  // 09 — Simulador do contrato da API de tarefas
  let apiTarefas = carregar(chaves.api);
  const apiResposta = document.querySelector("#api-resposta");

  function proximoIdApi() {
    return apiTarefas.length ? Math.max(...apiTarefas.map((t) => t.id)) + 1 : 1;
  }

  function responderApi(status, corpo) {
    const texto = corpo === null ? "" : JSON.stringify(corpo, null, 2);
    apiResposta.textContent = `HTTP ${status}\n${texto}`.trim();
  }

  document.querySelector("#api-post").addEventListener("click", () => {
    const titulo = document.querySelector("#api-titulo").value.trim();
    const prioridade = document.querySelector("#api-prioridade").value;
    if (!titulo) return responderApi("400 Bad Request", { erro: "O título não pode ficar vazio." });
    const tarefa = { id: proximoIdApi(), titulo, prioridade, concluida: false };
    apiTarefas.push(tarefa);
    salvar(chaves.api, apiTarefas);
    responderApi("201 Created", tarefa);
  });

  document.querySelector("#api-get").addEventListener("click", () => responderApi("200 OK", apiTarefas));
  document.querySelector("#api-patch").addEventListener("click", () => {
    if (!apiTarefas.length) return responderApi("404 Not Found", { erro: "Tarefa não encontrada." });
    apiTarefas[0].concluida = !apiTarefas[0].concluida;
    salvar(chaves.api, apiTarefas);
    responderApi("200 OK", apiTarefas[0]);
  });
  document.querySelector("#api-delete").addEventListener("click", () => {
    if (!apiTarefas.length) return responderApi("404 Not Found", { erro: "Tarefa não encontrada." });
    apiTarefas.shift();
    salvar(chaves.api, apiTarefas);
    responderApi("204 No Content", null);
  });

  // 10 — Analisador local de repositórios
  document.querySelector("#repo-calcular").addEventListener("click", () => {
    const checks = [...document.querySelectorAll(".repo-check")];
    const score = checks.reduce((total, check) => total + (check.checked ? Number(check.dataset.pontos) : 0), 0);
    const faltando = checks.filter((check) => !check.checked).map((check) => check.parentElement.textContent.trim().replace(/\s*\(\d+\)$/, ""));
    document.querySelector("#repo-resultado").textContent =
      `Score: ${score}/100\n` +
      (faltando.length ? `Faltando: ${faltando.join(", ")}\nAção: adicione evidências objetivas antes de aumentar o score.` : "Todos os checks do exercício estão presentes.");
  });

  // Bônus — Busca binária
  const buscaLista = document.querySelector("#busca-lista");
  const buscaAlvo = document.querySelector("#busca-alvo");
  const buscaResultado = document.querySelector("#busca-resultado");
  document.querySelector("#executar-busca").addEventListener("click", () => {
    const numeros = buscaLista.value.split(",").map((valor) => Number(valor.trim())).filter((valor) => Number.isFinite(valor)).sort((a, b) => a - b);
    const alvo = Number(buscaAlvo.value.trim());
    if (!numeros.length || !Number.isFinite(alvo)) {
      buscaResultado.textContent = "Informe uma lista numérica separada por vírgulas e um alvo válido.";
      return;
    }
    let inicio = 0;
    let fim = numeros.length - 1;
    let passo = 1;
    let encontrado = -1;
    const linhas = [`Lista ordenada: [${numeros.join(", ")}]`];
    while (inicio <= fim) {
      const meio = Math.floor((inicio + fim) / 2);
      const valor = numeros[meio];
      linhas.push(`Passo ${passo}: início=${inicio}, meio=${meio}, fim=${fim}, valor=${valor}`);
      if (valor === alvo) {
        encontrado = meio;
        break;
      }
      if (valor < alvo) inicio = meio + 1;
      else fim = meio - 1;
      passo += 1;
    }
    linhas.push(encontrado >= 0 ? `Encontrado: ${alvo} no índice ${encontrado}.` : `Resultado: ${alvo} não está na lista.`);
    linhas.push(`Comparações realizadas: ${passo}.`);
    buscaResultado.textContent = linhas.join("\n");
  });
})();
