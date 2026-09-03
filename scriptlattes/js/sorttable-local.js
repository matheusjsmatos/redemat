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
