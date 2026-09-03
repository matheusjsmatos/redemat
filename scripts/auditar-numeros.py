#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditar-numeros.py — confere cada número publicado no portal contra a entrega
consolidada, e imprime um checklist com veredito por item.

USO
    python3 scripts/auditar-numeros.py <pasta-da-entrega-consolidada>
    python3 scripts/auditar-numeros.py ~/Dropbox/codex/apcn/10_analises/entrega_atualizada_lattes_20260829

POR QUE ESTE SCRIPT EXISTE
    O portal publicou 202 como "artigos com coautoria de discentes/egressos".
    202 é a SOMA POR DOCENTE; o número de artigos únicos é 168. É a mesma
    confusão entre "contagem por docente" e "produto único" que já apareceu em
    outros indicadores. Este script existe para que essa classe de erro seja
    detectada por máquina, e não por leitura atenta.

REGRA DE OURO
    Todo indicador de produção tem DUAS contagens legítimas e diferentes:
      · produto único   — cada artigo/projeto/patente conta uma vez no Programa
      · soma por docente — cada artigo conta uma vez por docente coautor
    Publicar uma com o rótulo da outra é erro de fato, não de estilo. O script
    imprime as duas, sempre, e o portal precisa dizer qual está mostrando.

O QUE NÃO FAZ
    Não escreve em site-data.js. Imprime o checklist e um bloco pronto para
    colar; a decisão de publicar é da coordenação.
