/* ==========================================================================
   REDEMAT — Componentes compartilhados
   Header, footer, navegação móvel, selos de proveniência e utilitários.
   ========================================================================== */

(function () {
  'use strict';

  /* ------------------------------------------------------- prévia no GitHub
     Enquanto o portal estiver servido pelo GitHub Pages, ele é uma PRÉVIA: o
     site oficial do Programa continua em redemat.ufop.br. Duas cópias do mesmo
     conteúdo indexadas confundem quem procura o Programa no Google — e a que
     não deveria aparecer é a prévia.

     Por isso, e só no domínio github.io, a página declara `noindex`. Não é
     controle de acesso: quem tem o link abre normalmente. É para o buscador
     não guardar a prévia.

     A checagem é pelo hostname, então isto se desliga sozinho quando o portal
     for para o domínio definitivo — não há nada para lembrar de remover. */
  const PREVIA_GITHUB = /(^|\.)github\.io$/.test(location.hostname);
  if (PREVIA_GITHUB) {
    const m = document.createElement('meta');
    m.name = 'robots';
    m.content = 'noindex, nofollow';
    document.head.appendChild(m);
  }

  const NAV = [
    { href: 'programa.html',           label: 'Programa' },
    { href: 'pesquisa.html',           label: 'Pesquisa' },
    { href: 'pessoas.html',            label: 'Pessoas' },
    { href: 'oportunidades.html',      label: 'Oportunidades' },
    { href: 'cursos.html',             label: 'Cursos' },
    { href: 'normas.html',             label: 'Normas' },
    { href: 'indicadores.html',        label: 'Indicadores' },
    { href: 'producao-lattes.html',    label: 'Produção' },
    { href: 'internacionalizacao.html',label: 'Internacional' }
  ];

  const LOGO_SVG = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">' +
    '<circle cx="12" cy="12" r="2.6" fill="#0B1F3A"/>' +
    '<circle cx="12" cy="3.4" r="1.7" fill="#0B1F3A"/>' +
    '<circle cx="19.4" cy="7.7" r="1.7" fill="#0B1F3A"/>' +
    '<circle cx="19.4" cy="16.3" r="1.7" fill="#0B1F3A"/>' +
    '<circle cx="12" cy="20.6" r="1.7" fill="#0B1F3A"/>' +
    '<circle cx="4.6" cy="16.3" r="1.7" fill="#0B1F3A"/>' +
    '<circle cx="4.6" cy="7.7" r="1.7" fill="#0B1F3A"/>' +
    '<g stroke="#0B1F3A" stroke-width="1.15">' +
    '<path d="M12 5.1v4.3M17.9 8.6l-3.7 2.1M17.9 15.4l-3.7-2.1M12 18.9v-4.3M6.1 15.4l3.7-2.1M6.1 8.6l3.7 2.1"/></g></svg>';

  /* ------------------------------------------------------------- header */
  function header(active, base) {
    base = base || '';
    const links = NAV.map(function (n) {
      const cur = n.href === active ? ' aria-current="page"' : '';
      return '<a href="' + base + 'pages/' + n.href + '"' + cur + '>' + n.label + '</a>';
    }).join('');

    return '' +
      '<a href="#conteudo" class="skip-nav">Pular para o conteúdo principal</a>' +
      '<header class="site-header" role="banner">' +
        '<div class="hdr-in">' +
          '<a href="' + base + 'index.html" class="brand" aria-label="REDEMAT — página inicial">' +
            '<img src="' + base + 'assets/img/redemat-logo.png" alt="REDEMAT — Engenharia de Materiais" class="brand-logo" width="640" height="180">' +
            '<span class="brand-sub-inst">UFOP&nbsp;·&nbsp;UEMG</span>' +
          '</a>' +
          '<button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navMain" aria-label="Abrir menu de navegação">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">' +
            '<path d="M3 6h18M3 12h18M3 18h18"/></svg></button>' +
          '<nav class="nav-main" id="navMain" aria-label="Navegação principal">' + links + '</nav>' +
          '<a href="' + base + 'pages/processo-seletivo.html" class="hdr-cta">Ingresso</a>' +
        '</div>' +
      '</header>';
  }

  /* ------------------------------------------------------------- footer */
  function footer(base) {
    base = base || '';
    const R = window.REDEMAT;
    const c = R.programa.contato;
    const upd = R.meta.atualizado.split('-').reverse().join('/');

    return '<footer class="site-footer" role="contentinfo">' +
      '<div class="ft-in">' +
        '<div class="ft-grid">' +
          '<div>' +
            '<p class="ft-h">REDEMAT</p>' +
            '<p class="ft-txt">' + R.programa.nome + '<br>' +
              'Rede Temática em Engenharia de Materiais<br>' +
              'UFOP · UEMG — Área Engenharias II<br>' +
              'Conceito CAPES ' + R.programa.conceito_capes.valor + '</p>' +
          '</div>' +
          '<div>' +
            '<p class="ft-h">Contato</p>' +
            '<p class="ft-txt">' + (c.endereco_detalhe ? '<strong>' + c.endereco_detalhe + '</strong><br>' : '') +
              c.endereco + '<br>' +
              (c.telefone ? c.telefone + '<br>' : '') +
              '<a href="mailto:' + c.email + '">' + c.email + '</a></p>' +
          '</div>' +
          '<div>' +
            '<p class="ft-h">Navegação</p>' +
            '<ul class="ft-list">' +
              '<li><a href="' + base + 'pages/programa.html">O Programa</a></li>' +
              '<li><a href="' + base + 'pages/pesquisa.html">Áreas e linhas</a></li>' +
              '<li><a href="' + base + 'pages/pessoas.html">Corpo docente</a></li>' +
              '<li><a href="' + base + 'pages/discentes.html">Corpo discente</a></li>' +
              '<li><a href="' + base + 'pages/cursos.html">Cursos</a></li>' +
              '<li><a href="' + base + 'pages/oportunidades.html">Oportunidades</a></li>' +
              '<li><a href="' + base + 'pages/laboratorios.html">Laboratórios</a></li>' +
              '<li><a href="' + base + 'pages/reconhecimentos.html">Prêmios e patentes</a></li>' +
              '<li><a href="' + base + 'pages/normas.html">Normas</a></li>' +
            '</ul>' +
          '</div>' +
          '<div>' +
            '<p class="ft-h">Transparência</p>' +
            '<ul class="ft-list">' +
              '<li><a href="' + base + 'pages/indicadores.html">Indicadores</a></li>' +
              '<li><a href="' + base + 'pages/indicadores.html#metodologia">Metodologia de dados</a></li>' +
              '<li><a href="' + base + 'pages/indicadores.html#conflitos">Conflitos de dados</a></li>' +
              '<li><a href="' + base + 'pages/producao-lattes.html">Produção Lattes</a></li>' +
              '<li><a href="' + base + 'pages/normas.html#atas">Atas do Colegiado</a></li>' +
            '</ul>' +
          '</div>' +
        '</div>' +
        '<div class="ft-social">' +
          R.programa.redes.map(function (r) {
            const k = r.nome.toLowerCase();
            return '<a href="' + r.url + '" target="_blank" rel="noopener" class="soc-link" aria-label="' + r.nome + ' da REDEMAT (abre em nova aba)">' +
              (ICO[k] || ICO.ext) + '<span>' + r.handle + '</span></a>';
          }).join('') +
        '</div>' +
        '<div class="ft-inst">' +
          '<a href="https://www.ufop.br" target="_blank" rel="noopener" aria-label="Universidade Federal de Ouro Preto (abre em nova aba)">' +
            '<img src="' + base + 'assets/img/ufop-logo.png" alt="Universidade Federal de Ouro Preto" class="inst-logo inst-logo--tall"></a>' +
          '<a href="https://www.uemg.br" target="_blank" rel="noopener" aria-label="Universidade do Estado de Minas Gerais (abre em nova aba)">' +
            '<img src="' + base + 'assets/img/uemg-logo.png" alt="Universidade do Estado de Minas Gerais" class="inst-logo"></a>' +
          '<img src="' + base + 'assets/img/redemat-logo.png" alt="REDEMAT — Rede Temática em Engenharia de Materiais" class="inst-logo inst-logo--wide">' +
        '</div>' +
        '<div class="ft-bot">' +
          '<p>© 2026 REDEMAT — Universidade Federal de Ouro Preto e Universidade do Estado de Minas Gerais.</p>' +
          '<p>Dados atualizados em ' + upd + ' · <a href="' + base + 'pages/indicadores.html#metodologia">fontes e metodologia</a></p>' +
        '</div>' +
      '</div>' +
    '</footer>';
  }

  /* ------------------------------------------------- selo de proveniência */
  const STATUS_MAP = {
    VALIDADO:      { cls: 'val', txt: 'Validado' },
    PRELIMINAR:    { cls: 'pre', txt: 'Preliminar' },
    PARCIAL:       { cls: 'pre', txt: 'Parcial' },
    DIVERGENTE:    { cls: 'div', txt: 'Divergente' },
    PENDENTE:      { cls: 'div', txt: 'Pendente' },
    EM_DEFINICAO:  { cls: 'nd',  txt: 'Em definição' },
    NAO_DISPONIVEL:{ cls: 'nd',  txt: 'Não disponível' }
  };

  /* Estado desconhecido cai para "Em definição" para não quebrar a página, mas
     grita no console: cair em silêncio é publicar um dado sob o rótulo errado.
     Foi o que aconteceu com 'PARCIAL', que os dados usavam e este mapa não
     tinha — a página de prêmios imprimia "Em definição" no lugar de "Parcial". */
  function badge(status) {
    let s = STATUS_MAP[status];
    if (!s) {
      s = STATUS_MAP.EM_DEFINICAO;
      if (window.console && console.warn) {
        console.warn('[REDEMAT] status "' + status + '" não está em STATUS_MAP ' +
          '(assets/js/components.js) e foi rotulado como "Em definição". ' +
          'Corrija o dado ou acrescente o estado ao mapa.');
      }
    }
    return '<span class="badge badge--' + s.cls + '">' + s.txt + '</span>';
  }

  /* ------------------------------------------------------------ ícones */
  const ICO = {
    info:  '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>',
    warn:  '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>',
    empty: '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" clip-rule="evenodd"/></svg>',
    mail:  '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/><path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/></svg>',
    doc:   '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"/></svg>',
    people:'<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"/></svg>',
    chart: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/></svg>',
    globe: '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM4.332 8.027a6.012 6.012 0 011.912-2.706C6.512 5.73 6.974 6 7.5 6A1.5 1.5 0 019 7.5V8a2 2 0 004 0 2 2 0 011.523-1.943A5.977 5.977 0 0116 10c0 .34-.028.675-.083 1H15a2 2 0 00-2 2v2.197A5.973 5.973 0 0110 16v-2a2 2 0 00-2-2 2 2 0 01-2-2 2 2 0 00-1.668-1.973z" clip-rule="evenodd"/></svg>',
    cap:   '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0z"/></svg>',
    check: '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>',
    flask: '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill-rule="evenodd" d="M7 2a1 1 0 000 2h1v3.5L3.4 15.2A2 2 0 005.1 18h9.8a2 2 0 001.7-2.8L12 7.5V4h1a1 1 0 100-2H7zm3 4h.01M10 6v2.2l4.2 7.3H5.8L10 8.2V6z" clip-rule="evenodd"/></svg>',
    youtube:  '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23 12s0-3.9-.5-5.8a3 3 0 0 0-2.1-2.1C18.5 3.6 12 3.6 12 3.6s-6.5 0-8.4.5A3 3 0 0 0 1.5 6.2C1 8.1 1 12 1 12s0 3.9.5 5.8a3 3 0 0 0 2.1 2.1c1.9.5 8.4.5 8.4.5s6.5 0 8.4-.5a3 3 0 0 0 2.1-2.1C23 15.9 23 12 23 12zM9.8 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg>',
    instagram:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.7.1-.9 0-1.4.2-1.7.3-.4.2-.7.4-1 .6-.3.3-.5.6-.6 1-.1.3-.3.8-.3 1.7-.1 1.2-.1 1.6-.1 4.7s0 3.5.1 4.7c0 .9.2 1.4.3 1.7.2.4.4.7.6 1 .3.3.6.5 1 .6.3.1.8.3 1.7.3 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c.9 0 1.4-.2 1.7-.3.4-.2.7-.4 1-.6.3-.3.5-.6.6-1 .1-.3.3-.8.3-1.7.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c0-.9-.2-1.4-.3-1.7-.2-.4-.4-.7-.6-1-.3-.3-.6-.5-1-.6-.3-.1-.8-.3-1.7-.3-1.2-.1-1.6-.1-4.7-.1zm0 3.1a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.8a3.2 3.2 0 1 0 0 6.4 3.2 3.2 0 0 0 0-6.4zm6.4-2a1.2 1.2 0 1 1-2.4 0 1.2 1.2 0 0 1 2.4 0z"/></svg>',
    linkedin: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.9 21.5H2.6V8.6h4.3v12.9zM4.7 6.8a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5zm16.8 14.7h-4.3v-6.8c0-1.6-.6-2.7-2-2.7-1.1 0-1.8.7-2.1 1.4-.1.3-.1.6-.1 1v7.1H8.7s.1-11.6 0-12.9H13v1.8c.6-.9 1.6-2.1 3.8-2.1 2.8 0 4.8 1.8 4.8 5.7v7.5z"/></svg>',
    ext:   '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"/><path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"/></svg>'
  };

  /* ------------------------------------------------------------ notas */
  function note(kind, html) {
    const ico = kind === 'warn' ? ICO.warn : ICO.info;
    return '<div class="note note--' + kind + '" role="note">' + ico + '<div>' + html + '</div></div>';
  }

  function noteFonte(fonteId, ref, status) {
    const R = window.REDEMAT;
    const f = R.meta.fontes.filter(function (x) { return x.id === fonteId; })[0];
    const nome = f ? f.nome : fonteId;
    const rf = ref ? ' — ' + ref : '';
    return '<div class="note note--prov" role="note">' + ICO.info +
      '<div><strong>Fonte:</strong> ' + nome + rf +
      (f ? ' · coleta em ' + f.coleta.split('-').reverse().join('/') : '') +
      (status ? ' &nbsp;' + badge(status) : '') + '</div></div>';
  }

  function empty(msg, sub) {
    return '<div class="empty-state" role="status">' + ICO.empty +
      '<p>' + (msg || 'Dado em processo de atualização.') + '</p>' +
      (sub ? '<p>' + sub + '</p>' : '') + '</div>';
  }

  /* --------------------------------------------------------- utilitários */
  /* Slug de foto a partir do nome: "Taíse Matte Manhabosco" -> taise-matte-manhabosco */
  function slugFoto(nome) {
    return String(nome || '')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  }

  /* Avatar com foto quando o arquivo existe; iniciais quando não.
     O onerror troca a <img> pelas iniciais sem alterar o layout. */
  /* Formatos de foto aceitos, na ordem em que são tentados quando não há
     manifesto. JPG primeiro porque é o que mais chega; GIF e AVIF no fim
     porque são raros num retrato institucional. */
  const FOTO_FORMATOS = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'avif'];

  /* window.FOTOS vem de assets/img/pessoas/fotos.js, gerado por
     scripts/conferir-fotos.py --manifesto varrendo a pasta. Com o manifesto o
     portal sabe de antemão quem tem foto e em que formato: zero requisição
     desperdiçada. Sem ele, o portal sonda os formatos um a um — funciona para
     quem só jogou os arquivos na pasta, ao custo de alguns 404 silenciosos. */
  let avisouManifesto = false;

  /* O manifesto manda sempre que o arquivo existe — inclusive vazio. A
     alternativa (tratar vazio como ausente) fazia o portal sondar 6 formatos
     para cada uma das 28 pessoas: mais de cem requisições 404 em cada
     carregamento, enquanto ninguém tem foto ainda.
     O custo dessa escolha é que uma foto solta na pasta não aparece até o
     manifesto ser regerado — então o portal avisa no console, uma vez. */
  function comManifesto() {
    const M = window.FOTOS;
    const tem = !!(M && typeof M === 'object');
    if (tem && !avisouManifesto && !Object.keys(M).length) {
      avisouManifesto = true;
      if (window.console && console.info) {
        console.info('[REDEMAT] assets/img/pessoas/fotos.js está vazio: nenhuma foto ' +
          'declarada, e todos aparecem com as iniciais. Depois de colocar arquivos em ' +
          'assets/img/pessoas/, rode: python3 scripts/conferir-fotos.py --manifesto');
      }
    }
    return tem;
  }

  function fotoDe(slug, base) {
    if (comManifesto()) {
      const ext = window.FOTOS[slug];
      return ext ? base + 'assets/img/pessoas/' + slug + '.' + ext : null;
    }
    return base + 'assets/img/pessoas/' + slug + '.' + FOTO_FORMATOS[0];
  }

  /* Chamado pelo onerror da <img>: tenta o formato seguinte e, esgotados,
     cai para as iniciais sem deslocar o layout. */
  function fotoErro(img) {
    const i = Number(img.getAttribute('data-fmt') || 0) + 1;
    if (comManifesto() || i >= FOTO_FORMATOS.length) {
      img.parentNode.classList.add('av--sem-foto');
      img.remove();
      return;
    }
    img.setAttribute('data-fmt', String(i));
    img.src = img.getAttribute('data-base') + 'assets/img/pessoas/' +
      img.getAttribute('data-slug') + '.' + FOTO_FORMATOS[i];
  }

  function avatar(nome, cor, base, slug, tamanho) {
    base = base || '';
    slug = slug || slugFoto(nome);
    const cls = 'av' + (tamanho ? ' av--' + tamanho : '');
    const src = fotoDe(slug, base);
    const ini = '<span class="av-ini" aria-hidden="true">' + initials(nome) + '</span>';

    /* Sem foto declarada no manifesto: nem gera a <img>. Iniciais direto. */
    if (!src) {
      return '<span class="' + cls + ' av--sem-foto" style="--av-cor:' +
        (cor || 'var(--navy-light)') + '">' + ini + '</span>';
    }
    return '<span class="' + cls + '" style="--av-cor:' + (cor || 'var(--navy-light)') + '">' +
      '<img src="' + src + '" alt="" loading="lazy" decoding="async" data-fmt="0" ' +
      'data-slug="' + slug + '" data-base="' + base + '" ' +
      'onerror="window.RC.fotoErro(this)">' + ini +
      '</span>';
  }

  function initials(nome) {
    const p = nome.replace(/\b(de|da|do|dos|das|e)\b/gi, '').trim().split(/\s+/);
    return ((p[0] || '')[0] + (p.length > 1 ? (p[p.length - 1] || '')[0] : '')).toUpperCase();
  }

  function lineColor(id) {
    return ({ l11: 'var(--l11)', l12: 'var(--l12)', l21: 'var(--l21)', l22: 'var(--l22)' })[id] || 'var(--text-soft)';
  }

  function lineInfo(id) {
    const R = window.REDEMAT;
    let found = null;
    R.areas.itens.forEach(function (a) {
      a.linhas.forEach(function (l) { if (l.id === id) found = { linha: l, area: a }; });
    });
    return found;
  }

  function num(n) { return new Intl.NumberFormat('pt-BR').format(n); }

  function brl(n) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }).format(n);
  }

  /* ------------------------------------------- fallback de gráfico offline
     Se a biblioteca Chart.js não carregar (sem internet, CDN bloqueado),
     o dado NÃO se perde: o canvas é substituído por uma tabela acessível.
     ---------------------------------------------------------------------- */
  function chartFallback(canvasId, cols, rows, msg) {
    const el = document.getElementById(canvasId);
    if (!el) return;
    const head = cols.map(function (c, i) {
      return '<th scope="col"' + (i ? ' style="text-align:right"' : '') + '>' + c + '</th>';
    }).join('');
    const body = rows.map(function (r) {
      return '<tr>' + r.map(function (v, i) {
        return i ? '<td class="num">' + (typeof v === 'number' ? num(v) : v) + '</td>' : '<th scope="row" style="font-weight:500">' + v + '</th>';
      }).join('') + '</tr>';
    }).join('');
    const box = el.closest('.chart-box') || el.parentNode;
    box.style.height = 'auto';
    box.innerHTML =
      '<div class="chart-fallback">' +
        '<p class="msg">' + (msg || 'Gráfico indisponível sem conexão à internet. Os dados estão na tabela abaixo.') + '</p>' +
        '<table><thead><tr>' + head + '</tr></thead><tbody>' + body + '</tbody></table>' +
      '</div>';
  }

  /* Executa `onReady` quando Chart.js estiver disponível; senão chama `onFail`. */
  function whenChart(onReady, onFail) {
    if (window.Chart) { onReady(); return; }
    let settled = false;
    const done = function (ok) {
      if (settled) return;
      settled = true;
      if (ok && window.Chart) onReady(); else onFail();
    };
    const s = document.querySelector('script[src*="chart"]');
    if (s) {
      s.addEventListener('load', function () { done(true); });
      s.addEventListener('error', function () { done(false); });
    }
    window.addEventListener('load', function () {
      setTimeout(function () { done(!!window.Chart); }, 400);
    });
    setTimeout(function () { done(!!window.Chart); }, 6000);
  }

  /* ------------------------------------------------------ contador animado */
  function animateCounters(root) {
    const els = (root || document).querySelectorAll('[data-count]');
    if (!els.length) return;
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const run = function (el) {
      const target = parseFloat(el.dataset.count);
      if (reduce) { el.textContent = num(target); return; }
      const dur = 1100, t0 = performance.now();
      const tick = function (now) {
        const p = Math.min((now - t0) / dur, 1);
        const e = 1 - Math.pow(1 - p, 3);
        el.textContent = num(Math.round(target * e));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };

    if (!('IntersectionObserver' in window)) { els.forEach(run); return; }
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { run(en.target); io.unobserve(en.target); }
      });
    }, { threshold: .35 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------------ menu móvel */
  function initNav() {
    const btn = document.getElementById('navToggle');
    const nav = document.getElementById('navMain');
    if (!btn || !nav) return;

    const isMobile = function () { return window.matchMedia('(max-width: 1180px)').matches; };
    const sync = function () { if (isMobile()) { nav.hidden = true; btn.setAttribute('aria-expanded', 'false'); } else { nav.hidden = false; } };
    sync();
    window.addEventListener('resize', sync);

    btn.addEventListener('click', function () {
      const open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      nav.hidden = open;
      btn.setAttribute('aria-label', open ? 'Abrir menu de navegação' : 'Fechar menu de navegação');
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isMobile() && !nav.hidden) { btn.click(); btn.focus(); }
    });
  }

  /* ------------------------------------------------------------- montagem */
  function mount(active, base) {
    const h = document.getElementById('site-header-slot');
    const f = document.getElementById('site-footer-slot');
    if (h) h.outerHTML = header(active, base);
    if (f) f.outerHTML = footer(base);
    initNav();
    animateCounters();
  }

  window.RC = {
    header: header, footer: footer, mount: mount,
    badge: badge, note: note, noteFonte: noteFonte, empty: empty,
    ICO: ICO, initials: initials, lineColor: lineColor, lineInfo: lineInfo,
    slugFoto: slugFoto, avatar: avatar, fotoErro: fotoErro,
    FOTO_FORMATOS: FOTO_FORMATOS,
    num: num, brl: brl, animateCounters: animateCounters,
    chartFallback: chartFallback, whenChart: whenChart
  };
})();
