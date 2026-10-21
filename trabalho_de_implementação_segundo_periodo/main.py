"""Gera 100.000 números aleatórios e compara nove algoritmos."""
import argparse
import random
from time import perf_counter

import selection_sort, bubble_sort, insertion_sort
import merge_sort, quick_sort, heap_sort
import counting_sort, radix_sort, bucket_sort

ALGORITMOS = {
    "selection": selection_sort.ordenar,
    "bubble": bubble_sort.ordenar,
    "insertion": insertion_sort.ordenar,
    "merge": merge_sort.ordenar,
    "quick": quick_sort.ordenar,
    "heap": heap_sort.ordenar,
    "counting": counting_sort.ordenar,
    "radix": radix_sort.ordenar,
    "bucket": bucket_sort.ordenar,
}
LENTOS = {"selection", "bubble", "insertion"}


def main():
    opcoes = argparse.ArgumentParser(description="Teste de ordenação")
    opcoes.add_argument("--algoritmo", choices=["todos", *ALGORITMOS], default="todos")
    opcoes.add_argument("--completo", action="store_true", help="Usa 100.000 em todos")
    args = opcoes.parse_args()

    # A mesma lista de 100 mil números para repetir os testes.
    gerador = random.Random(42)
    lista = [gerador.randint(0, 99999) for _ in range(100000)]
    print("Lista criada: 100.000 elementos")
    print(f"{'Algoritmo':<12} {'Elementos':>10} {'Tempo(s)':>12}  Teste")

    nomes = ALGORITMOS if args.algoritmo == "todos" else {args.algoritmo: ALGORITMOS[args.algoritmo]}
    for nome, funcao in nomes.items():
        # Os quadráticos usam amostra por padrão, para evitar espera longa.
        dados = lista[:1000] if nome in LENTOS and not args.completo else lista
        esperado = sorted(dados)
        inicio = perf_counter()
        resultado = funcao(dados)
        tempo = perf_counter() - inicio
        print(f"{nome:<12} {len(dados):>10} {tempo:>12.4f}  {'OK' if resultado == esperado else 'ERRO'}")

    if not args.completo:
        print("\nSelection, Bubble e Insertion: amostra de 1.000 números.")
        print("Para forçar 100.000 em um deles: --algoritmo bubble --completo")


if __name__ == "__main__":
    main()
