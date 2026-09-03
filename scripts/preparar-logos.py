#!/usr/bin/env python3
"""
preparar-logos.py — prepara logos de parceiros para o portal REDEMAT.

USO
    python3 scripts/preparar-logos.py <pasta-com-os-downloads> [--aplicar]

Sem --aplicar, apenas mostra o que faria (simulação).

O QUE FAZ
    1. Lê os slugs de parceiros de assets/js/site-data.js
    2. Casa cada arquivo da pasta com um slug, pelo nome
    3. Redimensiona para 120 px de altura, preservando proporção
    4. Torna transparente o fundo branco, quando detectado
    5. Grava em assets/img/parceiros/<slug>.png

O QUE NÃO FAZ
    Não baixa nada da internet. Baixe os arquivos você mesmo, respeitando a
    autorização de uso de cada marca — ver docs/logos-parceiros.md.
"""

import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "assets", "img", "parceiros")
ALTURA = 120


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def slugs_do_portal():
    """Extrai slug + nome do array parceiros.itens em site-data.js."""
    p = os.path.join(RAIZ, "assets", "js", "site-data.js")
    if not os.path.exists(p):
        sys.exit(f"ERRO: não encontrei {p}")
    txt = open(p, encoding="utf-8").read()
    pares = re.findall(r"nome:\s*'([^']+)',\s*slug:\s*'([^']+)'", txt)
    if not pares:
        sys.exit("ERRO: nenhum parceiro encontrado em site-data.js")
    return [{"nome": n, "slug": s} for n, s in pares]


def casar(arquivo, parceiros):
    """Casa um nome de arquivo com o parceiro mais provável."""
    base = norm(os.path.splitext(os.path.basename(arquivo))[0])
    if not base:
        return None
    # 1) slug exato dentro do nome do arquivo
    for p in parceiros:
        if norm(p["slug"]) and norm(p["slug"]) in base:
            return p
    # 2) nome da instituição dentro do nome do arquivo
    for p in parceiros:
        if norm(p["nome"]) and norm(p["nome"]) in base:
            return p
    # 3) primeira palavra do nome (>=4 letras) dentro do nome do arquivo
    for p in parceiros:
        prim = norm(p["nome"].split()[0])
        if len(prim) >= 4 and prim in base:
            return p
    return None


def processar(origem, destino, aplicar):
    try:
        from PIL import Image
    except ImportError:
        sys.exit("ERRO: Pillow não instalado. Rode: pip install pillow")

    im = Image.open(origem).convert("RGBA")
    px = im.load()
    w, h = im.size

    # fundo branco -> transparente, se os 4 cantos forem claros
    cantos = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    if all(c[0] > 240 and c[1] > 240 and c[2] > 240 for c in cantos):
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if r > 242 and g > 242 and b > 242:
                    px[x, y] = (r, g, b, 0)

    if h > ALTURA:
        im = im.resize((max(1, round(w * ALTURA / h)), ALTURA), Image.LANCZOS)

    if aplicar:
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        im.save(destino, optimize=True)
    return im.size


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    pasta = sys.argv[1]
    aplicar = "--aplicar" in sys.argv

    if not os.path.isdir(pasta):
        sys.exit(f"ERRO: pasta não encontrada: {pasta}")

    parceiros = slugs_do_portal()
    print(f"{len(parceiros)} parceiros cadastrados no portal\n")

    exts = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp")
    arquivos = [os.path.join(pasta, f) for f in sorted(os.listdir(pasta))
                if f.lower().endswith(exts)]
    if not arquivos:
        sys.exit(f"ERRO: nenhuma imagem em {pasta}")

    casados, sobraram = [], []
    for a in arquivos:
        p = casar(a, parceiros)
        (casados if p else sobraram).append((a, p))

    print(f"{'APLICANDO' if aplicar else 'SIMULAÇÃO'} — {len(casados)} de {len(arquivos)} arquivos casados\n")
    for a, p in casados:
        dest = os.path.join(DESTINO, p["slug"] + ".png")
        try:
            tam = processar(a, dest, aplicar)
            print(f"  {os.path.basename(a)[:38]:<40} -> {p['slug']}.png  ({tam[0]}x{tam[1]})")
        except Exception as e:
            print(f"  {os.path.basename(a)[:38]:<40} -> ERRO: {e}")

    if sobraram:
        print(f"\n{len(sobraram)} arquivo(s) sem correspondência — renomeie incluindo o slug:")
        for a, _ in sobraram:
            print(f"  {os.path.basename(a)}")
        print("\n  Slugs disponíveis:")
        for i in range(0, len(parceiros), 4):
            print("   " + "  ".join(f"{p['slug']:<16}" for p in parceiros[i:i + 4]))

    faltando = [p for p in parceiros
                if not os.path.exists(os.path.join(DESTINO, p["slug"] + ".png"))]
    if faltando:
        print(f"\n{len(faltando)} parceiro(s) ainda sem logo:")
        print("   " + ", ".join(p["nome"] for p in faltando))

    if not aplicar:
        print("\nNada foi gravado. Para gravar, rode de novo com --aplicar")
    else:
        print(f"\nGravado em {DESTINO}")
        print("Confira em http://localhost:8080/ — os cartões atualizam sozinhos.")


if __name__ == "__main__":
    main()
