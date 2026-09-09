#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""importar-documentos.py — traz para o portal os documentos que ele hoje
linka no site antigo, e reescreve os links para o arquivo local.

USO
    python3 scripts/importar-documentos.py [pasta do backup] [--aplicar]

POR QUE
    `site-data.js` aponta atas e normas para
    https://redemat.ufop.br/sites/default/files/... — endereços do OpenScholar
    que MORREM quando o domínio for substituído (Fase 4). Guardar o arquivo no
    próprio portal é o que faz o link sobreviver à troca.

O SUFIXO __q
    O script de backup grava cada arquivo com um sufixo de hash antes da
    extensão (`ata_..._2024__q0d3e7b01.pdf`), vindo da query string da URL.
    Aqui o sufixo é removido, e o nome volta a ser o que a URL original pedia
    — é assim que os dois lados se encontram.

Sem --aplicar, apenas relata.
"""
import io, os, re, shutil, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP = (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--')
          else os.path.expanduser('~/Dropbox/claude/redemat/backup-site-redemat'))
APLICAR = '--aplicar' in sys.argv
DESTINO = os.path.join(RAIZ, 'documentos')
BASE_URL = 'https://redemat.ufop.br/sites/default/files/'
SUFIXO = re.compile(r'__q[0-9a-f]{6,10}(?=\.[A-Za-z0-9]+$)')


def acha_pasta_de_arquivos(raiz):
    """O backup pode ter uma subpasta com nome esquisito; procura files/."""
    for base, dirs, _ in os.walk(raiz):
        if base.replace('\\', '/').endswith('sites/default/files/redemat/files'):
            return base
    return None


def main():
    origem = acha_pasta_de_arquivos(BACKUP)
    if not origem:
        sys.exit('Não achei sites/default/files/redemat/files em ' + BACKUP)

    # nome limpo -> caminho no backup
    disponivel = {}
    for n in os.listdir(origem):
        limpo = SUFIXO.sub('', n)
        disponivel.setdefault(limpo, os.path.join(origem, n))
    print('backup: %d arquivos em %s' % (len(disponivel), os.path.relpath(origem, BACKUP)))

    sd = os.path.join(RAIZ, 'assets', 'js', 'site-data.js')
    texto = io.open(sd, encoding='utf-8').read()
    urls = sorted(set(re.findall(re.escape(BASE_URL) + r"[^'\"\s]+", texto)))
    print('site-data aponta para %d arquivos do site antigo' % len(urls))

    achados, faltando, novo = [], [], texto
    for u in urls:
        nome = u.rsplit('/', 1)[-1]
        if nome in disponivel:
            achados.append((u, nome, disponivel[nome]))
            novo = novo.replace(u, '../documentos/' + nome)
        else:
            faltando.append((u, nome))

    for u, nome, src in achados:
        print('  OK   %s' % nome)
    for u, nome in faltando:
        print('  FALTA %s' % nome)

    if not APLICAR:
        print('\n(relatório apenas — rode com --aplicar para copiar e reescrever)')
        return 0

    os.makedirs(DESTINO, exist_ok=True)
    for _, nome, src in achados:
        shutil.copy2(src, os.path.join(DESTINO, nome))
    io.open(sd, 'w', encoding='utf-8').write(novo)
    print('\ncopiados %d para documentos/ e reescritos os links em site-data.js'
          % len(achados))
    if faltando:
        print('%d continuam apontando para o site antigo, por não estarem no '
              'backup.' % len(faltando))
    return 0


if __name__ == '__main__':
    sys.exit(main())
