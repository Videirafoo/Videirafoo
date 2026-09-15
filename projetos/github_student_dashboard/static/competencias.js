(() => {
  const matrix = document.getElementById("matriz");
  const summary = document.getElementById("resumo");
  const updatedAt = document.getElementById("atualizacao");
  const refreshButton = document.getElementById("atualizar");
  const errorBox = document.getElementById("erro");

  const labels = {
    forte: "Evidência forte",
    parcial: "Evidência parcial",
    sem_evidencia: "Sem evidência verificada",
    indisponivel: "Verificação indisponível",
    verificada: "verificada",
    ausente: "ausente",
  };

  function text(tag, value, className) {
    const node = document.createElement(tag);
    node.textContent = value;
    if (className) node.className = className;
    return node;
  }

  function metric(value, label) {
    const node = document.createElement("div");
    node.className = "metric";
    node.append(text("strong", String(value)));
    node.append(text("span", label));
    return node;
  }

  function renderSummary(data) {
    const info = data.resumo || {};
    summary.replaceChildren(
      metric(info.total_competencias ?? 0, "competências avaliadas"),
      metric(`${info.evidencias_verificadas ?? 0}/${info.total_evidencias ?? 0}`, "evidências verificadas"),
      metric(info.forte ?? 0, "com evidência forte"),
      metric(info.parcial ?? 0, "com evidência parcial")
    );
  }

  function renderEvidence(item) {
    const box = document.createElement("div");
    box.className = "evidence";

    const top = document.createElement("div");
    top.className = "evidence-top";

    const title = document.createElement("div");
    const dot = text("span", "●", `dot ${item.estado}`);
    title.append(dot, document.createTextNode(` ${item.titulo}`));
    top.append(title);

    if (item.url) {
      const link = document.createElement("a");
      link.href = item.url;
      link.textContent = "Abrir evidência →";
      if (item.url.startsWith("http")) {
        link.target = "_blank";
        link.rel = "noreferrer";
      }
      top.append(link);
    }

    box.append(top, text("p", item.detalhe || labels[item.estado] || item.estado));
    return box;
  }

  function renderMatrix(data) {
    matrix.replaceChildren();
    for (const item of data.competencias || []) {
      const card = document.createElement("article");
      card.className = "card";

      const head = document.createElement("div");
      head.className = "card-head";
      const heading = document.createElement("div");
      heading.append(
        text("span", `Nível ${item.nivel}`, "level"),
        text("h2", item.titulo),
        text("p", item.descricao, "desc")
      );
      head.append(heading, text("span", labels[item.estado_evidencia] || item.estado_evidencia, `state state-${item.estado_evidencia}`));
      card.append(head);

      const list = document.createElement("div");
      list.className = "evidence-list";
      for (const evidence of item.evidencias || []) list.append(renderEvidence(evidence));
      card.append(list);

      const next = document.createElement("div");
      next.className = "next";
      next.append(text("strong", "Próximo passo: "), document.createTextNode(item.proximo_passo || "—"));
      card.append(next);
      matrix.append(card);
    }
  }

  async function loadMatrix() {
    refreshButton.disabled = true;
    errorBox.hidden = true;
    updatedAt.textContent = "Consultando evidências públicas…";
    try {
      const response = await fetch("/api/competencias", { headers: { Accept: "application/json" } });
      const data = await response.json();
      if (!response.ok) throw new Error(data.erro || `HTTP ${response.status}`);
      renderSummary(data);
      renderMatrix(data);
      const when = data.gerado_em ? new Date(data.gerado_em).toLocaleString("pt-BR") : "agora";
      updatedAt.textContent = `Última verificação: ${when}. Cache de até ${data.cache_segundos ?? 600}s para respeitar a API pública.`;
    } catch (error) {
      errorBox.textContent = `Não foi possível atualizar a matriz: ${error.message}`;
      errorBox.hidden = false;
      updatedAt.textContent = "Falha ao consultar as evidências.";
    } finally {
      refreshButton.disabled = false;
    }
  }

  refreshButton?.addEventListener("click", loadMatrix);
  loadMatrix();
})();
