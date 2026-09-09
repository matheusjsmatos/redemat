# -*- coding: utf-8 -*-
"""gerar-historico.py — gera assets/js/historico-dados.js

USO
    python3 scripts/gerar-historico.py [pasta dos relatórios]
    (padrão: ~/Dropbox/claude/redemat/relatorios)

Gera assets/js/historico-dados.js — o painel histórico do corpo docente.

FONTE: as 13 coletas CAPES da REDEMAT (2013-2025), em
       Dropbox/claude/redemat/relatorios/relatorio_dados_enviados_coleta_*.xlsx

DUAS JANELAS DIFERENTES, E ISSO IMPORTA:

  Período no Programa  — COMPLETO. A coluna "Início da Carga Horária" das
                         coletas guarda a data real de entrada, e a mais antiga
                         é 06/09/1996, a fundação. Então o período é verdadeiro
                         mesmo para quem entrou 17 anos antes da primeira
                         coleta deste conjunto.

  Contribuições        — RECORTADAS em 2013-2025. Orientação, produção e
                         projeto só existem nas coletas a partir de 2013. Para
                         quem está no Programa desde 1996, o número publicado
                         é MENOR que a obra da pessoa. A página diz isso; sem
                         esse aviso, a homenagem viraria subnotificação.

ORDEM: cronológica por entrada no Programa, NUNCA por volume de produção. O
portal proíbe ranking público de docentes, e um painel de homenagem ordenado
por contagem seria exatamente isso.
"""
import csv, glob, io, json, os, re, sys, unicodedata, warnings
import pandas as pd
warnings.filterwarnings('ignore')

# Exclusão formal do conjunto publicado do portal, decidida pela coordenação.
# Não é nomeada nas páginas: nomear alguém como excluído é afirmação pública
# sobre a pessoa (ver CHANGELOG v4.7).
EXCLUIR = {'GUILHERME JORGE BRIGOLINI SILVA'}

# ── grafia publicada dos nomes. Os relatórios CAPES guardam nome em CAIXA
#    ALTA E SEM ACENTO; numa homenagem, errar o acento é errar o nome da
#    pessoa. A grafia vem de data/nomes-docentes.csv, cujo campo
#    `fonte_grafia` diz de onde: SITE_DATA (quadro atual), LATTES (ID de 16
#    dígitos) ou CONFERIR — este último publicado como vem da CAPES, com o
#    cartão marcado, porque acento de nome de pessoa não se adivinha.
# ── resumo do Lattes. Extraído do cache do ScriptLattes por
#    scripts/extrair-resumos-lattes.py e casado pelo ID de 16 dígitos que
#    data/nomes-docentes.csv já guarda. Quem não tem currículo em cache fica
#    sem resumo, e o cartão simplesmente não mostra a seção.
# ── saídas declaradas pela coordenação. A coleta CAPES é a fonte de tudo
#    menos de uma coisa: se a pessoa AINDA está no quadro hoje. A coleta é
#    anual e retrospectiva, então quem saiu depois do último envio continua
#    listado nela — foi o que aconteceu com sete docentes, marcados como "no
#    quadro" quando já haviam saído. Só a coordenação sabe isso, e é o que
#    data/saidas-docentes.csv registra.
def resumir(t, limite=230):
    """Primeiro trecho do resumo, cortado em fim de frase quando dá.

    O resumo do Lattes vai de 375 a 4000 caracteres — cabe no cartão só um
    começo. Corta na última frase inteira antes do limite; se não houver
    ponto, corta na última palavra. Nunca no meio de uma palavra."""
    if len(t) <= limite:
        return t, ''
    corte = t.rfind('. ', 0, limite)
    if corte < limite * 0.55:
        corte = t.rfind(' ', 0, limite)
    return t[:corte + 1].strip(), t

PASTA = (sys.argv[1] if len(sys.argv) > 1
         else os.path.expanduser('~/Dropbox/claude/redemat/relatorios'))
