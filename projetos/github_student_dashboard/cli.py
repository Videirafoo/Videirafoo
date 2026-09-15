import argparse
import json

from projetos.github_student_dashboard.engine import analisar_repositorio_remoto
from projetos.github_student_dashboard.github_client import GitHubApiError


def main():
    parser = argparse.ArgumentParser(
        description="Analisa um repositório público do GitHub com checks determinísticos."
    )
    parser.add_argument("repositorio", help="Formato: usuario/repositorio")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Exibe o relatório completo em JSON.",
    )
    argumentos = parser.parse_args()

    try:
        relatorio = analisar_repositorio_remoto(argumentos.repositorio)
    except (ValueError, GitHubApiError) as erro:
        print(f"Erro: {erro}")
        raise SystemExit(1) from erro

    if argumentos.json:
        print(json.dumps(relatorio, ensure_ascii=False, indent=2))
        return

    print(f"\n=== {relatorio['repositorio']} ===")
    print(f"Score: {relatorio['score']}/100")

    print("\nChecks:")
    for nome, passou in relatorio["checks"].items():
        print(f"- {nome}: {'OK' if passou else 'FALTA'}")

    if relatorio["recomendacoes"]:
        print("\nPróximas melhorias:")
        for item in relatorio["recomendacoes"]:
            print(f"- [{item['prioridade']}] {item['acao']}")
    else:
        print("\nNenhuma ausência encontrada nos checks atuais.")


if __name__ == "__main__":
    main()
