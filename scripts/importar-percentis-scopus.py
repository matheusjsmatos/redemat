#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
importar-percentis-scopus.py — completa o percentil Scopus dos periódicos que o
snapshot automático não cobriu, a partir de consulta manual ao Scopus Sources.

POR QUE ISTO EXISTE
    O snapshot Scopus da entrega consolidada cobre 98 dos 204 periódicos do
    conjunto. Os outros 106 não foram localizados pela busca automática — entre
    eles Chemical Physics Letters, que EXISTE no Scopus e tem CiteScore 5,8 e
    percentil 80. Ausência de métrica no snapshot não é ausência de métrica no
    Scopus, e não é qualidade zero.

    Não é possível raspar o Scopus: scopus.com bloqueia acesso automatizado
    (robots.txt) e as páginas de fonte exigem sessão. O caminho confiável é a
    consulta na interface — inclusive o botão "Download Scopus Source List", que
    entrega CiteScore e percentil de todos os títulos numa planilha só. Este
    script transforma esse trabalho manual em dado do portal, com procedência.

USO
    # 1. gera a lista do que falta, ordenada por número de artigos
    python3 scripts/importar-percentis-scopus.py --listar

    # 2. preencha data/percentis-scopus-manuais.csv na interface do Scopus
    #    (ou cole as linhas da Scopus Source List baixada)

    # 3. aplica no mapa de publicações do portal
    python3 scripts/importar-percentis-scopus.py            # simulação
    python3 scripts/importar-percentis-scopus.py --aplicar   # grava

O QUE MARCA
    Cada periódico preenchido por esta via recebe `m: 1` em
    assets/js/mapa-pub-dados.js. A página mostra esses títulos com marca
    própria: percentil conferido à mão não se mistura com percentil de snapshot
    automático, mesmo quando os dois estão certos.
"""

import csv
import io
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPA = os.path.join(RAIZ, 'assets', 'js', 'mapa-pub-dados.js')
MANUAIS = os.path.join(RAIZ, 'data', 'percentis-scopus-manuais.csv')
PENDENTES = os.path.join(RAIZ, 'data', 'percentis-scopus-pendentes.csv')

CAMPOS = ['codigo', 'periodico', 'citescore', 'percentil', 'quartil',
          'categoria', 'rank', 'total_categoria', 'ano_metrica',
          'fonte', 'consultado_em', 'conferido_por']


def norm(t):
    return re.sub(r'[^a-z0-9]', '', (t or '').lower())


def ler_mapa():
    txt = io.open(MAPA, encoding='utf-8').read()
    i, j = txt.find('{'), txt.rfind('}')
    return txt[:i], json.loads(txt[i:j + 1])


def quartil_do_percentil(p):
    """Q1 = percentil >= 75; Q2 >= 50; Q3 >= 25; Q4 abaixo.
    O Scopus publica o quartil junto com o percentil; esta conversão só é usada
    quando a planilha traz o percentil e não traz o quartil."""
    p = float(p)
    return 'Q1' if p >= 75 else 'Q2' if p >= 50 else 'Q3' if p >= 25 else 'Q4'


def listar():
    _, M = ler_mapa()
    faltam = [(v.get('a') or 0, k, v.get('n') or k)
              for k, v in M['revistas'].items() if v.get('p') in (None, '')]
    faltam.sort(reverse=True)
    with io.open(PENDENTES, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['artigos', 'codigo', 'periodico'] + CAMPOS[2:])
        for a, k, n in faltam:
            w.writerow([a, k, n] + [''] * (len(CAMPOS) - 2))
    print('%d periódico(s) sem percentil, em %d artigos.'
          % (len(faltam), sum(a for a, _, _ in faltam)))
    print('gravado: ' + os.path.relpath(PENDENTES, RAIZ))
    print()
    print('Os 15 com mais artigos — é onde a consulta manual rende mais:')
    for a, k, n in faltam[:15]:
        print('  %3d artigos  %-10s %s' % (a, k, n[:60]))
    return 0


def aplicar(gravar):
    if not os.path.exists(MANUAIS):
        print('ERRO: não encontrei ' + os.path.relpath(MANUAIS, RAIZ))
        print('Rode primeiro com --listar e preencha o arquivo.')
        return 1
    cab, M = ler_mapa()
    with io.open(MANUAIS, encoding='utf-8-sig', newline='') as f:
        linhas = [r for r in csv.DictReader(f)
                  if (r.get('percentil') or '').strip()]

    porcod = {k.lower(): k for k in M['revistas']}
    pornome = {norm(v.get('n')): k for k, v in M['revistas'].items()}

    casou, nao = [], []
    for r in linhas:
        cod = (r.get('codigo') or '').strip().lower()
        k = porcod.get(cod) or pornome.get(norm(r.get('periodico')))
        if not k:
            nao.append(r.get('periodico') or r.get('codigo'))
            continue
        rev = M['revistas'][k]
        pct = str(int(float(r['percentil'])))
        q = (r.get('quartil') or '').strip() or quartil_do_percentil(pct)
        antes = (rev.get('p'), rev.get('q'))
        rev['p'] = pct
        rev['q'] = q
        if (r.get('categoria') or '').strip():
            rev['c'] = r['categoria'].strip()
        if (r.get('citescore') or '').strip():
            rev['cs'] = r['citescore'].strip()
        rev['m'] = 1
        casou.append((k, rev.get('n'), antes, (pct, q)))

    print('%d linha(s) com percentil no CSV manual' % len(linhas))
    for k, n, antes, dep in casou:
        print('  %-10s %-48s %s -> percentil %s (%s)'
              % (k, (n or '')[:48], 'vazio' if antes[0] in (None, '') else antes[0],
                 dep[0], dep[1]))
    for n in nao:
        print('  NAO CASOU: %s — confira o código ou o nome exato do periódico' % n)

    M.setdefault('resumo', {})
    M['resumo']['revistas_com_percentil_manual'] = len(casou)

    if not gravar:
        print()
        print('SIMULAÇÃO — nada foi gravado. Rode com --aplicar para gravar.')
        return 0

    with io.open(MAPA, 'w', encoding='utf-8') as f:
        f.write(cab + json.dumps(M, ensure_ascii=False, indent=1) + ';\n')
    print()
    print('gravado: ' + os.path.relpath(MAPA, RAIZ))
    print('Confira a página de produção antes de publicar: os títulos com')
    print('percentil manual aparecem marcados na tabela de Q1.')
    return 0


if __name__ == '__main__':
    if '--listar' in sys.argv:
        sys.exit(listar())
    sys.exit(aplicar('--aplicar' in sys.argv))