ARQS = sorted(glob.glob(os.path.join(PASTA, 'relatorio_dados_enviados_coleta_*.xlsx')))
if not ARQS:
    sys.exit('Nenhum relatorio_dados_enviados_coleta_*.xlsx em ' + PASTA + '\n'
             'Uso: python3 scripts/gerar-historico.py [pasta dos relatórios]')


def _coleta(f):
    return int(re.search(r'(\d{4})\.xlsx$', f).group(1))


def _junta(aba):
    """Concatena a mesma aba das 13 coletas, marcando de qual veio."""
    partes = []
    for f in ARQS:
        try:
            d = pd.read_excel(f, sheet_name=aba)
        except Exception:
            continue
        if not len(d):
            continue
        d['coleta'] = _coleta(f)
        partes.append(d)
    if not partes:
        sys.exit('Aba "%s" não encontrada em nenhum relatório.' % aba)
    return pd.concat(partes, ignore_index=True)


print('lendo %d coletas de %s' % (len(ARQS), PASTA))
D = _junta('Docentes')
T = _junta('Trabalhos de Conclusão')
P = _junta('Produção Intelectual')
J = _junta('Projetos de Pesquisa')


def norm(s):
    if not isinstance(s, str):
        return ''
    t = unicodedata.normalize('NFD', s)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', t).strip().upper()


SAIDAS = {}
RESUMOS = {}
LATTES_DE = {}
GRAFIA = {}
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_NOMES = os.path.join(RAIZ, 'data', 'nomes-docentes.csv')
if os.path.exists(CSV_NOMES):
    for r in csv.DictReader(io.open(CSV_NOMES, encoding='utf-8')):
        GRAFIA[r['chave_capes']] = (r['nome_publicado'], r['fonte_grafia'])
        if r.get('lattes'):
            LATTES_DE[r['chave_capes']] = r['lattes']

CSV_SAIDAS = os.path.join(RAIZ, 'data', 'saidas-docentes.csv')
if os.path.exists(CSV_SAIDAS):
    for r in csv.DictReader(io.open(CSV_SAIDAS, encoding='utf-8')):
        SAIDAS[norm(r['nome'])] = r['saida_declarada']

CSV_RESUMOS = os.path.join(RAIZ, 'data', 'lattes-resumos.csv')
if os.path.exists(CSV_RESUMOS):
    for r in csv.DictReader(io.open(CSV_RESUMOS, encoding='utf-8')):
        if r.get('resumo'):
            RESUMOS[r['lattes']] = r['resumo'].strip()



def slug(nome):
    s = unicodedata.normalize('NFD', nome)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


# Erros de digitação na própria coleta CAPES. Corrigidos por tabela explícita,
# não por heurística: cada entrada é uma decisão conferível.
CORRECOES = {
    'Caracterização Física, Quimica e Microestrutural':
        'Caracterização Física, Química e Microestrutural',
    'Tecnologias Integradas para o Aproveitamento de de Rejeito da Mineração de Ferro':
        'Tecnologias Integradas para o Aproveitamento de Rejeito da Mineração de Ferro',
}


def titulo_cap(s):
    """MAIÚSCULAS DE FORMULÁRIO -> Capitalização legível, preservando siglas."""
    if not isinstance(s, str):
        return ''
    s = re.sub(r'\s+', ' ', s).strip()
    if not s:
        return ''
    MIN = {'de','da','do','das','dos','e','em','a','o','as','os','para','com',
           'no','na','nos','nas','por','ao','aos','à','às','the','of','and',
           'in','for','on','to','a','an'}
    SIG = {'DRX','MEV','AFM','UFOP','UEMG','CAPES','CNPQ','FAPEMIG','PVC','PET',
           'ABS','LED','UV','PH','CO2','SO2','NOX','TIO2','ZNO','AL2O3','SIO2',
           'FE','MG','II','III','IV','V','VI','3D','2D','1D','EUA','BR','USP'}
    out = []
    for i, w in enumerate(s.split(' ')):
        nu = re.sub(r'[^A-Z0-9]', '', w.upper())
        if nu in SIG:
            out.append(w.upper())
        elif i > 0 and w.lower() in MIN:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:].lower())
    t = ' '.join(out)
    t = t[:1].upper() + t[1:]
    return CORRECOES.get(t, t)


