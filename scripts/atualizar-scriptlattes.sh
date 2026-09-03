#!/usr/bin/env bash
# =============================================================================
# atualizar-scriptlattes.sh
# Sincroniza a saída do ScriptLattes para dentro do portal REDEMAT.
#
# USO
#   ./scripts/atualizar-scriptlattes.sh <pasta-de-saida-do-scriptlattes>
#
# EXEMPLOS
#   # local atual dos dados (Dropbox)
#   ./scripts/atualizar-scriptlattes.sh ~/Dropbox/claude/redemat/teste-01
#
#   # a partir da saída original no WSL
#   ./scripts/atualizar-scriptlattes.sh ~/Documentos/softwares/scriptLattes/redemat/teste-01
#
# O QUE FAZ
#   1. Valida que a pasta de origem tem cara de saída do ScriptLattes
#   2. Faz backup da versão anterior em scriptlattes.bak/
#   3. Copia o relatório para scriptlattes/, já sem o docente excluído
#   4. Ajusta a listagem de membros e o rótulo técnico "teste-01"
#   5. Substitui recursos externos que quebram o relatório (ver abaixo)
#   6. Injeta a folha de legibilidade e o link de volta ao portal
#   7. Escreve scriptlattes/SYNC.json com data e inventário da sincronização
#   8. Regenera assets/js/grafo-dados.js pelo scripts/gerar-grafo.py
#
# POR QUE A ETAPA 5 EXISTE
#   A saída do ScriptLattes carrega um <script> de sorttable.js hospedado em
#   http:// num servidor de terceiros. Servido por HTTPS, o navegador bloqueia
#   como conteúdo misto e a ordenação das tabelas morre em silêncio; e o
#   relatório passa a depender de um site que não é nosso. O script instala uma
#   cópia local equivalente. O grafo interativo do ScriptLattes é um applet
#   Java, que nenhum navegador atual executa: a página passa a apontar para o
#   grafo em SVG do portal.
#
# O QUE NÃO FAZ
#   Não roda o ScriptLattes nem baixa currículos. Rode o ScriptLattes antes,
#   confira a saída, e só então sincronize.
#   Não apaga arquivos da máquina do usuário: em vez de copiar-e-remover, exclui
#   na cópia. Isso mantém o script utilizável onde a remoção não é permitida.
# =============================================================================

set -euo pipefail

DEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$DEST_DIR/scriptlattes"
BAK="$DEST_DIR/scriptlattes.bak"

# Docente formalmente excluído do conjunto de 24 publicado no portal.
# O ScriptLattes preserva os 25 currículos da coleta original; aqui removemos
# apenas a página individual, mantendo o relatório íntegro no backup.
EXCLUIR_LATTES="8755682183778618"   # Guilherme Jorge Brigolini Silva

c_red()  { printf '\033[31m%s\033[0m\n' "$*"; }
c_grn()  { printf '\033[32m%s\033[0m\n' "$*"; }
c_yel()  { printf '\033[33m%s\033[0m\n' "$*"; }
c_bld()  { printf '\033[1m%s\033[0m\n'  "$*"; }

