(() => {
  const STORAGE_KEY = "videirafoo_trilha_v1";
  const checks = Array.from(document.querySelectorAll(".mission-check"));
  const progressText = document.getElementById("progresso-texto");
  const progressBar = document.getElementById("progresso-barra");
  const resetButton = document.getElementById("resetar-progresso");

  function readProgress() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      const value = raw ? JSON.parse(raw) : [];
      return Array.isArray(value) ? new Set(value.filter((item) => typeof item === "string")) : new Set();
    } catch (_) {
      return new Set();
    }
  }

  function writeProgress(progress) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(progress)));
  }

  function renderProgress(progress) {
    checks.forEach((check) => {
      check.checked = progress.has(check.value);
    });

    const completed = checks.filter((check) => check.checked).length;
    const total = checks.length;
    const percent = total ? Math.round((completed / total) * 100) : 0;
    progressText.textContent = `${completed} de ${total} missões concluídas — ${percent}%`;
    progressBar.style.width = `${percent}%`;
    progressBar.setAttribute("aria-valuenow", String(percent));
  }

  let progress = readProgress();
  renderProgress(progress);

  checks.forEach((check) => {
    check.addEventListener("change", () => {
      if (check.checked) {
        progress.add(check.value);
      } else {
        progress.delete(check.value);
      }
      writeProgress(progress);
      renderProgress(progress);
    });
  });

  resetButton?.addEventListener("click", () => {
    progress = new Set();
    localStorage.removeItem(STORAGE_KEY);
    renderProgress(progress);
  });
})();
