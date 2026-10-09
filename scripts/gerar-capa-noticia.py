#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera a capa de uma notícia do mural, em SVG, na linguagem visual do portal.

Por que gerar em vez de usar foto
---------------------------------
Foto de pessoa ou de terceiro só vai ao ar com autorização escrita, e a única
imagem de terceiro que o portal usa hoje está justamente com `autorizacao:
'PENDENTE'`. Uma capa desenhada a partir da paleta e dos motivos do próprio
site não tem esse problema e envelhece melhor.

O que NÃO entra na imagem
-------------------------
Nada que dependa de data: "inscrições abertas", prazo, contagem de vagas. A
página calcula a situação do processo a partir do cronograma justamente para
não anunciar prazo vencido — gravar "inscrições abertas" dentro de um JPG
reintroduziria o mesmo erro num lugar onde ninguém vai procurar. A imagem
carrega só o que continua verdadeiro: nível, turma e Programa.

    python3 scripts/gerar-capa-noticia.py
"""
import math, os, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, 'assets', 'img', 'mural')

W, H = 1280, 720
NAVY, NAVY_MID, NAVY_LIGHT = '#0B1F3A', '#122B50', '#1E3A5F'
AMBER, AMBER_LIGHT = '#B8860B', '#D9A521'


def favo(cx, cy, r):
    """Um hexágono de ponta para cima — o motivo de rede 2D que o portal já usa
    nas ilustrações das linhas de pesquisa."""
    p = []
    for i in range(6):
        a = math.radians(60 * i - 30)
        p.append('%.1f,%.1f' % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return '<polygon points="' + ' '.join(p) + '"/>'


def rede(x0, y0, cols, linhas, r):
    dx, dy = r * math.sqrt(3), r * 1.5
    saida = []
    for l in range(linhas):
        for c in range(cols):
            cx = x0 + c * dx + (dx / 2 if l % 2 else 0)
            saida.append(favo(cx, y0 + l * dy, r))
    return ''.join(saida)


def svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}" role="img">
  <defs>
    <linearGradient id="fundo" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{NAVY}"/>
      <stop offset="55%" stop-color="{NAVY_MID}"/>
      <stop offset="100%" stop-color="{NAVY_LIGHT}"/>
    </linearGradient>
    <pattern id="pontos" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="1.5" cy="1.5" r="1.5" fill="#fff" opacity=".07"/>
    </pattern>
    <linearGradient id="esmaece" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{NAVY}" stop-opacity="1"/>
      <stop offset="55%" stop-color="{NAVY}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#fundo)"/>
  <rect width="{W}" height="{H}" fill="url(#pontos)"/>

  <!-- Rede hexagonal, sangrando pela direita. Opacidade baixa: é textura,
       não ilustração; o texto tem de continuar sendo o que se lê primeiro. -->
  <g fill="none" stroke="#fff" stroke-width="1.6" opacity=".16">
    {rede(700, -60, 9, 11, 58)}
  </g>
  <!-- Véu que apaga a rede sob o texto, para o contraste não cair. -->
  <rect width="{W}" height="{H}" fill="url(#esmaece)" opacity=".92"/>

  <g font-family="Inter, 'DejaVu Sans', sans-serif">
    <rect x="96" y="150" width="54" height="5" rx="2.5" fill="{AMBER_LIGHT}"/>
    <text x="96" y="196" fill="{AMBER_LIGHT}" font-size="22" font-weight="800"
          letter-spacing="4.5">PROCESSO SELETIVO</text>

    <text x="96" y="296" fill="#fff" font-size="62" font-weight="800">Mestrado em</text>
    <text x="96" y="372" fill="#fff" font-size="62" font-weight="800">Engenharia de Materiais</text>

    <text x="96" y="470" fill="{AMBER_LIGHT}" font-size="44" font-weight="700">Turma 2027/1</text>

    <rect x="96" y="524" width="300" height="1" fill="#fff" opacity=".28"/>
    <text x="96" y="572" fill="#fff" font-size="23" font-weight="600" opacity=".82">
      REDEMAT · UFOP — UEMG</text>
    <text x="96" y="606" fill="#fff" font-size="19" font-weight="400" opacity=".55">
      Rede Temática em Engenharia de Materiais</text>

    <text x="{W - 96}" y="606" fill="#fff" font-size="18" font-weight="500"
          opacity=".5" text-anchor="end">Edital REDEMAT nº 7/2026</text>
  </g>
</svg>
'''


def main():
    os.makedirs(DEST, exist_ok=True)
    base = os.path.join(DEST, 'processo-seletivo-2027-1')
    with open(base + '.svg', 'w', encoding='utf-8') as f:
        f.write(svg())
    print('svg:', base + '.svg')

    # Rasteriza com o Chromium do Playwright: é o que existe aqui e o que
    # renderiza a fonte Inter do mesmo jeito que o navegador do visitante.
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('playwright ausente — ficou só o SVG'); return
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        p = b.new_page(viewport={'width': W, 'height': H})
        p.goto('file://' + base + '.svg')
        p.wait_for_timeout(400)
        p.screenshot(path=base + '.png')
        b.close()
    print('png:', base + '.png')
    for alvo, args in ((base + '.jpg', ['-quality', '86']),
                       (base + '.webp', ['-quality', '82'])):
        r = subprocess.run(['convert', base + '.png'] + args + [alvo],
                           capture_output=True)
        if r.returncode == 0:
            print('%s: %.0f KB' % (alvo, os.path.getsize(alvo) / 1024))
        else:
            print('não converteu', alvo, r.stderr.decode()[:100])


if __name__ == '__main__':
    main()