# ---------------------------------------------------------------- argumentos
if [[ $# -lt 1 ]]; then
  c_red "ERRO: informe a pasta de saída do ScriptLattes."
  echo
  echo "Uso: $0 <pasta-de-saida-do-scriptlattes>"
  echo
  echo "Exemplo:"
  echo "  $0 ~/Documentos/softwares/scriptLattes/redemat/teste-01"
  exit 1
fi

SRC="${1%/}"

if [[ ! -d "$SRC" ]]; then
  c_red "ERRO: pasta não encontrada: $SRC"
  exit 1
fi

# ------------------------------------------------------------------ validação
c_bld "1/8  Validando a origem"

faltando=()
for f in index.html membros.html; do
  [[ -f "$SRC/$f" ]] || faltando+=("$f")
done

n_membros=$(find "$SRC" -maxdepth 1 -name 'membro-*.html' | wc -l | tr -d ' ')

if [[ ${#faltando[@]} -gt 0 ]]; then
  c_red "ERRO: a pasta não parece ser uma saída do ScriptLattes."
  c_red "      Arquivos ausentes: ${faltando[*]}"
  exit 1
fi

if [[ "$n_membros" -lt 5 ]]; then
  c_red "ERRO: encontrei apenas $n_membros página(s) membro-*.html."
  c_red "      Esperado: uma por docente. A saída parece incompleta."
  exit 1
fi

echo "     origem: $SRC"
echo "     páginas de membro: $n_membros"

# --------------------------------------------------------------------- backup
c_bld "2/8  Backup da versão anterior"
if [[ -d "$DEST" ]]; then
  mkdir -p "$BAK"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a "$DEST"/ "$BAK"/
  else
    cp -R "$DEST"/. "$BAK"/
  fi
  echo "     versão anterior copiada para scriptlattes.bak/"
else
  echo "     nenhuma versão anterior (primeira sincronização)"
fi

# ----------------------------------------------------------------------- copia
c_bld "3/8  Copiando o relatório (já sem o docente excluído)"
mkdir -p "$DEST"
if command -v rsync >/dev/null 2>&1; then
  # A exclusão é feita AQUI, no filtro da cópia, e não com rm depois: o script
  # roda em ambientes onde remover arquivo não é permitido.
  rsync -a --exclude '.git' --exclude '*.pyc' \
        --exclude "membro-$EXCLUIR_LATTES.html" "$SRC"/ "$DEST"/
else
  # Sem rsync: copia tudo e a exclusão é tratada na etapa 4.
  c_yel "     rsync não encontrado — copiando com cp (sem filtro de exclusão)"
  cp -R "$SRC"/. "$DEST"/
fi
n_arq=$(find "$DEST" -type f | wc -l | tr -d ' ')
echo "     $n_arq arquivos copiados"

# --------------------------------------------------------- exclusão formal
c_bld "4/8  Conferindo a exclusão e o rótulo do grupo"
if [[ -f "$DEST/membro-$EXCLUIR_LATTES.html" ]]; then
  # Chegou até aqui porque a cópia foi feita sem rsync (sem filtro de exclusão)
  # ou sobrou de uma sincronização anterior. Tenta remover; onde a remoção não
  # é permitida, vira página de aviso — nos dois casos o currículo fora do
  # conjunto de 24 deixa de ser publicado.
  rm -f "$DEST/membro-$EXCLUIR_LATTES.html" 2>/dev/null || true
fi
if [[ ! -f "$DEST/membro-$EXCLUIR_LATTES.html" ]]; then
  echo "     página do docente excluído fora da cópia publicada"
else
  cat > "$DEST/membro-$EXCLUIR_LATTES.html" <<'STUB'
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Página não publicada — REDEMAT</title>
<link rel="stylesheet" href="portal-redemat.css"></head><body>
<div id="portal-back"><a href="../pages/producao-lattes.html">&#8592; Voltar ao portal REDEMAT</a>
<span>Relatório ScriptLattes</span></div>
<p style="padding:2rem 1.2rem;max-width:52ch">Esta página individual não integra o
conjunto de 24 docentes publicado no portal. O relatório completo, com todos os
currículos da coleta original, fica preservado em <code>scriptlattes.bak/</code>.</p>
</body></html>
STUB
  c_yel "     página do docente excluído substituída por aviso (remoção não permitida aqui)"
fi

if true; then
  # remove o link da listagem de membros, se presente
  if [[ -f "$DEST/membros.html" ]]; then
    python3 - "$DEST/membros.html" "$EXCLUIR_LATTES" <<'PY'
import io, re, sys
p, lid = sys.argv[1], sys.argv[2]
s = io.open(p, encoding='utf-8', errors='replace').read()
# remove a linha/bloco da tabela que referencia o membro excluído
s = re.sub(r'<tr[^>]*>(?:(?!</tr>).)*membro-' + re.escape(lid) + r'\.html(?:(?!</tr>).)*</tr>', '', s, flags=re.S | re.I)
io.open(p, 'w', encoding='utf-8').write(s)
PY
    echo "     referência conferida em membros.html"
  fi
fi

# ------------------------------------- currículos fora do conjunto publicado
# A coleta do ScriptLattes preserva mais currículos do que o conjunto de 24
# docentes que o portal publica: a pasta traz páginas individuais de pessoas
# que não constam em membros.html. Publicá-las expõe currículo de quem não
# está no conjunto declarado, sem ninguém ter decidido isso — e sem link no
# índice, ficam acessíveis apenas por URL direta, o que é pior.
# Aqui elas saem do conjunto publicado. O relatório íntegro fica no backup.
c_bld "4b/8 Retirando currículos fora do conjunto publicado"
python3 - "$DEST" <<'PYEOF'
import glob, io, os, re, sys
dest = sys.argv[1]
idx = os.path.join(dest, 'membros.html')
if not os.path.exists(idx):
    print('     membros.html ausente — nada a conferir')
    raise SystemExit(0)
html = io.open(idx, encoding='utf-8', errors='replace').read()
indexados = set(re.findall(r'membro-(\d+)\.html', html))
STUB = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">\n'
        '<title>Pagina nao publicada - REDEMAT</title>\n'
        '<link rel="stylesheet" href="portal-redemat.css"></head><body>\n'
        '<div id="portal-back"><a href="../pages/producao-lattes.html">&#8592; Voltar ao portal REDEMAT</a>'
        '<span>Relatorio ScriptLattes</span></div>\n'
        '<p style="padding:2rem 1.2rem;max-width:52ch">Este curriculo nao integra o conjunto '
        'de docentes publicado no portal e por isso sua pagina individual nao e '
        'divulgada aqui. O relatorio completo da coleta fica preservado em '
        '<code>scriptlattes.bak/</code>.</p>\n</body></html>\n')
fora = []
for caminho in sorted(glob.glob(os.path.join(dest, 'membro-*.html'))):
    lid = os.path.basename(caminho).replace('membro-', '').replace('.html', '')
    if lid in indexados:
        continue
    nome = ''
    try:
        t = io.open(caminho, encoding='utf-8', errors='replace').read()
        if 'nao integra o conjunto' in t or 'não integra o conjunto' in t:
            continue                      # já tratada numa sincronização anterior
        m = re.search(r'<h3>([^<]{4,70})', t)
        nome = (m.group(1).strip() if m else '')
    except OSError:
        pass
    fora.append((lid, nome))
    try:
        os.remove(caminho)
    except OSError:
        io.open(caminho, 'w', encoding='utf-8').write(STUB)
if not fora:
    print('     todos os curriculos da pasta constam no indice')
else:
    print('     %d curriculo(s) fora do conjunto publicado, retirado(s):' % len(fora))
    for lid, nome in fora:
        print('       %s  %s' % (lid, nome or '(nome nao identificado)'))
    io.open(os.path.join(dest, 'FORA-DO-CONJUNTO.txt'), 'w', encoding='utf-8').write(
        'Curriculos presentes na coleta e fora do conjunto publicado no portal.\n'
        'Nao constam em membros.html; a pagina individual nao e divulgada.\n'
        'O relatorio integro da coleta fica em scriptlattes.bak/.\n\n'
        + '\n'.join('%s  %s' % (l, n) for l, n in fora) + '\n')
PYEOF

# ------------------------------------------------------------------- rótulos
c_bld "5a/8 Trocando o rótulo técnico por REDEMAT"
alterados=0
while IFS= read -r -d '' f; do
  if grep -q 'teste-01' "$f" 2>/dev/null; then
    python3 - "$f" <<'PY'
import io, sys
p = sys.argv[1]
s = io.open(p, encoding='utf-8', errors='replace').read()
# só nos textos visíveis; nomes de arquivo de exportação são preservados
s = s.replace('>teste-01<', '>REDEMAT<')
s = s.replace('teste-01</title>', 'REDEMAT</title>')
s = s.replace('<title>teste-01', '<title>REDEMAT')
s = s.replace('Grupo teste-01', 'REDEMAT')
io.open(p, 'w', encoding='utf-8').write(s)
PY
    alterados=$((alterados + 1))
  fi
done < <(find "$DEST" -name '*.html' -print0)
echo "     $alterados arquivo(s) ajustado(s)"

# --------------------------------------------- recursos externos quebrados
c_bld "5b/8 Substituindo recursos externos que quebram o relatorio"

# Copia local do sorttable: mesma interface (clique no <th> ordena a coluna),
# sem depender de um servidor de terceiros por http://.
cat > "$DEST/js/sorttable-local.js" <<'JSEOF'
/* sorttable-local.js — ordenacao de tabelas <table class="sortable">.
   Instalado por scripts/atualizar-scriptlattes.sh em substituicao ao
   sorttable.js externo servido por http://, que o navegador bloqueia como
   conteudo misto quando a pagina e servida por HTTPS. */
(function () {
  'use strict';
  function valor(td) {
    var t = (td.textContent || '').trim();
    var n = t.replace(/\./g, '').replace(',', '.');
    return (n !== '' && !isNaN(n)) ? parseFloat(n) : t.toLocaleLowerCase('pt-BR');
  }
  function ordenar(tab, col, asc) {
    var tb = tab.tBodies[0]; if (!tb) return;
    var lin = Array.prototype.slice.call(tb.rows);
    lin.sort(function (a, b) {
      var x = valor(a.cells[col]), y = valor(b.cells[col]);
      if (x === y) return 0;
      if (typeof x === 'number' && typeof y === 'number') return asc ? x - y : y - x;
      return asc ? String(x).localeCompare(String(y), 'pt-BR')
                 : String(y).localeCompare(String(x), 'pt-BR');
    });
    lin.forEach(function (r) { tb.appendChild(r); });
  }
  function ligar(tab) {
    var cab = tab.tHead && tab.tHead.rows[0];
    if (!cab) { cab = tab.rows[0]; }
    if (!cab) return;
    Array.prototype.forEach.call(cab.cells, function (th, i) {
      th.style.cursor = 'pointer';
      th.setAttribute('title', 'Clique para ordenar por esta coluna');
      th.setAttribute('tabindex', '0');
      th.setAttribute('aria-sort', 'none');
      function faz() {
        var asc = th.getAttribute('aria-sort') !== 'ascending';
        Array.prototype.forEach.call(cab.cells, function (o) { o.setAttribute('aria-sort', 'none'); });
        th.setAttribute('aria-sort', asc ? 'ascending' : 'descending');
        ordenar(tab, i, asc);
      }
      th.addEventListener('click', faz);
      th.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); faz(); }
      });
    });
  }
  document.addEventListener('DOMContentLoaded', function () {
    Array.prototype.forEach.call(document.querySelectorAll('table.sortable'), ligar);
  });
}());
JSEOF

