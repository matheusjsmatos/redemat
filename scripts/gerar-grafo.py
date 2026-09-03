#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar-grafo.py — converte o grafo de colaborações do ScriptLattes em dados
do portal (assets/js/grafo-dados.js).

USO
    python3 scripts/gerar-grafo.py <pasta-da-saida-do-scriptlattes>
    python3 scripts/gerar-grafo.py ~/Dropbox/claude/redemat/teste-01

LÊ
    grafoDeColaboracoesComPesos.dot   nós, arestas e pesos (nº de produções
                                      em coautoria entre os dois docentes)
    grafoDeColaboracoes.html          tabela de Collaboration Rank
    assets/js/site-data.js            nome canônico e linha de pesquisa,
                                      casados pelo ID Lattes de 16 dígitos

ESCREVE
    assets/js/grafo-dados.js          window.GRAFO = {...}

POR QUE NÃO USAR O PNG DO SCRIPTLATTES
    O ScriptLattes entrega o grafo como imagem (com mapa de área clicável) e
    como applet Java — tecnologia que nenhum navegador atual executa. O portal
    redesenha o mesmo grafo em SVG a partir dos dados brutos do .dot: o
    conteúdo é idêntico, mas fica acessível, navegável por teclado e legível
    no celular.

LAYOUT
    Fruchterman-Reingold com semente fixa, por componente conexa, e as
    componentes empacotadas lado a lado. Semente fixa = layout estável entre
    execuções: rodar de novo com os mesmos dados dá o mesmo desenho.
    Os docentes sem coautoria interna no período ficam FORA da simulação, numa
    faixa própria — a alternativa (deixar a força espalhá-los) sugeriria
    proximidade que o dado não afirma.

O QUE ESTE SCRIPT NÃO FAZ
    Não altera site-data.js. Se o número de nós ou arestas mudou, o script
    avisa no final e a atualização do agregado publicado é decisão humana.
