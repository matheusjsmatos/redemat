#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extrair-resumos-lattes.py — tira o Resumo do Lattes do cache do ScriptLattes.

USO
    python3 scripts/extrair-resumos-lattes.py [pasta do cache]
    (padrão: ~/Dropbox/claude/redemat/cache)

O ScriptLattes guarda o HTML bruto de cada currículo em cache/<id de 16
dígitos>, e o Lattes traz o resumo num <p class="resumo">. É texto que a
própria pessoa escreveu sobre si — por isso vai para o painel histórico como
resumo, e não uma descrição redigida por nós.

Grava data/lattes-resumos.csv, lido por gerar-historico.py e casado com o
docente pelo ID que data/nomes-docentes.csv já guarda.
"""
import csv, glob, html, io, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = (sys.argv[1] if len(sys.argv) > 1
         else os.path.expanduser('~/Dropbox/claude/redemat/cache'))


def texto(t):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t))).strip()


def main():
    ids = {}
    for base in (CACHE, os.path.join(CACHE, 'backup')):
        for f in glob.glob(os.path.join(base, '*')):
            n = os.path.basename(f)
            # o cache raiz é mais recente que o backup e tem precedência
            if re.fullmatch(r'\d{16}', n) and os.path.isfile(f) and (n not in ids or base == CACHE):
                ids[n] = f
    if not ids:
        sys.exit('Nenhum currículo em cache em ' + CACHE)

    linhas = []
    for i, f in sorted(ids.items()):
        s = io.open(f, encoding='utf-8', errors='ignore').read()
        m = re.search(r'class="nome"[^>]*>(.*?)</', s, re.S)
        nome = texto(m.group(1)) if m else ''
        m = re.search(r'class="resumo"[^>]*>(.*?)</p>', s, re.S)
        res = texto(m.group(1)) if m else ''
        linhas.append({'lattes': i, 'nome_lattes': nome, 'chars': len(res), 'resumo': res})
        print('%s  %-42s %5d chars' % (i, nome[:42], len(res)))

    destino = os.path.join(RAIZ, 'data', 'lattes-resumos.csv')
    with io.open(destino, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=['lattes', 'nome_lattes', 'chars', 'resumo'])
        w.writeheader(); w.writerows(linhas)
    vazios = sum(1 for l in linhas if not l['resumo'])
    print('\ngravado %s — %d currículos, %d sem resumo'
          % (os.path.relpath(destino, RAIZ), len(linhas), vazios))
    return 0


if __name__ == '__main__':
    sys.exit(main())