python3 - "$DEST" <<'PYEOF'
import io, os, re, sys
dest = sys.argv[1]
n_sort = n_http = n_applet = 0
AVISO = ('<p style="padding:2rem 1.2rem;max-width:60ch">O ScriptLattes gera esta versao '
         'interativa do grafo como <em>applet</em> Java, tecnologia que nenhum navegador '
         'atual executa. O portal REDEMAT redesenha o mesmo grafo em SVG, com selecao por '
         'docente e navegacao por teclado: '
         '<a href="../pages/producao-lattes.html#colaboracao">abrir o grafo de colaboracoes '
         'no portal</a>. A versao estatica, em imagem, continua em '
         '<a href="grafoDeColaboracoes.html">grafoDeColaboracoes.html</a>.</p>')
for name in sorted(os.listdir(dest)):
    if not name.endswith('.html'):
        continue
    p = os.path.join(dest, name)
    s = io.open(p, encoding='utf-8', errors='replace').read()
    o = s
    s2 = re.sub(r'<script[^>]*src="https?://professor\.ufabc\.edu\.br/[^"]*sorttable\.js"[^>]*>\s*</script>',
                '<script type="text/javascript" charset="utf8" src="js/sorttable-local.js"></script>', s)
    if s2 != s:
        n_sort += 1
    s = s2
    s2 = s.replace('href="http://lattes.cnpq.br/', 'href="https://lattes.cnpq.br/')
    s2 = s2.replace('href="http://scriptlattes.sourceforge.net/', 'href="https://scriptlattes.sourceforge.net/')
    if s2 != s:
        n_http += 1
    s = s2
    if '<applet' in s.lower():
        s = re.sub(r'<applet.*?</applet>', AVISO, s, flags=re.S | re.I)
        n_applet += 1
    if s != o:
        io.open(p, 'w', encoding='utf-8').write(s)
