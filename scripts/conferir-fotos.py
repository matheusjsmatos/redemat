#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conferir-fotos.py — diz que arquivo de foto o portal espera para cada pessoa,
quais já estão na pasta, e gera o manifesto que o portal lê.

USO
    python3 scripts/conferir-fotos.py                 # só relata
    python3 scripts/conferir-fotos.py --manifesto     # relata e grava fotos.js
    python3 scripts/conferir-fotos.py --csv           # relata e grava a lista
    python3 scripts/conferir-fotos.py --manifesto --csv

QUEM ENTRA
    Docentes, pós-doutorandos e a secretaria e equipe técnica — as três
    populações que o portal exibe em cartão com foto.

FORMATOS ACEITOS
    jpg · jpeg · png · webp · gif · avif

    Basta um deles. Se houver mais de um arquivo para a mesma pessoa, vence o
    primeiro dessa ordem e o script avisa da duplicata: dois arquivos para a
    mesma pessoa é sinal de troca de foto pela metade.

    GIF animado funciona, mas o portal não consegue pausá-lo: CSS não para a
    animação de um GIF, nem com `prefers-reduced-motion`. Para retrato
    institucional, prefira imagem estática.

POR QUE O MANIFESTO
    `assets/img/pessoas/fotos.js` declara quem tem foto e em que formato, e o
    portal confia nele: quem não está declarado vai direto para as iniciais,
    sem uma única requisição inútil. Sem o arquivo, o portal sonda os seis
    formatos pessoa por pessoa — mais de cem 404 silenciosos por página
    enquanto ninguém tem foto.

    A consequência é que **foto na pasta sem manifesto regerado não aparece**.
    Rode com --manifesto sempre que adicionar ou trocar fotos; o portal também
    avisa no console do navegador quando o manifesto está vazio.

CONSENTIMENTO
    Cada pessoa precisa autorizar por escrito o uso da própria imagem (LGPD).
    O script não sabe quem autorizou: a coluna `autorizacao` do CSV fica em
    branco para a coordenação preencher. Publicar sem ela é decisão de quem
    publica, não deste script.
