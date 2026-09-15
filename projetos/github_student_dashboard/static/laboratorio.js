(() => {
  "use strict";

  const STORAGE_TAREFAS = "videirafoo-lab-tarefas-v1";
  const STORAGE_ESTOQUE = "videirafoo-lab-estoque-v1";
  const moeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

  function carregar(chave) {
    try {
      const valor = JSON.parse(localStorage.getItem(chave) || "[]");
      return Array.isArray(valor) ? valor : [];
    } catch (_erro) {
      return [];
    }
  }

  function salvar(chave, valor) {
    localStorage.setItem(chave, JSON.stringify(valor));
  }

  function botaoRemover(rotulo, onClick) {
    const botao = document.createElement("button");
    botao.type = "button";
    botao.className = "secondary";
    botao.textContent = rotulo;
    botao.addEventListener("click", onClick);
    return botao;
  }

  let tarefas = carregar(STORAGE_TAREFAS);
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
      const texto = document.createElement("span");
      texto.textContent = tarefa.texto;
      if (tarefa.concluida) texto.className = "done";
      check.addEventListener("change", () => {
        tarefa.concluida = check.checked;
        salvar(STORAGE_TAREFAS, tarefas);
        renderTarefas();
      });
      principal.append(check, texto);
      li.append(principal, botaoRemover("Excluir", () => {
        tarefas = tarefas.filter((item) => item.id !== tarefa.id);
        salvar(STORAGE_TAREFAS, tarefas);
        renderTarefas();
      }));
      tarefasLista.appendChild(li);
    });
  }

  tarefasForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const texto = tarefaTexto.value.trim();
    if (!texto) return;
    tarefas.push({ id: crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`, texto, concluida: false });
    salvar(STORAGE_TAREFAS, tarefas);
    tarefaTexto.value = "";
    renderTarefas();
    tarefaTexto.focus();
  });
  renderTarefas();

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

  let estoque = carregar(STORAGE_ESTOQUE);
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
      const descricao = document.createElement("span");
      descricao.textContent = `${produto.nome} — ${produto.quantidade} × ${moeda.format(produto.preco)}`;
      li.append(descricao, botaoRemover("Excluir", () => {
        estoque = estoque.filter((item) => item.id !== produto.id);
        salvar(STORAGE_ESTOQUE, estoque);
        renderEstoque();
      }));
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
    estoque.push({ id: crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`, nome, quantidade, preco });
    salvar(STORAGE_ESTOQUE, estoque);
    estoqueForm.reset();
    renderEstoque();
    produtoNome.focus();
  });
  renderEstoque();

  const buscaLista = document.querySelector("#busca-lista");
  const buscaAlvo = document.querySelector("#busca-alvo");
  const buscaResultado = document.querySelector("#busca-resultado");

  document.querySelector("#executar-busca").addEventListener("click", () => {
    const numeros = buscaLista.value
      .split(",")
      .map((valor) => Number(valor.trim()))
      .filter((valor) => Number.isFinite(valor))
      .sort((a, b) => a - b);
    const alvo = Number(buscaAlvo.value.trim());
    if (!numeros.length || !Number.isFinite(alvo)) {
      buscaResultado.textContent = "Informe uma lista numérica separada por vírgulas e um alvo válido.";
      return;
    }

    let inicio = 0;
    let fim = numeros.length - 1;
    let passo = 1;
    const linhas = [`Lista ordenada: [${numeros.join(", ")}]`];
    let encontrado = -1;

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