def nome_proprio(nome):
    """Nome de pessoa em caixa mista, com as partículas em minúscula."""
    MIN = {'de','da','do','das','dos','e'}
    return ' '.join(w.lower() if w.lower() in MIN else w.capitalize()
                    for w in re.sub(r'\s+', ' ', nome.strip()).split(' '))


# ─────────────────────────────────────────────── período e categorias
D['ini'] = pd.to_datetime(D['Início da Carga Horária'], dayfirst=True, errors='coerce')
D['fim'] = pd.to_datetime(D['Fim da Carga Horária'], dayfirst=True, errors='coerce')
D['chave'] = D['Nome Docente'].map(norm)

ULTIMA_COLETA = int(D.coleta.max())

pessoas = {}
for ch, g in D.groupby('chave'):
    if ch in EXCLUIR:
        continue
    g = g.sort_values('coleta')
    cats = g.groupby('coleta')['Categoria'].first().to_dict()
    ult = int(max(cats))
    ini = g['ini'].min()
    fim = g['fim'].max()
    # No quadro: aparece na coleta mais recente do conjunto — a não ser que a
    # coordenação já tenha declarado a saída, que é informação mais nova que a
    # coleta e por isso tem precedência.
    saida_declarada = SAIDAS.get(ch)
    no_quadro = (ult >= ULTIMA_COLETA - 1) and not saida_declarada
    tit = pd.to_numeric(g['Ano Titulação'], errors='coerce').dropna()
    bruto = g['Nome Docente'].value_counts().idxmax()
    graf = GRAFIA.get(norm(bruto))
    nome = graf[0] if graf else nome_proprio(bruto)
    grafia_conferir = (graf[1] == 'CONFERIR') if graf else True
    pessoas[ch] = {
        'nome': nome,
        'grafia_conferir': bool(grafia_conferir),
        'lattes': LATTES_DE.get(norm(bruto), ''),
        'foto': slug(nome),
        'ies': sorted(set(g['IES Sigla'].dropna())),
        'titulacao': int(tit.iloc[0]) if len(tit) else None,
        'entrada': ini.strftime('%Y-%m-%d') if pd.notna(ini) else None,
        'entrada_ano': int(ini.year) if pd.notna(ini) else None,
        'saida': (saida_declarada or (fim.strftime('%Y-%m-%d')
                  if (pd.notna(fim) and not no_quadro) else None)),
        'saida_fonte': ('COORDENACAO' if saida_declarada else
                        ('COLETA' if (pd.notna(fim) and not no_quadro) else '')),
        'no_quadro': bool(no_quadro),
        'primeira_coleta': int(min(cats)),
        'ultima_coleta': ult,
        'categoria': cats[ult].capitalize(),
        'categorias_distintas': sorted({v.capitalize() for v in cats.values()}),
        'coletas': len(cats),
    }

# ─────────────────────────────────────────────── orientações concluídas
def tk(s):
    return re.sub(r'[^A-Z0-9 ]', '', norm(s))[:120]

Tp = T[T['Principal?'].astype(str).str.strip().str.lower() == 'sim'].copy()
Tp['obj'] = (Tp['Nome Trabalho de Conclusão'].map(tk) + '|' +
             Tp['Nome Autor'].map(norm) + '|' + Tp['Data da Defesa'].astype(str))
Tp['chave'] = Tp['Nome Orientador'].map(norm)
Tu = Tp.drop_duplicates(subset=['obj', 'chave'])
Tu = Tu.assign(ano=pd.to_datetime(Tu['Data da Defesa'], dayfirst=True,
                                  errors='coerce').dt.year)

