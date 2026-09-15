#!/usr/bin/env python3
"""Gera SVGs estáticos do perfil usando apenas dados públicos do GitHub.

Os arquivos são publicados no branch gh-pages pelo workflow do perfil. Isso evita
que o README dependa de serviços terceiros de cards que podem aplicar rate limit.
"""

from __future__ import annotations

import json
import os
import urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path


USER = os.getenv("PROFILE_USER", "Videirafoo")
TOKEN = os.getenv("GITHUB_TOKEN", "")
OUTPUT_DIR = Path(os.getenv("PROFILE_OUTPUT_DIR", "dist"))

BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
TEXT = "#f0f6fc"
MUTED = "#8b949e"
ACCENT = "#58a6ff"
GREEN = "#3fb950"


def request_json(url: str, *, method: str = "GET", payload: dict | None = None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Videirafoo-profile-card-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def contribution_stats() -> dict | None:
    if not TOKEN:
        return None

    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays { date contributionCount }
            }
          }
        }
      }
    }
    """

    try:
        data = request_json(
            "https://api.github.com/graphql",
            method="POST",
            payload={"query": query, "variables": {"login": USER}},
        )
        calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        days = []
        for week in calendar["weeks"]:
            days.extend(week["contributionDays"])
        days.sort(key=lambda item: item["date"])

        longest = 0
        current_run = 0
        for item in days:
            if item["contributionCount"] > 0:
                current_run += 1
                longest = max(longest, current_run)
            else:
                current_run = 0

        by_date = {date.fromisoformat(item["date"]): item["contributionCount"] for item in days}
        cursor = datetime.now(timezone.utc).date()
        if by_date.get(cursor, 0) == 0:
            cursor -= timedelta(days=1)

        current = 0
        while by_date.get(cursor, 0) > 0:
            current += 1
            cursor -= timedelta(days=1)

        return {
            "total": int(calendar["totalContributions"]),
            "current": current,
            "longest": longest,
        }
    except Exception as exc:  # fallback: o card continua útil sem GraphQL
        print(f"Aviso: não foi possível obter contribuições: {exc}")
        return None


def svg_header(width: int, height: int, title: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">',
        "<style>",
        "text{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Inter,Arial,sans-serif}",
        ".title{fill:#f0f6fc;font-size:24px;font-weight:700}",
        ".label{fill:#8b949e;font-size:14px}",
        ".value{fill:#f0f6fc;font-size:30px;font-weight:700}",
        ".small{fill:#8b949e;font-size:12px}",
        "</style>",
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="{BG}" stroke="{BORDER}"/>',
        f'<text class="title" x="28" y="40">{escape(title)}</text>',
    ]


def metric(lines: list[str], x: int, y: int, label: str, value: str) -> None:
    lines.append(f'<text class="label" x="{x}" y="{y}">{escape(label)}</text>')
    lines.append(f'<text class="value" x="{x}" y="{y + 34}">{escape(value)}</text>')


def generate_cards() -> None:
    profile = request_json(f"https://api.github.com/users/{USER}")
    repos = request_json(
        f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=updated"
    )
    own_repos = [repo for repo in repos if not repo.get("fork")]

    public_repos = int(profile.get("public_repos", len(repos)))
    followers = int(profile.get("followers", 0))
    stars = sum(int(repo.get("stargazers_count", 0)) for repo in own_repos)
    forks = sum(int(repo.get("forks_count", 0)) for repo in own_repos)
    contributions = contribution_stats()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    metrics = svg_header(760, 230, "GitHub em números")
    metric(metrics, 30, 82, "Repositórios públicos", str(public_repos))
    metric(metrics, 210, 82, "Stars recebidas", str(stars))
    metric(metrics, 390, 82, "Forks recebidos", str(forks))
    metric(metrics, 570, 82, "Seguidores", str(followers))

    if contributions:
        metric(metrics, 30, 158, "Contribuições (12 meses)", str(contributions["total"]))
        metric(metrics, 260, 158, "Sequência atual", f'{contributions["current"]} dia(s)')
        metric(metrics, 480, 158, "Maior sequência", f'{contributions["longest"]} dia(s)')
    else:
        metrics.append(
            '<text class="small" x="30" y="178">Métricas de contribuição indisponíveis nesta execução.</text>'
        )

    updated = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    metrics.append(f'<text class="small" x="30" y="214">Atualizado automaticamente: {updated}</text>')
    metrics.append("</svg>")
    (OUTPUT_DIR / "profile-metrics.svg").write_text("\n".join(metrics), encoding="utf-8")

    language_counts = Counter(
        repo.get("language") for repo in own_repos if repo.get("language")
    )
    top_languages = language_counts.most_common(5)
    total_with_language = sum(language_counts.values()) or 1

    languages = svg_header(760, 250, "Linguagens por repositório")
    if not top_languages:
        languages.append('<text class="label" x="30" y="90">Nenhuma linguagem informada pela API.</text>')
    else:
        start_y = 78
        bar_x = 210
        bar_width = 500
        for index, (language, count) in enumerate(top_languages):
            y = start_y + index * 34
            pct = count / total_with_language
            width = max(14, int(bar_width * pct))
            languages.append(f'<text class="label" x="30" y="{y + 14}">{escape(language)}</text>')
            languages.append(f'<rect x="{bar_x}" y="{y}" width="{bar_width}" height="16" rx="8" fill="{PANEL}"/>')
            languages.append(f'<rect x="{bar_x}" y="{y}" width="{width}" height="16" rx="8" fill="{ACCENT}"/>')
            languages.append(f'<text class="small" x="{bar_x + bar_width - 4}" y="{y + 13}" text-anchor="end">{count} repo(s)</text>')

    languages.append(f'<text class="small" x="30" y="232">Base: {len(own_repos)} repositório(s) próprio(s) não-fork.</text>')
    languages.append("</svg>")
    (OUTPUT_DIR / "profile-languages.svg").write_text("\n".join(languages), encoding="utf-8")


if __name__ == "__main__":
    generate_cards()