"""

import io
import json
import math
import os
import random
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SITE_DATA = os.path.join(RAIZ, 'assets', 'js', 'site-data.js')
SAIDA = os.path.join(RAIZ, 'assets', 'js', 'grafo-dados.js')

LARGURA, ALTURA = 1000.0, 730.0
MARGEM = 76.0
# Folga lateral do viewBox: os rótulos ficam FORA do círculo e passariam da
# borda. O desenho ocupa 0..LARGURA; o viewBox abre espaço para o texto.
FOLGA_ESQ, FOLGA_DIR = 30.0, 60.0

# Três faixas horizontais, para que o desenho diga a verdade sobre a rede:
#   NUCLEO   componente conexa maior — o núcleo de coautoria do Programa
#   GRUPOS   componentes conexas menores, sem ligação com o núcleo
#   ISOLADOS docentes sem nenhuma coautoria interna no período
FX_NUCLEO = (120.0, MARGEM, 880.0, 0.64 * ALTURA)
Y_GRUPOS = 0.775 * ALTURA
Y_ISOLADOS = 0.955 * ALTURA


# --------------------------------------------------------------- leitura .dot
def ler_dot(caminho):
    """Extrai nós (id, lattes, rótulo, produções internas) e arestas com peso."""
    txt = io.open(caminho, encoding='utf-8', errors='replace').read()

    nos = {}
    # bloco de nó:  12  [URL="membro-7172...html", ... label="Nome [1]", ...];
    for m in re.finditer(r'(?m)^\t(\d+)\t\[(.*?)\];', txt, re.S):
        nid, corpo = m.group(1), m.group(2)
        url = re.search(r'URL="membro-(\d+)\.html"', corpo)
        lab = re.search(r'label="(.*?)"', corpo)
        if not (url and lab):
            continue
        rotulo = lab.group(1)
        prod = re.search(r'\[(\d+)\]\s*$', rotulo)
        nos[nid] = {
            'lattes': url.group(1),
            'rotulo_dot': re.sub(r'\s*\[\d+\]\s*$', '', rotulo).strip(),
            'prod_interna': int(prod.group(1)) if prod else 0,
        }

    arestas = []
    # aresta:  0 -- 2  [fontsize=8, label=2.0, ...];
    for m in re.finditer(r'(?m)^\t(\d+) -- (\d+)\t\[(.*?)\];', txt, re.S):
        a, b, corpo = m.group(1), m.group(2), m.group(3)
        peso = re.search(r'label=([\d.]+)', corpo)
        arestas.append({'a': a, 'b': b, 'peso': float(peso.group(1)) if peso else 1.0})

    return nos, arestas


def ler_rank(caminho):
    """Collaboration Rank por nome, da tabela do grafoDeColaboracoes.html."""
    if not os.path.exists(caminho):
        return {}
    txt = io.open(caminho, encoding='utf-8', errors='replace').read()
    rank = {}
    for m in re.finditer(r'<tr><td>([\d.]+)</td><td>([^<]+)</td></tr>', txt):
        rank[normaliza(m.group(2))] = float(m.group(1))
    return rank


# ------------------------------------------------------------ site-data.js
def normaliza(s):
    import unicodedata
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z ]', '', s.lower()).strip()


def ler_docentes():
    """{lattes: {nome, linha, cat, ies}} do site-data.js."""
    txt = io.open(SITE_DATA, encoding='utf-8', errors='replace').read()
    ini = txt.find('docentes: {')
    fim = txt.find('/* ---', ini)
    bloco = txt[ini:fim if fim > 0 else len(txt)]
    out = {}
    for m in re.finditer(r"\{\s*nome:\s*'([^']+)'(.*?)\}", bloco, re.S):
        nome, resto = m.group(1), m.group(2)
        lat = re.search(r"lattes:\s*'(\d+)'", resto)
        if not lat:
            continue
        linha = re.search(r"linha:\s*'(\w+)'", resto)
        cat = re.search(r"cat:\s*'(\w+)'", resto)
        ies = re.search(r"ies:\s*'(\w+)'", resto)
        out[lat.group(1)] = {
            'nome': nome,
            'linha': linha.group(1) if linha else None,
            'cat': cat.group(1) if cat else None,
            'ies': ies.group(1) if ies else None,
        }
    return out


# ------------------------------------------------------------------- layout
def componentes(ids, arestas):
    adj = {i: set() for i in ids}
    for e in arestas:
        if e['a'] in adj and e['b'] in adj:
            adj[e['a']].add(e['b'])
            adj[e['b']].add(e['a'])
    vistos, comps = set(), []
    for i in sorted(ids, key=lambda x: int(x)):
        if i in vistos:
            continue
        pilha, comp = [i], []
        vistos.add(i)
        while pilha:
            u = pilha.pop()
            comp.append(u)
            for v in sorted(adj[u], key=lambda x: int(x)):
                if v not in vistos:
                    vistos.add(v)
                    pilha.append(v)
        comps.append(sorted(comp, key=lambda x: int(x)))
    return sorted(comps, key=len, reverse=True), adj


def spring(comp, arestas, iteracoes=600, semente=20260902):
    """Fruchterman-Reingold em caixa unitária. Semente fixa = layout estável."""
    if len(comp) == 1:
        return {comp[0]: (0.5, 0.5)}
    rnd = random.Random(semente)
    pos = {}
    n = len(comp)
    for k, i in enumerate(comp):                      # início em círculo:
        ang = 2 * math.pi * k / n                     # determinístico e sem
        pos[i] = [0.5 + 0.35 * math.cos(ang) + rnd.uniform(-.02, .02),
                  0.5 + 0.35 * math.sin(ang) + rnd.uniform(-.02, .02)]
    dentro = [e for e in arestas if e['a'] in pos and e['b'] in pos]
    k = math.sqrt(1.0 / n)
    t = 0.12
    for it in range(iteracoes):
        desl = {i: [0.0, 0.0] for i in comp}
        for ai in range(n):                                   # repulsão
            for bi in range(ai + 1, n):
                u, v = comp[ai], comp[bi]
                dx, dy = pos[u][0] - pos[v][0], pos[u][1] - pos[v][1]
                d2 = dx * dx + dy * dy or 1e-6
                d = math.sqrt(d2)
                f = (k * k) / d2
                desl[u][0] += dx / d * f
                desl[u][1] += dy / d * f
                desl[v][0] -= dx / d * f
                desl[v][1] -= dy / d * f
        for e in dentro:                                      # atração
            u, v = e['a'], e['b']
            dx, dy = pos[u][0] - pos[v][0], pos[u][1] - pos[v][1]
            d = math.sqrt(dx * dx + dy * dy) or 1e-6
            f = (d * d) / k * (0.6 + 0.4 * min(e['peso'], 8) / 8.0)
            desl[u][0] -= dx / d * f
            desl[u][1] -= dy / d * f
            desl[v][0] += dx / d * f
            desl[v][1] += dy / d * f
        for i in comp:                                        # passo
            dx, dy = desl[i]
            d = math.sqrt(dx * dx + dy * dy) or 1e-6
            pos[i][0] += dx / d * min(d, t)
            pos[i][1] += dy / d * min(d, t)
        t = max(t * 0.985, 0.002)
    return {i: (pos[i][0], pos[i][1]) for i in comp}


def normalizar_caixa(pos, x0, y0, larg, alt):
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    dx = (max(xs) - min(xs)) or 1.0
    dy = (max(ys) - min(ys)) or 1.0
    out = {}
    for i, (x, y) in pos.items():
        out[i] = [x0 + (x - min(xs)) / dx * larg,
                  y0 + (y - min(ys)) / dy * alt]
    return out


def ordenar_caminho(comp, adj):
    """Ordena uma componente pequena para desenho em linha, sem cruzar arestas:
    começa numa ponta e caminha. Se não for um caminho, o nó de maior grau vai
    para o meio."""
    grau = {i: len(adj[i]) for i in comp}
    if all(g <= 2 for g in grau.values()):
        inicio = min((i for i in comp if grau[i] <= 1),
                     key=lambda z: int(z), default=min(comp, key=lambda z: int(z)))
        ordem, vistos, atual = [inicio], {inicio}, inicio
        while True:
            prox = [v for v in sorted(adj[atual], key=lambda z: int(z)) if v not in vistos]
            if not prox:
                break
            atual = prox[0]
            vistos.add(atual)
            ordem.append(atual)
        ordem += [i for i in sorted(comp, key=lambda z: int(z)) if i not in vistos]
        return ordem
    hub = max(comp, key=lambda i: (grau[i], -int(i)))
    resto = [i for i in sorted(comp, key=lambda z: int(z)) if i != hub]
    meio = len(resto) // 2
    return resto[:meio] + [hub] + resto[meio:]


def raio(prod):
    """Raio do nó — área proporcional às produções em coautoria interna."""
    return 9.0 + 3.3 * math.sqrt(prod)


def largura_rotulo(txt):
    """Largura aproximada do rótulo em px, para 11,5px de Inter.
    Aproximação deliberada: o objetivo é reservar espaço, não medir tipografia."""
    return 6.15 * len(txt) + 4


def separar_rotulos(pos, raios, rot, lado, viewbox, passos=420):
    """Desfaz sobreposição de RETÂNGULOS (círculo + rótulo), empurrando cada par
    pelo eixo de menor penetração. Sem isso os nomes do miolo do grafo nascem
    uns sobre os outros — é o que o overlap=false do graphviz não resolve,
    porque ele só conhece os círculos."""
    vx, vy, vw, vh = viewbox

    PX, PY = 9.0, 4.0            # folga mínima entre caixas: 3px encostado lê
                                 # como sobreposição, mesmo sem ser
    def caixa(i):
        x, y = pos[i]
        r, w = raios[i], largura_rotulo(rot[i])
        if lado[i] > 0:                                    # rótulo à direita
            return [x - r - PX, y - 11 - PY, x + r + 7 + w + PX, y + 11 + PY]
        if lado[i] < 0:                                    # rótulo à esquerda
            return [x - r - 7 - w - PX, y - 11 - PY, x + r + PX, y + 11 + PY]
        return [x - max(r, w / 2) - PX, y - r - PY, x + max(r, w / 2) + PX, y + r + 22 + PY]

    ids = list(pos.keys())
    for _ in range(passos):
        moveu = False
        for ai in range(len(ids)):
            for bi in range(ai + 1, len(ids)):
                u, v = ids[ai], ids[bi]
                a, b = caixa(u), caixa(v)
                ox = min(a[2], b[2]) - max(a[0], b[0])
                oy = min(a[3], b[3]) - max(a[1], b[1])
                if ox <= 0 or oy <= 0:
                    continue
                moveu = True
                if oy <= ox:                               # separa na vertical
                    d = (oy + 3) / 2
                    s = 1 if pos[u][1] <= pos[v][1] else -1
                    pos[u][1] -= s * d
                    pos[v][1] += s * d
                else:                                      # separa na horizontal
                    d = (ox + 3) / 2
                    s = 1 if pos[u][0] <= pos[v][0] else -1
                    pos[u][0] -= s * d
                    pos[v][0] += s * d
        for i in ids:                                      # confina no viewBox
            c = caixa(i)
            if c[0] < vx + 6:
                pos[i][0] += (vx + 6) - c[0]
            if c[2] > vx + vw - 6:
                pos[i][0] -= c[2] - (vx + vw - 6)
            pos[i][1] = min(max(pos[i][1], vy + raios[i] + 14), vy + vh - raios[i] - 14)
        if not moveu:
            break
    return pos


def separar(pos, raios, caixa, passos=260):
    """Afasta nós cujos círculos se sobrepõem, mantendo todos dentro da caixa.
    Equivalente ao overlap=false do graphviz: preserva a topologia do layout e
    só desfaz colisão, para que nenhum rótulo nasça em cima de outro."""
    x0, y0, x1, y1 = caixa
    ids = list(pos.keys())
    for _ in range(passos):
        moveu = False
        for ai in range(len(ids)):
            for bi in range(ai + 1, len(ids)):
                u, v = ids[ai], ids[bi]
                dx = pos[v][0] - pos[u][0]
                dy = pos[v][1] - pos[u][1]
                d = math.sqrt(dx * dx + dy * dy) or 1e-6
                minimo = raios[u] + raios[v] + 30
                if d < minimo:
                    empurra = (minimo - d) / 2
                    ux, uy = dx / d, dy / d
                    pos[u][0] -= ux * empurra
                    pos[u][1] -= uy * empurra
                    pos[v][0] += ux * empurra
                    pos[v][1] += uy * empurra
                    moveu = True
        for i in ids:                                   # confina na caixa
            pos[i][0] = min(max(pos[i][0], x0 + raios[i]), x1 - raios[i])
            pos[i][1] = min(max(pos[i][1], y0 + raios[i]), y1 - raios[i])
        if not moveu:
            break
    return pos


# --------------------------------------------------------------------- main
def main():
    if len(sys.argv) < 2:
        print('Uso: python3 scripts/gerar-grafo.py <pasta-da-saida-do-scriptlattes>')
        return 1
    src = os.path.expanduser(sys.argv[1].rstrip('/'))
    dot = os.path.join(src, 'grafoDeColaboracoesComPesos.dot')
    if not os.path.exists(dot):
        print('ERRO: não encontrei grafoDeColaboracoesComPesos.dot em ' + src)
        return 1

    nos, arestas = ler_dot(dot)
    rank = ler_rank(os.path.join(src, 'grafoDeColaboracoes.html'))
    doc = ler_docentes()

    # data de processamento declarada pelo próprio relatório
    proc, periodo = None, None
    hpath = os.path.join(src, 'grafoDeColaboracoes.html')
    if os.path.exists(hpath):
        h = io.open(hpath, encoding='utf-8', errors='replace').read()
        m = re.search(r'Data de processamento:\s*([\d/]+\s[\d:]+)', h)
        proc = m.group(1) if m else None
        m = re.search(r'produções desde (\d{4}) até (\d{4})', h)
        periodo = (m.group(1) + '–' + m.group(2)) if m else None

    faltando = [n['lattes'] for n in nos.values() if n['lattes'] not in doc]

    def abreviar(nome):
        """Primeiro nome + último sobrenome — o rótulo que cabe no desenho.
        O nome completo continua no painel e no title do nó."""
        p = [t for t in nome.split() if t.lower() not in ('de', 'da', 'do', 'dos', 'das', 'e')]
        return p[0] + ' ' + p[-1] if len(p) > 1 else nome

    itens = []
    for nid, n in nos.items():
        d = doc.get(n['lattes'], {})
        nome = d.get('nome') or n['rotulo_dot']
        itens.append({
            'id': int(nid),
            'nome': nome,
            'abrev': abreviar(nome),
            'curto': n['rotulo_dot'],
            'lattes': n['lattes'],
            'prod': n['prod_interna'],
            'rank': rank.get(normaliza(nome), rank.get(normaliza(n['rotulo_dot']))),
            'linha': d.get('linha'),
            'cat': d.get('cat'),
            'ies': d.get('ies'),
        })

    ids = [str(i['id']) for i in itens]
    comps, adj = componentes(ids, arestas)
    conexas = [c for c in comps if len(c) > 1]
    isolados = [c[0] for c in comps if len(c) == 1]

    # ---- posições em três faixas: núcleo, grupos separados, sem coautoria
    raios = {str(i['id']): raio(i['prod']) for i in itens}
    pos, lados = {}, {}

    nucleo = conexas[0] if conexas else []
    grupos = conexas[1:]

    if nucleo:
        p = normalizar_caixa(spring(nucleo, arestas),
                             FX_NUCLEO[0], FX_NUCLEO[1],
                             FX_NUCLEO[2] - FX_NUCLEO[0], FX_NUCLEO[3] - FX_NUCLEO[1])
        p = separar(p, raios, FX_NUCLEO)
        # lado do rótulo: para fora do centro do núcleo, decidido uma vez
        cx = sum(v[0] for v in p.values()) / len(p)
        lado = {i: (1 if p[i][0] >= cx else -1) for i in p}
        rot = {str(it['id']): it['abrev'] for it in itens}
        p = separar_rotulos(p, raios, rot, lado,
                            (-FOLGA_ESQ, MARGEM - 24, LARGURA + FOLGA_ESQ + FOLGA_DIR,
                             FX_NUCLEO[3] - MARGEM + 48))
        lados.update(lado)
        pos.update(p)

    # grupos separados: cada um numa fatia da faixa do meio, na horizontal
    if grupos:
        largura_util = LARGURA - 2 * MARGEM
        total_g = sum(len(c) for c in grupos)
        x = MARGEM
        for c in grupos:
            fatia = largura_util * len(c) / total_g
            passo = min(fatia / max(len(c), 1), 170)
            base = x + (fatia - passo * (len(c) - 1)) / 2
            for k, i in enumerate(ordenar_caminho(c, adj)):
                pos[i] = [base + k * passo, Y_GRUPOS]
            x += fatia

    # sem coautoria interna: linha de baixo, espaçamento uniforme
    if isolados:
        passo = (LARGURA - 2 * MARGEM) / max(len(isolados) - 1, 1)
        for k, i in enumerate(isolados):
            pos[i] = [MARGEM + k * passo, Y_ISOLADOS]

    for it in itens:
        sid = str(it['id'])
        it['x'] = round(pos[sid][0], 1)
        it['y'] = round(pos[sid][1], 1)
        it['r'] = round(raios[sid], 1)
        it['iso'] = sid in isolados
        it['nucleo'] = sid in nucleo
        it['lado'] = lados.get(sid, 0)
        it['grau'] = len(adj[sid])

    itens.sort(key=lambda i: normaliza(i['nome']))

    dados = {
        'meta': {
            'fonte': 'ScriptLattes V9 — grafoDeColaboracoesComPesos.dot',
            'origem': os.path.basename(src),
            'processado_em': proc,
            'periodo': periodo,
            'gerado_por': 'scripts/gerar-grafo.py',
            'nota': ('Cada aresta liga dois docentes do Programa e o peso é o número de '
                     'produções assinadas em conjunto. O valor em cada nó é o total de '
                     'produções em coautoria com outros membros do próprio grupo — não é '
                     'a produção total do docente.'),
            'layout': ('Fruchterman-Reingold com semente fixa, por componente conexa. '
                       'Docentes sem coautoria interna no período ficam numa faixa '
                       'separada, fora da simulação.'),
        },
        'stats': {
            'nos': len(itens),
            'arestas': len(arestas),
            'peso_total': int(sum(e['peso'] for e in arestas)),
            'componentes': len(comps),
            'nucleo': len(nucleo),
            'grupos': len(grupos),
            'isolados': len(isolados),
            'densidade': round(2 * len(arestas) / (len(itens) * (len(itens) - 1)), 4),
        },
        'nos': itens,
        'arestas': [{'a': int(e['a']), 'b': int(e['b']), 'p': int(e['peso'])} for e in arestas],
        'largura': LARGURA,
        'altura': ALTURA,
        'viewbox': [-FOLGA_ESQ, 0, LARGURA + FOLGA_ESQ + FOLGA_DIR, ALTURA],
    }

    cab = ('/* grafo-dados.js — grafo de colaborações internas da REDEMAT.\n'
           '   GERADO por scripts/gerar-grafo.py a partir do .dot do ScriptLattes.\n'
           '   NÃO EDITAR À MÃO: rode o script de novo quando a saída mudar.\n'
           '   Fonte: ' + str(dados['meta']['fonte']) + '\n'
           '   Processado em: ' + str(proc) + ' — produções ' + str(periodo) + '\n'
           '   Carregado por <script> (e não por fetch) para funcionar também\n'
           '   quando a página é aberta direto no navegador (file://). */\n')

    with io.open(SAIDA, 'w', encoding='utf-8') as f:
        f.write(cab + 'window.GRAFO = ' +
                json.dumps(dados, ensure_ascii=False, indent=1) + ';\n')

    print('OK  ' + os.path.relpath(SAIDA, RAIZ))
    print('    %d nós · %d arestas · %d componentes (%d docente(s) sem coautoria interna)'
          % (len(itens), len(arestas), len(comps), len(isolados)))
    print('    peso total (produções em coautoria interna): %d' % dados['stats']['peso_total'])
    if faltando:
        print('AVISO  ID Lattes no grafo sem docente correspondente em site-data.js: '
              + ', '.join(faltando))
    sem_rank = [i['nome'] for i in itens if i['rank'] is None]
    if sem_rank:
        print('AVISO  sem Collaboration Rank: ' + ', '.join(sem_rank))
    print()
    print('CONFERÊNCIA HUMANA — o script não escreve em site-data.js.')
    print('  Se colaboracao.interna em site-data.js não disser nos: %d / arestas: %d,'
          % (len(itens), len(arestas)))
    print('  a atualização do número publicado é decisão da coordenação.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
