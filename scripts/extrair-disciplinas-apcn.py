#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai a estrutura curricular (seção 8 da APCN) para data/disciplinas.json.

A seção 8 do documento é texto corrido: o Word não marca "disciplina" como
estrutura, só numera os parágrafos. O que delimita um componente é o padrão
    8.<g>.<n>. <Nome> — <N> h — <M> créditos
seguido de "Ementa." e "Referências." até o próximo marcador. O agrupamento
vem do primeiro nível: 8.4 é o núcleo comum e 8.5 a 8.8 são as quatro linhas.

Os docentes responsáveis NÃO estão junto da ementa: estão na seção 8.3, numa
lista corrida por linha. São casados aqui por nome normalizado, e quando o
nome na 8.3 não bate com nenhuma ementa o script DIZ — não descarta em
silêncio, porque divergência entre as duas listas é informação, não ruído.

    python3 scripts/extrair-disciplinas-apcn.py <caminho do .docx ou .txt>
"""
import json, os, re, sys, unicodedata, zipfile, html as _html

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, 'data', 'disciplinas.json')

GRUPOS = {
    '4': ('Núcleo comum', None, None),
    '5': ('Área 1, Linha 1.1', 'Processamento, Estrutura e Desempenho de Materiais',
          'Processamento, Manufatura e Engenharia de Superfícies'),
    '6': ('Área 1, Linha 1.2', 'Processamento, Estrutura e Desempenho de Materiais',
          'Estrutura, Propriedades, Degradação, Modelagem e Integridade'),
    '7': ('Área 2, Linha 2.1', 'Materiais Estratégicos, Funcionais e Sustentáveis',
          'Recursos Minerais, Minerais Críticos e Economia Circular'),
    '8': ('Área 2, Linha 2.2', 'Materiais Estratégicos, Funcionais e Sustentáveis',
          'Materiais Funcionais, Biomateriais, Transição Energética, '
          'Desenvolvimento de Novos Materiais e Inovação Tecnológica'),
}

# O nome não pode começar por dígito: sem isso o padrão casa dentro de uma
# remissão como "...apresentadas no item 8.5.8.8.8.6. Tecnologia..." e inventa
# uma disciplina cujo nome é o número da seguinte.
CAB = re.compile(r'8\.([4-8])\.(\d+)\.\s*(?!\d)(.{3,140}?)\s*[—-]\s*(\d+)\s*h\s*[—-]\s*(\d+)\s*cr[ée]ditos')

# "Disciplina compartilhada com a Linha 1.1. Ementa e referências apresentadas
# no item 8.5.8." — não é disciplina nova, é a mesma ofertada em duas linhas.
REMISSAO = re.compile(r'compartilhada com a (Linha [\d.]+).*?item\s*(8\.\d+\.\d+)', re.S)


def norm(s):
    s = unicodedata.normalize('NFD', str(s or ''))
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9 ]+', ' ', re.sub(r'\s+', ' ', s).strip().lower()).strip()


def le(caminho):
    if caminho.lower().endswith('.docx'):
        x = zipfile.ZipFile(caminho).read('word/document.xml').decode('utf-8', 'replace')
        x = re.sub(r'</w:p>', '\n', x)
        return _html.unescape(re.sub(r'<[^>]+>', '', x))
    return open(caminho, encoding='utf-8').read()


def corta(t, rotulo, seguintes):
    """Texto após `rotulo` até o primeiro dos `seguintes`. Sem o rótulo, ''."""
    i = t.find(rotulo)
    if i < 0:
        return ''
    t = t[i + len(rotulo):]
    fins = [t.find(s) for s in seguintes if t.find(s) > 0]
    return re.sub(r'\s+', ' ', t[:min(fins)] if fins else t).strip(' .;')


def responsaveis(txt):
    """Seção 8.3: 'Nome da disciplina — Fulano, Beltrano; Outra — ...'."""
    i = txt.find('8.3.')
    j = txt.find('8.4. Ementas')
    if i < 0 or j < 0:
        return {}
    bloco = txt[i:j]
    mapa = {}
    for trecho in re.split(r'(?:Núcleo comum:|Linha \d\.\d:)', bloco)[1:]:
        for item in trecho.split(';'):
            if '—' not in item and '-' not in item:
                continue
            p = re.split(r'\s[—–]\s|\s-\s', item, maxsplit=1)
            if len(p) != 2:
                continue
            nome, pessoas = p
            nome = re.sub(r'^[^A-Za-zÀ-ÿ]+', '', nome).strip(' .')
            pessoas = re.sub(r'\s*\(.*?\)', '', pessoas)
            pessoas = re.sub(r'\bcom (?:apoio|participação)[^,.;]*', '', pessoas, flags=re.I)
            lista = [x.strip(' .') for x in re.split(r',| e (?=[A-ZÀ-Ý])', pessoas)
                     if 3 < len(x.strip()) < 60 and not x.strip().lower().startswith(
                         ('conforme', 'sem ', 'o objetivo'))]
            if nome and lista:
                mapa.setdefault(norm(nome), []).extend(lista)
    return {k: list(dict.fromkeys(v)) for k, v in mapa.items()}


def main():
    if len(sys.argv) < 2:
        sys.exit('uso: extrair-disciplinas-apcn.py <arquivo.docx|.txt>')
    txt = le(sys.argv[1])
    resp = responsaveis(txt)

    marcas = list(CAB.finditer(txt))
    discs, usados = [], set()
    for k, m in enumerate(marcas):
        g, n, nome, h, cr = m.groups()
        nome = re.sub(r'\s+', ' ', nome).strip(' .:')
        corpo = txt[m.end(): marcas[k + 1].start() if k + 1 < len(marcas) else len(txt)]
        # Duas disciplinas escrevem "Ementa:" com dois-pontos, e os três
        # Tópicos Avançados dividem uma "Ementa comum." declarada só na última.
        ementa = ''
        for rot in ('Ementa comum.', 'Ementa.', 'Ementa:'):
            ementa = corta(corpo, rot, ['Referências.', 'Referencias.', 'Referências:'])
            if ementa:
                break
        refs = ''
        for rot in ('Referências.', 'Referencias.', 'Referências:'):
            refs = corta(corpo, rot, ['Ementa.', 'Ementa:', '\n8.'])
            if refs:
                break
        rot, area, linha = GRUPOS[g]
        rem = REMISSAO.search(corpo[:400])
        chave = norm(nome)
        docentes = resp.get(chave, [])
        if not docentes:                      # casamento frouxo: prefixo comum
            for k2, v in resp.items():
                if k2 and (k2.startswith(chave[:22]) or chave.startswith(k2[:22])):
                    docentes = v; chave = k2; break
        if docentes:
            usados.add(chave)
        discs.append({
            'id': '%s.%s' % (g, n), 'nome': nome,
            'compartilhada_com': rem.group(1) if rem else None,
            'ementa_em': rem.group(2) if rem else None,
            'horas': int(h), 'creditos': int(cr),
            'grupo': rot, 'area': area, 'linha': linha,
            'ementa': ementa, 'referencias': refs,
            'docentes': docentes,
            'fonte': 'APCN 2026', 'ref': 'seção 8.%s.%s' % (g, n),
            'status': 'VALIDADO' if ementa else 'PARCIAL',
        })

    por_sec = {'8.%s' % x['id']: x for x in discs}
    # Remissão: a disciplina compartilhada herda ementa, referências e docentes
    # da entrada original, e guarda de onde veio.
    for x in discs:
        if x['ementa_em'] and x['ementa_em'] in por_sec:
            orig = por_sec[x['ementa_em']]
            x['ementa'] = x['ementa'] or orig['ementa']
            x['referencias'] = x['referencias'] or orig['referencias']
            x['docentes'] = x['docentes'] or orig['docentes']
            x['status'] = 'VALIDADO' if x['ementa'] else 'PARCIAL'
    # "Ementa comum.": os Tópicos Avançados I, II e III dividem uma só, escrita
    # depois do terceiro marcador. Quem ficou sem herda do irmão seguinte.
    for i, x in enumerate(discs):
        if x['ementa']:
            continue
        for y in discs[i + 1:i + 4]:
            if y['grupo'] == x['grupo'] and y['ementa'] and \
               norm(x['nome'])[:28] == norm(y['nome'])[:28]:
                x['ementa'], x['referencias'] = y['ementa'], y['referencias']
                x['ementa_comum_com'] = '8.' + y['id']
                x['status'] = 'VALIDADO'
                break

    sobra = [k for k in resp if k not in usados]
    d = {'meta': {'fonte': 'Proposta APCN — Doutorado REDEMAT 2026',
                  'ref': 'seção 8 — Estrutura curricular e disciplinas',
                  'arquivo': os.path.basename(sys.argv[1]),
                  'total': len(discs),
                  'sem_ementa': sum(1 for x in discs if not x['ementa']),
                  'sem_docente': sum(1 for x in discs if not x['docentes']),
                  'na_8_3_sem_ementa': sobra},
          'disciplinas': discs}
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    json.dump(d, open(SAIDA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print('disciplinas: %d' % len(discs))
    for g in sorted(GRUPOS):
        sub = [x for x in discs if x['id'].startswith(g + '.')]
        print('  8.%s %-20s %2d  (sem ementa: %d, sem docente: %d)' % (
            g, GRUPOS[g][0], len(sub),
            sum(1 for x in sub if not x['ementa']),
            sum(1 for x in sub if not x['docentes'])))
    if sobra:
        print('\nNa seção 8.3 mas sem ementa correspondente (%d):' % len(sobra))
        for s in sobra:
            print('  -', s[:70])


if __name__ == '__main__':
    main()
