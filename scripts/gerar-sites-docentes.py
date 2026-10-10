#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data/sites-docentes.json -> assets/js/sites-docentes.js

O portal é servido também em file:// durante a edição, onde fetch() não
funciona. Por isso todo dado que a página lê chega por <script src>, e não por
requisição. Este script faz a ponte: a planilha e o assistente editam o JSON,
que é o formato de trabalho, e o portal lê o .js gerado a partir dele.

    python3 scripts/gerar-sites-docentes.py
"""
import json, os, unicodedata, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(RAIZ, 'data', 'sites-docentes.json')
DEST = os.path.join(RAIZ, 'assets', 'js', 'sites-docentes.js')


def chave(nome):
    """Nome sem acento e em minúsculas. O cadastro de docentes e esta lista
    nem sempre grafam o nome do mesmo jeito — foi um acento que já fez oito
    docentes do quadro serem publicados como externos ao Programa."""
    s = unicodedata.normalize('NFD', nome or '')
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', s).strip().lower()


def main():
    d = json.load(open(ORIG, encoding='utf-8'))
    mapa = {}
    for x in d['docentes']:
        campos = {k: v for k, v in x.items()
                  if k in ('site_pessoal', 'site_grupo', 'nome_grupo', 'site_particular') and v}
        if campos:
            mapa[chave(x['nome'])] = campos
    js = ('/* GERADO POR scripts/gerar-sites-docentes.py — não editar à mão.\n'
          '   Fonte: data/sites-docentes.json (%s, %s). */\n'
          'window.SITES_DOCENTES = %s;\n') % (
        d['meta'].get('fonte', ''), d['meta'].get('coleta', ''),
        json.dumps(mapa, ensure_ascii=False, indent=1))
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    open(DEST, 'w', encoding='utf-8').write(js)
    print('gravado:', DEST)
    print('docentes com ao menos um endereço:', len(mapa))
    for k, v in mapa.items():
        print('  %-36s %s' % (k, ', '.join(v)))


if __name__ == '__main__':
    main()