print("     sorttable local em %d pagina(s); %d pagina(s) com links https; %d applet(s) substituido(s)"
      % (n_sort, n_http, n_applet))
PYEOF

# ------------------------------------------------- legibilidade + volta ao portal
c_bld "6/8  Injetando folha de legibilidade e link de retorno"

cat > "$DEST/portal-redemat.css" <<'CSS'
/* Ajustes de legibilidade aplicados pelo portal REDEMAT.
   Gerado por scripts/atualizar-scriptlattes.sh — não editar à mão. */
body { font-family: 'Inter', -apple-system, 'Segoe UI', system-ui, sans-serif; color: #16202E; }
table { border-collapse: collapse; }
th { background: #0B1F3A !important; color: #fff !important; font-weight: 700;
     text-transform: uppercase; font-size: .72rem; letter-spacing: .05em; padding: .6rem .8rem !important; }
td { padding: .55rem .8rem !important; border-bottom: 1px solid #E3E8EF; vertical-align: top; }
tr:nth-child(even) td { background: #FBFCFD; }
.tabulator-cell, .tabulator-col-title { white-space: normal !important; }
.tabulator-col { min-width: 110px; }
.tabulator-row { min-height: 34px; }
.tabulator { overflow-x: auto; }
#portal-back {
  position: sticky; top: 0; z-index: 9999;
  display: flex; align-items: center; gap: .6rem;
  background: #0B1F3A; border-bottom: 3px solid #B8860B;
  padding: .6rem 1.1rem; font-size: .84rem;
}
#portal-back a { color: #D9A521; font-weight: 700; text-decoration: none; }
#portal-back a:hover { text-decoration: underline; }
#portal-back span { color: rgba(255,255,255,.6); }
CSS

python3 - "$DEST" <<'PY'
import io, os, re, sys
dest = sys.argv[1]
BACK = ('<div id="portal-back"><a href="../pages/producao-lattes.html">&#8592; Voltar ao portal REDEMAT</a>'
        '<span>Relatório ScriptLattes — dados brutos dos currículos Lattes</span></div>')
LINK = '<link rel="stylesheet" href="portal-redemat.css">'
n = 0
for name in sorted(os.listdir(dest)):
    if not name.endswith('.html'):
        continue
    p = os.path.join(dest, name)
    s = io.open(p, encoding='utf-8', errors='replace').read()
    if 'portal-redemat.css' in s:
        continue
    if re.search(r'</head>', s, re.I):
        s = re.sub(r'</head>', LINK + '\n</head>', s, count=1, flags=re.I)
    else:
        s = LINK + s
    if re.search(r'<body[^>]*>', s, re.I):
        s = re.sub(r'(<body[^>]*>)', r'\1\n' + BACK, s, count=1, flags=re.I)
    io.open(p, 'w', encoding='utf-8').write(s)
    n += 1
print(f"     {n} página(s) com folha e link de retorno")
PY

# ---------------------------------------------------------------- inventário
c_bld "7/8  Registrando a sincronização"
python3 - "$DEST" "$SRC" <<'PY'
import io, json, os, sys, datetime, glob
dest, src = sys.argv[1], sys.argv[2]
arquivos = sorted(glob.glob(os.path.join(dest, 'membro-*.html')))
# Onde a remocao nao e permitida, a pagina fora do conjunto vira aviso em vez
# de desaparecer. Contar arquivos daria um numero de docentes que nao existe;
# o que vale e quantas paginas de curriculo estao de fato publicadas.
def publicada(caminho):
    try:
        t = io.open(caminho, encoding='utf-8', errors='replace').read(1200)
    except OSError:
        return False
    return 'nao integra o conjunto' not in t and 'nao e divulgada' not in t
publicadas = [c for c in arquivos if publicada(c)]
substituidas = [c for c in arquivos if c not in publicadas]
membros = [os.path.basename(c) for c in publicadas]
info = {
    "sincronizado_em": datetime.datetime.now().isoformat(timespec='seconds'),
    "origem": src,
    "paginas_membro_publicadas": len(membros),
    "paginas_substituidas_por_aviso": len(substituidas),
    "lattes_ids": [m.replace('membro-', '').replace('.html', '') for m in membros],
    "arquivos_html": len(glob.glob(os.path.join(dest, '*.html'))),
    "fora_do_conjunto": (io.open(os.path.join(dest, 'FORA-DO-CONJUNTO.txt'),
                                 encoding='utf-8').read().count('\n') - 5
                         if os.path.exists(os.path.join(dest, 'FORA-DO-CONJUNTO.txt')) else 0),
    "tem_metricas": os.path.exists(os.path.join(dest, 'metricas.html')),
    "tem_grafo": os.path.exists(os.path.join(dest, 'grafoDeColaboracoes.html')),
    "nota": ("Saída do ScriptLattes sincronizada pelo portal. Currículos fora do conjunto "
             "publicado — o docente formalmente excluído e os que não constam em membros.html — "
             "têm a página individual retirada; onde a remoção não é permitida, a página passa a "
             "exibir aviso. O relatório íntegro da coleta fica em scriptlattes.bak/. "
             "Os nomes retirados ficam em FORA-DO-CONJUNTO.txt.")
}
with open(os.path.join(dest, 'SYNC.json'), 'w', encoding='utf-8') as f:
    json.dump(info, f, ensure_ascii=False, indent=2)
# Mesmo conteudo como <script>, para a pagina saber que o relatorio existe sem
# depender de fetch (que o navegador bloqueia quando o site abre por file://).
with io.open(os.path.join(dest, 'sync-info.js'), 'w', encoding='utf-8') as f:
    f.write('/* Gerado por scripts/atualizar-scriptlattes.sh — nao editar. */\n'
            'window.SL_SYNC = ' + json.dumps(info, ensure_ascii=False) + ';\n')
print("     scriptlattes/SYNC.json — %d curriculo(s) publicado(s), %d substituido(s) por aviso, %d paginas HTML"
      % (info['paginas_membro_publicadas'], info['paginas_substituidas_por_aviso'], info['arquivos_html']))
PY

# ---------------------------------------------------------------- grafo SVG
c_bld "8/8  Regenerando o grafo de colaboracoes do portal"
if [[ -f "$DEST_DIR/scripts/gerar-grafo.py" ]]; then
  if python3 "$DEST_DIR/scripts/gerar-grafo.py" "$SRC"; then
    :
  else
    c_yel "     gerar-grafo.py falhou — o portal segue com o grafo anterior"
  fi
else
  c_yel "     scripts/gerar-grafo.py nao encontrado (nada a fazer)"
fi

echo
c_grn "Sincronizacao concluida."
echo
c_bld "Próximos passos"
cat <<'NEXT'
  1. Sirva o portal por HTTP para o mapa e o relatório funcionarem:
       python3 -m http.server 8080
     e abra  http://localhost:8080/

  2. Confira em http://localhost:8080/pages/producao-lattes.html#scriptlattes
     se todos os blocos abrem.

  3. Confira o grafo em http://localhost:8080/pages/producao-lattes.html#colaboracao
     A etapa 8 já regenerou assets/js/grafo-dados.js a partir do .dot desta
     coleta. Se o número de nós ou arestas mudou, o gerador avisa no terminal.

  4. Se os NÚMEROS mudaram (nova coleta de currículos), atualize também
     assets/js/site-data.js — o portal não lê os agregados do ScriptLattes
     automaticamente, por decisão de governança: todo número publicado passa
     por conferência antes de entrar. Rode scripts/extrair-dados.py para
     recalcular os agregados a partir dos JSON dos currículos.
NEXT
