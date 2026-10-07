#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Importa o acervo de notícias do portal OpenScholar antigo (redemat.ufop.br).

Por que existe
--------------
O site antigo vai ser desligado. Tudo o que ele publica — texto das notícias,
editais em PDF, imagens — precisa estar DENTRO deste repositório antes disso,
senão cada link vira um 404 no dia do desligamento. O portal novo não pode
apontar para o antigo em lugar nenhum.

Como roda
---------
O ambiente onde o assistente trabalha não alcança redemat.ufop.br (falha de
DNS). Este script roda na máquina do Programa, que alcança. Cada execução tem
tempo limitado, então ele é RETOMÁVEL: o que já baixou fica registrado em
data/noticias.json e não é baixado de novo.

    python3 scripts/importar-noticias-antigas.py --indice       # só o índice
    python3 scripts/importar-noticias-antigas.py --limite 12    # 12 notícias
    python3 scripts/importar-noticias-antigas.py --limite 12    # ...de novo

O que NÃO faz
-------------
Não classifica por tema nem por semestre — isso é de outro script, para que as
regras de classificação possam ser revistas sem baixar nada de novo.
"""
import argparse, hashlib, html, json, os, re, sys, time, urllib.parse, urllib.request

BASE = 'https://redemat.ufop.br'
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON = os.path.join(RAIZ, 'data', 'noticias.json')
DOCS = os.path.join(RAIZ, 'assets', 'doc', 'noticias')
IMGS = os.path.join(RAIZ, 'assets', 'img', 'noticias')

MES = {'janeiro':1,'fevereiro':2,'março':3,'marco':3,'abril':4,'maio':5,'junho':6,
       'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}

UA = {'User-Agent': 'REDEMAT-portal/1.0 (migracao do acervo institucional)'}


# Intervalo entre requisições. NÃO baixe isto para zero: a primeira tentativa
# desta migração disparou ~15 requisições em poucos segundos e o servidor passou
# a recusar conexão por vários minutos. O acervo tem 109 notícias mais anexos;
# são alguns minutos de qualquer jeito, e um crawl educado é a diferença entre
# terminar devagar e ser bloqueado no meio.
PAUSA = 3.0
_ultima = [0.0]


def busca(url, binario=False, tentativas=4):
    for i in range(tentativas):
        espera = PAUSA - (time.time() - _ultima[0])
        if espera > 0:
            time.sleep(espera)
        _ultima[0] = time.time()
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=25) as r:
                b = r.read()
                tipo = r.headers.get('Content-Type', '')
            return b if binario else b.decode('utf-8', 'replace'), tipo
        except Exception as e:
            if i == tentativas - 1:
                return (None, str(e))
            # Recusa de conexão costuma ser bloqueio por excesso: espera mais.
            time.sleep(8 * (i + 1) if 'refused' in str(e).lower() else 2 * (i + 1))


def texto(t):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', t or ''))).strip()


def data_iso(d):
    """'Julho 7, 2026' -> '2026-07-07'. Sem mês reconhecido, devolve ''."""
    m = re.match(r'(\w+)\s+(\d+),\s*(\d{4})', html.unescape(d or '').strip())
    if not m:
        return ''
    mes = MES.get(m.group(1).lower())
    return '%s-%02d-%02d' % (m.group(3), mes, int(m.group(2))) if mes else ''


def carrega():
    if os.path.exists(JSON):
        with open(JSON, encoding='utf-8') as f:
            return json.load(f)
    return {'meta': {}, 'noticias': []}


def grava(d):
    os.makedirs(os.path.dirname(JSON), exist_ok=True)
    d['meta']['atualizado'] = time.strftime('%Y-%m-%d %H:%M')
    d['meta']['fonte'] = BASE + '/news'
    d['meta']['total'] = len(d['noticias'])
    d['meta']['com_corpo'] = sum(1 for n in d['noticias'] if n.get('corpo'))
    with open(JSON, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)


def monta_indice(d):
    """Percorre /news?page=N até uma página sem artigo. Não baixa corpo."""
    por_node = {n['node']: n for n in d['noticias']}
    p, vazias = 0, 0
    while vazias < 2 and p < 60:
        s, _ = busca('%s/news?page=%d' % (BASE, p))
        if s is None:
            print('  página %d falhou: %s' % (p, _)); p += 1; continue
        achou = 0
        for m in re.finditer(
                r'<article id="node-(\d+)".*?<h1 class="node-title".*?<a href="([^"]+)"[^>]*>(.*?)</a>'
                r'.*?date-display-single">([^<]*)<', s, re.S):
            nid, u, t, dt = m.groups()
            achou += 1
            if nid in por_node:
                continue
            reg = {'node': nid, 'url': html.unescape(u), 'titulo': texto(t),
                   'data': data_iso(dt), 'data_txt': html.unescape(dt).strip(),
                   'corpo': None, 'anexos': [], 'imagens': [], 'pendencias': []}
            por_node[nid] = reg
            d['noticias'].append(reg)
        print('  página %d: %d artigos' % (p, achou))
        vazias = vazias + 1 if achou == 0 else 0
        p += 1
    d['noticias'].sort(key=lambda n: (n['data'] or '0000', n['node']))
    return d


def nome_arquivo(url):
    """Nome local estável. O hash evita que dois anexos de nome igual
    (há vários 'edital.pdf' no acervo) se sobrescrevam."""
    cam = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    base = os.path.basename(cam) or 'arquivo'
    base = re.sub(r'[^A-Za-z0-9._-]+', '-', base).strip('-.') or 'arquivo'
    if len(base) > 70:
        raiz, ext = os.path.splitext(base)
        base = raiz[:60] + ext
    return hashlib.sha1(url.encode()).hexdigest()[:6] + '-' + base


def baixa_binario(url, destino_dir, reg, especie):
    os.makedirs(destino_dir, exist_ok=True)
    nome = nome_arquivo(url)
    caminho = os.path.join(destino_dir, nome)
    if os.path.exists(caminho) and os.path.getsize(caminho) > 0:
        return nome
    r = busca(url, binario=True)
    if isinstance(r, tuple):            # erro
        reg['pendencias'].append('%s não baixado: %s (%s)' % (especie, url, r[1][:80]))
        return None
    with open(caminho, 'wb') as f:
        f.write(r)
    return nome


# Extensões que tratamos como documento para download. Uma página HTML do site
# antigo NÃO entra aqui: ela é outra notícia ou outra página, e vira pendência
# para ser resolvida pelo mapa de redirecionamento, não um arquivo solto.
DOC_EXT = ('.pdf', '.doc', '.docx', '.odt', '.xls', '.xlsx', '.ods', '.ppt',
           '.pptx', '.zip', '.rtf', '.csv', '.txt')
IMG_EXT = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp')


def processa(reg):
    s, _ = busca(reg['url'])
    if s is None:
        reg['pendencias'].append('página não baixada: %s' % _[:120])
        return False

    m = re.search(r'<div class="node-content".*?>(.*?)(?:<div class="[^"]*field-name-field-news|'
                  r'<footer|<div id="comments|</article>)', s, re.S)
    corpo = m.group(1) if m else ''
    mb = re.search(r'field-name-body.*?<div class="field-item even">(.*)', corpo, re.S)
    if mb:
        corpo = mb.group(1)
    corpo = re.sub(r'<div class="field field-name-field-news-date.*?</div></div></div>', '', corpo, flags=re.S)
    corpo = corpo.strip()

    # Data: a página individual é mais confiável que o teaser do índice.
    md = re.search(r'date-display-single">([^<]*)<', s)
    if md:
        iso = data_iso(md.group(1))
        if iso:
            reg['data'], reg['data_txt'] = iso, html.unescape(md.group(1)).strip()

    novos = {}
    for m in re.finditer(r'(href|src)="([^"]+)"', corpo):
        attr, u = m.groups()
        u = html.unescape(u)
        if u.startswith(('mailto:', 'tel:', '#', 'javascript:', 'data:')):
            continue
        absu = urllib.parse.urljoin(reg['url'], u)
        host = urllib.parse.urlparse(absu).netloc
        ext = os.path.splitext(urllib.parse.urlparse(absu).path)[1].lower()
        if 'redemat.ufop.br' not in host:
            continue                                   # link externo fica como está
        if ext in DOC_EXT:
            nome = baixa_binario(absu, os.path.join(DOCS, reg['node']), reg, 'anexo')
            if nome:
                novos[u] = 'assets/doc/noticias/%s/%s' % (reg['node'], nome)
                reg['anexos'].append({'arquivo': novos[u], 'origem': absu,
                                      'rotulo': ''})
        elif ext in IMG_EXT:
            nome = baixa_binario(absu, os.path.join(IMGS, reg['node']), reg, 'imagem')
            if nome:
                novos[u] = 'assets/img/noticias/%s/%s' % (reg['node'], nome)
                reg['imagens'].append({'arquivo': novos[u], 'origem': absu})
        else:
            # Link para outra página do site antigo. Não inventa destino: anota.
            reg['pendencias'].append('link interno sem equivalente ainda: %s' % absu)

    for velho, novo in novos.items():
        corpo = corpo.replace('"%s"' % velho, '"%s"' % novo)

    reg['corpo'] = corpo
    reg['anexos'] = [dict(t) for t in {tuple(sorted(a.items())) for a in reg['anexos']}]
    reg['imagens'] = [dict(t) for t in {tuple(sorted(a.items())) for a in reg['imagens']}]
    reg['pendencias'] = sorted(set(reg['pendencias']))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--indice', action='store_true', help='só atualiza o índice')
    ap.add_argument('--limite', type=int, default=0, help='quantas notícias baixar nesta execução')
    ap.add_argument('--refazer', action='store_true', help='rebaixa mesmo o que já tem corpo')
    ap.add_argument('--pausa', type=float, default=PAUSA, help='segundos entre requisições')
    a = ap.parse_args()
    globals()['PAUSA'] = a.pausa

    d = carrega()
    if a.indice or not d['noticias']:
        print('Montando o índice…')
        d = monta_indice(d)
        grava(d)
        print('índice: %d notícias' % len(d['noticias']))
        if a.indice:
            return

    pend = [n for n in d['noticias'] if a.refazer or not n.get('corpo')]
    print('faltam %d de %d' % (len(pend), len(d['noticias'])))
    n_ok = 0
    for reg in pend[: a.limite or len(pend)]:
        ok = processa(reg)
        n_ok += ok
        print(' %s %s %s  anexos=%d img=%d' % ('ok ' if ok else 'ERRO', reg['data'],
              reg['titulo'][:58], len(reg['anexos']), len(reg['imagens'])))
        grava(d)
    rest = sum(1 for n in d['noticias'] if not n.get('corpo'))
    print('baixadas nesta execução: %d | ainda faltam: %d' % (n_ok, rest))


if __name__ == '__main__':
    main()