for ch, g in Tu.groupby('chave'):
    if ch not in pessoas:
        continue
    t = g['Tipo do Trabalho de Conclusão'].value_counts()
    anos = g['ano'].dropna()
    pessoas[ch].update({
        'teses': int(t.get('TESE', 0)),
        'dissertacoes': int(t.get('DISSERTAÇÃO', 0)),
        'defesas_periodo': ([int(anos.min()), int(anos.max())] if len(anos) else None),
    })

# ─────────────────────────────────────────────── produção
P2 = P[P['Produção Glosada?'].astype(str).str.strip().str.lower() != 'sim'].copy()
P2['obj'] = (P2['Título da Produção'].map(tk) + '|' +
             P2['Ano da Produção'].astype(str) + '|' +
             P2['Subtipo da Produção'].astype(str))
P2['chave'] = P2['Nome do Autor'].map(norm)
Pu = P2.drop_duplicates(subset=['obj', 'chave'])

SUB = {'ARTIGO EM PERIÓDICO': 'artigos', 'LIVRO': 'livros',
       'PATENTE': 'patentes', 'TRABALHO EM ANAIS': 'anais'}

for ch, g in Pu.groupby('chave'):
    if ch not in pessoas:
        continue
    sub = g['Subtipo da Produção'].value_counts()
    pessoas[ch].update({v: int(sub.get(k, 0)) for k, v in SUB.items()})
    # destaques nomeados: livros e patentes, que é o que se lê numa homenagem
    for k, campo in (('LIVRO', 'livros_titulos'), ('PATENTE', 'patentes_titulos')):
        tt = (g[g['Subtipo da Produção'] == k]['Título da Produção']
              .dropna().map(titulo_cap).drop_duplicates().tolist())
        if tt:
            pessoas[ch][campo] = tt[:12]
    # linhas de pesquisa em que a pessoa produziu
    ln = g['Linha de Pesquisa'].dropna().map(titulo_cap).value_counts()
    if len(ln):
        pessoas[ch]['linhas'] = list(ln.head(3).index)

# ─────────────────────────────────────────────── projetos
J['chave'] = J['Nome Membro do Projeto'].map(norm)
Ju = J.drop_duplicates(subset=['Nome do Projeto de Pesquisa', 'chave'])
resp = (J[J['Membro Responsável'].astype(str).str.strip().str.lower() == 'sim']
        .drop_duplicates(subset=['Nome do Projeto de Pesquisa', 'chave']))
for ch, g in Ju.groupby('chave'):
    if ch in pessoas:
        pessoas[ch]['projetos'] = int(len(g))
for ch, g in resp.groupby('chave'):
    if ch in pessoas:
        pessoas[ch]['projetos_coordenados'] = int(len(g))

# ─────────────────────────────────────────────── resumo do Lattes
_com = 0
for p in pessoas.values():
    t = RESUMOS.get(p.get('lattes') or '')
    if t:
        curto, cheio = resumir(t)
        p['resumo'] = curto
        if cheio:
            p['resumo_completo'] = cheio
        _com += 1

# ─────────────────────────────────────────────── agrupamento cronológico
def fase(ano):
    if ano <= 1996: return 'fundacao'
    if ano <= 1999: return 'p1997'
    if ano <= 2009: return 'p2000'
    if ano <= 2019: return 'p2010'
    return 'p2020'

for p in pessoas.values():
    p['fase'] = fase(p['entrada_ano'] or 9999)

lista = sorted(pessoas.values(),
               key=lambda p: (p['entrada'] or '9999', p['nome']))

FASES = [
    {'id': 'fundacao', 'titulo': 'Fundação — setembro de 1996',
     'texto': 'Os docentes que assinaram o início da rede. A REDEMAT nasceu como '
              'programa em associação entre UFOP e UEMG, e estes são os nomes '
              'registrados no primeiro quadro.'},
    {'id': 'p1997', 'titulo': '1997 a 1999',
     'texto': 'A primeira expansão, ainda na década de fundação.'},
    {'id': 'p2000', 'titulo': 'Anos 2000',
     'texto': 'A década em que o Programa consolidou o Doutorado e ampliou as '
              'linhas de pesquisa.'},
    {'id': 'p2010', 'titulo': 'Anos 2010',
     'texto': 'A geração que sucedeu a fundadora e assumiu a orientação da '
              'maior parte das defesas do período coberto pelas coletas.'},
    {'id': 'p2020', 'titulo': 'Anos 2020',
     'texto': 'As entradas mais recentes no quadro docente.'},
]

