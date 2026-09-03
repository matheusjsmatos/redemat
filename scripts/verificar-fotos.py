# -*- coding: utf-8 -*-
"""verificar-fotos.py — confere o sistema de fotos e a saúde geral das páginas.

USO
    python3 -m http.server 8099 --directory .   # em outro terminal
    python3 scripts/verificar-fotos.py

Verificação final: 14 páginas, erro de JS, 404 locais, e os três estados do
manifesto de fotos (vazio, preenchido, ausente).

Duas coisas que o teste tem de respeitar, senão acusa falha onde não há:

  - Só contam recursos servidos pelo próprio portal. Fontes do Google, cdnjs e
    tiles do OpenStreetMap ficam de fora: o contêiner de verificação não tem
    saída para eles (ERR_TUNNEL_CONNECTION_FAILED).
  - As abas de pós-doutorandos e da secretaria começam com `hidden`, e as fotos
    são `loading="lazy"`: dentro de painel escondido o navegador não busca a
    imagem nenhuma. Para conferir essas fotos é preciso ABRIR a aba primeiro —
    é assim que o visitante faz, e é assim que o teste faz.
"""
import io
import os
import re
import shutil
import subprocess
import sys

from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(RAIZ, 'assets', 'img', 'pessoas')
HOST = '127.0.0.1:8099'
BASE = 'http://' + HOST + '/'

PAGINAS = ['index.html'] + ['pages/' + f for f in sorted(os.listdir(os.path.join(RAIZ, 'pages')))
                            if f.endswith('.html')]

IGNORAR = ('sync-info.js',)   # só existe depois da sincronização do ScriptLattes

def fixtures():
    """Uma imagem 8x8 em cada formato aceito, gerada na hora.

    Precisa ser imagem de verdade: o teste confere `naturalWidth > 0` depois de
    `decode()`, e bytes inventados à mão passam pelo 404 mas não decodificam —
    o que aparece como falha do portal sem ser.
    """
    from PIL import Image
    im = Image.new('RGB', (8, 8), (30, 60, 120))
    out = {}
    for ext, fmt in (('png', 'PNG'), ('jpg', 'JPEG'), ('jpeg', 'JPEG'),
                     ('webp', 'WEBP'), ('gif', 'GIF'), ('avif', 'AVIF')):
        b = io.BytesIO()
        try:
            im.save(b, fmt)
        except Exception as e:                     # AVIF depende do Pillow com libavif
            print('   (sem fixture .%s: %s — formato não testado)' % (ext, e))
            continue
        out[ext] = b.getvalue()
    return out


FIX = fixtures()

# Conta as fotos vivas percorrendo TODAS as abas, uma a uma.
JS_FOTOS = """async () => {
  const abas = [...document.querySelectorAll('[role="tab"]')];
  for (const a of abas) { a.click(); await new Promise(r => setTimeout(r, 120)); }
  const im = [...document.querySelectorAll('.av img')];
  im.forEach(i => { i.loading = 'eager'; });
  await new Promise(r => setTimeout(r, 900));
  await Promise.all(im.map(i => i.decode ? i.decode().catch(() => {}) : null));
  return {
    total: im.length,
    vivas: im.filter(i => i.naturalWidth > 0).length,
    exts: im.filter(i => i.naturalWidth > 0)
            .map(i => i.src.split('.').pop()).sort(),
    mortas: im.filter(i => i.naturalWidth === 0).map(i => i.getAttribute('data-slug'))
  };
}"""


def local(url):
    return HOST in url


def visita(pg, pagina, espera=350, abrir_abas=False):
    erros, q404 = [], []

    def console(m):
        url = (m.location or {}).get('url') or ''
        if m.type != 'error':
            return
        if any(i in url for i in IGNORAR):
            return
        if 'net::' in m.text and not local(url):
            return          # recurso externo bloqueado pelo contêiner
        erros.append(m.text + ('  [' + url.replace(BASE, '') + ']' if url else ''))

    p = pg.new_page()
    p.on('console', console)
    p.on('pageerror', lambda e: erros.append('EXCEÇÃO: ' + str(e)))
    p.on('response', lambda r: q404.append(r.url)
         if r.status >= 400 and local(r.url) else None)
    p.goto(BASE + pagina, wait_until='networkidle')
    p.wait_for_timeout(espera)
    largura = p.evaluate('document.documentElement.scrollWidth - '
                         'document.documentElement.clientWidth')
    dados = p.evaluate("""() => ({
        av: document.querySelectorAll('.av').length,
        img: document.querySelectorAll('.av img').length,
        ini: document.querySelectorAll('.av--sem-foto').length,
        aninhado: document.querySelectorAll('a.mural-card a').length
    })""")
    if abrir_abas:
        dados.update(p.evaluate(JS_FOTOS))
    p.close()
    q404 = [u for u in q404 if not any(i in u for i in IGNORAR)]
    return erros, q404, largura, dados