"""

import collections
import csv
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DATA = os.path.join(RAIZ, 'assets', 'js', 'site-data.js')


def rows(caminho):
    if not os.path.exists(caminho):
        return None
    with io.open(caminho, encoding='utf-8-sig', errors='replace', newline='') as f:
        return list(csv.DictReader(f))


def norm(t):
    return re.sub(r'[^a-z0-9]', '', (t or '').lower())[:70]


def num(s):
    s = re.sub(r'[^\d,.-]', '', str(s or ''))
    if not s:
        return None
    if ',' in s and '.' in s:
        s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        s = s.replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


# --------------------------------------------------------- valores do portal
def ler_site_data():
    """Lê os números hoje publicados, direto do site-data.js."""
    if not os.path.exists(SITE_DATA):
        return {}
    t = io.open(SITE_DATA, encoding='utf-8').read()
    def g(pad, conv=int):
        m = re.search(pad, t)
        if not m:
            return None
        try:
            return conv(m.group(1).replace('.', '').replace(',', '.')
                        if conv is float else m.group(1))
        except ValueError:
            return None
    return {
        'total_unico': g(r'total_unico:\s*(\d+)'),
        'total_somado': g(r'total_somado:\s*(\d+)'),
        'com_doi': g(r'com_doi:\s*(\d+)'),
        'n_periodicos': g(r'n_periodicos:\s*(\d+)'),
        'com_discentes': g(r'com_discentes:\s*\{\s*valor:\s*(\d+)'),
        'q1': g(r'Q1:\s*(\d+)'), 'q2': g(r'Q2:\s*(\d+)'),
        'q3': g(r'Q3:\s*(\d+)'), 'q4': g(r'Q4:\s*(\d+)'),
        'sem_quartil': g(r'sem_quartil:\s*(\d+)'),
        'ne': g(r'\bne:\s*(\d+)'),
        'proj_unicos': g(r'unicos_recorte:\s*(\d+)'),
        # "vinculos" também aparece na lista de países; ancora no bloco projetos
        'proj_vinculos': g(r'unicos_recorte:\s*\d+,\s*\n\s*vinculos:\s*(\d+)'),
        'grafo_nos': g(r'nos:\s*(\d+),\s*arestas'),
        'grafo_arestas': g(r'arestas:\s*(\d+)'),
    }


# ------------------------------------------------------------------ checklist
CK = []


def check(item, publicado, consolidado, fonte, nota=''):
    if publicado is None:
        v = 'NAO_PUBLICADO'
    elif consolidado is None:
        v = 'SEM_FONTE'
    elif abs(float(publicado) - float(consolidado)) < 0.5:
        v = 'OK'
    else:
        v = 'DIVERGENTE'
    CK.append({'item': item, 'publicado': publicado, 'consolidado': consolidado,
               'veredito': v, 'fonte': fonte, 'nota': nota})


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    B = os.path.expanduser(sys.argv[1].rstrip('/'))
    D = os.path.join(B, '09_relatorio_producao_bibliografica_tecnica_tecnologica_20260831')
    S = ler_site_data()

    # ---------------------------------------------------- produção de artigos
    ev = rows(os.path.join(D, '05_evidencias_artigos_deduplicados.csv'))
    if ev:
        # Dedup determinístico: o mesmo artigo aparece uma vez por docente
        # coautor, e às vezes só uma dessas linhas traz o quartil. Fica a linha
        # COM métrica — descartá-la por ordem de leitura inventaria um "sem
        # quartil" que a fonte não afirma.
        chave = {}
        for x in ev:
            k = x['DOI'].strip().lower() or norm(x['Título'])
            ant = chave.get(k)
            if ant is None or (not (ant['Quartil'] or '').strip()
                               and (x['Quartil'] or '').strip()):
                chave[k] = x
        unicos = len(chave)
        por_ano = collections.Counter(x['Ano'] for x in chave.values())
        doi_dist = len({x['DOI'].strip().lower() for x in ev if x['DOI'].strip()})
        periodicos = len({(x['Periódico'] or '').strip() for x in ev if (x['Periódico'] or '').strip()})
        q_unico = collections.Counter((x['Quartil'] or '').strip() or 'SEM' for x in chave.values())
        q_reg = collections.Counter((x['Quartil'] or '').strip() or 'SEM' for x in ev)

        check('Artigos únicos 2021–2026', S.get('total_unico'), unicos,
              '09/05_evidencias_artigos_deduplicados.csv',
              'deduplicado por DOI; sem DOI, título normalizado')
        check('Registros docente–artigo', S.get('total_somado'), len(ev),
              '09/05_evidencias_artigos_deduplicados.csv',
              'soma por docente — NÃO é contagem de artigos')
        check('Artigos com DOI distinto', S.get('com_doi'), doi_dist,
              '09/05_evidencias_artigos_deduplicados.csv')
        check('Periódicos distintos', S.get('n_periodicos'), periodicos,
              '09/05_evidencias_artigos_deduplicados.csv')
        for q in ('Q1', 'Q2', 'Q3', 'Q4'):
            check('Artigos únicos em ' + q, S.get(q.lower()), q_unico.get(q, 0),
                  '09/05_evidencias_artigos_deduplicados.csv',
                  'por registro docente–artigo seria %d' % q_reg.get(q, 0))
        check('Artigos sem métrica Scopus', S.get('sem_quartil'),
              q_unico.get('SEM', 0),
              '09/05_evidencias_artigos_deduplicados.csv',
              'periódico não localizado no snapshot — não é qualidade zero')
        check('Artigos marcados NE (não elegível)', S.get('ne'),
              q_unico.get('NE', 0),
              '09/05_evidencias_artigos_deduplicados.csv',
              'contados à parte dos sem métrica; a soma fecha em %d'
              % (sum(q_unico.values())))
        print('SÉRIE ANUAL de artigos únicos:', dict(sorted(por_ano.items())))

    # --------------------------------------------- coautoria com discentes
    amplo = rows(os.path.join(B, '06_cruzamento_discentes_lattes_2021_2026',
                              'resumo_anual_2021_2026.csv'))
    pdoc = rows(os.path.join(B, '06_cruzamento_discentes_lattes_2021_2026',
                             'resumo_por_docente_2021_2026.csv'))
    if amplo and pdoc:
        unicos_disc = sum(int(x['artigos_unicos_com_discente_egresso']) for x in amplo)
        soma_disc = sum(int(x['artigos_com_discentes_egressos_2021_2026']) for x in pdoc)
        check('Artigos ÚNICOS com coautoria de discente/egresso',
              S.get('com_discentes'), unicos_disc,
              '06/resumo_anual_2021_2026.csv',
              'a soma por docente dá %d — é esse número que estava publicado' % soma_disc)
        print('SÉRIE ANUAL com discente/egresso:',
              {x['ano']: int(x['artigos_unicos_com_discente_egresso']) for x in amplo})
        print('SOMA POR DOCENTE (não publicar como artigos):', soma_disc)

    estrito = rows(os.path.join(D, '02_producao_com_discentes_egressos.csv'))
    if estrito:
        art = len({(x['Produção'].strip().lower(), x['Ano']) for x in estrito})
        print('CRITÉRIO ESTRITO (orientador comprovado): %d artigos, %d docentes'
              % (art, len({x['Nome Docente'] for x in estrito})))

    # ------------------------------------------------------------- formação
    t = rows(os.path.join(D, '03a_teses_defendidas.csv'))
    d = rows(os.path.join(D, '03b_dissertacoes_defendidas.csv'))
    if t and d:
        print('DEFESAS COMPROVADAS 2021–2026: %d teses + %d dissertações = %d'
              % (len(t), len(d), len(t) + len(d)))
        print('  teses por ano      :', dict(sorted(collections.Counter(x['Ano'] for x in t).items())))
        print('  dissertações por ano:', dict(sorted(collections.Counter(x['Ano'] for x in d).items())))

    # ------------------------------------------------------------- patentes
    pat = rows(os.path.join(D, '04_patentes.csv'))
    dest = rows(os.path.join(D, '04b_destaques_patentes_pi.csv'))
    if pat:
        print('PATENTES: %d únicas no Lattes (todos os anos), %d destacadas'
              % (len(pat), len(dest or [])))

    # ------------------------------------------------------------- projetos
    par = rows(os.path.join(B, '07 - projetos', 'capitulo_11_preenchido',
                            'sintese_capitulo_11.csv'))
    if par:
        v = {x['Indicador']: x['Resultado'] for x in par}
        check('Projetos únicos no recorte', S.get('proj_unicos'),
              num(v.get('Projetos únicos no recorte')),
              '07/sintese_capitulo_11.csv')
        check('Vínculos professor–projeto', S.get('proj_vinculos'),
              num(v.get('Vínculos professor–projeto consolidados')),
              '07/sintese_capitulo_11.csv')
        print('PROJETOS — síntese da planilha atualizada:')
        for k, val in v.items():
            print('   %-52s %s' % (k[:52], val))

    # --------------------------------------------------------------- saída
    print()
    print('=' * 78)
    print('CHECKLIST')
    print('=' * 78)
    larg = max(len(c['item']) for c in CK) if CK else 10
    for c in CK:
        print('%-11s %-*s  portal=%-10s fonte=%-10s  %s'
              % (c['veredito'], larg, c['item'],
                 c['publicado'], c['consolidado'], c['fonte']))
        if c['nota']:
            print('%-11s %-*s  %s' % ('', larg, '', c['nota']))
    div = [c for c in CK if c['veredito'] == 'DIVERGENTE']
    print()
    print('%d item(ns) conferido(s) · %d OK · %d DIVERGENTE · %d sem publicação'
          % (len(CK), sum(1 for c in CK if c['veredito'] == 'OK'), len(div),
             sum(1 for c in CK if c['veredito'] == 'NAO_PUBLICADO')))

    saida = os.path.join(RAIZ, 'data', 'checklist-numeros.csv')
    with io.open(saida, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['item', 'publicado', 'consolidado',
                                          'veredito', 'fonte', 'nota'])
        w.writeheader()
        w.writerows(CK)
    print('gravado: ' + os.path.relpath(saida, RAIZ))
    return 0


if __name__ == '__main__':
    sys.exit(main())