totais = {
    'docentes': len(lista),
    'no_quadro': sum(1 for p in lista if p['no_quadro']),
    'passaram': sum(1 for p in lista if not p['no_quadro']),
    'fundadores': sum(1 for p in lista if p['fase'] == 'fundacao'),
    'fundadores_no_quadro': sum(1 for p in lista
                                if p['fase'] == 'fundacao' and p['no_quadro']),
    'ies': sorted({i for p in lista for i in p['ies']}),
    'entrada_mais_antiga': min(p['entrada'] for p in lista if p['entrada']),
    'coletas': [int(c) for c in sorted(D.coleta.unique())],
    'teses': sum(p.get('teses', 0) for p in lista),
    'dissertacoes': sum(p.get('dissertacoes', 0) for p in lista),
    'orientacoes_unicas': int(Tu['obj'].nunique()),
    'producao_unica': int(Pu['obj'].nunique()),
    'artigos_unicos': int(Pu[Pu['Subtipo da Produção'] == 'ARTIGO EM PERIÓDICO']['obj'].nunique()),
    'livros_unicos': int(Pu[Pu['Subtipo da Produção'] == 'LIVRO']['obj'].nunique()),
    'patentes_unicas': int(Pu[Pu['Subtipo da Produção'] == 'PATENTE']['obj'].nunique()),
    'projetos': int(J['Nome do Projeto de Pesquisa'].nunique()),
    'com_foto': 0,
    'grafia_conferir': sum(1 for p in lista if p.get('grafia_conferir')),
    'com_resumo': sum(1 for p in lista if p.get('resumo')),
    'com_lattes': sum(1 for p in lista if p.get('lattes')),
    'saidas_declaradas': sum(1 for p in lista if p.get('saida_fonte') == 'COORDENACAO'),
}

saida = {'meta': {
    'fonte': 'CAPES_COLETA',
    'ref': 'redemat/relatorios/relatorio_dados_enviados_coleta_2013..2025.xlsx',
    'coleta': '2026-09-08',
    'status': 'VALIDADO',
    'janela_contribuicoes': [2013, 2025],
    'ultima_coleta': ULTIMA_COLETA,
}, 'totais': totais, 'fases': FASES, 'docentes': lista}

DEST = os.path.join(RAIZ, 'assets', 'js', 'historico-dados.js')
with open(DEST, 'w', encoding='utf-8') as f:
    f.write('/* historico-dados.js — painel histórico do corpo docente da REDEMAT.\n'
            '   GERADO por scripts/gerar-historico.py a partir das 13 coletas CAPES\n'
            '   (2013-2025). NÃO EDITAR À MÃO.\n\n'
            '   Período no Programa: completo, a partir de 06/09/1996 (coluna\n'
            '   "Início da Carga Horária" das coletas).\n'
            '   Contribuições: recortadas em 2013-2025, que é o alcance destas\n'
            '   coletas — para quem entrou em 1996, o número é MENOR que a obra. */\n'
            'window.HISTORICO = ' +
            json.dumps(saida, ensure_ascii=False, indent=1) + ';\n')

print('=== PAINEL HISTÓRICO')
for k, v in totais.items():
    print('   %-24s %s' % (k, v))
print()
print('por fase:')
for f_ in FASES:
    n = [p for p in lista if p['fase'] == f_['id']]
    print('   %-28s %2d docentes (%d no quadro)'
          % (f_['titulo'][:28], len(n), sum(1 for p in n if p['no_quadro'])))
print()
print('gravado:', DEST, '(%d KB)' % (os.path.getsize(DEST) // 1024))