def main():
    ruim = 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')

        # ---------------- A. varredura das 14 páginas (manifesto vazio)
        print('=== A. 14 páginas, manifesto vazio (estado de entrega)')
        pg = nav.new_context(viewport={'width': 1280, 'height': 900})
        tot_av = 0
        for pagina in PAGINAS:
            erros, q404, larg, d = visita(pg, pagina)
            tot_av += d['av']
            ok = not erros and not q404 and larg <= 0 and d['aninhado'] == 0
            if not ok:
                ruim += 1
            print('%-4s %-28s av:%-3d img:%-2d ini:%-3d scrollX:%+d' %
                  ('OK' if ok else 'FALHA', pagina, d['av'], d['img'], d['ini'], larg))
            for e in erros[:3]:
                print('       JS: ' + e[:160])
            for u in q404[:5]:
                print('       404: ' + u.replace(BASE, ''))
        pg.close()
        print('   %d avatares no portal, todos com iniciais — nenhuma foto enviada ainda'
              % tot_av)

        # ---------------- B. quatro formatos declarados no manifesto
        print()
        print('=== B. cada formato aceito, declarado no manifesto — renderiza?')
        criados = []
        try:
            amostras = [('geraldo-lucio-de-faria', 'png'),          # docente
                        ('thiago-cazati', 'avif'),                  # docente
                        ('dalila-chaves-sicupira', 'jpeg'),         # docente + coordenação
                        ('adarlene-moreira-silva', 'webp'),         # pós-doc
                        ('gustavo-henrique-silvestre', 'gif'),      # pós-doc
                        ('rodrigo-cesario-lourenco', 'jpg')]        # secretaria
            amostras = [(s, e) for s, e in amostras if e in FIX]
            for slug, ext in amostras:
                caminho = os.path.join(PASTA, slug + '.' + ext)
                io.open(caminho, 'wb').write(FIX[ext])
                criados.append(caminho)
            n_doc = sum(1 for s, e in amostras
                        if s not in ('adarlene-moreira-silva',
                                     'gustavo-henrique-silvestre',
                                     'rodrigo-cesario-lourenco'))
            subprocess.run([sys.executable, 'scripts/conferir-fotos.py', '--manifesto'],
                           cwd=RAIZ, capture_output=True)
            man = io.open(os.path.join(PASTA, 'fotos.js'), encoding='utf-8').read()
            decl = dict(re.findall(r'"([^"]+)": "(\w+)"', man))
            print('   manifesto: %d — %s' % (len(decl), ', '.join(sorted(
                '%s→%s' % (k.split('-')[0], v) for k, v in decl.items()))))

            pg = nav.new_context(viewport={'width': 1280, 'height': 900})
            for pagina, n in (('pages/pessoas.html', len(amostras)),
                              ('pages/programa.html', 1)):
                erros, q404, larg, d = visita(pg, pagina, 500, abrir_abas=True)
                ok = (not erros and not q404 and d['img'] == n and d['vivas'] == n)
                if not ok:
                    ruim += 1
                print('%-4s %-24s <img>:%d (esperado %d) · vivas:%d [%s] · 404:%d' %
                      ('OK' if ok else 'FALHA', pagina, d['img'], n, d['vivas'],
                       ' '.join(d['exts']), len(q404)))
                if d.get('mortas'):
                    print('       sem carregar: ' + ', '.join(d['mortas'][:6]))
                for u in q404[:4]:
                    print('       404: ' + u.replace(BASE, ''))
            pg.close()
        finally:
            for c in criados:
                os.remove(c)
            subprocess.run([sys.executable, 'scripts/conferir-fotos.py',
                            '--manifesto', '--csv'], cwd=RAIZ, capture_output=True)

        # ---------------- C. manifesto vazio + foto solta: avisa e não sonda
        print()
        print('=== C. manifesto vazio com foto solta na pasta')
        solto = os.path.join(PASTA, 'thiago-cazati.gif')
        io.open(solto, 'wb').write(FIX['gif'])
        try:
            pg = nav.new_context(viewport={'width': 1280, 'height': 900})
            p = pg.new_page()
            msgs, q404 = [], []
            p.on('console', lambda m: msgs.append(m.text))
            p.on('response', lambda r: q404.append(r.url)
                 if r.status >= 400 and local(r.url) else None)
            p.goto(BASE + 'pages/pessoas.html', wait_until='networkidle')
            p.evaluate(JS_FOTOS)
            img = p.evaluate("document.querySelectorAll('.av img').length")
            p.close()
            pg.close()
            fotos404 = [u for u in q404 if '/img/pessoas/' in u]
            aviso = any('conferir-fotos.py' in m for m in msgs)
            ok = not fotos404 and aviso and img == 0
            if not ok:
                ruim += 1
            print('%-4s 404 de foto: %d · aviso no console: %s · <img> geradas: %d'
                  % ('OK' if ok else 'FALHA', len(fotos404), 'sim' if aviso else 'NÃO', img))
        finally:
            os.remove(solto)

        # ---------------- D. sem manifesto: sondagem em cadeia funciona
        print()
        print('=== D. fotos.js ausente + foto só em .gif — sondagem em cadeia')
        man = os.path.join(PASTA, 'fotos.js')
        guarda = man + '.bak'
        shutil.move(man, guarda)
        io.open(os.path.join(PASTA, 'thiago-cazati.gif'), 'wb').write(FIX['gif'])
        try:
            pg = nav.new_context(viewport={'width': 1280, 'height': 900})
            p = pg.new_page()
            p.goto(BASE + 'pages/pessoas.html', wait_until='networkidle')
            r = p.evaluate("""async () => {
                const im = [...document.querySelectorAll('.av img')];
                im.forEach(i => { i.loading = 'eager'; });
                await new Promise(r => setTimeout(r, 2500));
                const vivas = [...document.querySelectorAll('.av img')]
                                .filter(i => i.naturalWidth > 0);
                return { restantes: document.querySelectorAll('.av img').length,
                         vivas: vivas.length,
                         gif: vivas.filter(i => /\\.gif$/.test(i.src))
                                   .map(i => i.getAttribute('data-slug')) };
            }""")
            p.close()
            pg.close()
            ok = r['vivas'] == 1 and r['gif'] == ['thiago-cazati']
            if not ok:
                ruim += 1
            print('%-4s <img> restantes: %d · vivas: %d (esperado 1) · em .gif: %s'
                  % ('OK' if ok else 'FALHA', r['restantes'], r['vivas'], r['gif'] or '—'))
        finally:
            os.remove(os.path.join(PASTA, 'thiago-cazati.gif'))
            shutil.move(guarda, man)

        # ---------------- E. pontos de quebra
        print()
        print('=== E. 8 pontos de quebra × 14 páginas')
        for larg in (1920, 1440, 1280, 1024, 768, 640, 480, 360):
            pg = nav.new_context(viewport={'width': larg, 'height': 900})
            pior, onde = 0, ''
            for pagina in PAGINAS:
                p = pg.new_page()
                p.goto(BASE + pagina, wait_until='networkidle')
                p.wait_for_timeout(200)
                x = p.evaluate('document.documentElement.scrollWidth - '
                               'document.documentElement.clientWidth')
                if x > pior:
                    pior, onde = x, pagina
                p.close()
            pg.close()
            if pior > 0:
                ruim += 1
            print('%-4s %4dpx  scrollX máx %+d %s' %
                  ('OK' if pior <= 0 else 'FALHA', larg, pior, onde))

        nav.close()

    print()
    print('RESULTADO: %s' % ('tudo OK' if ruim == 0 else '%d verificação(ões) com falha' % ruim))
    return 1 if ruim else 0


if __name__ == '__main__':
    sys.exit(main())
