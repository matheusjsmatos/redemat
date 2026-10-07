#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Devolve o conteúdo de planilhas/REDEMAT-dados-do-site.xlsx para os dados.

É a volta do caminho que `gerar-planilha-dados.py` faz na ida. Quem mantém o
Programa edita a planilha; este script escreve o que mudou em
data/sites-docentes.json e data/disciplinas.json.

Só grava o que a planilha autoriza editar — as colunas de fundo amarelo. Uma
alteração feita numa coluna cinza é relatada e ignorada, porque aquele campo
vem de outra fonte (coleta CAPES, Lattes, proposta APCN) e seria desfeito na
próxima atualização automática. Ignorar em silêncio faria a pessoa pensar que
a edição pegou.

    python3 scripts/planilha-para-dados.py            # mostra o que mudaria
    python3 scripts/planilha-para-dados.py --aplicar  # grava
"""
import argparse, json, os, re, sys
from openpyxl import load_workbook

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(RAIZ, 'planilhas', 'REDEMAT-dados-do-site.xlsx')
SITES = os.path.join(RAIZ, 'data', 'sites-docentes.json')
DISC = os.path.join(RAIZ, 'data', 'disciplinas.json')

EDIT_DOC = ['Site pessoal', 'Site do grupo', 'Nome do grupo', 'Observação']
EDIT_DISC = ['Nome', 'Horas', 'Créditos', 'Docentes responsáveis',
             'Ementa', 'Referências']
CAMPO_DOC = {'Site pessoal': 'site_pessoal', 'Site do grupo': 'site_grupo',
             'Nome do grupo': 'nome_grupo', 'Observação': 'observacao'}
CAMPO_DISC = {'Nome': 'nome', 'Horas': 'horas', 'Créditos': 'creditos',
              'Docentes responsáveis': 'docentes', 'Ementa': 'ementa',
              'Referências': 'referencias'}

URL_OK = re.compile(r'^https?://[^\s]+\.[^\s]+$')


def linhas(ws):
    cab = [c.value for c in ws[1]]
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r and r[0] is not None:
            yield dict(zip(cab, r))


def txt(v):
    return '' if v is None else str(v).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--aplicar', action='store_true')
    a = ap.parse_args()

    if not os.path.exists(PLAN):
        sys.exit('planilha não encontrada: %s' % PLAN)
    wb = load_workbook(PLAN, data_only=True)

    mudancas, avisos = [], []

    # ------------------------------------------------------------- docentes
    sites = json.load(open(SITES, encoding='utf-8'))
    por_nome = {d['nome']: d for d in sites['docentes']}
    for lin in linhas(wb['Docentes']):
        nome = txt(lin.get('Nome'))
        reg = por_nome.get(nome)
        novo = {CAMPO_DOC[c]: txt(lin.get(c)) for c in EDIT_DOC}
        if not any(novo.values()):
            if reg and any(reg.get(v) for v in CAMPO_DOC.values()):
                avisos.append('%s: a planilha está vazia e o registro tem dados — '
                              'nada apagado. Para remover um site, diga '
                              'explicitamente.' % nome)
            continue
        for rot, campo in CAMPO_DOC.items():
            v = novo[campo]
            if campo.startswith('site') and v and not URL_OK.match(v):
                avisos.append('%s: "%s" não parece um endereço completo '
                              '(falta http:// ou https://) — não gravado.' % (nome, v))
                novo[campo] = reg.get(campo, '') if reg else ''
        if reg is None:
            reg = {'nome': nome, 'fonte': 'COORDENACAO'}
            sites['docentes'].append(reg)
            mudancas.append('docente NOVO: %s' % nome)
        for campo, v in novo.items():
            if v and reg.get(campo, '') != v:
                mudancas.append('%s · %s: %r -> %r' % (nome, campo, reg.get(campo, ''), v))
                reg[campo] = v
    sites['docentes'].sort(key=lambda d: d['nome'])

    # ---------------------------------------------------------- disciplinas
    disc = json.load(open(DISC, encoding='utf-8'))
    por_id = {d['id']: d for d in disc['disciplinas']}
    for lin in linhas(wb['Disciplinas']):
        ident = txt(lin.get('Código'))
        reg = por_id.get(ident)
        if reg is None:
            avisos.append('disciplina %s não existe nos dados — linha nova na '
                          'planilha não cria disciplina, para não publicar '
                          'componente curricular por engano.' % ident)
            continue
        for rot in EDIT_DISC:
            campo = CAMPO_DISC[rot]
            v = lin.get(rot)
            if v is None or txt(v) == '':
                continue
            if campo in ('horas', 'creditos'):
                try:
                    v = int(float(v))
                except (TypeError, ValueError):
                    avisos.append('%s · %s: "%s" não é número — não gravado.'
                                  % (ident, campo, v))
                    continue
            elif campo == 'docentes':
                v = [x.strip() for x in str(v).split(';') if x.strip()]
            else:
                v = txt(v)
            if reg.get(campo) != v:
                antes = reg.get(campo)
                mudancas.append('%s · %s: %s -> %s' % (
                    ident, campo, str(antes)[:45], str(v)[:45]))
                reg[campo] = v
                reg['fonte'] = 'APCN 2026 + revisão da coordenação'

    disc['meta']['sem_docente'] = sum(1 for x in disc['disciplinas'] if not x['docentes'])

    print('alterações: %d' % len(mudancas))
    for m in mudancas:
        print('  ', m)
    if avisos:
        print('\navisos: %d' % len(avisos))
        for v in avisos:
            print('  !', v)
    if not a.aplicar:
        print('\n(simulação — rode com --aplicar para gravar)')
        return
    json.dump(sites, open(SITES, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(disc, open(DISC, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\ngravado em data/sites-docentes.json e data/disciplinas.json')


if __name__ == '__main__':
    main()