"""

import csv
import io
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DATA = os.path.join(RAIZ, 'assets', 'js', 'site-data.js')
PASTA = os.path.join(RAIZ, 'assets', 'img', 'pessoas')

FORMATOS = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'avif']


def slug(nome):
    s = unicodedata.normalize('NFD', nome)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9]+', '-', s.lower())
    return s.strip('-')


def pessoas():
    """(nome, papel, slug_declarado) para docentes, pós-doc e secretaria."""
    t = io.open(SITE_DATA, encoding='utf-8').read()
    out = []

    ini = t.find('docentes: {')
    bloco = t[ini:t.find('/* ---', ini)]
    for m in re.finditer(r"\{\s*nome:\s*'([^']+)'(.*?)\}", bloco, re.S):
        cat = re.search(r"cat:\s*'(\w+)'", m.group(2))
        out.append((m.group(1),
                    'Docente ' + (cat.group(1) if cat else ''), None))

    ini = t.find('comunidade: {')
    if ini > 0:
        bloco = t[ini:t.find('\n  },', ini)]
        for rotulo, chave in (('Pós-doutorando', 'posdoc'),
                              ('Secretaria e equipe técnica', 'tecnicos')):
            i = bloco.find(chave + ':')
            if i < 0:
                continue
            trecho = bloco[i:bloco.find(']', i)]
            for m in re.finditer(r"\{[^{}]*?nome:\s*'([^']+)'[^{}]*?\}", trecho, re.S):
                item = m.group(0)
                f = re.search(r"foto:\s*'([^']+)'", item)
                cargo = re.search(r"cargo:\s*'([^']+)'", item)
                out.append((m.group(1),
                            cargo.group(1) if cargo else rotulo,
                            f.group(1) if f else None))
    return out


"""Assinatura de cada formato nos primeiros bytes do arquivo. Serve para
   pegar o caso comum de renomear a extensão: um JPEG salvo como `.gif`
   funciona no Chrome, que fareja o conteúdo, mas depende de o servidor não
   mandar `X-Content-Type-Options: nosniff` — com ele, a imagem não aparece.
   Melhor descobrir aqui do que no ar."""
ASSINATURAS = [
    ('jpg',  lambda b: b[:3] == b'\xff\xd8\xff'),
    ('png',  lambda b: b[:8] == b'\x89PNG\r\n\x1a\n'),
    ('gif',  lambda b: b[:6] in (b'GIF87a', b'GIF89a')),
    ('webp', lambda b: b[:4] == b'RIFF' and b[8:12] == b'WEBP'),
    ('avif', lambda b: b[4:8] == b'ftyp' and b'avif' in b[8:20]),
]

EQUIVALENTES = {'jpg': 'jpg', 'jpeg': 'jpg'}      # .jpeg e .jpg são o mesmo formato

TAMANHO_ALERTA = 300 * 1024                       # acima disso, vale reencodar


def formato_real(caminho):
    """O formato pelos bytes, ou None se não reconhecer nenhum."""
    try:
        with io.open(caminho, 'rb') as f:
            b = f.read(32)
    except OSError:
        return None
    for nome, testa in ASSINATURAS:
        if testa(b):
            return nome
    return None


def arquivos_por_slug():
    """{slug: [ext, ...]} do que está de fato na pasta."""
    achado = {}
    if not os.path.isdir(PASTA):
        return achado
    for nome in sorted(os.listdir(PASTA)):
        base, ponto, ext = nome.rpartition('.')
        if not ponto:
            continue
        ext = ext.lower()
        if ext in FORMATOS:
            achado.setdefault(base, []).append(ext)
    return achado


def main():
    gente = pessoas()
    naPasta = arquivos_por_slug()

    linhas, manifesto, dup, orfaos = [], {}, [], []
    trocados, pesados = [], []
    for nome, papel, declarado in gente:
        sl = declarado or slug(nome)
        exts = naPasta.get(sl, [])
        exts = [e for e in FORMATOS if e in exts]      # ordem de preferência
        if exts:
            manifesto[sl] = exts[0]
            caminho = os.path.join(PASTA, sl + '.' + exts[0])
            real = formato_real(caminho)
            dito = EQUIVALENTES.get(exts[0], exts[0])
            if real and real != dito:
                trocados.append((sl, exts[0], real))
            tam = os.path.getsize(caminho)
            if tam > TAMANHO_ALERTA:
                pesados.append((sl + '.' + exts[0], tam))
        if len(exts) > 1:
            dup.append((sl, exts))
        linhas.append({'nome': nome, 'papel': papel, 'slug': sl,
                       'arquivo_esperado': sl + '.<' + '|'.join(FORMATOS) + '>',
                       'arquivo_encontrado': (sl + '.' + exts[0]) if exts else '',
                       'na_pasta': 'sim' if exts else 'nao',
                       'autorizacao': ''})

    esperados = {l['slug'] for l in linhas}
    for sl in naPasta:
        if sl not in esperados:
            orfaos.append(sl)

    larg = max(len(l['nome']) for l in linhas)
    for l in linhas:
        print('%s  %-*s  %-30s %s' % ('OK ' if l['na_pasta'] == 'sim' else '-- ',
                                      larg, l['nome'], l['papel'][:30],
                                      l['arquivo_encontrado'] or (l['slug'] + '.' + FORMATOS[0])))
    com = sum(1 for l in linhas if l['na_pasta'] == 'sim')
    print()
    print('%d pessoa(s) · %d com foto · %d sem foto' % (len(linhas), com, len(linhas) - com))
    print('formatos aceitos: ' + ' · '.join(FORMATOS))
    print('pasta: ' + os.path.relpath(PASTA, RAIZ))

    for sl, exts in dup:
        print('AVISO  %s tem %d arquivos (%s). O portal usa o .%s; apague os outros.'
              % (sl, len(exts), ', '.join(exts), exts[0]))
    for sl in orfaos:
        print('AVISO  %s.* está na pasta e não corresponde a ninguém do portal. '
              'Confira o slug com este script.' % sl)
    for sl, dito, real in trocados:
        print('AVISO  %s.%s é na verdade um %s. Renomeie para %s.%s.'
              % (sl, dito, real.upper(), sl, real))
    if trocados:
        print('       Trocar só a extensão não converte o arquivo. O Chrome fareja o')
        print('       conteúdo e mostra a imagem mesmo assim, mas isso depende de o')
        print('       servidor não enviar X-Content-Type-Options: nosniff — com esse')
        print('       cabeçalho, a foto simplesmente não aparece. Renomear resolve.')
    for arq, tam in pesados:
        print('AVISO  %s tem %d KB — acima dos 40–120 KB da especificação.'
              % (arq, tam // 1024))
    if pesados:
        print('       Recorte quadrado em 400×400 e salve como JPG qualidade 82 ou')
        print('       WebP: mesma nitidez no cartão de 48 px, uma fração do peso.')
    if com < len(linhas):
        print('As pessoas sem foto aparecem com as iniciais — o portal não quebra.')

    if '--manifesto' in sys.argv:
        destino = os.path.join(PASTA, 'fotos.js')
        with io.open(destino, 'w', encoding='utf-8') as f:
            f.write('/* fotos.js — quem tem foto e em que formato.\n'
                    '   GERADO por scripts/conferir-fotos.py --manifesto.\n'
                    '   NÃO EDITAR À MÃO: rode o script de novo depois de mexer na pasta.\n'
                    '   Com este arquivo o portal não faz requisição para quem não tem\n'
                    '   foto; sem ele, o portal sonda os formatos e gera 404 silenciosos. */\n'
                    'window.FOTOS = ' + json.dumps(manifesto, ensure_ascii=False,
                                                   indent=1, sort_keys=True) + ';\n')
        print('gravado: ' + os.path.relpath(destino, RAIZ) +
              ' — %d foto(s) declarada(s)' % len(manifesto))
        if not manifesto:
            print('       manifesto vazio: enquanto ninguém tiver foto, o portal')
            print('       vai direto para as iniciais e não faz requisição nenhuma.')
            print('       Depois de colocar arquivos na pasta, rode este script de')
            print('       novo — o portal confia no manifesto, e foto não declarada')
            print('       não aparece (ele avisa isso no console do navegador).')

    if '--csv' in sys.argv:
        destino = os.path.join(PASTA, 'LISTA-DE-FOTOS.csv')
        with io.open(destino, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['nome', 'papel', 'slug',
                                              'arquivo_esperado', 'arquivo_encontrado',
                                              'na_pasta', 'autorizacao'])
            w.writeheader()
            w.writerows(linhas)
        print('gravado: ' + os.path.relpath(destino, RAIZ))
    return 0


if __name__ == '__main__':
    sys.exit(main())
