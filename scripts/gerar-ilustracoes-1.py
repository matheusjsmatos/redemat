#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar-ilustracoes.py — desenha as ilustrações do portal em SVG.

USO
    python3 scripts/gerar-ilustracoes.py

POR QUE GERAR EM VEZ DE BAIXAR
    Não é possível baixar imagens nesta sessão, e imagem de banco de imagens
    sobre "ciência" costuma ser genérica ou de licença duvidosa. Estas são
    desenhadas a partir do próprio objeto de estudo: a rede moiré vem da
    matemática de duas redes triangulares giradas uma em relação à outra; a
    curva de transformação de fase vem da forma de uma curva TTC; a
    microestrutura vem de um diagrama de Voronoi. São ilustrações, não dados —
    mas a forma é a forma certa.

    SVG, e não bitmap: escala em qualquer tela, pesa poucos KB, e o texto
    dentro delas continua sendo texto.

SAÍDA
    assets/img/ilustra/*.svg
"""

import io
import math
import re
import os
import random

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, 'assets', 'img', 'ilustra')

# paleta espelhando os tokens de assets/css/styles.css
NAVY = '#0B1F3A'
NAVY_MID = '#16324F'
AMBER = '#B8860B'
AMBER_L = '#D9A521'
A1 = '#1D6FA5'
A2 = '#1B8A6B'
L11 = '#1D6FA5'
L12 = '#4C6FBF'
L21 = '#1B8A6B'
L22 = '#8B5CB8'
CLARO = '#F7F9FB'


def cabeca(w, h, titulo, desc, fundo=CLARO):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'role="img" aria-labelledby="t d" preserveAspectRatio="xMidYMid slice">\n'
        '<title id="t">%s</title><desc id="d">%s</desc>\n'
        '<rect width="%d" height="%d" fill="%s"/>\n' % (w, h, titulo, desc, w, h, fundo))


def grava(nome, svg):
    """Grava duas versões de cada ilustração:

    · nome.svg       — completa, com os rótulos. Vai em cartão e figura, onde
                       a legenda dentro do desenho ajuda.
    · nome-hero.svg  — sem nenhum <text>. Vai como fundo de hero, onde o
                       texto do desenho apareceria por trás do título da
                       página e competiria com ele.
    """
    os.makedirs(SAIDA, exist_ok=True)
    caminho = os.path.join(SAIDA, nome)
    io.open(caminho, 'w', encoding='utf-8').write(svg + '</svg>\n')

    sem = re.sub(r'<text\b.*?</text>', '', svg, flags=re.S)
    sem = re.sub(r'<g[^>]*>\s*</g>', '', sem)          # grupos que ficaram vazios
    hero = os.path.join(SAIDA, nome.replace('.svg', '-hero.svg'))
    io.open(hero, 'w', encoding='utf-8').write(sem + '</svg>\n')
    return caminho


# ---------------------------------------------------------------- moiré
def moire(nome='moire.svg', w=800, h=420, a=26.0, theta=5.5):
    """Duas redes triangulares giradas de `theta` graus: o padrão de larga
    escala que aparece é a super-rede moiré, com período a/(2 sin(theta/2)).
    É o objeto do artigo na Nature Nanotechnology — MoS2 sobre WSe2."""
    svg = cabeca(w, h, 'Super-rede moiré de duas redes triangulares giradas',
                 'Duas redes atômicas triangulares sobrepostas com pequeno ângulo de giro. '
                 'A interferência entre elas gera um padrão de larga escala, a super-rede moiré, '
                 'cujo período cresce quando o ângulo de giro diminui.', '#081729')

    # halo de fundo
    svg += ('<defs><radialGradient id="g" cx="50%%" cy="45%%" r="70%%">'
            '<stop offset="0" stop-color="#123A5E"/><stop offset="1" stop-color="#081729"/>'
            '</radialGradient></defs>'
            '<rect width="%d" height="%d" fill="url(#g)"/>\n' % (w, h))

    def rede(ang, cor, r, op):
        s = '<g fill="%s" opacity="%.2f">' % (cor, op)
        t = math.radians(ang)
        n = int(max(w, h) / a) + 6
        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                # base triangular
                x = a * (i + 0.5 * j)
                y = a * (math.sqrt(3) / 2) * j
                xr = x * math.cos(t) - y * math.sin(t) + w / 2
                yr = x * math.sin(t) + y * math.cos(t) + h / 2
                if -a < xr < w + a and -a < yr < h + a:
                    # r por círculo: em SVG o atributo r não é herdado do grupo
                    s += '<circle cx="%.0f" cy="%.0f" r="%.1f"/>' % (xr, yr, r)
        return s + '</g>\n'

    svg += rede(0, '#6FB3E0', 3.0, 0.75)
    svg += rede(theta, '#D9A521', 3.0, 0.75)

    # células moiré: período L = a / (2 sin(theta/2))
    L = a / (2 * math.sin(math.radians(theta) / 2))
    svg += '<g fill="none" stroke="#FFFFFF" stroke-opacity=".22" stroke-width="1.2">'
    for i in range(-3, 4):
        for j in range(-2, 3):
            cx = w / 2 + L * (i + 0.5 * j)
            cy = h / 2 + L * (math.sqrt(3) / 2) * j
            if -L < cx < w + L and -L < cy < h + L:
                pts = ' '.join('%.0f,%.0f' % (cx + L / math.sqrt(3) * math.cos(math.radians(60 * k + 30)),
                                              cy + L / math.sqrt(3) * math.sin(math.radians(60 * k + 30)))
                               for k in range(6))
                svg += '<polygon points="%s"/>' % pts
    svg += '</g>\n'

    svg += ('<text x="30" y="%d" font-family="Inter,system-ui,sans-serif" font-size="13" '
            'font-weight="700" fill="#FFFFFF" opacity=".85">MoS'
            '<tspan baseline-shift="sub" font-size="10">2</tspan> / WSe'
            '<tspan baseline-shift="sub" font-size="10">2</tspan> — giro de %.1f°</text>\n'
            % (h - 26, theta))
    return grava(nome, svg)


# ------------------------------------------------------- microestrutura
def microestrutura(nome='area-1.svg', w=800, h=420, semente=7):
    """Grãos por diagrama de Voronoi + curva de resfriamento: a forma da
    metalografia e a forma de uma curva de transformação sob resfriamento
    contínuo — do que a Área 1 trata.

    Voronoi de verdade, recortado na moldura: 46 polígonos em vez de milhares
    de quadradinhos. Sai um arquivo ~40x menor e um contorno de grão limpo."""
    rnd = random.Random(semente)
    svg = cabeca(w, h, 'Microestrutura de grãos e curva de transformação',
                 'Mosaico de grãos, como numa metalografia, ao lado de uma curva de '
                 'transformação de fase sob resfriamento contínuo.', '#0E2438')
    cores = ['#17405F', '#1D5478', '#123650', '#22648C', '#0F2C43', '#2A7099']
    sementes = [(rnd.uniform(-60, w + 60), rnd.uniform(-60, h + 60)) for _ in range(52)]
    celulas = _voronoi_recortado(sementes, -20, -20, w + 20, h + 20)
    svg += '<g stroke="#0A1B2B" stroke-opacity=".55" stroke-width="1.4">'
    for k, poli in enumerate(celulas):
        if len(poli) < 3:
            continue
        pts = ' '.join('%.0f,%.0f' % pt for pt in poli)
        svg += '<polygon points="%s" fill="%s"/>' % (pts, cores[k % len(cores)])
    svg += '</g>\n'
    # curva de resfriamento contínuo
    d = 'M 60 %d' % (h - 60)
    for i in range(1, 61):
        x = 60 + i * (w - 160) / 60.0
        y = (h - 60) - (h - 150) * (1 - math.exp(-3.2 * i / 60.0))
        d += ' L %.0f %.0f' % (x, y)
    svg += ('<path d="%s" fill="none" stroke="#D9A521" stroke-width="3.4" '
            'stroke-linecap="round"/>\n' % d)
    svg += ('<text x="60" y="%d" font-size="12" font-weight="700" fill="#FFFFFF" '
            'opacity=".85" font-family="Inter,system-ui,sans-serif">'
            'Processamento &#183; estrutura &#183; desempenho</text>\n' % (h - 28))
    return grava(nome, svg)


def _voronoi_recortado(sementes, x0, y0, x1, y1):
    """Células de Voronoi recortadas no retângulo, por corte sucessivo de
    meio-plano (Sutherland-Hodgman). Sem dependência externa: o algoritmo é
    curto e o resultado é exato para a moldura."""
    def corta(poli, a, b, c):
        """Mantém o lado a*x + b*y <= c."""
        saida = []
        n = len(poli)
        for i in range(n):
            px, py = poli[i]
            qx, qy = poli[(i + 1) % n]
            dp = a * px + b * py - c
            dq = a * qx + b * qy - c
            if dp <= 0:
                saida.append((px, py))
            if (dp < 0 < dq) or (dq < 0 < dp):
                t = dp / (dp - dq)
                saida.append((px + t * (qx - px), py + t * (qy - py)))
        return saida

    out = []
    for (sx, sy) in sementes:
        poli = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for (ox, oy) in sementes:
            if (ox, oy) == (sx, sy):
                continue
            # mediatriz entre a semente e a outra: metade mais perto da semente
            a, b = 2 * (ox - sx), 2 * (oy - sy)
            c = ox * ox + oy * oy - sx * sx - sy * sy
            poli = corta(poli, a, b, c)
            if len(poli) < 3:
                break
        out.append(poli)
    return out


# --------------------------------------------------- economia circular
def circular(nome='area-2.svg', w=800, h=420):
    """Ciclo fechado recurso → material → produto → resíduo → recurso, com
    um nó destacado: é a leitura da Área 2."""
    svg = cabeca(w, h, 'Ciclo de materiais e economia circular',
                 'Ciclo fechado ligando recurso mineral, material, produto e resíduo, '
                 'indicando o reaproveitamento que caracteriza a economia circular.', '#0B2A22')
    cx, cy, R = w / 2, h / 2, 132
    svg += ('<circle cx="%.0f" cy="%.0f" r="%d" fill="none" stroke="#2FA983" '
            'stroke-width="2.4" stroke-dasharray="7 9" opacity=".85"/>\n' % (cx, cy, R))
    etapas = [('Recurso\nmineral', '#2FA983'), ('Processo\nmetalúrgico', '#6FB3E0'),
              ('Material\nfuncional', '#D9A521'), ('Produto', '#C9A6E8'),
              ('Resíduo e\ncoproduto', '#7FD8B8')]
    for k, (rot, cor) in enumerate(etapas):
        ang = math.radians(-90 + k * 360.0 / len(etapas))
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        svg += '<circle cx="%.1f" cy="%.1f" r="34" fill="%s" opacity=".92"/>' % (x, y, cor)
        linhas = rot.split('\n')
        for li, ln in enumerate(linhas):
            svg += ('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10.5" '
                    'font-weight="700" font-family="Inter,system-ui,sans-serif" fill="#082018">%s</text>'
                    % (x, y + 3 + (li - (len(linhas) - 1) / 2.0) * 12, ln))
        # seta para o próximo
        ang2 = math.radians(-90 + (k + 0.5) * 360.0 / len(etapas))
        svg += ('<path d="M %.1f %.1f l -7 -5 l 0 10 z" fill="#2FA983" opacity=".9"/>'
                % (cx + R * math.cos(ang2), cy + R * math.sin(ang2)))
    svg += ('<text x="%.0f" y="%.0f" text-anchor="middle" font-size="12.5" font-weight="800" '
            'font-family="Inter,system-ui,sans-serif" fill="#FFFFFF" opacity=".85">'
            'Materiais estratégicos,</text>'
            '<text x="%.0f" y="%.0f" text-anchor="middle" font-size="12.5" font-weight="800" '
            'font-family="Inter,system-ui,sans-serif" fill="#FFFFFF" opacity=".85">'
            'funcionais e sustentáveis</text>\n' % (cx, cy - 4, cx, cy + 13))
    return grava(nome, svg)


# ------------------------------------------------------------ superfície
def superficie(nome='linha-11.svg', w=560, h=300):
    """Substrato, camadas de revestimento e zona afetada por um feixe: a
    geometria de um tratamento de superfície a laser."""
    svg = cabeca(w, h, 'Camadas de revestimento e zona afetada por feixe',
                 'Substrato com camadas de revestimento e uma zona afetada pelo calor de um '
                 'feixe de laser incidente, como em tratamento e modificação de superfícies.',
                 '#0E2438')
    # pilha: substrato grosso, intercamada, revestimento
    pilha = [(h - 150, 150, '#123650', 'substrato'),
             (h - 176, 26, '#1B4A6B', 'intercamada'),
             (h - 196, 20, '#2A7099', 'revestimento')]
    for y, alt, cor, _ in pilha:
        svg += '<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y, w, alt, cor)
    topo = h - 196
    # feixe estreito, com halo
    fx = int(w * 0.42)
    svg += ('<path d="M %d 34 L %d %d L %d %d Z" fill="#D9A521" opacity=".20"/>'
            % (fx, fx - 20, topo, fx + 20, topo))
    svg += '<line x1="%d" y1="34" x2="%d" y2="%d" stroke="#FFD873" stroke-width="3"/>' % (fx, fx, topo)
    # zona afetada pelo calor: meia-elipse PARA DENTRO das camadas, recortada
    # na superfície — a poça de fusão cresce para baixo, não para cima
    svg += ('<clipPath id="dentro"><rect x="0" y="%d" width="%d" height="%d"/></clipPath>'
            % (topo, w, h - topo))
    svg += ('<g clip-path="url(#dentro)">'
            '<ellipse cx="%d" cy="%d" rx="52" ry="58" fill="#D9A521" opacity=".26"/>'
            '<ellipse cx="%d" cy="%d" rx="34" ry="36" fill="#FFD873" opacity=".22"/></g>'
            % (fx, topo, fx, topo))
    svg += '<ellipse cx="%d" cy="%d" rx="52" ry="7" fill="#FFD873" opacity=".7"/>' % (fx, topo)
    # respingos
    rnd = random.Random(5)
    for _ in range(16):
        svg += ('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#FFFFFF" opacity="%.2f"/>'
                % (fx + rnd.uniform(-72, 72), topo - rnd.uniform(4, 34),
                   rnd.uniform(1.4, 2.6), rnd.uniform(.35, .8)))
    # rótulos das camadas
    for y, alt, _, rot in pilha:
        svg += ('<text x="%d" y="%d" text-anchor="end" font-size="10" fill="#FFFFFF" '
                'opacity=".6" font-family="Inter,system-ui,sans-serif">%s</text>'
                % (w - 14, y + alt / 2 + 4, rot))
    svg += ('<text x="18" y="26" font-size="11.5" font-weight="700" fill="#FFFFFF" opacity=".85" '
            'font-family="Inter,system-ui,sans-serif">Processamento, manufatura e superf&#237;cies</text>\n')
    return grava(nome, svg)


# ------------------------------------------------------------ integridade
def integridade(nome='linha-12.svg', w=560, h=300):
    """Curva S-N (Wöhler) com trinca: fadiga, fratura e integridade."""
    svg = cabeca(w, h, 'Curva de fadiga e trinca',
                 'Curva tensão-vida decrescente com patamar, ao lado de uma trinca ramificada — '
                 'o par que caracteriza estudos de fadiga, fratura e integridade.', '#101E38')
    x0, y0, x1, y1 = 64, 40, w - 30, h - 56
    svg += ('<g stroke="#FFFFFF" stroke-opacity=".18" stroke-width="1">'
            + ''.join('<line x1="%d" y1="%.0f" x2="%d" y2="%.0f"/>'
                      % (x0, y0 + k * (y1 - y0) / 4.0, x1, y0 + k * (y1 - y0) / 4.0)
                      for k in range(5)) + '</g>')
    svg += ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#FFFFFF" stroke-opacity=".45"/>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#FFFFFF" stroke-opacity=".45"/>'
            % (x0, y0, x0, y1, x0, y1, x1, y1))
    d = 'M %d %d' % (x0, y0 + 14)
    for i in range(1, 81):
        t = i / 80.0
        x = x0 + t * (x1 - x0)
        y = y0 + 14 + (y1 - y0 - 40) * (1 - math.exp(-3.4 * t))
        d += ' L %.1f %.1f' % (x, y)
    svg += ('<path d="%s" fill="none" stroke="#7F9BE0" stroke-width="3.4" stroke-linecap="round"/>\n'
            % d)
    # trinca ramificada
    tr = 'M %d %d' % (x1 - 130, y1 - 12)
    px, py = x1 - 130, y1 - 12
    rnd = random.Random(3)
    for _ in range(9):
        px += rnd.uniform(6, 15)
        py -= rnd.uniform(4, 13)
        tr += ' L %.1f %.1f' % (px, py)
    svg += '<path d="%s" fill="none" stroke="#D9A521" stroke-width="2.4" stroke-linejoin="round"/>' % tr
    svg += ('<text x="%d" y="30" font-size="10.5" fill="#FFFFFF" opacity=".65" '
            'font-family="Inter,system-ui,sans-serif">tensão</text>'
            '<text x="%d" y="%d" text-anchor="end" font-size="10.5" fill="#FFFFFF" opacity=".65" '
            'font-family="Inter,system-ui,sans-serif">ciclos até a falha</text>' % (x0 - 46, x1, y1 + 20))
    svg += ('<text x="18" y="%d" font-size="11.5" font-weight="700" fill="#FFFFFF" opacity=".8" '
            'font-family="Inter,system-ui,sans-serif">Estrutura, degradação e integridade</text>\n'
            % (h - 14))
    return grava(nome, svg)


# ------------------------------------------------------- hidrometalurgia
def hidrometalurgia(nome='linha-21.svg', w=560, h=300):
    """Coluna de separação com gradiente e íons metálicos recuperados em
    sequência: a leitura de hidrometalurgia e minerais críticos."""
    svg = cabeca(w, h, 'Separa&#231;&#227;o em coluna e recupera&#231;&#227;o de metais',
                 'Coluna de separação com gradiente de concentração e íons metálicos recuperados '
                 'em alturas diferentes, como em processos hidrometalúrgicos.', '#0B2A22')
    svg += ('<defs><linearGradient id="col" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#3FC79A"/><stop offset="1" stop-color="#0C4433"/>'
            '</linearGradient></defs>')
    cx = int(w * 0.62)
    lar, top, alt = 92, 52, h - 116
    svg += '<rect x="%d" y="%d" width="%d" height="%d" rx="16" fill="url(#col)" opacity=".92"/>' % (
        cx - lar // 2, top, lar, alt)
    rnd = random.Random(11)
    for _ in range(44):
        svg += ('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#FFFFFF" opacity="%.2f"/>'
                % (cx - lar / 2 + rnd.uniform(9, lar - 9), top + rnd.uniform(8, alt - 8),
                   rnd.choice([2.0, 2.8, 3.6]), rnd.uniform(.3, .85)))
    # metais recuperados, cada um numa altura
    metais = ['Li', 'Ni', 'Co', 'Terras raras']
    for k, rot in enumerate(metais):
        y = top + 34 + k * (alt - 68) / (len(metais) - 1.0)
        svg += ('<text x="30" y="%.0f" font-size="11.5" font-weight="700" fill="#7FD8B8" '
                'font-family="Inter,system-ui,sans-serif">%s</text>' % (y + 4, rot))
        svg += ('<line x1="%d" y1="%.0f" x2="%d" y2="%.0f" stroke="#7FD8B8" '
                'stroke-opacity=".45" stroke-dasharray="4 4"/>'
                % (30 + 8.5 * len(rot) + 10, y, cx - lar // 2 - 8, y))
        svg += ('<path d="M %d %.0f l -7 -4 l 0 8 z" fill="#7FD8B8" opacity=".8"/>'
                % (cx - lar // 2 - 6, y))
    svg += ('<text x="18" y="30" font-size="11.5" font-weight="700" fill="#FFFFFF" opacity=".85" '
            'font-family="Inter,system-ui,sans-serif">Minerais cr&#237;ticos e economia circular</text>\n')
    return grava(nome, svg)


# ------------------------------------------------------- material 2D/dispositivo
def dispositivo(nome='linha-22.svg', w=560, h=300):
    """Folha 2D hexagonal sobre eletrodos: materiais funcionais e dispositivos."""
    svg = cabeca(w, h, 'Folha bidimensional sobre eletrodos',
                 'Rede hexagonal de um material bidimensional apoiada em dois eletrodos, '
                 'a geometria típica de um dispositivo de teste.', '#1A1030')
    # eletrodos
    svg += '<rect x="40" y="%d" width="120" height="26" rx="4" fill="#D9A521"/>' % (h - 96)
    svg += '<rect x="%d" y="%d" width="120" height="26" rx="4" fill="#D9A521"/>' % (w - 160, h - 96)
    # folha hexagonal
    svg += '<g fill="none" stroke="#C9A6E8" stroke-width="1.6" opacity=".9">'
    a = 26.0
    for j in range(-1, 5):
        for i in range(-1, 13):
            cx = 60 + a * 1.5 * i
            cy = (h - 120) - a * math.sqrt(3) * j - (a * math.sqrt(3) / 2 if i % 2 else 0)
            if cy < 20 or cy > h - 100:
                continue
            pts = ' '.join('%.1f,%.1f' % (cx + a * math.cos(math.radians(60 * k)),
                                          cy + a * math.sin(math.radians(60 * k)))
                           for k in range(6))
            svg += '<polygon points="%s"/>' % pts
    svg += '</g>'
    svg += ('<path d="M 100 %d Q %d %d %d %d" fill="none" stroke="#FFD873" stroke-width="2.6" '
            'stroke-dasharray="5 6" opacity=".9"/>' % (h - 96, w // 2, h - 150, w - 100, h - 96))
    svg += ('<text x="18" y="%d" font-size="11.5" font-weight="700" fill="#FFFFFF" opacity=".8" '
            'font-family="Inter,system-ui,sans-serif">Materiais funcionais, energia e inovação</text>\n'
            % (h - 14))
    return grava(nome, svg)


# ------------------------------------------------------------- laboratório
def laboratorio(nome='laboratorios.svg', w=800, h=300):
    """Bancada esquemática com difratômetro, microscópio eletrônico e forno
    tubular — três dos equipamentos que os laboratórios do Programa têm."""
    svg = cabeca(w, h, 'Bancada de caracteriza&#231;&#227;o de materiais',
                 'Esquema de bancada com difratômetro de raios X, microscópio eletrônico e forno '
                 'tubular, equipamentos presentes nos laboratórios do Programa.', '#0E2438')
    base = h - 62
    svg += '<rect x="0" y="%d" width="%d" height="14" fill="#16324F"/>' % (base, w)

    # difratômetro: goniômetro com braços de fonte e detector
    dx = 148
    svg += ('<g stroke="#6FB3E0" stroke-width="3" fill="none" stroke-linecap="round">'
            '<circle cx="%d" cy="%d" r="74"/>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d"/>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d"/></g>'
            % (dx, base - 82, dx, base - 82, dx - 62, base - 122,
               dx, base - 82, dx + 66, base - 116))
    svg += ('<circle cx="%d" cy="%d" r="9" fill="#D9A521"/>'
            '<rect x="%d" y="%d" width="26" height="18" rx="4" fill="#6FB3E0"/>'
            '<rect x="%d" y="%d" width="26" height="18" rx="4" fill="#6FB3E0"/>'
            % (dx, base - 82, dx - 78, base - 134, dx + 56, base - 128))

    # microscópio eletrônico: coluna com feixe convergente
    mx = 400
    svg += ('<rect x="%d" y="%d" width="44" height="128" rx="8" fill="#2A7099"/>'
            '<rect x="%d" y="%d" width="96" height="16" rx="5" fill="#1B4A6B"/>'
            % (mx - 22, base - 176, mx - 48, base - 46))
    for k in range(3):
        svg += '<rect x="%d" y="%d" width="60" height="9" rx="4" fill="#6FB3E0" opacity=".85"/>' % (
            mx - 30, base - 158 + k * 34)
    svg += ('<path d="M %d %d L %d %d L %d %d Z" fill="#D9A521" opacity=".55"/>'
            % (mx, base - 48, mx - 15, base - 30, mx + 15, base - 30))

    # forno tubular com resistências
    fx = 648
    svg += ('<rect x="%d" y="%d" width="190" height="88" rx="12" fill="#1B4A6B"/>'
            '<rect x="%d" y="%d" width="152" height="44" rx="8" fill="#D9A521" opacity=".5"/>'
            % (fx - 95, base - 100, fx - 76, base - 78))
    for k in range(7):
        svg += '<circle cx="%d" cy="%d" r="4" fill="#FFD873"/>' % (fx - 60 + k * 20, base - 56)
    svg += '<rect x="%d" y="%d" width="26" height="14" rx="3" fill="#0E2438"/>' % (fx + 95, base - 78)

    svg += ('<g font-family="Inter,system-ui,sans-serif" font-size="11.5" font-weight="700" '
            'fill="#FFFFFF" opacity=".8">'
            '<text x="%d" y="%d" text-anchor="middle">Difra&#231;&#227;o de raios X</text>'
            '<text x="%d" y="%d" text-anchor="middle">Microscopia eletr&#244;nica</text>'
            '<text x="%d" y="%d" text-anchor="middle">Tratamento t&#233;rmico</text></g>\n'
            % (dx, h - 22, mx, h - 22, fx, h - 22))
    return grava(nome, svg)


# ---------------------------------------------------------- trajetória
def trajetoria(nome='oportunidades.svg', w=800, h=300):
    """IC → TCC → mestrado → doutorado → pós-doc: o caminho que a página de
    oportunidades descreve."""
    svg = cabeca(w, h, 'Trajetória de formação em pesquisa',
                 'Sequência de etapas de formação, da iniciação científica ao pós-doutorado, '
                 'ligadas por uma linha ascendente.', '#0E2438')
    etapas = [('Iniciação\ncientífica', '#6FB3E0'), ('TCC', '#2A7099'),
              ('Mestrado', '#2FA983'), ('Doutorado', '#D9A521'), ('Pós-\ndoutorado', '#C9A6E8')]
    n = len(etapas)
    pontos = []
    for k in range(n):
        x = 88 + k * (w - 176) / (n - 1.0)
        y = h - 96 - k * 26
        pontos.append((x, y))
    svg += ('<path d="M %s" fill="none" stroke="#FFFFFF" stroke-opacity=".25" '
            'stroke-width="2.5" stroke-linecap="round"/>'
            % ' L '.join('%.0f %.0f' % p for p in pontos))
    for k, ((x, y), (rot, cor)) in enumerate(zip(pontos, etapas)):
        svg += '<circle cx="%.0f" cy="%.0f" r="%d" fill="%s" opacity=".95"/>' % (x, y, 24 + k * 2, cor)
        for li, ln in enumerate(rot.split('\n')):
            svg += ('<text x="%.0f" y="%.0f" text-anchor="middle" font-size="11" font-weight="700" '
                    'font-family="Inter,system-ui,sans-serif" fill="#FFFFFF" opacity=".9">%s</text>'
                    % (x, y + 44 + li * 13, ln))
    svg += ('<text x="30" y="42" font-size="12.5" font-weight="800" fill="#FFFFFF" opacity=".85" '
            'font-family="Inter,system-ui,sans-serif">Da graduação ao pós-doutorado</text>\n')
    return grava(nome, svg)


# ------------------------------------------------------------------ prêmio
def premio(nome='premio.svg', w=800, h=420):
    """Pôster e destaque — a cena do prêmio de melhor pôster."""
    svg = cabeca(w, h, 'Sessão de pôsteres com trabalho destacado',
                 'Painéis de pôster em sequência, com um deles destacado por uma marca de '
                 'reconhecimento.', '#101E38')
    for k in range(5):
        x = 56 + k * 148
        alto = k == 2
        svg += ('<rect x="%d" y="%d" width="118" height="196" rx="8" fill="%s" opacity="%.2f"/>'
                % (x, 96 if alto else 112, '#D9A521' if alto else '#1B4A6B', 1 if alto else .8))
        for li in range(6):
            svg += ('<rect x="%d" y="%d" width="%d" height="6" rx="3" fill="%s" opacity=".55"/>'
                    % (x + 14, (116 if alto else 132) + li * 22, 90 - (li % 3) * 18,
                       '#5A3F06' if alto else '#7FB4D9'))
        if alto:
            svg += ('<circle cx="%d" cy="86" r="26" fill="#FFD873"/>'
                    '<path d="M %d 74 l 6 12 13 2 -9 9 2 13 -12 -6 -12 6 2 -13 -9 -9 13 -2 z" '
                    'fill="#8A6508"/>' % (x + 59, x + 53))
    svg += ('<text x="30" y="%d" font-size="12.5" font-weight="800" fill="#FFFFFF" opacity=".85" '
            'font-family="Inter,system-ui,sans-serif">Prêmios e reconhecimentos</text>\n' % (h - 26))
    return grava(nome, svg)


# ------------------------------------------------------- árvore de orientações
def linhagem(nome='historico.svg', w=800, h=420, semente=1996):
    """A árvore de orientações — o que um legado acadêmico literalmente é.

    Cada docente orienta mestres e doutores, e parte deles passa a orientar.
    O desenho é essa recursão: um tronco em 1996 que se ramifica em três
    gerações, com a espessura de cada galho caindo conforme se afasta da raiz
    e os nós ganhando a cor das duas áreas de concentração.

    Não é diagrama de dados — é a forma do objeto. A contagem real de
    orientações está na página, em texto.
    """
    import math
    rnd = random.Random(semente)
    svg = cabeca(w, h, 'Árvore de orientações da REDEMAT',
                 'Um tronco à esquerda se ramifica em três gerações de galhos '
                 'para a direita; cada nó representa um trabalho orientado, e a '
                 'cor distingue as duas áreas de concentração do Programa.')

    galhos, nos = [], []

    def ramo(x, y, ang, comp, largura, nivel):
        x2 = x + comp * math.cos(ang)
        y2 = y + comp * math.sin(ang)
        galhos.append((x, y, x2, y2, largura, nivel))
        if nivel >= 4:
            nos.append((x2, y2, 3.0, nivel))
            return
        nos.append((x2, y2, 6.0 - nivel * 0.9, nivel))
        for k in (-1, 1):
            ramo(x2, y2, ang + k * rnd.uniform(.26, .44),
                 comp * rnd.uniform(.58, .70), largura * .60, nivel + 1)
        if rnd.random() < .40:                      # alguns galhos trifurcam
            ramo(x2, y2, ang + rnd.uniform(-.10, .10),
                 comp * rnd.uniform(.52, .64), largura * .52, nivel + 1)

    # três troncos partindo da mesma origem: a associação UFOP-UEMG e o
    # crescimento em leque ao longo de trinta anos
    for ang in (-0.34, 0.0, 0.34):
        ramo(58, h / 2, ang, 176, 7.4, 0)

    svg += '<g stroke-linecap="round" fill="none">\n'
    for x1, y1, x2, y2, lg, nv in galhos:
        cor = NAVY if nv == 0 else (NAVY_MID if nv == 1 else '#8AA0B8')
        op = 1 if nv == 0 else (.85 if nv == 1 else .55)
        svg += ('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" stroke="%s" '
                'stroke-width="%.2f" opacity="%.2f"/>\n'
                % (x1, y1, (x1 + x2) / 2, (y1 + y2) / 2 - (y2 - y1) * .18,
                   x2, y2, cor, lg, op))
    svg += '</g>\n<g stroke="#FFFFFF" stroke-width="1.1">\n'
    for x, y, r, nv in nos:
        cor = A1 if (x + y) % 2 < 1 else A2
        svg += ('<circle cx="%.1f" cy="%.1f" r="%.2f" fill="%s" opacity="%.2f"/>\n'
                % (x, y, max(r, 2.0), cor, .92 if nv < 3 else .7))
    svg += '</g>\n'
    # a raiz: o ponto de origem em 1996
    svg += ('<circle cx="64" cy="%.1f" r="9" fill="%s" stroke="#FFFFFF" '
            'stroke-width="2.2"/>\n' % (h / 2, AMBER))
    svg += ('<text x="64" y="%.1f" text-anchor="middle" font-family="Inter, '
            'sans-serif" font-size="13" font-weight="700" fill="%s">1996</text>\n'
            % (h / 2 + 34, NAVY))
    svg += ('<text x="%d" y="%.1f" text-anchor="end" font-family="Inter, '
            'sans-serif" font-size="13" font-weight="700" fill="%s">'
            'trinta anos de orientações</text>\n' % (w - 26, h / 2 + 34, NAVY_MID))
    return grava(nome, svg)


if __name__ == '__main__':
    feitos = [moire(), microestrutura(), circular(), superficie(), integridade(),
              hidrometalurgia(), dispositivo(), laboratorio(), trajetoria(), premio(),
              linhagem()]
    for f in feitos:
        print('%7d B  %s' % (os.path.getsize(f), os.path.relpath(f, RAIZ)))
    print('\n%d ilustrações em %s' % (len(feitos), os.path.relpath(SAIDA, RAIZ)))
