/* ==========================================================================
   REDEMAT — Camada de dados com proveniência
   --------------------------------------------------------------------------
   REGRA FUNDAMENTAL: nenhum dado sem origem rastreável.
   Todo registro carrega { valor, fonte, ref, coleta, status }.

   status:
     VALIDADO      → conferido em ≥2 fontes ou confirmado por documento oficial
     PRELIMINAR    → coletado, aguarda validação formal (exibido com aviso)
     DIVERGENTE    → fontes conflitam; publicação suspensa
     EM_DEFINICAO  → decisão institucional pendente
     NAO_PUBLICAR  → dado interno/sensível; jamais renderizado no portal público

   NÃO CONTÉM (por decisão de governança + LGPD):
     CPF, telefone pessoal, endereço residencial, salário, score interno
     por docente, h-index individual, ranking individual de produção ou
     de captação, respostas individuais de autoavaliação.
   ========================================================================== */

const REDEMAT = {

  /* ---------------------------------------------------------------- meta */
  meta: {
    versao: '4.9',
    atualizado: '2026-09-08',
    fontes: [
      { id: 'CONSOL',   nome: 'Entrega consolidada Lattes REDEMAT 2021–2026',   ref: 'codex/apcn/10_analises/entrega_atualizada_lattes_20260829 — corte 29/08/2026', coleta: '2026-08-29' },
      { id: 'SCOPUS_M', nome: 'Scopus Sources — consulta manual na interface',  ref: 'scopus.com/sources.uri · data/percentis-scopus-manuais.csv', coleta: '2026-09-02' },
      { id: 'SITE',     nome: 'Site institucional REDEMAT',                    ref: 'https://redemat.ufop.br/',                    coleta: '2026-09-01' },
      { id: 'DOCENTES', nome: 'Página oficial de docentes',                    ref: 'https://redemat.ufop.br/docentes-1',          coleta: '2026-09-02' },
      { id: 'LATTES',   nome: 'Currículos Lattes/CNPq via ScriptLattes',       ref: 'scriptlattes/json — 25 currículos, 28/08/2026', coleta: '2026-08-28' },
      { id: 'APCN',     nome: 'Painel analítico APCN REDEMAT (interno)',       ref: 'portal_integrado_apcn_redemat_20260829',      coleta: '2026-08-29' },
      { id: 'PROPOSTA', nome: 'Esqueleto da Proposta APCN Doutorado v0.1',     ref: 'Esqueleto_Proposta_APCN_Doutorado_REDEMAT_2026', coleta: '2026-07-31' },
      { id: 'CURRIC',   nome: 'Proposta de estrutura curricular',              ref: 'Proposta de estrutura curricular.docx',       coleta: '2026-09-02' },
      { id: 'CAPTACAO', nome: 'Panorama de captação (planilha deduplicada)',   ref: 'REDEMAT_APCN_2026_Panorama_Captacao...xlsx',  coleta: '2026-08-29' },
      { id: 'MAPA',     nome: 'Mapa de publicações docente × periódico',        ref: 'mapa_publicacoes_dados.xlsx — ScriptLattes + Scopus 2025', coleta: '2026-08-29' },
      { id: 'PAINEL',   nome: 'Painel de projetos e captação (portal integrado)', ref: 'projetos-data.js — corte 29/08/2026',       coleta: '2026-08-29' },
      { id: 'NORMAS',   nome: 'Página de normas do Programa',                   ref: 'https://redemat.ufop.br/normas',              coleta: '2026-09-02' },
      { id: 'PESSOAS',  nome: 'Páginas de discentes, pós-doutorandos e técnicos', ref: 'https://redemat.ufop.br/discentes-0 · /pós-doutorandos · /técnicos', coleta: '2026-09-02' },
      { id: 'COORD',    nome: 'Informação direta da coordenação do Programa',    ref: 'Vice-coordenação — Prof. Matheus J. S. Matos', coleta: '2026-09-02' },
      { id: 'DISCENTES',nome: 'Página oficial de discentes',                      ref: 'https://redemat.ufop.br/discentes-0', coleta: '2026-09-02' },
      { id: 'GEO',      nome: 'Mapa geolocalizado de colaborações',               ref: 'mapa-colaboracoes-dados.json — OpenAlex + Lattes, auditoria 01/09/2026', coleta: '2026-09-01' },
      { id: 'SL2010',   nome: 'ScriptLattes — relatório 2010–2026 do painel integrado', ref: 'portal_integrado_apcn_redemat_20260829/scriptlattes — processamento de 28/08/2026', coleta: '2026-08-28' },
      { id: 'LABS',     nome: 'Página oficial de laboratórios',            ref: 'https://redemat.ufop.br/laboratorios',        coleta: '2026-09-03' },
      { id: 'GORCEIX',  nome: 'Fundação Gorceix — Apoio à EM-UFOP',         ref: 'https://site.gorceix.org.br/apoio-a-em-ufop',  coleta: '2026-09-03' },
      { id: 'PATENTES', nome: 'Página oficial de patentes e softwares',    ref: 'https://redemat.ufop.br/patentes',            coleta: '2026-09-03' },
      { id: 'NEWS',     nome: 'Notícias do site institucional',            ref: 'https://redemat.ufop.br/news/',               coleta: '2026-09-03' },
      { id: 'ATAS',     nome: 'Atas das reuniões do Colegiado',                 ref: 'https://redemat.ufop.br/atas-das-reuniões-do-colegiado', coleta: '2026-09-02' }
    ],
    aviso_global: 'Indicadores derivados de currículos Lattes e de bases internas de trabalho são marcados como PRELIMINAR até conferência na Plataforma Sucupira.',
    /* Unidade de contagem: a distinção que motivou a auditoria da v4.2. */
    unidade_de_contagem: 'Todo indicador de produção pode ser contado por produto único (cada artigo, projeto ou patente conta uma vez no Programa) ou por soma por docente (uma vez para cada docente envolvido). São medidas diferentes e nenhuma substitui a outra. Cada número deste portal declara qual unidade usa, e scripts/auditar-numeros.py confere isso contra a entrega consolidada.'
  },

  /* ------------------------------------------------------------ programa */
  programa: {
    nome: 'Programa de Pós-Graduação em Engenharia de Materiais',
    nome_en: 'Interinstitutional Graduate Program on Materials Engineering',
    rede: 'REDEMAT — Rede Temática em Engenharia de Materiais',
    sigla: 'REDEMAT',
    codigo_capes: { valor: '32007019007P3', fonte: 'PROPOSTA', status: 'VALIDADO' },
    area_avaliacao: 'Engenharias II',
    area_basica: 'Engenharia de Materiais e Metalúrgica',
    modalidade: 'Acadêmica — ensino presencial, regime semestral',
    forma_associativa: {
      valor: 'UFOP (coordenadora) + UEMG (associada)',
      fonte: 'PROPOSTA', status: 'VALIDADO'
    },
    conceito_capes: { valor: 4, fonte: 'SITE', status: 'VALIDADO' },
    ano_concepcao: { valor: 1995, fonte: 'PROPOSTA', status: 'VALIDADO' },
    ano_inicio_mestrado: { valor: 1996, fonte: 'PROPOSTA', ref: 'Ficha "Ano de início do Programa"', status: 'VALIDADO' },
    /* Composição institucional — quem forma a rede. Vem do enunciado da
       coordenação e das páginas das unidades; é o que a home passa a dizer. */
    composicao: {
      fonte: 'COORD', ref: 'Coordenação do Programa; páginas institucionais das unidades', status: 'VALIDADO',
      resumo: 'A REDEMAT é um programa em rede da UFOP e da UEMG. Na UFOP reúne os Departamentos de Física e de Química, do Instituto de Ciências Exatas e Biológicas, e o Departamento de Engenharia Metalúrgica e de Materiais, da Escola de Minas, onde funciona a secretaria. Na UEMG, a Escola de Design.',
      unidades: [
        {
          ies: 'UFOP', ies_nome: 'Universidade Federal de Ouro Preto', url: 'https://www.ufop.br/',
          escola: 'Escola de Minas', escola_url: 'https://em.ufop.br/',
          departamentos: [
            { sigla: 'DEMET', nome: 'Departamento de Engenharia Metalúrgica e de Materiais', unidade: 'Escola de Minas', papel: 'Sede da secretaria do Programa' },
            { sigla: 'DEFIS', nome: 'Departamento de Física', unidade: 'Instituto de Ciências Exatas e Biológicas' },
            { sigla: 'DEQUI', nome: 'Departamento de Química', unidade: 'Instituto de Ciências Exatas e Biológicas' }
          ]
        },
        {
          ies: 'UEMG', ies_nome: 'Universidade do Estado de Minas Gerais', url: 'http://www.uemg.br/',
          escola: 'Escola de Design', escola_url: 'http://ed.uemg.br/',
          departamentos: [
            { sigla: 'ED-UEMG', nome: 'Escola de Design', unidade: 'Belo Horizonte' }
          ]
        }
      ],
      nota: 'Esta composição por departamentos é o que dá ao Programa a combinação de metalurgia, física, química e design — e é ela que explica por que a mesma rede orienta trabalhos em aço microligado e em design de moda.'
    },
    contato: {
      /* A secretaria funciona na Escola de Minas, Campus Morro do Cruzeiro.
         O endereço da Praça Tiradentes é o que consta no cadastro do site
         institucional — mantido como endereço de correspondência declarado. */
      endereco: 'Escola de Minas — Campus Universitário Morro do Cruzeiro, Ouro Preto — MG, 35400-000',
      endereco_detalhe: 'Secretaria do Programa',
      endereco_fonte: 'COORD', endereco_status: 'VALIDADO',
      endereco_cadastro: 'Praça Tiradentes, 20 — Centro, Ouro Preto — MG, 35400-084',
      endereco_cadastro_fonte: 'DOCENTES',
      endereco_nota: 'A secretaria atende na Escola de Minas, no Campus Morro do Cruzeiro. O endereço da Praça Tiradentes consta no cadastro do site institucional e permanece como endereço de correspondência.',
      telefone: '(31) 3559-1596',
      email: 'redemat@ufop.edu.br',
      email_coord: 'coordenacao.redemat.em@ufop.edu.br',
      email_vice: 'vicecoordenacao.redemat.em@ufop.edu.br',
      site: 'https://redemat.ufop.br'
    },
    redes: [
      { nome: 'YouTube',   url: 'https://www.youtube.com/@REDEMAT', handle: '@REDEMAT' },
      { nome: 'Instagram', url: 'https://www.instagram.com/redemat.ufop/', handle: '@redemat.ufop' },
      { nome: 'LinkedIn',  url: 'https://www.linkedin.com/in/redemat-ufop-uemg-4838333a9/', handle: 'REDEMAT UFOP-UEMG' }
    ],
    /* `foto` é explícito porque o slug não sai do nome com título: o portal
       geraria "profa-dra-dalila..." e "matheus-j-s-matos". Aqui aponta para o
       mesmo arquivo usado na lista de docentes. */
    coordenacao: [
      { cargo: 'Coordenadora',      nome: 'Profa. Dra. Dalila Chaves Sicupira', email: 'coordenacao.redemat.em@ufop.edu.br', foto: 'dalila-chaves-sicupira' },
      { cargo: 'Vice-Coordenador',  nome: 'Prof. Dr. Matheus J. S. Matos',      email: 'vicecoordenacao.redemat.em@ufop.edu.br', foto: 'matheus-josue-de-souza-matos' }
    ],
    comissao_apcn: {
      valor: ['Profa. Dra. Dalila Chaves Sicupira', 'Prof. Dr. Matheus J. S. Matos', 'Profa. Dra. Eliane Ayres',
              'Prof. Dr. Versiane Albis Leão', 'Prof. Dr. Geraldo Lúcio de Faria', 'Prof. Dr. Marcelo Gomes Speziali'],
      fonte: 'PROPOSTA', status: 'VALIDADO'
    },
    missao: {
      valor: 'Formar mestres e doutores com sólida qualificação científica, tecnológica, ética e interdisciplinar em Engenharia de Materiais, capazes de produzir conhecimento no estado da arte, liderar projetos e desenvolver soluções para desafios industriais e sociais, contribuindo para o desenvolvimento sustentável.',
      fonte: 'PROPOSTA', ref: 'seção 5.1 — minuta', status: 'PRELIMINAR'
    },
    visao: {
      valor: 'Ser reconhecida como Programa associativo de referência nacional em Engenharia de Materiais, distinguindo-se pela excelência na formação, pela integração UFOP-UEMG, pela qualidade e regularidade da produção com discentes e egressos, e pela atuação em minerais críticos, materiais avançados e sustentabilidade.',
      fonte: 'PROPOSTA', ref: 'seção 5.2 — minuta', status: 'PRELIMINAR'
    },
    valor_gerado: {
      valor: [
        'Formação de pesquisadores, docentes, profissionais e lideranças científicas e tecnológicas.',
        'Produção de conhecimento, métodos, bases de dados, materiais, processos, dispositivos e produtos.',
        'Soluções para mineração, metalurgia, siderurgia, manufatura, energia, saúde, ambiente e cadeias de materiais.',
        'Agregação de valor a minerais e resíduos; circularidade e descarbonização de processos.',
        'Fortalecimento da cooperação entre universidade, empresas, governo e sociedade.',
        'Nucleação de grupos de pesquisa, internacionalização e formação em rede.',
        'Transferência de tecnologia, propriedade intelectual, empreendedorismo e inovação de base científica.'
      ],
      fonte: 'PROPOSTA', ref: 'seção 5.3', status: 'PRELIMINAR'
    }
  },

  /* ------------------------------------------------------------ timeline */
  timeline: {
    status: 'VALIDADO', fonte: 'PROPOSTA',
    itens: [
      { ano: '1995', texto: 'Criação da REDEMAT pela união entre UFOP, UEMG e CETEC, constituindo a Rede Temática em Engenharia de Materiais — estrutura interinstitucional, interdepartamental e multi-unidades.' },
      { ano: '1996', texto: 'Início formal das atividades do Mestrado em Engenharia de Materiais.' },
      { ano: '1998', texto: 'Início da formação de especialistas, mestres e doutores em Engenharia de Materiais e em Sistemas Mínero-Metalúrgicos.' },
      { ano: '1999', texto: 'Primeiras parcerias com empresas e entidades para disseminação de conhecimento avançado e capacitação em nível de especialização e pós-graduação.' },
      { ano: '2014', texto: 'O CETEC é incorporado pela FIEMG e deixa de integrar formalmente a rede; a REDEMAT segue com UFOP na coordenação geral e UEMG como instituição associada.' },
      { ano: '2018', texto: 'Início dos processos de autoavaliação institucional do Programa (reformulados em 2020).' },
      { ano: '2026', texto: 'Elaboração da proposta de criação do curso de Doutorado Acadêmico (APCN/CAPES 2026) e reorganização da arquitetura acadêmica em duas áreas de concentração e quatro linhas de pesquisa.' }
    ]
  },

  /* ---------------------------------------------------------------- KPIs */
  kpis: [
    { id: 'docentes',  valor: 24,  rotulo: 'Docentes no corpo permanente e colaborador', sufixo: '',
      fonte: 'DOCENTES + APCN', ref: 'Página oficial de docentes; núcleo APCN 29/08/2026', status: 'VALIDADO', cor: 'var(--navy)' },
    { id: 'permanentes', valor: 21, rotulo: 'Docentes permanentes', sufixo: '',
      fonte: 'PROPOSTA + LATTES', ref: 'Tabela de corpo docente da proposta APCN', status: 'VALIDADO', cor: 'var(--area1)' },
    { id: 'bolsistas', valor: 11, rotulo: 'Bolsistas de produtividade CNPq (PQ e DT)', sufixo: '',
      fonte: 'PROPOSTA + LATTES', ref: '8 PQ + 3 DT', status: 'VALIDADO', cor: 'var(--amber)' },
    { id: 'artigos',   valor: 308, rotulo: 'Artigos em periódicos (2021–2026)', sufixo: '',
      fonte: 'LATTES', ref: 'Deduplicado por DOI/título — 94% com DOI', status: 'PRELIMINAR', cor: 'var(--area2)' },
    { id: 'mestres',   valor: 118, rotulo: 'Dissertações de mestrado concluídas (2021–2026)', sufixo: '',
      fonte: 'APCN', ref: 'Somatório de orientações concluídas', status: 'PRELIMINAR', cor: 'var(--l12)' },
    { id: 'doutores',  valor: 48,  rotulo: 'Teses de doutorado orientadas (2021–2026)', sufixo: '',
      fonte: 'APCN', ref: 'Orientações de doutorado concluídas pelo corpo docente em programas diversos', status: 'PRELIMINAR', cor: 'var(--l22)' },
    { id: 'projetos',  valor: 110, rotulo: 'Projetos de pesquisa únicos (2021–2026)', sufixo: '',
      fonte: 'CAPTACAO', ref: 'Planilha deduplicada — recorte 2021–2026', status: 'PRELIMINAR', cor: 'var(--l21)' },
    { id: 'conceito',  valor: 4,   rotulo: 'Conceito CAPES', sufixo: '',
      fonte: 'SITE', ref: 'Avaliação quadrienal', status: 'VALIDADO', cor: 'var(--amber)' }
  ],

  /* ------------------------------- áreas de concentração e linhas (2+4) */
  areas: {
    fonte: 'PROPOSTA + CURRIC', ref: 'seções 6.2 e 6.3 da proposta APCN 2026',
    status: 'PRELIMINAR',
    nota: 'Arquitetura de duas áreas e quatro linhas proposta em 2026 para substituir as 17 linhas históricas. Aguarda aprovação no Colegiado.',
    itens: [
      {
        id: 'a1', codigo: 'Área de Concentração 1',
        nome: 'Processamento, Estrutura e Desempenho de Materiais',
        cor: 'var(--area1)', pale: 'var(--area1-pale)',
        descricao: 'Reúne pesquisas voltadas à obtenção, transformação, modificação, caracterização, modelagem e avaliação do desempenho de materiais. O eixo integrador é a compreensão e o controle das relações entre processamento, estrutura, propriedades, degradação e desempenho em condições de aplicação.',
        linhas: [
          {
            id: 'l11', codigo: 'Linha 1.1', cor: 'var(--l11)',
            nome: 'Processamento, Manufatura e Engenharia de Superfícies',
            escopo: 'Síntese, elaboração, processamento e transformação de materiais; processos metalúrgicos; conformação; manufatura convencional e aditiva; tratamentos térmicos e químicos; soldagem; sinterização; processamento a laser; revestimentos; modificação de superfícies; corrosão; tribologia; otimização de processos.',
            palavras: ['Manufatura aditiva', 'Tratamentos térmicos', 'Soldagem', 'Engenharia de superfícies', 'Tribologia', 'Corrosão', 'Sinterização', 'Revestimentos']
          },
          {
            id: 'l12', codigo: 'Linha 1.2', cor: 'var(--l12)',
            nome: 'Estrutura, Propriedades, Degradação, Modelagem e Integridade',
            escopo: 'Relações estrutura-microestrutura-propriedades-desempenho; transformações de fase; comportamento mecânico, físico, químico, eletrônico, óptico e magnético; fadiga, fratura, degradação e integridade; caracterização multiescala; modelagem computacional e multiescala; inteligência artificial aplicada a materiais.',
            palavras: ['Transformações de fase', 'Comportamento mecânico', 'Fadiga e fratura', 'Modelagem multiescala', 'DFT e ab initio', 'Dinâmica molecular', 'IA em materiais', 'Caracterização']
          }
        ]
      },
      {
        id: 'a2', codigo: 'Área de Concentração 2',
        nome: 'Materiais Estratégicos, Funcionais e Sustentáveis',
        cor: 'var(--area2)', pale: 'var(--area2-pale)',
        descricao: 'Integra pesquisas orientadas ao desenvolvimento e à aplicação de materiais com relevância estratégica, funcional, ambiental e social. Abrange a cadeia que vai de recursos minerais e resíduos à obtenção de materiais, dispositivos e produtos, incorporando transição energética e economia circular.',
        linhas: [
          {
            id: 'l21', codigo: 'Linha 2.1', cor: 'var(--l21)',
            nome: 'Recursos Minerais, Minerais Críticos e Economia Circular',
            escopo: 'Processamento e valorização de recursos minerais; minerais críticos e estratégicos; hidrometalurgia, bio-hidrometalurgia, pirometalurgia e eletrometalurgia; recuperação e reciclagem de metais; rejeitos e coprodutos; materiais e processos de baixo carbono; tratamento de águas e efluentes.',
            palavras: ['Minerais críticos', 'Hidrometalurgia', 'Pirometalurgia', 'Mineração urbana', 'Economia circular', 'Rejeitos e coprodutos', 'Baixo carbono']
          },
          {
            id: 'l22', codigo: 'Linha 2.2', cor: 'var(--l22)',
            nome: 'Materiais Funcionais, Biomateriais, Transição Energética, Desenvolvimento de Novos Materiais e Inovação Tecnológica',
            escopo: 'Materiais eletrônicos, ópticos, magnéticos, inteligentes, nanoestruturados e bidimensionais; biomateriais e materiais para saúde; materiais para conversão e armazenamento de energia; polímeros funcionais, compósitos e cerâmicos; sensores, dispositivos e sistemas para energia e ambiente.',
            palavras: ['Nanomateriais', 'Materiais 2D', 'Biomateriais', 'Armazenamento de energia', 'Polímeros funcionais', 'Sensores e dispositivos', 'Design de materiais']
          }
        ]
      }
    ]
  },

  eixos_transversais: {
    fonte: 'PROPOSTA', ref: 'seção 6 — tabela de eixos transversais', status: 'PRELIMINAR',
    itens: [
      { nome: 'Caracterização avançada',            funcao: 'Suporta todas as áreas e linhas sem constituir linha autônoma.' },
      { nome: 'Modelagem, ciência de dados e IA',   funcao: 'Integra simulação, análise de dados, descoberta de materiais e otimização de processos.' },
      { nome: 'Sustentabilidade e ciclo de vida',   funcao: 'Avalia recursos, energia, emissões, resíduos, circularidade e impactos.' },
      { nome: 'Inovação e transferência',           funcao: 'Conecta resultados científicos a patentes, licenças, protótipos, empresas e políticas.' },
      { nome: 'Integridade e ciência aberta',       funcao: 'Promove ética, reprodutibilidade, gestão de dados e comunicação científica.' }
    ]
  },

  /* ------------------------------------------------------------- docentes
     Vinculação de linha:
       VALIDADO     → nomeado como docente principal da linha na proposta APCN
       PRELIMINAR   → inferido da responsabilidade por disciplina na proposta curricular
       EM_DEFINICAO → sem vinculação documentada
     Contagens individuais de produção/captação NÃO constam por decisão de
     governança (vedado ranking público de docentes).
  ------------------------------------------------------------------------ */
  docentes: {
    fonte: 'DOCENTES + PROPOSTA + LATTES',
    ref: 'Página oficial de docentes; tabela de corpo docente da proposta APCN; IDs Lattes do ScriptLattes',
    status: 'VALIDADO',
    /* O conjunto publicado é de 24, e a página oficial lista 25. A diferença é
       registrada como CONTAGEM, sem identificar a pessoa: nomear alguém como
       excluído é uma afirmação pública sobre essa pessoa, e o portal não tem
       por que fazê-la para explicar um número. Ver o conflito "Número de
       docentes permanentes" em `conflitos`. */
    conjunto_nota: 'A página oficial do Programa lista 25 registros de docentes; o conjunto adotado nesta versão do portal é de 24 — 21 permanentes e 3 colaboradores, conforme a tabela de corpo docente da proposta APCN.',
    itens: [
      { nome: 'Alan Barros de Oliveira',            cat: 'permanente', ies: 'UFOP', bolsa: 'PQ-2',  ch: '20h', dp: 2, lattes: '2373454332205980', email: 'oliveira@ufop.edu.br',            linha: 'l12', linhaStatus: 'VALIDADO' },
      { nome: 'Américo Tristão Bernardes',          cat: 'permanente', ies: 'UFOP', bolsa: null,    ch: '20h', dp: 2, lattes: '1219153096910234', email: 'atb@ufop.edu.br',                 linha: 'l12', linhaStatus: 'PRELIMINAR' },
      { nome: 'Ana Paula Moreira Barboza',          cat: 'permanente', ies: 'UFOP', bolsa: 'PQ-2',  ch: '20h', dp: 2, lattes: '4012812193989993', email: 'ana.barboza@ufop.edu.br',         linha: 'l12', linhaStatus: 'VALIDADO' },
      { nome: 'Antônio Valadão Cardoso',            cat: 'colaborador', ies: 'UEMG', bolsa: 'PQ UEMG', bolsaAgencia: 'UEMG', ch: '40h', dp: 0, lattes: '4629729793297288', email: null,   linha: null,  linhaStatus: 'EM_DEFINICAO' },
      { nome: 'Claudio Gouvea dos Santos',          cat: 'permanente', ies: 'UFOP', bolsa: null,    ch: '20h', dp: 1, lattes: '7624637352404779', email: 'claudio@ufop.edu.br',             linha: 'l11', linhaStatus: 'PRELIMINAR' },
      { nome: 'Dalila Chaves Sicupira',             cat: 'permanente', ies: 'UFOP', bolsa: null,    ch: '40h', dp: 1, lattes: '2402619959878318', email: 'coordenacao.redemat.em@ufop.edu.br', linha: 'l11', linhaStatus: 'PRELIMINAR', cargo: 'Coordenadora' },
      { nome: 'Eliane Ayres',                       cat: 'permanente', ies: 'UEMG', bolsa: 'DT-C',  ch: '20h', dp: 2, lattes: '1370798140664840', email: 'eayres.pu@hotmail.com',           linha: 'l22', linhaStatus: 'VALIDADO' },
      { nome: 'Fernando Gabriel da Silva Araújo',   cat: 'permanente', ies: 'UFOP', bolsa: null,    ch: '40h', dp: 1, lattes: '8915679278888857', email: 'fgabriel@ufop.edu.br',            linha: 'l11', linhaStatus: 'PRELIMINAR' },
      { nome: 'Geraldo Lúcio de Faria',             cat: 'permanente', ies: 'UFOP', bolsa: 'PQ-1D', ch: '20h', dp: 2, lattes: '0954824992144106', email: 'geraldofaria@ufop.edu.br',        linha: 'l11', linhaStatus: 'VALIDADO' },
      { nome: 'Heloisa Nazaré dos Santos',          cat: 'colaborador', ies: 'UEMG', bolsa: null,   ch: '20h', dp: 0, lattes: '7238982117122755', email: 'heloisa.santos@uemg.br',          linha: 'l22', linhaStatus: 'PRELIMINAR' },
      { nome: 'Hugo Bonette de Carvalho',           cat: 'permanente', ies: 'UFOP', bolsa: null,    ch: '40h', dp: 1, lattes: '1642083834158700', email: 'bonette@gmail.com',               linha: 'l11', linhaStatus: 'PRELIMINAR' },
      { nome: 'Ive Silvestre de Almeida',           cat: 'colaborador', ies: 'UFOP', bolsa: null,   ch: '20h', dp: 2, lattes: '8756368667136851', email: 'ive.almeida@ufop.edu.br',         linha: 'l22', linhaStatus: 'PRELIMINAR' },
      { nome: 'Johne Jesus Mol Peixoto',            cat: 'permanente', ies: 'UFOP', bolsa: 'PQ-C',  ch: '40h', dp: 1, lattes: '7172124269609011', email: 'johne.peixoto@ufop.edu.br',       linha: 'l11', linhaStatus: 'VALIDADO' },
      { nome: 'Leonardo Barbosa Godefroid',         cat: 'permanente', ies: 'UFOP', bolsa: null,    ch: '20h', dp: 2, lattes: '1995142616892313', email: 'leonardo@ufop.edu.br',            linha: 'l12', linhaStatus: 'PRELIMINAR' },
      { nome: 'Marcelo Gomes Speziali',             cat: 'permanente', ies: 'UFOP', bolsa: 'DT-C',  ch: '10h', dp: 3, lattes: '7307092459450276', email: 'speziali@ufop.edu.br',            linha: 'l22', linhaStatus: 'VALIDADO' },
      { nome: 'Matheus Josué de Souza Matos',       cat: 'permanente', ies: 'UFOP', bolsa: 'PQ-2',  ch: '20h', dp: 2, lattes: '6221953730638193', email: 'vicecoordenacao.redemat.em@ufop.edu.br', linha: 'l12', linhaStatus: 'VALIDADO', cargo: 'Vice-Coordenador' },
      { nome: 'Paulo Santos Assis',                 cat: 'permanente', ies: 'UFOP', bolsa: 'DT-C',  ch: '20h', dp: 2, lattes: '7360474381329605', email: 'assis@ufop.edu.br',               linha: 'l21', linhaStatus: 'VALIDADO' },
      { nome: 'Rita de Castro Engler',              cat: 'permanente', ies: 'UEMG', bolsa: null,    ch: '20h', dp: 2, lattes: '1848076566428564', email: 'rita.engler@gmail.com',           linha: 'l21', linhaStatus: 'PRELIMINAR' },
      { nome: 'Rodrigo Fernando Bianchi',           cat: 'permanente', ies: 'UFOP', bolsa: 'PQ-2',  ch: '20h', dp: 2, lattes: '0576192110271130', email: 'bianchi@ufop.edu.br',             linha: 'l22', linhaStatus: 'VALIDADO' },
      { nome: 'Rodrigo Rangel Porcaro',             cat: 'permanente', ies: 'UFOP', bolsa: null,    ch: '20h', dp: 1, lattes: '3405298711596512', email: 'rodrigo.porcaro@ufop.edu.br',     linha: 'l11', linhaStatus: 'PRELIMINAR' },
      { nome: 'Taíse Matte Manhabosco',             cat: 'permanente', ies: 'UFOP', bolsa: 'PQ-2',  ch: '20h', dp: 2, lattes: '9945942332231660', email: 'taise@ufop.edu.br',               linha: 'l11', linhaStatus: 'VALIDADO' },
      { nome: 'Thiago Cazati',                      cat: 'permanente', ies: 'UFOP', bolsa: null,    ch: '20h', dp: 2, lattes: '0873693558323059', email: 'thcazati@ufop.edu.br',            linha: 'l22', linhaStatus: 'VALIDADO' },
      { nome: 'Versiane Albis Leão',                cat: 'permanente', ies: 'UFOP', bolsa: 'PQ-1C', ch: '20h', dp: 2, lattes: '4062848906639188', email: 'versiane@ufop.edu.br',            linha: 'l21', linhaStatus: 'VALIDADO' },
      { nome: 'Víctor de Andrade Alvarenga Oliveira', cat: 'permanente', ies: 'UFOP', bolsa: null,  ch: '20h', dp: 1, lattes: '9004123547060623', email: 'victor@ufop.edu.br',              linha: 'l21', linhaStatus: 'PRELIMINAR' }
    ]
  },

  /* ------------------------------------------------------------- produção */
  producao: {
    fonte: 'CONSOL', ref: 'entrega_atualizada_lattes_20260829 — 09/05_evidencias_artigos_deduplicados.csv', status: 'VALIDADO',
    /* DUAS CONTAGENS, DOIS RÓTULOS. É a distinção que produziu o erro do "202":
         total_unico  — cada artigo conta UMA vez no Programa (308)
         registros    — cada artigo conta uma vez por docente coautor (366)
       Publicar uma com o rótulo da outra é erro de fato. Conferido por
       scripts/auditar-numeros.py contra a entrega consolidada. */
    nota: 'Artigos deduplicados por DOI (94% dos registros) e, na ausência de DOI, por título normalizado. Os 366 registros docente–artigo somam mais que os 308 artigos únicos por causa da coautoria interna ao Programa: um artigo assinado por três docentes aparece em três registros e conta uma única vez no total do Programa.',
    anos: ['2021', '2022', '2023', '2024', '2025', '2026'],
    unicos:      { 2021: 62, 2022: 48, 2023: 57, 2024: 49, 2025: 53, 2026: 39 },
    por_docente: { 2021: 75, 2022: 58, 2023: 66, 2024: 56, 2025: 65, 2026: 50 },
    total_unico: 308,
    total_somado: 366,
    com_doi: 289,
    n_periodicos: 204,
    /* Série oficial/ATD 2021–2024 — recorte diferente, registrada por
       divergir da série Lattes acima. Não é substituível uma pela outra. */
    serie_oficial_2021_2024: {
      fonte: 'CONSOL', ref: '02_dados_capitulo_10/serie_anual_artigos_discentes.csv', status: 'PRELIMINAR',
      unicos: { 2021: 99, 2022: 49, 2023: 55, 2024: 50 }, total: 253,
      nota: 'Contagem oficial do quadriênio (coleta/ATD). Difere da série Lattes principalmente em 2021 (99 contra 62). A conciliação das duas séries é pendência da Comissão de Produção.'
    },
    aviso_2026: 'O ano de 2026 está em curso — a coleta cobre até agosto de 2026.',
    /* Qualis CAPES segue indisponível — é classificação distinta do Scopus. */
    qualis: {
      status: 'PARCIAL',
      fonte: 'CONSOL', ref: '04_auditoria_dpide2/serie_anual_dpide2.csv',
      nota: 'A classificação Qualis CAPES não está preenchida nos registros Lattes, e por isso não existe distribuição Qualis do conjunto completo de artigos. Existe, porém, para um subconjunto documentado: os 69 artigos com coautoria de discente ou egresso do quadriênio 2021–2024, classificados na auditoria DPIDE2. É esse subconjunto — e só ele — que o portal publica por estrato.',
      subconjunto: {
        escopo: '69 artigos com coautoria de discente/egresso, quadriênio 2021–2024',
        estratos: { A1: 12, A2: 9, A3: 20, A4: 5, B1: 13, B2: 1, B3: 2, B4: 2, C: 5 },
        por_ano: {
          2021: { total: 21, A1: 4, A2: 2, A3: 5, A4: 3, B1: 3, B2: 0, B3: 0, B4: 2, C: 2 },
          2022: { total: 17, A1: 2, A2: 1, A3: 6, A4: 2, B1: 3, B2: 0, B3: 1, B4: 0, C: 2 },
          2023: { total: 15, A1: 2, A2: 2, A3: 6, A4: 0, B1: 3, B2: 1, B3: 1, B4: 0, C: 0 },
          2024: { total: 16, A1: 4, A2: 4, A3: 3, A4: 0, B1: 4, B2: 0, B3: 0, B4: 0, C: 1 }
        },
        aviso: 'Este recorte NÃO representa o perfil Qualis do Programa: é o subconjunto com coautoria discente do quadriênio, escolhido por ser o único com estrato atribuído e auditado. Extrapolá-lo para o conjunto seria inventar dado.'
      }
    },

    /* Quartil Scopus 2025 dos periódicos — dado disponível e publicável. */
    scopus: {
      fonte: 'CONSOL', ref: '09/05_evidencias_artigos_deduplicados.csv — snapshot Scopus de 10/08/2026', status: 'VALIDADO',
      rotulo: 'Quartil Scopus',
      /* unicos  = por ARTIGO (cada artigo uma vez)
         vinculos = por REGISTRO docente–artigo. Os dois são publicados porque
         os dois circulam; o que não pode é trocar os rótulos. */
      unicos: { Q1: 85, Q2: 47, Q3: 21, Q4: 4, ne: 5, sem_quartil: 146 },
      vinculos: { Q1: 103, Q2: 59, Q3: 27, Q4: 4, ne: 5, sem_quartil: 168 },
      periodicos_com_percentil: 98,
      periodicos_total: 204,
      nota: 'Quartil do periódico na base Scopus, na categoria de maior percentil. 157 dos 308 artigos únicos (51%) estão em periódicos com quartil atribuído; 5 aparecem como NE (não elegível) e 146 sem métrica, concentrados em periódicos nacionais fora da indexação Scopus. Percentuais calculados apenas sobre os artigos com quartil conhecido.',
      cobertura: 'O snapshot Scopus cobre 98 dos 204 periódicos do conjunto. A ausência de métrica não é qualidade zero: significa que o veículo não foi localizado na base, e 106 periódicos seguem sem percentil (ver data/percentis-scopus-manuais.csv).',
      aviso: 'Quartil Scopus NÃO é Qualis CAPES. A comprovação formal de percentil para a proposta APCN segue pendente.'
    },

    /* Periódicos de destaque — Q1 Scopus ordenados por percentil de impacto.
       Critério: quartil Q1 na categoria de maior percentil, ≥1 artigo do
       corpo docente no período. Ordenação decrescente por percentil. */
    periodicos_destaque_q1: {
      fonte: 'MAPA', ref: 'percentil Scopus 2025, categoria de maior percentil', status: 'PRELIMINAR',
      criterio: 'Periódicos em quartil Q1 com pelo menos um artigo do corpo docente entre 2021 e 2026, ordenados pelo percentil Scopus 2025.',
      nota: 'O percentil indica a posição do periódico na sua categoria: percentil 95 significa que o periódico está acima de 95% dos títulos da área. É indicador de impacto do veículo, não do artigo nem do autor.'
    },

    /* Periódicos mais utilizados — perfil de veículos, não ranking de docentes. */
    periodicos_destaque: [
      { cod: 'TMMM',   nome: 'Tecnologia em Metalurgia, Materiais e Mineração', artigos: 22, docentes: 6, pct: null, q: null },
      { cod: 'MatRes', nome: 'Materials Research',                              artigos: 14, docentes: 7, pct: 43, q: 'Q3' },
      { cod: 'JPCC',   nome: 'Journal of Physical Chemistry C',                 artigos: 8,  docentes: 4, pct: 68, q: 'Q2' },
      { cod: 'BJD',    nome: 'Brazilian Journal of Development',                artigos: 8,  docentes: 5, pct: null, q: null },
      { cod: 'Metals', nome: 'Metals',                                          artigos: 7,  docentes: 6, pct: 77, q: 'Q1' },
      { cod: 'SRI',    nome: 'Steel Research International',                    artigos: 7,  docentes: 3, pct: 66, q: 'Q2' },
      { cod: 'JMRTJT', nome: 'Journal of Materials Research and Technology',    artigos: 6,  docentes: 4, pct: 90, q: 'Q1' },
      { cod: 'JAC',    nome: 'Journal of Alloys and Compounds',                 artigos: 5,  docentes: 1, pct: 91, q: 'Q1' },
      { cod: 'LiqCryst', nome: 'Liquid Crystals',                               artigos: 5,  docentes: 3, pct: 56, q: 'Q2' },
      { cod: 'MMAP',   nome: 'Metallography, Microstructure, and Analysis',     artigos: 5,  docentes: 3, pct: 57, q: 'Q2' },
      { cod: 'CerInt', nome: 'Ceramics International',                          artigos: 4,  docentes: 4, pct: 83, q: 'Q1' },
      { cod: 'IJAMT',  nome: 'International Journal of Advanced Manufacturing Technology', artigos: 4, docentes: 3, pct: 80, q: 'Q1' }
    ],
    /* p50 é SOMA POR DOCENTE, não contagem de artigos — rótulo explícito
       porque a versão anterior dizia só "145 acima do P50". */
    p50: {
      valor: 145, unidade: 'registros docente–artigo',
      fonte: 'CONSOL', ref: '09/01_producao_docente.csv — coluna "Artigos P>50", somada nos 24 docentes',
      status: 'VALIDADO',
      nota: 'Soma por docente de artigos em periódico com percentil Scopus maior que 50. Um artigo com três docentes coautores entra três vezes nesta soma.'
    },
    /* O ERRO CORRIGIDO: 202 era a soma por docente, publicada como se fosse
       o número de artigos. São três medidas diferentes, cada uma com escopo
       próprio, e nenhuma substitui a outra. */
    com_discentes: {
      valor: 168, unidade: 'artigos únicos',
      fonte: 'CONSOL', ref: '06_cruzamento_discentes_lattes_2021_2026/resumo_anual_2021_2026.csv',
      status: 'VALIDADO',
      por_ano: { 2021: 35, 2022: 21, 2023: 30, 2024: 27, 2025: 31, 2026: 24 },
      soma_por_docente: 202,
      criterio: 'Coautoria de pessoa confirmada como discente ou egresso da REDEMAT em base institucional, em artigos de 2021 a 2026.',
      criterio_estrito: {
        valor: 96, docentes: 17,
        ref: '09/02_producao_com_discentes_egressos.csv',
        nota: 'Recorte mais exigente: conta o artigo só quando o docente coautor é também o orientador principal daquele discente, comprovado no Lattes e na base institucional. Ser discente do Programa não basta para atribuir a produção ao docente.'
      },
      oficial_2021_2024: {
        valor: 69, base: 253, pct: 27.3,
        ref: '02_dados_capitulo_10/resumo_auditoria_planilhas_lattes.csv',
        nota: 'Recorte oficial do quadriênio: 69 dos 253 artigos únicos (27,3%).'
      },
      aviso: 'A soma por docente (202) não é número de artigos: um artigo com dois docentes coautores e um discente entra duas vezes nessa soma e uma vez no total do Programa.'
    },
    /* Defesas com evidência nominal — divergem do total do painel, e as duas
       ficam declaradas em vez de escolhidas em silêncio. */
    defesas_comprovadas: {
      fonte: 'CONSOL', ref: '09/03a_teses_defendidas.csv e 09/03b_dissertacoes_defendidas.csv', status: 'VALIDADO',
      teses: 34, dissertacoes: 60, total: 94,
      teses_por_ano: { 2021: 1, 2022: 8, 2023: 7, 2024: 9, 2025: 4, 2026: 5 },
      dissertacoes_por_ano: { 2021: 14, 2022: 11, 2023: 10, 2024: 9, 2025: 8, 2026: 8 },
      nota: 'Defesas de 2021 a 2026 com título, discente, orientador e ano identificados no relatório consolidado. O painel APCN registra 48 teses e 118 dissertações no mesmo período — recorte mais amplo, sem a mesma evidência nominal. A conciliação é pendência da Secretaria.',
      divergencia: { painel_teses: 48, painel_dissertacoes: 118 }
    },
    /* Patentes e propriedade intelectual — bloco novo, sem filtro de ano. */
    patentes: {
      fonte: 'CONSOL', ref: '10_relatorio_patentes_lattes_todos_os_anos_20260831', status: 'VALIDADO',
      unicas: 47, declaracoes: 48, destaques_pi: 8, unicas_2021_2024: 6,
      periodo: 'todos os anos declarados nos currículos',
      nota: 'Extraídas do HTML bruto do cache Lattes: o campo de patentes dos JSON consolidados vem vazio. Deduplicadas por número de registro e, quando o número está truncado, por título e ano. A mesma patente em dois currículos conta uma vez.',
      aviso: 'Depósito, concessão e licenciamento constam como escritos no Lattes. A situação atual de cada processo exige validação no INPI/DIRPA e não é afirmada por este portal.',
      /* Destaques: são os 8 itens que o próprio Programa selecionou e descreveu
         na página institucional de patentes — 7 patentes e 1 software. Não são
         "as 8 melhores das 47": são as que têm descrição de aplicação escrita
         pelo Programa. As outras 39 constam no Lattes sem essa descrição. */
      destaques: {
        fonte: 'PATENTES', ref: 'https://redemat.ufop.br/patentes', status: 'VALIDADO',
        nota: 'Seleção descrita pelo Programa na página institucional de patentes. O inventário completo do Lattes tem 47 patentes únicas; estas 8 são as que vêm com descrição de aplicação.',
        itens: [
          { tipo: 'patente', numero: 'BR 10 2016 014846-4', ano: 2016, ano_concessao: 2022,
            situacao: 'Concedida', situacao_cor: 'val',
            titulo: 'Processo de concentração de partículas finas e ultrafinas de materiais contendo óxidos de ferro, por tratamento redutor',
            inventores: 'Fernando Gabriel da Silva Araújo; Jefferson J. Mendes',
            docentes: ['Fernando Gabriel da Silva Araújo'],
            aplicacao: 'Recuperação de ferro em rejeitos de mineração por processamento termoquímico, transformando óxidos em fases de susceptibilidade magnética diferenciada.',
            detalhe: 'Carta patente concedida em janeiro de 2022.' },
          { tipo: 'patente', numero: 'BR 10 2024 005386-9', ano: 2024,
            situacao: 'Pedido em análise', situacao_cor: 'pre',
            titulo: 'Produto composto por biomaterial para reparo ósseo',
            inventores: 'Ana Paula Moreira Barboza e outros — 14 inventores, em colaboração com UFSJ, UFJF e UFMG',
            docentes: ['Ana Paula Moreira Barboza'],
            aplicacao: 'Scaffold poroso com nanotubos funcionalizados para regeneração de tecido ósseo.' },
          { tipo: 'patente', numero: 'BR 10 2021 018255-5 A2', ano: 2021,
            situacao: 'Pedido em análise', situacao_cor: 'pre',
            titulo: 'Biogel com nanopartículas piezoelétricas',
            inventores: 'Rodrigo Ribeiro Resende; Érika Lorena Fonseca Costa de Alvarenga e outros — 9 inventores',
            docentes: [],
            aplicacao: 'Biogel com atividade osteoindutora para reparo ósseo.' },
          { tipo: 'patente', numero: 'BR 10 2018 075042-9', ano: 2018,
            situacao: 'Pedido em análise', situacao_cor: 'pre',
            titulo: 'Processo de preparação de dispositivo flexível para terapia com luz',
            inventores: 'Rodrigo Fernando Bianchi; G. Lacerda',
            docentes: ['Rodrigo Fernando Bianchi'],
            aplicacao: 'Dispositivo vestível para fototerapia de icterícia neonatal.' },
          { tipo: 'patente', numero: 'BR 10 2018 07501', ano: 2018,
            situacao: 'Pedido em análise', situacao_cor: 'pre',
            titulo: 'Processo de preparação de sensor de deformação',
            inventores: 'Rodrigo Fernando Bianchi; L. M. Mapa',
            docentes: ['Rodrigo Fernando Bianchi'],
            aplicacao: 'Sensor de deformação de pele humana com aplicação em tecnologia assistiva e inclusão social.' },
          { tipo: 'patente', numero: 'BR 10 2021 024334-1', ano: 2021,
            situacao: 'Pedido em análise', situacao_cor: 'pre',
            titulo: 'Aparelho e método de filtragem e esterilização por radiação não ionizante',
            inventores: 'B. G. Paiva',
            docentes: [],
            aplicacao: 'Tratamento de água por radiação não ionizante; a tecnologia é comercializada sob a marca Aqualux.' },
          { tipo: 'patente', numero: 'BR 10 2018 00071', ano: 2018,
            situacao: 'Pedido em análise — sob sigilo técnico', situacao_cor: 'nd',
            titulo: 'Processo para a extração de ouro',
            inventores: 'F. D. Mendes; Versiane Albis Leão',
            docentes: ['Versiane Albis Leão'],
            aplicacao: 'Detalhes técnicos não divulgados enquanto o pedido está sob sigilo.' },
          { tipo: 'software', numero: null, ano: null,
            situacao: 'Registro de software', situacao_cor: 'pre',
            titulo: 'Integrated Simulation and Optimization Tool for Short-Term Mining Planning',
            inventores: 'A. G. Martins; Paulo Santos Assis; M. J. F. Souza',
            docentes: ['Paulo Santos Assis'],
            aplicacao: 'Ferramenta que integra modelo de simulação e modelo de otimização para planejamento de curto prazo em mineração.' }
        ]
      }
    },
    atd_quadrienio: { valor: 0.472, fonte: 'PROPOSTA', ref: 'ATD auditado preliminar do quadriênio 2021–2024', status: 'PRELIMINAR' },
    livros_capitulos: { livros: 9, capitulos: 19, fonte: 'LATTES', status: 'PRELIMINAR' }
  },

  /* ------------------------------------------------------------- formação */
  formacao: {
    fonte: 'APCN', ref: 'Orientações concluídas 2021–2026 registradas nos currículos do núcleo', status: 'PRELIMINAR',
    mestrado_concluido: 118,
    doutorado_concluido: 48,
    orientacoes_ativas: 133,
    nota: 'Contagens somam orientações concluídas pelo corpo docente atual no período, incluindo orientações realizadas em outros programas. Números específicos de titulados pela REDEMAT dependem de conferência na Plataforma Sucupira.',
    historico_site: {
      dissertacoes: { valor: 430, fonte: 'SITE', status: 'PRELIMINAR' },
      teses: { valor: 132, fonte: 'SITE', status: 'PRELIMINAR' },
      nota: 'Totais históricos informados no site atual; ainda não conferidos contra a Plataforma Sucupira.'
    }
  },

  /* ------------------------------------------------------ internacional */
  internacionalizacao: {
    fonte: 'LATTES + PROPOSTA', status: 'PRELIMINAR',
    docentes_com_experiencia: { valor: 13, total: 24,
      ref: 'Docentes com estágio pós-doutoral ou experiência internacional formal registrada', status: 'PRELIMINAR' },
    paises: [
      { pais: 'Estados Unidos',  flag: '🇺🇸', vinculos: 18 },
      { pais: 'França',          flag: '🇫🇷', vinculos: 10 },
      { pais: 'Canadá',          flag: '🇨🇦', vinculos: 5 },
      { pais: 'África do Sul',   flag: '🇿🇦', vinculos: 4 },
      { pais: 'Suécia',          flag: '🇸🇪', vinculos: 3 },
      { pais: 'Inglaterra',      flag: '🇬🇧', vinculos: 3 },
      { pais: 'Noruega',         flag: '🇳🇴', vinculos: 2 }
    ],
    paises_nota: 'Vínculos institucionais no exterior extraídos da seção "Atuação Profissional" dos currículos Lattes do corpo docente. Contagem de vínculos, não de acordos formais vigentes.',
    acordos_formais: {
      status: 'EM_DEFINICAO',
      nota: 'O portfólio de acordos internacionais vigentes, com objeto, vigência e resultados, consta como pendência da proposta APCN. Será publicado após consolidação.'
    },
    metas: {
      valor: 'Ampliar mobilidade, cotutela, disciplinas e produção internacional; manter acordos ativos com coautoria e recepção de visitantes.',
      fonte: 'PROPOSTA', ref: 'Quadro de metas — Internacionalizar formação, 2026–2029', status: 'PRELIMINAR'
    }
  },

  /* ------------------------------------------------- mapa geolocalizado */
  mapa_geo: {
    fonte: 'GEO', status: 'PRELIMINAR',
    ref: 'OpenAlex + currículos Lattes, com revisão manual documentada — auditoria de 01/09/2026',
    publicacoes_com_doi: 288,
    publicacoes_resolvidas: 275,
    revisoes_manuais: 17,
    locais: 128,
    paises: 19,
    conexoes: 299,
    sem_openalex: 7,
    nao_vinculadas: 6,
    nota: 'Cada conexão liga um docente da REDEMAT a uma instituição coautora, geolocalizada. Construído a partir dos DOI das publicações de 2021–2026, resolvidos no OpenAlex.',
    auditoria: 'A geolocalização passou por auditoria manual documentada: 17 artigos revisados à mão e uma lista de instituições homônimas corrigidas (por exemplo, Gerdau Ouro Branco confundida com Rio Branco Institute, e a própria REDEMAT confundida com instituição de Portugal). Sete DOI sem registro no OpenAlex foram deixados fora do mapa em vez de receber afiliação inferida.',
    exclusoes: 'Fragmentos de resumo, endereço residencial e URL do Lattes que tinham sido interpretados como instituições foram removidos na auditoria.'
  },

  /* ---------------------------------------------------------- colaboração */
  colaboracao: {
    fonte: 'LATTES', ref: 'Grafo de coautoria ScriptLattes, processamento de 31/08/2026', status: 'PRELIMINAR',
    /* Números conferidos contra grafoDeColaboracoesComPesos.dot da execução de
       31/08/2026. A execução anterior (28/08) indicava 29 arestas; a coleta de
       31/08 fechou em 26. A diferença é de recoleta de currículos, não de
       critério — o número publicado passa a ser o da execução mais recente,
       que é a mesma que alimenta assets/js/grafo-dados.js. */
    interna: {
      nos: 24, arestas: 26, soma_pesos_arestas: 86,   /* soma dos pesos das arestas: NÃO é contagem de produções — uma produção com três membros conta em cada par */
      nucleo: 14, grupos_separados: 5, sem_coautoria_interna: 5,
      nota: 'Rede de coautoria entre os docentes do Programa — evidência de integração prévia do corpo docente. O desenho e os dados por docente ficam em assets/js/grafo-dados.js, gerado por scripts/gerar-grafo.py.',
      execucao_anterior: { arestas: 29, ref: 'ScriptLattes 28/08/2026' }
    },
    externa: { colaboradores: 797, nota: 'Coautores externos distintos identificados nos currículos do corpo docente.' }
  },

  /* ------------------------------------------------------------- projetos */
  projetos: {
    fonte: 'CONSOL', ref: 'REDEMAT_APCN_2026_Panorama_Captacao..._atualizado.xlsx (aba Panorama) e 07/sintese_capitulo_11.csv', status: 'VALIDADO',
    /* Números relidos da planilha ATUALIZADA da entrega consolidada. A versão
       anterior do portal trazia 119 projetos únicos e R$ 29,4 mi de
       coordenação, de uma execução anterior da planilha. Os valores abaixo
       vêm da aba Panorama, com o rótulo que a própria planilha usa —
       "vínculo", "projeto único" e "valor atribuível" são coisas distintas. */
    unicos_recorte: 108,
    vinculos: 129,
    vinculos_recorte: 118,
    vinculos_valor_conhecido: 105,
    compartilhados_entre_docentes: 2,
    conflito_valor_mesmo_id: 0,
    valor_global_dedup: 118205303.36,
    valor_coordenacao: 44381317.50,
    valor_participacao: 134163401.70,
    valor_coord_mais_participacao: 124333690.30,
    valor_atribuivel: 44962488.87,
    coordenacao_recorte: 74,
    participacoes_recorte: 44,
    vinculos_sem_pendencia: 56,
    leitura_valores: 'São quatro medidas diferentes e nenhuma é o "caixa" do Programa. O valor global sem dupla contagem (R$ 118,2 mi) soma cada projeto uma única vez. O valor sob coordenação/liderança (R$ 44,4 mi) é o valor integral dos projetos coordenados ou subcoordenados por docentes. O valor de participação (R$ 134,2 mi) é o valor integral de redes e projetos em que há participação — o mesmo montante pode aparecer para vários docentes, e somá-lo entre eles não tem significado institucional. O valor atribuível (R$ 45,0 mi) é a parcela informada como atribuível, e é indicador provisório.',
    valores_anteriores: { unicos_recorte: 119, unicos_contabilizaveis: 95, valor_coordenacao: 29410319.49, ref: 'execução anterior da planilha de captação' },
    coordenados: 72,
    coordenados_sem_pendencia: 55,
    coordenadores: 23,
    valor_conhecido: 63,
    valor_ausente: 9,
    alcancam_2026: 41,
    valor_alcanca_2026: 18728650.68,
    concentracao_top3_pct: 73.1,
    pendencias: 73,
    fonte_painel: 'PAINEL',
    redes_inct: [
      { nome: 'INCT/CNPq INEO — Instituto Nacional de Eletrônica Orgânica', valor: 14933744, projetos: 1 },
      { nome: 'INCT MIDAS',        valor: 9051308, projetos: 1 },
      { nome: 'INCT Nanocarbono',  valor: 5172933, projetos: 1 },
      { nome: 'Rede Sustentabilidade na Cadeia Produtiva', valor: 2126460, projetos: 1 },
      { nome: 'INCT — MCT/CNPq',   valor: null,    projetos: 1 }
    ],
    por_ies: [
      { nome: 'UFOP', projetos: 60, valor: 27303702 },
      { nome: 'UEMG', projetos: 12, valor: 2106618 }
    ],
    empresas_valor: [
      { nome: 'Vale',            projetos: 2, valor: 7915442 },
      { nome: 'CEMIG',           projetos: 1, valor: 7317668 },
      { nome: 'Gerdau',          projetos: 5, valor: 2471841 },
      { nome: 'Samarco',         projetos: 2, valor: 940324 },
      { nome: 'Vallourec',       projetos: 1, valor: 497334 },
      { nome: 'ArcelorMittal',   projetos: 3, valor: 454986 },
      { nome: 'Sapura Navegação',projetos: 2, valor: 226728 }
    ],
    agencias_valor: [
      { nome: 'FAPEMIG',              projetos: 31, valor: 7920767 },
      { nome: 'UFOP / combinações',   projetos: 7,  valor: 7681438 },
      { nome: 'UEMG / PROPP',         projetos: 4,  valor: 546016 },
      { nome: 'CNPq / combinações',   projetos: 9,  valor: 390600 },
      { nome: 'FINEP',                projetos: 1,  valor: null }
    ],
    nota: 'Valores globais por projeto, sem dupla contagem entre docentes e sem rateio anual. Há 73 pendências documentais ativas (valor, papel ou parcela atribuível), razão pela qual o indicador é PRELIMINAR. Valores individuais por docente não são publicados.',
    por_ano_inicio: { 2021: 10, 2022: 18, 2023: 23, 2024: 13, 2025: 18, 2026: 12 },
    financiadores: [
      { nome: 'FAPEMIG',           projetos: 41, tipo: 'agencia' },
      { nome: 'CNPq',              projetos: 18, tipo: 'agencia' },
      { nome: 'FINEP',             projetos: 3,  tipo: 'agencia' },
      { nome: 'Embrapii',          projetos: 3,  tipo: 'agencia' },
      { nome: 'Vale',              projetos: 4,  tipo: 'empresa' },
      { nome: 'Gerdau Açominas',   projetos: 2,  tipo: 'empresa' },
      { nome: 'Sapura Navegação',  projetos: 2,  tipo: 'empresa' },
      { nome: 'ArcelorMittal',     projetos: 1,  tipo: 'empresa' },
      { nome: 'CETENE/MCTI',       projetos: 1,  tipo: 'agencia' },
      { nome: 'UFOP',              projetos: 3,  tipo: 'institucional' },
      { nome: 'UEMG',              projetos: 1,  tipo: 'institucional' },
      { nome: 'Fundação Gorceix',  projetos: 6,  tipo: 'institucional' }
    ],
    financiadores_nota: 'Contagens agregam variações de grafia da mesma instituição na planilha de origem.'
  },

  /* ------------------------------------------------------------- parceiros
     `logo` aponta para assets/img/parceiros/<slug>.png. Se o arquivo não
     existir, o cartão renderiza o nome da instituição (fallback onerror).
     Os arquivos NÃO são incluídos no projeto: marcas registradas exigem
     autorização de uso. Ver README, seção "Logos de parceiros".
  ------------------------------------------------------------------------ */
  parceiros: {
    fonte: 'PROPOSTA + PAINEL', ref: 'seção 4.4 da proposta APCN; painel de projetos', status: 'PRELIMINAR',
    nota: 'Relação de cooperação histórica e de financiadores identificados nos projetos do período. O portfólio de instrumentos vigentes, com objeto, vigência e resultados, consta como pendência e será publicado após consolidação.',
    itens: [
      { nome: 'Vale',              slug: 'vale',          tipo: 'Empresa',       projetos: 2, comProjeto: true },
      { nome: 'CEMIG',             slug: 'cemig',         tipo: 'Empresa',       projetos: 1, comProjeto: true },
      { nome: 'Gerdau',            slug: 'gerdau',        tipo: 'Empresa',       projetos: 5, comProjeto: true },
      { nome: 'Samarco',           slug: 'samarco',       tipo: 'Empresa',       projetos: 2, comProjeto: true },
      { nome: 'ArcelorMittal',     slug: 'arcelormittal', tipo: 'Empresa',       projetos: 3, comProjeto: true },
      { nome: 'Vallourec',         slug: 'vallourec',     tipo: 'Empresa',       projetos: 1, comProjeto: true },
      { nome: 'Sapura Navegação',  slug: 'sapura',        tipo: 'Empresa',       projetos: 2, comProjeto: true },
      { nome: 'CBMM',              slug: 'cbmm',          tipo: 'Empresa',       projetos: null, comProjeto: false },
      { nome: 'Usiminas',          slug: 'usiminas',      tipo: 'Empresa',       projetos: null, comProjeto: false },
      { nome: 'Aperam',            slug: 'aperam',        tipo: 'Empresa',       projetos: null, comProjeto: false },
      { nome: 'Nexa',              slug: 'nexa',          tipo: 'Empresa',       projetos: null, comProjeto: false },
      { nome: 'Fundação Gorceix',  slug: 'gorceix',       tipo: 'Institucional', projetos: null, comProjeto: false },
      { nome: 'Embrapii',          slug: 'embrapii',      tipo: 'Institucional', projetos: 3, comProjeto: true },
      { nome: 'FAPEMIG',           slug: 'fapemig',       tipo: 'Fomento',       projetos: 31, comProjeto: true },
      { nome: 'CNPq',              slug: 'cnpq',          tipo: 'Fomento',       projetos: 9,  comProjeto: true },
      { nome: 'FINEP',             slug: 'finep',         tipo: 'Fomento',       projetos: 1,  comProjeto: true },
      { nome: 'CAPES',             slug: 'capes',         tipo: 'Fomento',       projetos: null, comProjeto: false }
    ],
    aviso_marca: 'Os logos das instituições parceiras são marcas registradas de seus titulares. O uso no portal requer autorização prévia de cada instituição. Enquanto não obtida, o portal exibe apenas o nome.'
  },

  /* -------------------------------------------------- alcance e nucleação */
  alcance: {
    fonte: 'PROPOSTA', ref: 'seções 4.3 — justificativa', status: 'PRELIMINAR',
    regioes: ['Carajás', 'São Luís', 'Marabá', 'Vitória', 'Ipatinga', 'Araxá'],
    nucleacao: [
      { instituicao: 'IFMG', detalhe: 'Campi de Ouro Preto, Ouro Branco, Congonhas e Juiz de Fora. Em Ouro Preto, a REDEMAT impulsionou a estruturação do núcleo de materiais, formando mais de 20 professores da área de metalurgia.' },
      { instituicao: 'CEFET-MG', detalhe: 'Unidades de Araxá e Belo Horizonte.' },
      { instituicao: 'UNIFEI', detalhe: 'Campus de Itabira.' },
      { instituicao: 'UFSJ', detalhe: 'Qualificação de quadros docentes.' },
      { instituicao: 'Unileste', detalhe: 'Qualificação de quadros docentes.' }
    ]
  },

  /* --------------------------------------------------- estrutura curricular */
  curriculo: {
    fonte: 'CURRIC', ref: 'Proposta de estrutura curricular', status: 'EM_DEFINICAO',
    nota: 'Estrutura em discussão no Colegiado. Todas as disciplinas constam como "validar e aprovar no Colegiado" — não representam oferta vigente.',
    creditos: {
      mestrado:  { nucleo: 8, linha: 10, total: 18 },
      doutorado: { nucleo: 8, linha: 22, total: 30 }
    },
    equivalencia: '15 horas-aula equivalem a 1 crédito (Resolução CEPE 8039 da UFOP).',
    totais: { nucleo_comum: 10, especificas: 29, total: 39 },
    nucleo_comum: [
      { nome: 'Fundamentos de Ciência e Engenharia de Materiais', ch: '60h' },
      { nome: 'Caracterização de Materiais e Técnicas Instrumentais', ch: '60h' },
      { nome: 'Métodos Estatísticos e Planejamento Experimental', ch: '30h' },
      { nome: 'Metodologia da Pesquisa Científica', ch: '45h' },
      { nome: 'Seminários em Ciência e Engenharia de Materiais', ch: '30h' },
      { nome: 'Fundamentos em Inovação Tecnológica — Patentes', ch: '60h' },
      { nome: 'Fundamentos em Inovação Tecnológica — Gestão, Tecnologias e Mercado', ch: '30h' },
      { nome: 'Tópicos Avançados em Ciência e Engenharia de Materiais I', ch: '30h' },
      { nome: 'Tópicos Avançados em Ciência e Engenharia de Materiais II', ch: '45h' },
      { nome: 'Tópicos Avançados em Ciência e Engenharia de Materiais III', ch: '60h' }
    ],
    especificas: {
      l11: ['Processamento e Transformação de Materiais', 'Processos Metalúrgicos e Tecnologias de Fabricação',
            'Tratamentos Térmicos de Metais', 'Fundamentos de Tecnologia e Metalurgia da Soldagem',
            'Engenharia de Superfícies e Revestimentos', 'Tribologia e Desgaste', 'Corrosão e Proteção de Materiais',
            'Tecnologia dos Materiais Cerâmicos e Vítreos', 'Tecnologia dos Materiais Poliméricos e Compósitos',
            'Innovative Biomass Utilization in Iron and Steelmaking', 'Injeção de Materiais Pulverizados em Altos-Fornos'],
      l12: ['Transformações de Fase e Evolução Microestrutural em Aços', 'Comportamento Mecânico dos Materiais',
            'Fadiga, Fratura e Mecânica da Fratura', 'Modelagem e Simulação Computacional de Materiais',
            'Estrutura Eletrônica e Métodos Quânticos em Materiais', 'Modelagem Atomística e Mesoscópica de Materiais',
            'Métodos Numéricos Aplicados à Engenharia de Materiais', 'Inteligência Artificial e Ciência de Dados em Materiais'],
      l21: ['Recursos Minerais Estratégicos e Críticos', 'Hidrometalurgia e Eletrometalurgia', 'Pirometalurgia',
            'Mineração Urbana', 'Economia Circular Aplicada aos Materiais'],
      l22: ['Biomateriais e Aplicações em Saúde', 'Introdução à Nanociência e Nanotecnologia',
            'Materiais para Conversão e Armazenamento de Energia', 'Materiais Inteligentes e Multifuncionais',
            'Projeto e Desenvolvimento de Novos Materiais', 'Materiais Têxteis']
    }
  },

  /* ------------------------------------------------------------- doutorado
     CORREÇÃO v3.0 — a versão anterior tratava o Doutorado como inexistente.
     O curso ESTÁ EM FUNCIONAMENTO (site oficial + 63 doutorandos matriculados).
     A proposta APCN 2026 é um item separado, registrado em `apcn`.
  ------------------------------------------------------------------------ */
  doutorado: {
    fonte: 'SITE', ref: 'https://redemat.ufop.br/doutorado', status: 'VALIDADO',
    ativo: true,
    nome: 'Doutorado em Engenharia de Materiais',
    nome_en: 'Doctoral Program in Materials Engineering',
    duracao: '8 semestres',
    periodicidade: 'Seleção anual única',
    publico: 'Mestres em engenharia, física, química, entre outras áreas afins',
    exigencia_producao: '2 artigos publicados ou submetidos',
    creditos: {
      obrigatorias: 9, eletivas: 21, estagio_docencia: 4, qualificacao: 1, defesa: 3, total: 34,
      nota_estagio: 'Estágio de docência obrigatório para bolsistas.'
    },
    bolsa: {
      valor_mensal: 2200, duracao_max_meses: 48,
      agencias: ['CNPq', 'CAPES', 'FAPEMIG', 'UFOP'],
      status: 'PRELIMINAR',
      nota: 'Valor informado no site do Programa. Valores de bolsa são definidos pelas agências e mudam periodicamente — confirme nas tabelas oficiais.'
    },
    matriculados: { valor: 63, fonte: 'PESSOAS', status: 'PRELIMINAR' }
  },

  /* ---------------------------------------------------- proposta APCN 2026 */
  apcn: {
    fonte: 'PROPOSTA', status: 'EM_DEFINICAO',
    titulo: 'Proposta de criação de curso de Doutorado em forma associativa UFOP-UEMG (APCN/CAPES 2026)',
    aviso: 'Documento de trabalho da Comissão APCN, versão 0.1 de 31/07/2026. NÃO se refere ao Doutorado atualmente em funcionamento, que segue com oferta e seleção regulares.',
    vagas_previstas: { valor: 10, ref: 'por seleção semestral — decisão colegiada após simulação de capacidade', status: 'EM_DEFINICAO' },
    creditos_previstos: 30,
    nucleo_previsto: { valor: '12 a 13 docentes habilitados', status: 'EM_DEFINICAO' },
    pendencias_criticas: [
      'Declarações oficiais de comprometimento da Reitoria/Pró-Reitoria da UFOP e da UEMG.',
      'Instrumento jurídico atualizado da associação UFOP-UEMG, com governança acadêmica e administrativa.',
      'Validação final do núcleo de 12 a 13 docentes habilitados à orientação de Doutorado.',
      'Comprovação dos percentis Scopus/Web of Science das produções destacadas e de pelo menos 60% do núcleo.',
      'Matriz completa área-linha-projeto-docente-disciplina-infraestrutura-produto/impacto.',
      'Política formal de autoavaliação, relatório de 2025, plano de ação e evidências de implementação.',
      'Resposta consolidada aos apontamentos da Avaliação Quadrienal 2021-2024.'
    ],
    perfil_comparado: [
      { dim: 'Objetivo formativo',  ms: 'Aprofundar conhecimento e aplicar metodologia científica.',    dr: 'Produzir conhecimento no estado da arte com autonomia e liderança.' },
      { dim: 'Complexidade',        ms: 'Problema delimitado, sob orientação próxima.',                 dr: 'Problema original e complexo, com desenho independente.' },
      { dim: 'Metodologia',         ms: 'Domínio e aplicação de métodos.',                              dr: 'Seleção, integração, desenvolvimento e crítica de métodos.' },
      { dim: 'Produção',            ms: 'Produto científico/tecnológico compatível com a dissertação.',  dr: 'Produção qualificada e/ou produto avançado vinculado à tese.' },
      { dim: 'Liderança',           ms: 'Participação em grupos e projetos.',                           dr: 'Coordenação de atividades, formação de estudantes e articulação de redes.' },
      { dim: 'Internacionalização', ms: 'Desejável.',                                                   dr: 'Fortemente incentivada e integrada ao projeto.' }
    ]
  },

  /* ------------------------------------------------------------- mestrado */
  mestrado: {
    fonte: 'SITE + CURRIC', status: 'PRELIMINAR',
    nome: 'Mestrado em Engenharia de Materiais',
    duracao: '4 semestres',
    creditos: 18,
    bolsa_capes: { valor: 1500, ref: 'valor mensal de referência CAPES informado no site atual', status: 'PRELIMINAR' },
    nota_bolsa: 'A disponibilidade de bolsas depende da cota anual do Programa e não é garantida a todos os aprovados.'
  },

  /* ----------------------------------------------------- processo seletivo */
  processo_seletivo: {
    fonte: 'SITE', status: 'PRELIMINAR',
    semestre: '2026/2',
    situacao: 'encerrado',
    nota: 'O edital 2026/2 foi encerrado. Vagas, cronograma e requisitos do próximo processo serão publicados pela secretaria. Requisitos e documentos específicos são definidos em cada edital.',
    etapas: [
      { titulo: 'Inscrição', desc: 'Envio de documentação conforme edital: histórico, currículo Lattes, proposta ou projeto de pesquisa e documentos de identificação.' },
      { titulo: 'Análise de currículo e proposta', desc: 'Avaliação do histórico acadêmico e da aderência da proposta às linhas de pesquisa do Programa pela banca examinadora.' },
      { titulo: 'Entrevista', desc: 'Entrevista com banca de docentes, presencial ou remota, sobre formação, interesse de pesquisa e aderência à linha pretendida.' },
      { titulo: 'Resultado e matrícula', desc: 'Publicação do resultado no site do Programa e matrícula no semestre de ingresso.' }
    ],
    dica: 'Recomenda-se contato prévio com o(a) docente cuja linha de pesquisa mais se aproxime do seu interesse, antes da inscrição.'
  },

  /* ------------------------------------------- autoavaliação e governança */
  autoavaliacao: {
    fonte: 'PROPOSTA', ref: 'seção 5.8', status: 'PRELIMINAR',
    historico: 'A REDEMAT iniciou processos de autoavaliação em 2018 e reformulou a proposta em 2020. A implementação não foi plenamente consolidada no quadriênio 2021–2024. Em 2025, a Comissão Própria de Avaliação da UFOP disponibilizou resultados por eixos para discentes da pós-graduação.',
    ciclo: [
      'Planejamento da autoavaliação, definição dos indicadores e atualização dos instrumentos.',
      'Coleta de dados com discentes, docentes, egressos, técnicos, gestores e parceiros externos.',
      'Análise das três dimensões: Programa; Formação e Produção Intelectual; Impacto.',
      'Diagnóstico de forças, fragilidades, riscos e causas.',
      'Definição de metas, ações, responsáveis, prazos e evidências.',
      'Discussão na Comissão de Autoavaliação, no Colegiado e na Assembleia Docente.',
      'Divulgação de síntese pública e preservação do relatório completo em repositório institucional.',
      'Monitoramento semestral e realimentação do planejamento estratégico.'
    ],
    governanca_dados: [
      { dim: 'Docentes e vínculos',      resp: 'Secretaria / Coordenação',              per: 'Semestral' },
      { dim: 'Produção e percentis',     resp: 'Docentes / Comissão de Produção',       per: 'Anual' },
      { dim: 'Projetos e financiamentos',resp: 'Docentes / Comissão de Projetos',       per: 'Semestral' },
      { dim: 'Discentes e egressos',     resp: 'Secretaria / Comissão de Egressos',     per: 'Anual' },
      { dim: 'Disciplinas',              resp: 'Secretaria / GT curricular',            per: 'Semestral' },
      { dim: 'Impacto e patentes',       resp: 'Docentes / NIT',                        per: 'Anual' }
    ],
    nota_lgpd: 'Respostas individuais de autoavaliação não são publicadas. Somente sínteses agregadas.'
  },


  /* ------------------------------------------- comunidade (além docentes) */
  comunidade: {
    fonte: 'PESSOAS', status: 'PRELIMINAR',
    discentes: {
      total: 117, doutorado: 63, mestrado: 54,
      ref: 'https://redemat.ufop.br/discentes-0',
      ingresso_faixa: 'Ingressos de 2012 a 2026',
      fomento: ['CAPES', 'FAPEMIG', 'Sem fomento'],
      nota: 'Contagem da página oficial de discentes. O portal publica apenas o agregado — a lista nominal com orientador, e-mail e situação de bolsa permanece na página institucional, cuja publicação é de responsabilidade da secretaria.',
      lgpd: 'Nomes, e-mails e vínculo de bolsa de discentes não são republicados neste portal.'
    },
    posdoc: {
      total: 3,
      ref: 'https://redemat.ufop.br/pós-doutorandos',
      itens: [
        { nome: 'Adarlêne Moreira Silva', supervisor: 'Versiane Albis Leão', grupo: 'Hidrometalurgia',
          email: 'adarlenems@gmail.com', foto: 'adarlene-moreira-silva',
          formacao: 'Doutorado e Mestrado em Engenharia de Materiais pela REDEMAT-UFOP; Graduação em Química com Habilitação em Química Industrial pela UFOP.',
          area: 'Engenharia de Materiais e Metalúrgica com ênfase em Hidrometalurgia — tratamento de efluentes líquidos, com atuação principal na remoção de sulfato e de manganês de água de mina visando o reúso.',
          fonte: 'COORD' },
        { nome: 'Gustavo Henrique Silvestre', supervisor: 'Matheus J. S. Matos', grupo: 'The Nanoscale Physics Group',
          email: 'gustavo.silvestre@ufop.edu.br', foto: 'gustavo-henrique-silvestre',
          area: 'Física da matéria condensada — simulações computacionais de propriedades eletrônicas, ópticas e optoeletrônicas; sistemas bidimensionais, nanomateriais de carbono, DFT e dinâmica molecular.' },
        { nome: 'Leonardo Villegas Lelovsky', supervisor: 'Matheus J. S. Matos', grupo: 'The Nanoscale Physics Group',
          email: 'lvillegas.sk@gmail.com', foto: 'leonardo-villegas-lelovsky',
          area: 'Física da matéria condensada — simulação de propriedades eletrônicas, ópticas e de transporte em sistemas semicondutores nanoestruturados; spintrônica, dispositivos de grafeno, isolantes topológicos e cálculos ab initio.' }
      ]
    },
    tecnicos: {
      total: 1,
      ref: 'https://redemat.ufop.br/técnicos',
      itens: [
        { nome: 'Rodrigo Cesário Lourenço', cargo: 'Secretário da REDEMAT', email: 'rodrigo.lourenco@ufop.edu.br', foto: 'rodrigo-cesario-lourenco' }
      ],
      nota: 'Contato telefônico direto do servidor não é republicado; use o telefone institucional do Programa.'
    },
    acolhimento: {
      titulo: 'Apoio psicológico e assistência estudantil',
      url: 'https://www.prace.ufop.br/assistencia-estudantil/psicologia',
      orgao: 'PRACE — Pró-Reitoria de Assuntos Comunitários e Estudantis da UFOP',
      texto: 'A UFOP oferece atendimento psicológico e programas de assistência estudantil a discentes de pós-graduação. O acesso é gratuito e sigiloso.'
    }
  },

  /* ---------------------------------------------------------------- fotos
     Slot de foto por pessoa. O campo `foto` guarda o slug; o arquivo vai em
     assets/img/pessoas/<slug>.jpg. Sem o arquivo, o cartão exibe as iniciais
     sobre a cor da linha de pesquisa — o layout não muda.
     Docentes usam o slug derivado do nome (ver RC.slugFoto em components.js).
  ------------------------------------------------------------------------ */
  fotos: {
    pasta: 'assets/img/pessoas/',
    formato: 'jpg',
    especificacao: 'Recorte quadrado, 400×400 px no mínimo, enquadramento do rosto e ombros, fundo neutro. JPG com qualidade 80–85.',
    nota: 'Nenhuma foto acompanha este pacote. Cada pessoa precisa autorizar o uso da própria imagem antes da publicação — o portal funciona sem foto e exibe as iniciais.',
    consentimento: 'Recomenda-se registrar a autorização de uso de imagem por escrito, conforme a LGPD, antes de publicar a foto de docentes, pós-doutorandos e técnicos.'
  },

  /* -------------------------------------------------------------- normas */
  normas: {
    fonte: 'NORMAS', ref: 'https://redemat.ufop.br/normas', status: 'VALIDADO',
    nota: 'Estrutura reproduzida da página oficial de normas. Os arquivos PDF permanecem hospedados no site institucional — este portal organiza e aponta para eles, sem duplicar as versões.',
    grupos: [
      { id: 'gerais', titulo: 'Normas gerais', icone: 'doc',
        itens: [
          { nome: 'Regimento Geral da UFOP', desc: 'Documento institucional que estabelece regras de organização e competências na UFOP.' },
          { nome: 'Norma Geral dos Programas de Pós-Graduação da UFOP', desc: 'Regras acadêmicas, prazos e procedimentos da pós-graduação stricto sensu.' },
          { nome: 'Regimento Interno da REDEMAT', desc: 'Estrutura do Programa, órgãos colegiados e rotinas de funcionamento.' }
        ] },
      { id: 'disciplinas', titulo: 'Aproveitamento de disciplinas', icone: 'cap',
        itens: [
          { nome: 'Norma de Aproveitamento de Disciplinas (REDEMAT)', desc: 'Regras para solicitação e análise de equivalência de disciplinas.' }
        ] },
      { id: 'bolsas', titulo: 'Bolsas', icone: 'chart',
        itens: [
          { nome: 'Normas de bolsas da PROPPI', desc: 'Orientação geral sobre bolsas de mestrado, doutorado e pós-doutorado.' },
          { nome: 'Normas de Concessão de Bolsas da REDEMAT', desc: 'Critérios internos e procedimentos de gestão das cotas.' },
          { nome: 'Portaria PROPPI nº 8/2018', desc: 'Distribuição e acompanhamento de bolsas de pós-graduação.' },
          { nome: 'Portaria PROPPI nº 11/2018', desc: 'Inscrição obrigatória na Feira de Pós-Graduação.' },
          { nome: 'Resolução CONPEP nº 192', desc: 'Acumulação de bolsas e composição de comissões.' },
          { nome: 'Resolução CONPEP nº 186', desc: 'Programa Institucional de Bolsas de Mestrado e Doutorado.' }
        ] },
      { id: 'docencia', titulo: 'Estágio de docência', icone: 'people',
        itens: [
          { nome: 'Norma de Estágio de Docência (REDEMAT)', desc: 'Procedimentos, responsabilidades e documentação.' },
          { nome: 'Resolução CEPE 7465', desc: 'Regulamentação institucional do estágio de docência.' },
          { nome: 'Resolução CEPE 8016', desc: 'Alterações na regulamentação anterior.' },
          { nome: 'Modelos de plano de atividades e de relatório', desc: 'Formulários de apoio ao estágio.' }
        ] },
      { id: 'orientacao', titulo: 'Orientação e coorientação', icone: 'people',
        itens: [
          { nome: 'Diretrizes de credenciamento de coorientador (REDEMAT)', desc: 'Critérios para aprovação de coorientação.' },
          { nome: 'Formulário eletrônico de registro', desc: 'Registro de coorientação.' },
          { nome: 'Documento de indicação formal', desc: 'Modelo para indicação pelo orientador.' }
        ] },
      { id: 'proap', titulo: 'Recursos PROAP', icone: 'flask',
        itens: [
          { nome: 'Diretrizes do PROAP (REDEMAT)', desc: 'Regras de uso e prestação de contas.' },
          { nome: 'Norma de Recursos PROAP (2026)', desc: 'Diretrizes consolidadas com detalhamento da distribuição.' },
          { nome: 'Formulários de recibo, solicitação e prestação de contas', desc: 'Documentos operacionais.' }
        ] },
      { id: 'credenciamento', titulo: 'Credenciamento docente', icone: 'check',
        itens: [
          { nome: 'Normas Gerais de Credenciamento de Docentes', desc: 'Critérios e procedimentos de credenciamento, recredenciamento e descredenciamento. Documento em PDF, atualizado em 29/04/2025.' },
          { nome: 'Critérios de Pontuação de Currículo (Anexo I)', desc: 'Sistema de pontos para avaliação de credenciamento.' }
        ] },
      { id: 'qualificacao', titulo: 'Exame de qualificação', icone: 'cap',
        itens: [
          { nome: 'Norma do Exame de Qualificação (REDEMAT)', desc: 'Regras, prazos e documentação exigida.' },
          { nome: 'Resolução CONPEP 57', desc: 'Sessões remotas por videoconferência.' },
          { nome: 'Formulário eletrônico de avaliação', desc: 'Registro da avaliação da banca.' }
        ] },
      { id: 'defesa', titulo: 'Defesa de dissertação e tese', icone: 'cap',
        itens: [
          { nome: 'Norma de Defesa (REDEMAT)', desc: 'Agendamento, banca, documentação e procedimentos.' },
          { nome: 'Guia de Normalização do SISBIN', desc: 'Padrões de formatação de trabalhos acadêmicos.' },
          { nome: 'Resolução CONPEP 57', desc: 'Procedimentos para defesa remota.' }
        ] },
      { id: 'posdefesa', titulo: 'Pós-defesa e diploma', icone: 'doc',
        itens: [
          { nome: 'Orientações de pós-defesa (REDEMAT)', desc: 'Procedimentos de depósito final e etapas seguintes.' },
          { nome: 'Portaria PROPPI nº 8/2024', desc: 'Registro e emissão de diploma pelo sistema MinhaUFOP.' }
        ] }
    ],
    formularios: [
      'Agendamento de evento (qualificação e defesa)',
      'Cadastro de membro externo de banca',
      'Solicitações gerais ao Programa'
    ],
    modelos: [
      'Modelo de capa e folha de rosto de dissertação e tese'
    ]
  },

  /* ---------------------------------------------------------------- atas */
  atas: {
    fonte: 'ATAS', ref: 'https://redemat.ufop.br/atas-das-reuniões-do-colegiado', status: 'VALIDADO',
    nota: 'Atas aprovadas das reuniões do Colegiado, hospedadas no site institucional. As decisões do Colegiado são públicas.',
    itens: [
      { ano: 2025, titulo: '1ª Reunião Extraordinária de 2025', data: null,
        url: 'https://redemat.ufop.br/sites/default/files/redemat/files/ata_da_1a_reuniao_extraordinaria_de_2025.docx' },
      { ano: 2024, titulo: '5ª Reunião Extraordinária de 2024', data: null,
        url: 'https://redemat.ufop.br/sites/default/files/redemat/files/ata_da_5a_reuniao_extraordinaria_de_2024.docx' },
      { ano: 2024, titulo: '4ª Reunião Extraordinária de 2024', data: null,
        url: 'https://redemat.ufop.br/sites/default/files/redemat/files/ata_da_4a_reuniao_extraordinaria_de_2024.docx' },
      { ano: 2024, titulo: '3ª Reunião Extraordinária de 2024', data: null,
        url: 'https://redemat.ufop.br/sites/default/files/redemat/files/ata_da_3a_reuniao_extraordinaria_de_2024.pdf' },
      { ano: 2024, titulo: '2ª Reunião Extraordinária de 2024', data: '2024-03-27',
        url: 'https://redemat.ufop.br/sites/default/files/redemat/files/ata_redemat_2a_reuniao_extraordinaria_2024_03_27_versao_final_aprovada_assinado.pdf' },
      { ano: 2024, titulo: '1ª Reunião de 2024 — eleição de coordenadores', data: null,
        url: 'https://redemat.ufop.br/sites/default/files/redemat/files/ata_da_1a_reuniao_ordinaria_de_2024_-_eleicao_coordenadores_redemat_aprovada.pdf' }
    ]
  },

  /* ----------------------------------------------------- notícias e mural
     Estrutura pronta para publicação editorial. Nenhum item fictício:
     a lista nasce vazia e a secretaria a alimenta. As categorias e o
     layout já funcionam com zero itens (estado vazio explicativo).
  ------------------------------------------------------------------------ */
  /* ------------------------------------------- prêmios e reconhecimentos */
  premios: {
    fonte: 'SL2010', ref: 'ScriptLattes — Pm-0 "Total de prêmios e títulos", processamento de 28/08/2026', status: 'VALIDADO',
    total_lattes: 10,
    publicados: 9,
    por_ano: { 2021: 1, 2022: 2, 2024: 3, 2025: 2, 2026: 2 },
    nota: 'Prêmios e títulos declarados nos currículos Lattes do corpo docente. O docente é identificado pelo índice de membro do relatório ScriptLattes, casado com a listagem de membros.',
    exclusao: 'O relatório do ScriptLattes registra dez prêmios no período; nove aparecem aqui. O décimo consta de currículo fora do conjunto de 24 docentes adotado nesta versão do portal.',
    /* Cada item foi mapeado do campo membros_ids do ScriptLattes para o nome
       do docente pelo índice em membros.html. Índice 9 = docente excluído. */
    itens: [
      { ano: 2026, docente: 'Marcelo Gomes Speziali', idx: 15,
        titulo: 'Menção Honrosa — XII Encontro Nacional de Propriedade Intelectual',
        detalhe: 'Pelo trabalho "Análise das transferências de tecnologia de NITs consolidados para a criação de um modelo de matchmaking de parceiros".',
        instituicao: 'XII Encontro Nacional de Propriedade Intelectual', tipo: 'trabalho' },
      { ano: 2025, docente: 'Geraldo Lúcio de Faria', idx: 8,
        titulo: 'Patrono da Turma de Formandos de Engenharia Metalúrgica',
        detalhe: 'Escolha da turma de formandos.',
        instituicao: 'UFOP', tipo: 'homenagem' },
      { ano: 2025, docente: 'Johne Jesus Mol Peixoto', idx: 13,
        titulo: 'Prêmio RHI Magnesita "Antonio Mourão Guimarães" — Refratários',
        detalhe: 'Reconhecimento técnico-temático na área de refratários.',
        instituicao: 'ABM — Associação Brasileira de Metalurgia, Materiais e Mineração', tipo: 'premio' },
      { ano: 2024, docente: 'Heloisa Nazaré dos Santos', idx: 10,
        titulo: 'Medalha Santos Dumont — Grau Ouro',
        detalhe: 'Condecoração militar-civil concedida pela Força Aérea Brasileira.',
        instituicao: 'Ministério da Defesa — Força Aérea Brasileira', tipo: 'medalha' },
      { ano: 2024, docente: 'Paulo Santos Assis', idx: 17,
        titulo: 'Plenary Session — Asia Conference, Changsha (Hunan, China)',
        detalhe: 'Convite para sessão plenária.',
        instituicao: 'Chinese Society of Metals', tipo: 'palestra' },
      { ano: 2024, docente: 'Dalila Chaves Sicupira', idx: 5,
        titulo: 'Prêmio Waelzholz Brasmetal Laminação',
        detalhe: null,
        instituicao: 'ABM — Associação Brasileira de Metalurgia, Materiais e Mineração', tipo: 'premio' },
      { ano: 2022, docente: 'Rodrigo Fernando Bianchi', idx: 19,
        titulo: 'Garrafa com dispositivo fotoelétrico para tornar a água adequada para consumo humano',
        detalhe: 'Reconhecimento de tecnologia de impacto social.',
        instituicao: 'Razões para Acreditar', tipo: 'produto' },
      { ano: 2022, docente: 'Eliane Ayres', idx: 6,
        titulo: 'Prêmio Patente do Ano — inovação para o bem-estar do ser humano',
        detalhe: null,
        instituicao: 'ABPI — Associação Brasileira da Propriedade Intelectual', tipo: 'premio' },
      { ano: 2021, docente: 'Ive Silvestre de Almeida', idx: 12,
        titulo: 'Melhor trabalho na área de Ciências Exatas e da Terra',
        detalhe: 'VI Mostra dos Programas de Pós-Graduação.',
        instituicao: 'Encontro de Saberes 2021 — UFOP', tipo: 'trabalho' }
    ],
    discentes: {
      nota: 'Prêmios de discentes não vêm dos currículos do corpo docente. Os que o portal publica vêm do mural de notícias do Programa e são cadastrados caso a caso.',
      itens: [
        { ano: 2026, nome: 'Igor Ferreira Curvelo', nivel: 'discente',
          titulo: 'Menção Honrosa no Prêmio de Melhor Pôster — Física de Materiais',
          instituicao: 'Encontro de Outono da Sociedade Brasileira de Física (EOSBF 2026)',
          trabalho: 'Modulation of the Valley Zeeman Effect by Pressure and Defects in Vanadium-Doped Tungsten Dichalcogenides',
          fonte: 'NEWS', ref: 'https://redemat.ufop.br/news/professor-da-redemat-e-estudante-recebem-destaque-no-eosbf-2026' }
      ]
    }
  },

  /* --------------------------- oportunidades para estudantes e egressos */
  oportunidades: {
    fonte: 'SL2010', ref: 'ScriptLattes — blocos de orientações e projetos, processamento de 28/08/2026, recorte 2021–2026', status: 'VALIDADO',
    nota: 'Estes números são o histórico do que o corpo docente de fato orientou e coordenou. Não são vagas abertas: mostram o tamanho e a variedade da porta de entrada. As vagas efetivas saem nos editais e no contato direto com cada orientador.',
    /* Concluídas e em andamento vêm de blocos SEPARADOS do ScriptLattes
       (OC* e OA*). Somar os dois daria dupla contagem de nada — são
       populações distintas — mas publicá-los juntos, sem rótulo, confundiria. */
    orientacoes: [
      { tipo: 'Iniciação científica', concluidas: 150, andamento: 24, publico: 'graduação',
        ref: 'OC5-0 e OA5-0', destaque: true,
        nota: 'A maior porta de entrada do Programa: 150 iniciações científicas concluídas em seis anos.' },
      { tipo: 'Trabalho de conclusão de curso', concluidas: 97, andamento: 6, publico: 'graduação',
        ref: 'OC4-0 e OA4-0', destaque: true },
      { tipo: 'Dissertação de mestrado', concluidas: 125, andamento: 57, publico: 'mestrado',
        ref: 'OC2-0 e OA2-0', destaque: true },
      { tipo: 'Tese de doutorado', concluidas: 52, andamento: 79, publico: 'doutorado',
        ref: 'OC1-0 e OA1-0', destaque: true },
      { tipo: 'Supervisão de pós-doutorado', concluidas: 11, andamento: 3, publico: 'pós-doutorado',
        ref: 'OC0-0 e OA0-0' },
      { tipo: 'Monografia de especialização', concluidas: 5, andamento: 0, publico: 'especialização',
        ref: 'OC3-0' },
      { tipo: 'Orientações de outra natureza', concluidas: 31, andamento: 6, publico: 'diversos',
        ref: 'OC6-0 e OA6-0' }
    ],
    totais: { concluidas: 471, andamento: 175,
      nota: 'Totais do ScriptLattes para todos os tipos de orientação, 2021–2026. Incluem os tipos listados acima.' },
    ic_por_ano: { 2021: 24, 2022: 43, 2023: 28, 2024: 24, 2025: 20, 2026: 11 },
    tcc_por_ano: { 2021: 23, 2022: 25, 2023: 16, 2024: 12, 2025: 17, 2026: 4 },
    /* Agências que financiaram as 150 ICs — é a resposta concreta a
       "que bolsa eu posso pleitear". */
    bolsas_ic: {
      ref: 'OC5-0 — campo "Agência de Fomento" das 150 iniciações científicas concluídas',
      itens: [
        { agencia: 'CNPq', sigla: 'CNPq', n: 48 },
        { agencia: 'FAPEMIG', sigla: 'FAPEMIG', n: 24 },
        { agencia: 'UFOP — PROPP, PIP e programas institucionais', sigla: 'UFOP', n: 14 },
        { agencia: 'UEMG — PAEx e apoio a projetos de extensão', sigla: 'UEMG', n: 4 },
        { agencia: 'UFMG', sigla: 'UFMG', n: 2 },
        { agencia: 'ArcelorMittal', sigla: 'Empresa', n: 1 }
      ],
      sem_agencia: 53,
      nota: 'Em 53 das 150 iniciações o currículo não declara agência — pode ser projeto voluntário ou registro incompleto, e o portal não infere qual.'
    },
    /* Cursos de graduação de onde vieram os orientandos de IC: mostra que a
       porta é multidisciplinar de fato, não de discurso. */
    cursos_ic: [
      { curso: 'Física', n: 36 }, { curso: 'Química Industrial', n: 26 },
      { curso: 'Engenharia Metalúrgica', n: 26 }, { curso: 'Engenharia Civil', n: 20 },
      { curso: 'Design de Produto', n: 8 }, { curso: 'Design de Moda', n: 5 },
      { curso: 'Engenharia de Controle e Automação', n: 4 },
      { curso: 'Engenharia Mecânica', n: 3 }, { curso: 'Farmácia', n: 3 },
      { curso: 'Engenharia de Minas', n: 2 }
    ],
    projetos_pesquisa: { valor: 97, ref: 'Pj-0 — projetos de pesquisa declarados nos currículos, 2021–2026',
      por_ano: { 2021: 17, 2022: 24, 2023: 26, 2024: 14, 2025: 12, 2026: 4 },
      nota: 'Projetos de pesquisa declarados nos currículos. É outra contagem que a do painel de captação (108 projetos únicos no recorte), porque a fonte e o critério são diferentes: aqui é o que cada docente declarou no Lattes.' },
    eventos: { participacao: 53, organizacao: 99, ref: 'Ep-0 e Eo-0' },
    como_participar: [
      { publico: 'Graduação', titulo: 'Iniciação científica e TCC',
        texto: 'Procure diretamente o docente cuja linha te interessa — a lista com e-mail está em Pessoas, e o mapa de publicações mostra em que cada um publica. Editais de bolsa de IC saem pela PROPP/UFOP, pela UEMG, pelo CNPq (PIBIC) e pela FAPEMIG.',
        acao: 'pessoas.html' },
      { publico: 'Mestrado e doutorado', titulo: 'Processo seletivo',
        texto: 'A entrada é por edital, com seleção anual para o doutorado e conforme edital para o mestrado. A escolha de orientador faz parte da inscrição: leia as linhas de pesquisa antes.',
        acao: 'processo-seletivo.html' },
      { publico: 'Pós-doutorado', titulo: 'Estágio pós-doutoral',
        texto: 'Depende de supervisor e de fonte de financiamento (bolsa de agência, projeto ou vínculo próprio). O contato é direto com o docente supervisor pretendido.',
        acao: 'pessoas.html' },
      { publico: 'Todos', titulo: 'Laboratórios e infraestrutura',
        texto: 'Antes de escolher orientação, veja em que laboratório o trabalho vai acontecer e com que equipamento. A relação está na página de laboratórios.',
        acao: 'laboratorios.html' }
    ]
  },

  /* ------------------------------------------------------- laboratórios */
  laboratorios: {
    fonte: 'LABS', ref: 'https://redemat.ufop.br/laboratorios', status: 'VALIDADO',
    total: 15,
    nota: 'Infraestrutura de pesquisa associada aos docentes do Programa. Onde o responsável não consta na página institucional, o campo fica vazio em vez de ser inferido.',

    /* Foto de abertura da página. Proveniência de imagem segue a mesma regra
       dos dados: fonte declarada, e nada publicado sem base.

       `autorizacao` é o campo que decide se a figura vai ao ar. 'PENDENTE'
       significa que temos a fonte mas NÃO temos permissão escrita — o rodapé
       do site de origem reserva todos os direitos. A página exibe a figura
       durante o desenvolvimento e imprime o estado; antes da substituição no
       domínio (Fase 4), este campo tem de estar em 'OK' ou a foto sai. */
    foto: {
      arquivo: 'campus-ufop-aereo',
      formatos: ['webp', 'jpg'],
      legenda: 'Vista aérea do campus da UFOP, com parte dos prédios da Escola de Minas.',
      alt: 'Vista aérea do campus da UFOP: blocos de pavilhões de sala de aula e ' +
           'laboratórios em telhado claro, com pátio interno arborizado, vias de ' +
           'acesso e mata ao redor.',
      credito: 'Fundação Gorceix',
      fonte: 'GORCEIX', ref: 'https://site.gorceix.org.br/apoio-a-em-ufop',
      coleta: '2026-09-03',
      autorizacao: 'PENDENTE',
      autorizacao_nota: 'Imagem obtida da página "Apoio à EM-UFOP" da Fundação Gorceix, ' +
        'sem crédito de fotógrafo na origem e sob rodapé de direitos reservados. ' +
        'Atribuir a fonte não substitui permissão: é necessária autorização escrita ' +
        'da Fundação Gorceix — ou substituição por imagem do acervo da própria UFOP — ' +
        'antes da publicação no domínio.'
    },
    itens: [
      { nome: 'NANOLAB — Laboratório de Nanociência e Nanotecnologia', sigla: 'NANOLAB',
        vinculo: 'UFOP', coordenador: 'Fernando Gabriel da Silva Araújo', email: 'fgabriel@ufop.edu.br',
        criado: '2024-04-22', local: 'Rua 9, Ouro Preto — MG',
        desc: 'Caracterização microestrutural de materiais, com análises micro e nanoestruturais e mineralógicas.',
        equipamentos: ['Difratômetro de raios X Bruker D2 Phaser', 'Espectrômetro de fluorescência de raios X Shimadzu EDX-720', 'Microtomografia de raios X Bruker SkyScan 1272', 'Microscópio de força atômica Park XE7', 'MEV com EDS Tescan TIMA', 'MEV com EDS e EBSD Tescan VEGA', 'Metalizadora Quorum QT150 ES'],
        tecnicas: ['MEV com EDS e EBSD', 'DRX', 'Fluorescência de raios X', 'Microtomografia', 'AFM'] },
      { nome: 'LPA — Laboratório Multiusuário de Processamento de Amostras (CPCMat/DEFIS)', sigla: 'LPA',
        vinculo: 'UFOP', responsavel: 'Mariana de Castro Prado', email: 'cpcmat@ufop.edu.br',
        telefone: '(31) 3559-1667', criado: '2026-02-03', local: 'Rua Quatro, Ouro Preto — MG',
        desc: 'Laboratório multiusuário de preparação e caracterização de amostras, aberto a ensino, pesquisa e demandas externas.',
        equipamentos: ['Ultrassom de ponta Sonics VCX500', 'Ultrassom de banho Unique USC2850', 'Misturador de alto cisalhamento Silverson L5M-A', 'Milli-Q Academic Qgard 1', 'Destilador Quimis Q-341.24', 'Centrífuga Benfer BMC', 'Microscópio metalográfico invertido Optech BE079'],
        tecnicas: ['Deionização e destilação', 'Ultrassom de ponta e de banho', 'Centrifugação', 'Microscopia óptica', 'Mistura por alto cisalhamento'] },
      { nome: 'CP — Laboratório de Simulação Computacional Multiescala (Grupo NANO)', sigla: 'CP',
        vinculo: 'UFOP', responsavel: 'Matheus Josué de Souza Matos', email: 'matheus.matos@ufop.edu.br',
        desc: 'Simulação de estrutura eletrônica e dinâmica molecular, com capacidade para cálculos de grande porte.',
        equipamentos: ['Cluster Beowulf com cerca de 40 nós heterogêneos (4 a 128 núcleos)', 'Escalonamento OpenPBS sobre CentOS'],
        tecnicas: ['DFT', 'Dinâmica molecular', 'Modelagem atomística'] },
      { nome: 'SPM — Laboratório de Microscopia de Sonda', sigla: 'SPM',
        vinculo: 'UFOP', responsavel: 'Ana Paula Moreira Barboza', email: 'ana.barboza@ufop.edu.br',
        desc: 'Microscopia por sonda para topografia e propriedades locais em materiais e sistemas biológicos.',
        equipamentos: ['AFM/SPM com módulos EFM e SKPM e controle ambiental'],
        tecnicas: ['AFM', 'EFM', 'SKPM'] },
      { nome: 'LED — Laboratório de Eletroquímica e Difusão', sigla: 'LED',
        vinculo: 'UFOP', responsavel: 'Taíse Matte Manhabosco', email: 'taise@ufop.edu.br',
        desc: 'Preparação e caracterização eletroquímica e de difusão em filmes finos e ultrafinos e em cerâmicas.',
        equipamentos: ['Fornos até 1600 °C', 'Autolab com espectroscopia de impedância', 'Evaporadora por feixe de elétrons Edwards', 'Bombas e estufa de vácuo', 'Prensa de 15 t'],
        tecnicas: ['Eletrodeposição', 'Impedância eletroquímica (EIS)', 'Evaporação por feixe de elétrons', 'Difusão e abrasão'] },
      { nome: 'LAMOe — Laboratório de Materiais Optoeletrônicos', sigla: 'LAMOe',
        vinculo: 'UFOP', responsavel: 'Thiago Cazati', email: 'thcazati@ufop.edu.br',
        desc: 'Caracterização óptica e fotofísica de materiais optoeletrônicos.',
        equipamentos: ['Espectrofotômetro Shimadzu UV-1800', 'Espectrofluorímetro Shimadzu RF-5301PC', 'PicoQuant FluoTime 200'],
        tecnicas: ['UV-Vis', 'Fluorescência estacionária', 'Fluorescência resolvida no tempo'] },
      { nome: 'SCNano — Crescimento e Síntese de Nanomateriais', sigla: 'SCNano',
        vinculo: 'UFOP', responsavel: 'Ive Silvestre de Almeida', email: 'ive.almeida@ufop.edu.br',
        desc: 'Crescimento e síntese controlada de nanomateriais, com processos de alta temperatura.',
        equipamentos: ['Fornos de alta temperatura', 'Capelas de exaustão', 'Controladores de fluxo de gases', 'Bombas de vácuo'],
        tecnicas: ['CVD', 'Rotas de síntese de nanomateriais'] },
      { nome: 'LAPPEM — Polímeros e Propriedades Eletrônicas de Materiais', sigla: 'LAPPEM',
        vinculo: 'UFOP', responsavel: 'Rodrigo Fernando Bianchi', email: 'bianchi@ufop.edu.br',
        desc: 'Preparação química e caracterização óptica e elétrica de filmes finos e dispositivos orgânicos.',
        equipamentos: ['Sistemas de deposição de filmes', 'Fontes e medidores elétricos', 'Instrumentação óptica'],
        tecnicas: ['Filmes finos', 'Caracterização óptica e elétrica', 'Testes de dispositivos orgânicos'] },
      { nome: 'Laboratório de Mecânica Granular', sigla: null,
        vinculo: 'UFOP', responsavel: 'Américo Tristão Bernardes', email: 'atb@ufop.edu.br',
        local: 'ICEB I — sala 113',
        desc: 'Laboratório multidisciplinar para experimentos e simulação em mecânica granular.',
        equipamentos: [], tecnicas: ['Experimentos em mecânica granular', 'Simulação computacional'] },
      { nome: 'Laboratório de Mecânica de Fratura', sigla: 'DEMET',
        vinculo: 'UFOP', responsavel: null,
        desc: 'Ensaios mecânicos, metalografia e avaliação eletroquímica aplicados a fratura, fadiga e degradação.',
        equipamentos: ['Máquina servo-hidráulica MTS 10 t', 'Máquina servo-hidráulica INSTRON 25 t', 'Microscópio óptico quantitativo Leica', 'Três microscópios metalográficos', 'Potenciostato/galvanostato', 'Máquina de eletroerosão'],
        tecnicas: ['Ensaios mecânicos', 'Metalografia quantitativa', 'Avaliação eletroquímica'] },
      { nome: 'Laboratório de Engenharia de Superfícies e Técnicas Afins', sigla: 'DEMET',
        vinculo: 'UFOP', responsavel: null,
        desc: 'Tratamento e caracterização de superfícies, com ênfase em processos a laser e ensaios de desgaste e erosão.',
        equipamentos: ['Laser Nd:YAG pulsado (1064 e 532 nm)', 'Máquinas de abrasão e de erosão', 'Cortadora de precisão', 'Lupas binoculares', 'Limpador ultrassônico'],
        tecnicas: ['Processamento a laser', 'Ensaios de desgaste e erosão'] },
      { nome: 'Laboratório de Tratamentos Térmicos e Fundição', sigla: 'DEMET',
        vinculo: 'UFOP', responsavel: null,
        desc: 'Tratamentos térmicos e fundição, com instrumentação para controle de ciclos térmicos e metalografia.',
        equipamentos: ['Dilatômetro até 1350 °C', 'Fornos de indução de 15 kg e 100 kg de aço', 'Quatro fornos mufla (1200 °C)', 'Seis fornos tubulares (1100 °C)', 'Forno de platina (1400 °C)', 'Oito microscópios metalográficos', 'Quatro politrizes'],
        tecnicas: ['Tratamentos térmicos', 'Fundição', 'Dilatometria', 'Metalografia'] },
      { nome: 'Núcleo de Valorização de Materiais e Minerais', sigla: 'DEMET',
        vinculo: 'UFOP', responsavel: null,
        desc: 'Valorização e caracterização de materiais e minérios, com análises químicas e modelagem física de operações metalúrgicas.',
        equipamentos: ['Absorção atômica', 'Adsorção de nitrogênio', 'Análise por via úmida', 'Modelos físicos de alto-forno, lingotamento contínuo e convertedor LD'],
        tecnicas: ['Análise química', 'Modelagem física e dinâmica de reatores metalúrgicos'] },
      { nome: 'Laboratório de Tratamentos Térmicos (DEFIS)', sigla: 'DEFIS',
        vinculo: 'UFOP', responsavel: null,
        desc: 'Tratamentos térmicos com aquisição de dados e suporte a metalografia e análise de microestrutura.',
        equipamentos: ['Forno mufla (1250 °C)', 'Forno tubular (1100 °C)', 'Forno mufla de 1 m³ (1350 °C)', 'Cinco microscópios metalográficos', 'Duas politrizes', 'Sistema de aquisição de imagens'],
        tecnicas: ['Tratamentos térmicos', 'Metalografia', 'Análise de imagem'] },
      { nome: 'Laboratórios de Processamento e Análise de Materiais (DEQUI)', sigla: 'DEQUI',
        vinculo: 'UFOP', responsavel: null,
        desc: 'Síntese e caracterização estrutural e espectroscópica, com ênfase em difração, Mössbauer e análises térmicas.',
        equipamentos: ['Difratômetro Shimadzu XRD-600', 'Espectrômetro Mössbauer', 'Espectrômetros UV-Vis e FTIR Perkin Elmer', 'Análises térmicas TGA, DTA e DSC Shimadzu'],
        tecnicas: ['DRX', 'Espectroscopia Mössbauer', 'UV-Vis e FTIR', 'Análise térmica', 'Síntese de polímeros'] }
    ],
    aviso: 'A relação é a publicada pelo Programa. O inventário formal de laboratórios, com área, capacidade e situação de cada equipamento, segue como pendência declarada para a proposta APCN.'
  },

  mural: {
    status: 'PARCIAL',
    nota: 'Espaço editorial do Programa. Os itens são cadastrados pela secretaria — este portal não gera notícias automaticamente nem publica conteúdo não confirmado.',
    categorias: [
      { id: 'noticia',    rotulo: 'Notícias',            cor: 'var(--navy)',  desc: 'Comunicados e acontecimentos do Programa.' },
      { id: 'artigo',     rotulo: 'Artigos publicados',  cor: 'var(--area2)', desc: 'Divulgação de artigos de docentes e discentes.' },
      { id: 'patente',    rotulo: 'Patentes e produtos', cor: 'var(--l22)',   desc: 'Depósitos, registros e produtos tecnológicos.' },
      { id: 'evento',     rotulo: 'Eventos',             cor: 'var(--area1)', desc: 'Seminários, defesas, congressos e visitas.' },
      { id: 'estudante',  rotulo: 'Trabalhos de estudantes', cor: 'var(--l12)', desc: 'Imagens e resultados de trabalhos discentes.' },
      { id: 'extensao',   rotulo: 'Extensão',            cor: 'var(--l21)',   desc: 'Projetos de extensão e ações com a comunidade.' },
      { id: 'oportunidade', rotulo: 'Oportunidades',     cor: 'var(--amber)', desc: 'Vagas de pesquisa, iniciação científica e pós-doutorado.' },
      { id: 'selecao',    rotulo: 'Processo seletivo',   cor: 'var(--st-div)', desc: 'Editais, prazos e resultados.' }
    ],
    /* Dois itens editoriais, cada um com fonte verificável no campo `fontes`.
       O portal não gera notícia: estes vieram do site institucional e das
       páginas dos veículos citados. */
    itens: [
      {
        categoria: 'artigo',
        data: '2023-06-15',
        titulo: 'Artigo com autoria da REDEMAT na Nature Nanotechnology mede o potencial moiré sob pressão',
        texto: 'Trabalho liderado pelo MIT, com o professor Matheus J. S. Matos (DEFIS/UFOP) entre os autores, mostrou que fônons moiré funcionam como sonda do potencial moiré em uma heteroestrutura de MoS₂/WSe₂ — e que a pressão hidrostática permite sintonizá-lo de forma contínua e reversível. Repercutiu no MIT News e em veículos de divulgação científica.',
        url: 'https://doi.org/10.1038/s41565-023-01413-3',
        imagem: 'assets/img/ilustra/moire.svg',
        imagemAlt: 'Duas redes atômicas triangulares giradas uma em relação à outra, formando um padrão moiré de larga escala.',
        destaque: true,
        exemplo: true,
        detalhe: {
          revista: 'Nature Nanotechnology', volume: '18', paginas: '1147–1153', ano: 2023,
          doi: '10.1038/s41565-023-01413-3',
          titulo_original: 'Pressure tuning of minibands in MoS₂/WSe₂ heterostructures revealed by moiré phonons',
          autor_redemat: 'Matheus J. S. Matos — Departamento de Física, UFOP',
          coautoria: 'MIT (Estados Unidos), UNAM (México), UFMG, UFF e UFOP',
          repercussao: [
            { veiculo: 'MIT News', url: 'https://news.mit.edu/2023/powerful-tool-studying-tuning-atomically-thin-materials-0627', data: '2023-06-27' },
            { veiculo: 'Phys.org', url: 'https://phys.org/news/2023-06-international-team-powerful-tool-tuning.html', data: '2023-06' },
            { veiculo: 'Métricas do artigo (Nature)', url: 'https://www.nature.com/articles/s41565-023-01413-3/metrics' }
          ],
          nota_editorial: 'Item mantido como MODELO de divulgação de artigo: mostra o formato — o que o trabalho fez, quem da REDEMAT participou, onde saiu e onde repercutiu, cada afirmação com link para a fonte.'
        }
      },
      {
        categoria: 'estudante',
        data: '2026-05-26',
        titulo: 'Estudante da REDEMAT recebe Menção Honrosa de melhor pôster no EOSBF 2026',
        texto: 'Igor Ferreira Curvelo recebeu Menção Honrosa no Prêmio de Melhor Pôster na área de Física de Materiais, no Encontro de Outono da Sociedade Brasileira de Física, com o trabalho sobre modulação do efeito Zeeman de vale por pressão e defeitos em dicalcogenetos de tungstênio dopados com vanádio. No mesmo encontro, Fellipe Augusto Santiago da Silva apresentou estudo in silico de grafeno dopado com boro e o professor Matheus J. S. Matos deu palestra convidada na trilha de Nanomateriais.',
        url: 'https://redemat.ufop.br/news/professor-da-redemat-e-estudante-recebem-destaque-no-eosbf-2026',
        imagem: 'assets/img/ilustra/premio.svg',
        imagemAlt: 'Painéis de pôster em sequência, com um deles destacado por uma marca de reconhecimento.',
        destaque: true,
        detalhe: {
          evento: 'Encontro de Outono da Sociedade Brasileira de Física — EOSBF 2026',
          premiado: 'Igor Ferreira Curvelo',
          premio: 'Menção Honrosa — Prêmio de Melhor Pôster, área de Física de Materiais',
          trabalho: 'Modulation of the Valley Zeeman Effect by Pressure and Defects in Vanadium-Doped Tungsten Dichalcogenides',
          demais: [
            { nome: 'Fellipe Augusto Santiago da Silva', trabalho: 'In Silico Study of Electronic and Vibrational Properties of Boron-Doped Graphene via DFT' },
            { nome: 'Matheus Josué de Souza Matos', trabalho: 'Palestra convidada: Theoretical Insights into Electronic Structure and Magnetic Interactions in Layered Quantum Magnets: NiPS₃ and NiI₂' }
          ]
        }
      }
    ]
  },

  /* ------------------------------------------------------ conflitos de dado */
  conflitos: [
    {
      campo: 'Situação do curso de Doutorado',
      resolvido: true,
      fontes: [
        { fonte: 'Site oficial /doutorado', valor: 'Curso ATIVO — 8 semestres, 34 créditos, seleção anual, bolsas de até 48 meses' },
        { fonte: 'Página de discentes', valor: '63 doutorandos matriculados, ingressos de 2012 a 2026' },
        { fonte: 'Site /indicadores', valor: '132 teses defendidas' },
        { fonte: 'Proposta APCN 2026', valor: '"Criação do curso de Doutorado Acadêmico" / "Nova proposta de curso"' }
      ],
      resolucao: 'RESOLVIDO com correção. O Doutorado da REDEMAT ESTÁ EM FUNCIONAMENTO, com oferta e seleção regulares — a versão 2.0 deste portal afirmava o contrário e foi corrigida. A proposta APCN 2026 refere-se à criação de um curso em forma associativa UFOP-UEMG e é tratada em seção própria, sem se confundir com o curso vigente. A relação formal entre os dois (substituição, reformulação ou curso adicional) deve ser esclarecida pela Comissão APCN.'
    },
    {
      campo: 'Valor global de captação de recursos',
      resolvido: false,
      fontes: [
        { fonte: 'Planilha de captação ATUALIZADA (entrega consolidada 29/08/2026)', valor: 'R$ 118.205.303,36 global sem dupla contagem; 108 projetos únicos no recorte; R$ 44.381.317,50 sob coordenação/liderança; R$ 44.962.488,87 atribuível' },
        { fonte: 'Execução anterior da mesma planilha (versão usada até a v4.1 do portal)', valor: 'R$ 118.205.303,36 global; 119 projetos únicos; 95 contabilizáveis; R$ 29.410.319,49 de coordenação' },
        { fonte: 'Planilha deduplicada (aba Projetos únicos), leitura anterior', valor: 'R$ 80.643.902,79 no recorte 2021–2026; 110 projetos' }
      ],
      resolucao: 'PARCIALMENTE RESOLVIDO na v4.2. O valor global sem dupla contagem (R$ 118,2 mi) se confirmou na planilha atualizada. Mudaram o número de projetos únicos (119 para 108) e o valor sob coordenação (R$ 29,4 mi para R$ 44,4 mi): o portal passa a publicar os valores da planilha atualizada, com os rótulos que ela própria usa. A conciliação com a leitura de R$ 80,6 mi segue a cargo da Comissão de Projetos.'
    },
    {
      campo: 'Número de bolsistas de produtividade',
      resolvido: false,
      fontes: [
        { fonte: 'Proposta APCN — tabela de corpo docente', valor: '11 bolsistas CNPq (8 PQ + 3 DT)' },
        { fonte: 'Painel de projetos (cenário PQ/DT)', valor: '10 bolsistas PQ/DT' },
        { fonte: 'Informação da coordenação', valor: 'Antônio Valadão Cardoso é bolsista de produtividade pela UEMG' }
      ],
      resolucao: 'O portal publica 11 bolsistas CNPq (conforme a tabela itemizada da proposta) mais 1 bolsista de produtividade pela UEMG, totalizando 12. A divergência de 10 vs. 11 no painel permanece para conferência.'
    },
    {
      campo: 'Endereço e telefone do Programa',
      resolvido: true,
      fontes: [
        { fonte: 'Páginas de docentes, técnicos e credenciamento', valor: 'Praça Tiradentes, 20 — Centro, Ouro Preto — MG, 35400-084 · (31) 3559-1596' },
        { fonte: 'Versão 2.0 deste portal', valor: 'Campus Morro do Cruzeiro (incorreto)' }
      ],
      resolucao: 'RESOLVIDO. O endereço institucional é Praça Tiradentes, 20, confirmado em três páginas do site oficial. A versão 2.0 informava o Campus Morro do Cruzeiro por inferência e foi corrigida.'
    },
    {
      campo: 'Classificação da produção por estrato',
      resolvido: false,
      fontes: [
        { fonte: 'ScriptLattes (campo Qualis)', valor: 'vazio em 100% dos registros' },
        { fonte: 'Auditoria DPIDE2 (entrega consolidada)', valor: 'estrato Qualis atribuído aos 69 artigos com coautoria discente/egresso do quadriênio 2021–2024' },
        { fonte: 'Snapshot Scopus (entrega consolidada, 10/08/2026)', valor: 'quartil para 98 dos 204 periódicos — Q1 85, Q2 47, Q3 21, Q4 4 dos artigos únicos; 5 NE e 146 sem métrica' },
        { fonte: 'Mapa de publicações (leitura anterior do portal)', valor: 'Q1 92, Q2 55, Q3 32, Q4 4; 127 sem quartil' }
      ],
      resolucao: 'PARCIALMENTE RESOLVIDO na v4.2. O Qualis do conjunto completo segue indisponível, mas existe e passa a ser publicado para um subconjunto documentado: os 69 artigos com coautoria discente/egresso do quadriênio, com aviso explícito de que o recorte não representa o perfil do Programa. A distribuição Scopus foi recontada por ARTIGO ÚNICO a partir da entrega consolidada (a leitura anterior misturava contagem por docente); os dois conjuntos de números ficam registrados. A comprovação formal de percentil para a APCN segue pendente.'
    },
    {
      campo: 'Unidade de contagem da produção (produto único × soma por docente)',
      resolvido: true,
      fontes: [
        { fonte: 'Portal, até a v4.1', valor: '202 publicado como "artigos com coautoria de discentes e egressos"' },
        { fonte: 'Entrega consolidada — 06/resumo_anual_2021_2026.csv', valor: '168 artigos únicos com coautoria de discente/egresso' },
        { fonte: 'Entrega consolidada — 06/resumo_por_docente_2021_2026.csv', valor: '202 é a SOMA das contagens por docente' },
        { fonte: 'Entrega consolidada — 09/02_producao_com_discentes_egressos.csv', valor: '96 artigos no critério estrito (docente coautor é o orientador principal comprovado)' }
      ],
      resolucao: 'RESOLVIDO na v4.2, por apontamento da coordenação. O 202 estava com o rótulo errado: era a soma por docente, não a contagem de artigos. A mesma classe de erro foi procurada em todos os indicadores de produção e encontrada em mais três (total de artigos, distribuição por quartil Scopus e produções acima do P50). O portal passa a dizer sempre qual unidade está mostrando, e scripts/auditar-numeros.py confere cada número publicado contra a entrega consolidada.'
    },
    {
      campo: 'Defesas de mestrado e doutorado no período',
      resolvido: false,
      fontes: [
        { fonte: 'Painel APCN', valor: '48 teses e 118 dissertações (2021–2026)' },
        { fonte: 'Entrega consolidada — 09/03a e 09/03b', valor: '34 teses e 60 dissertações com título, discente, orientador e ano identificados' }
      ],
      resolucao: 'O portal publica as 94 defesas com evidência nominal como número validado e mantém o total do painel como referência declarada. Os dois recortes não são intercambiáveis: o do painel é mais amplo e não traz a mesma evidência item a item. Conciliação a cargo da Secretaria.'
    },
    {
      campo: 'Número de docentes permanentes',
      resolvido: true,
      fontes: [
        { fonte: 'Site /indicadores', valor: '21 permanentes' },
        { fonte: 'Contagem da página de docentes', valor: '25 registros; conjunto adotado: 24' },
        { fonte: 'Painel APCN', valor: '24 no núcleo analítico' },
        { fonte: 'Proposta APCN — tabela de corpo docente', valor: '21 permanentes + 3 colaboradores' }
      ],
      resolucao: 'RESOLVIDO. A página oficial lista 25 registros de docentes; o conjunto adotado nesta versão do portal é de 24 — 21 permanentes e 3 colaboradores, conforme a tabela de corpo docente da proposta APCN e os rótulos dos currículos Lattes. O valor 21 do site refere-se apenas aos permanentes.'
    },
    {
      campo: 'Categoria formal de docentes (permanente/colaborador)',
      resolvido: false,
      fontes: [
        { fonte: 'Rótulo no currículo Lattes', valor: '21 permanentes / 3 colaboradores' },
        { fonte: 'Categoria oficial 2024 (painel APCN)', valor: '19 permanentes / 4 colaboradores / 1 sem categoria' }
      ],
      resolucao: 'Divergência entre o rótulo declarado no Lattes e a categoria oficial registrada em 2024. O portal adota a tabela da proposta APCN (21+3). A conferência formal por docente consta como providência na matriz de conformidade da proposta.'
    },
    {
      campo: 'Distribuição Qualis da produção',
      resolvido: false,
      fontes: [{ fonte: 'ScriptLattes', valor: 'campo Qualis vazio em 100% dos registros' }],
      resolucao: 'NÃO PUBLICADO. A comprovação de percentil Scopus/WoS e a distribuição por estrato constam como pendência crítica da proposta APCN. Nenhuma estimativa é exibida.'
    },
    {
      campo: 'Totais históricos de titulados (430 dissertações / 132 teses)',
      resolvido: false,
      fontes: [{ fonte: 'Site atual', valor: '430 dissertações e 132 teses' }],
      resolucao: 'Exibido como dado histórico do site atual, marcado PRELIMINAR. Depende de conferência na Plataforma Sucupira. Não confundir com as 118 dissertações e 48 teses do recorte 2021–2026.'
    },
    {
      campo: 'Estrutura de áreas e linhas de pesquisa',
      resolvido: false,
      fontes: [
        { fonte: 'Site atual', valor: '3 áreas (Biomateriais e Compósitos / Materiais Avançados / Tecnologia Mineral)' },
        { fonte: 'Avaliação quadrienal + proposta APCN', valor: '17 linhas históricas, com sobreposição' },
        { fonte: 'Proposta APCN 2026', valor: '2 áreas de concentração e 4 linhas de pesquisa' }
      ],
      resolucao: 'O portal adota a arquitetura de 2 áreas e 4 linhas da proposta APCN 2026, marcada PRELIMINAR, com aviso de que aguarda aprovação no Colegiado.'
    },
    {
      campo: 'Valores de captação de recursos',
      resolvido: false,
      fontes: [{ fonte: 'Planilha de captação', valor: 'R$ 80.643.902,79 sem dupla contagem (2021–2026), com 73 pendências ativas' }],
      resolucao: 'Publicado somente o agregado institucional, marcado PRELIMINAR. Valores por docente não são publicados. Pendências documentais impedem status VALIDADO.'
    }
  ],

  /* --------------------------------------------------------- infraestrutura */
  infraestrutura: {
    status: 'EM_DEFINICAO',
    nota: 'O inventário de laboratórios, equipamentos multiusuários, biblioteca e recursos de informática está em processo de confirmação com os responsáveis de cada laboratório e consta como providência na matriz de conformidade da proposta APCN (seção 14). Nenhuma lista é publicada antes dessa validação.',
    uemg: {
      valor: 'Laboratórios de design, prototipagem, gemas e joias, materiais e ensaios',
      fonte: 'PROPOSTA', ref: 'ficha da instituição associada — infraestrutura disponibilizada', status: 'PRELIMINAR'
    }
  }
};

if (typeof window !== 'undefined') window.REDEMAT = REDEMAT;
if (typeof module !== 'undefined' && module.exports) module.exports = REDEMAT;
