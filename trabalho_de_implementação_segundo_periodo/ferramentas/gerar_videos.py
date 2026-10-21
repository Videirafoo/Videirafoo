"""Gera vídeos MP4 a partir das nove animações SVG do trabalho.

Uso (opcional): python ferramentas/gerar_videos.py
Requer: pip install cairosvg e FFmpeg instalado.
"""
from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import cairosvg

BASE = Path(__file__).resolve().parents[1]
SVG_NS = "{http://www.w3.org/2000/svg}"


def converter(arquivo):
    arvore = ET.parse(arquivo)
    raiz = arvore.getroot()
    quadros = raiz.findall(f".//{SVG_NS}g[@data-frame]")

    # Remove as animações: cada imagem será um estado parado.
    for grupo in quadros:
        for elemento in list(grupo):
            if elemento.tag == f"{SVG_NS}animate":
                grupo.remove(elemento)

    destino = BASE / "videos"
    destino.mkdir(exist_ok=True)
    nome = arquivo.stem

    with tempfile.TemporaryDirectory() as pasta:
        pasta = Path(pasta)
        for i, atual in enumerate(quadros):
            for grupo in quadros:
                grupo.set("opacity", "1" if grupo is atual else "0")
            png = pasta / f"quadro_{i:03}.png"
            cairosvg.svg2png(bytestring=ET.tostring(raiz), write_to=str(png))

        # Cada quadro dura meio segundo; vídeo sem áudio, com repetição no SVG original.
        entrada = str(pasta / "quadro_%03d.png")
        mp4 = destino / f"{nome}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-framerate", "2",
            "-i", entrada, "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(mp4)
        ], check=True)
        print(f"Vídeo gerado: {mp4.name} ({len(quadros)} etapas)")


if __name__ == "__main__":
    for arquivo in sorted((BASE / "animacoes").glob("*_sort.svg")):
        converter(arquivo)
