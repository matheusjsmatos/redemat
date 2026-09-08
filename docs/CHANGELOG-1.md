# Registro de correções — Portal REDEMAT

## Versão 4.9 — 08/09/2026

Memória do corpo docente: os 48 docentes que passaram pela REDEMAT desde o
primeiro quadro, apurados das 13 coletas oficiais enviadas à CAPES.

### A página — `pages/historico.html`

Décima página do portal, ligada ao menu e à seção de história do Programa. O
corpo docente **atual** continua em `pessoas.html`; esta é a memória, e as duas
não se misturam.

Os cartões estão agrupados em cinco fases cronológicas de entrada — Fundação,
1997–1999, anos 2000, 2010 e 2020 — e dentro de cada fase em ordem de data de
entrada. Cada cartão traz foto (ou iniciais), situação, período, categoria, IES,
ano de doutorado, as linhas em que a pessoa produziu, as contribuições
registradas e, quando existem, os **títulos** dos livros e das patentes.

Filtro por nome, linha ou instituição, e por situação ou fase.

### A fonte: 13 coletas CAPES, 5,4 MB de planilha

`scripts/gerar-historico.py` (novo) lê os treze
`relatorio_dados_enviados_coleta_*.xlsx` de 2013 a 2025 e monta
`assets/js/historico-dados.js`. Nada foi digitado à mão.

Cada coleta é um **retrato do ano**, e a mesma produção reaparece nas coletas
seguintes — somar linhas daria número inflado. Então cada objeto é identificado
e contado uma vez: produção por (título normalizado, ano, subtipo), defesa por
(título, autor, data), projeto pelo nome. Das 45 762 linhas de produção
intelectual restaram **2 353 produções distintas**; dos 1 392 registros de
trabalho de conclusão, **292 defesas** — o resto eram linhas de banca.

| Apurado nas coletas 2013–2025 | |
|---|---|
| Docentes distintos | **48** (31 no quadro, 17 já saíram) |
| Da turma do primeiro quadro | **12** (6 ainda em atividade) |
| Defesas com orientador principal | **292** — 90 teses e 202 dissertações |
| Produções distintas | **2 353** |
| Artigos em periódicos | 906 |
| Livros | 56 |
| Patentes | 24 |
| Projetos de pesquisa | 81 |

### Duas janelas diferentes, e a página diz qual é qual

Este é o ponto que decide se a página homenageia ou subnotifica:

- **Período no Programa — completo.** A coluna "Início da Carga Horária" das
  coletas guarda a data real de entrada, e a mais antiga é **06/09/1996**. O
  período está certo mesmo para quem entrou dezessete anos antes da primeira
  coleta deste conjunto.
- **Contribuições — recortadas em 2013–2025.** Orientação, produção e projeto só
  existem nas coletas a partir de 2013. Para quem está no Programa desde o
  primeiro quadro, o número publicado é **menor** que a obra da pessoa.

A página abre dizendo isso. Sem esse aviso, "6 dissertações" ao lado de "no
Programa desde 06/09/1996" leria como o total de trinta anos de trabalho — e
seria uma homenagem que diminui o homenageado.

### Registro, não classificação

A regra do portal proíbe ranking público de docentes e análise individual de
desempenho. Um painel de homenagem precisa dizer o que a pessoa fez; o que ele
não pode é comparar e pontuar. A distinção está implementada:

- ordem **cronológica de entrada**, nunca por volume;
- nenhuma barra, gráfico ou escala comparando pessoas;
- nenhum índice, score ou posição;
- contagem ausente **desaparece** em vez de mostrar zero — um zero em "livros"
  significaria que a pessoa não escreveu livro, quando significa apenas que não
  há livro dela nas coletas de 2013–2025.

### O problema que quase estragou a homenagem: nome sem acento

Os relatórios CAPES guardam nome de pessoa em **caixa alta e sem acento**. Sem
tratamento, a página publicaria "Antonio Claret Soares Sabioni", "Antonio
Valadao Cardoso", "Jairo Jose Drummond Camara" — errando o nome de quem está
sendo homenageado.

A grafia passou a vir de fonte, registrada em `data/nomes-docentes.csv` com o
campo `fonte_grafia`:

| Fonte | Nomes |
|---|---|
| `SITE_DATA` — cadastro do quadro atual | 24 |
| `LATTES` — ID de 16 dígitos, do `FORA-DO-CONJUNTO.txt` | 15 |
| `CONFERIR` — publicado como vem da CAPES | **9** |

Os nove aparecem com o marcador **"grafia a conferir"** no próprio cartão, e a
página tem nota explicando por quê. Acento em nome de pessoa não se adivinha —
menos ainda numa homenagem.

Duas etiquetas de linha de pesquisa também vinham com erro na origem
("Quimica" sem acento, "de de" duplicado) e foram corrigidas por tabela
explícita no gerador, não por heurística.

### Outras mudanças

- **`C.esc()` no `components.js`.** A função de escapar texto estava duplicada
  dentro de `producao-lattes.html`; passou a viver nos componentes, onde
  qualquer página que monte HTML a partir de string possa usar.
- **Décimo item no menu.** Medido em nove larguras de 1024 a 1920 px: cabe, com
  22 px de folga até o botão Ingresso em 1200 px, porque a faixa 1181–1400 já
  aperta espaçamento e esconde o subtítulo institucional.
- **`scripts/gerar-ilustracoes.py`** ganhou a `linhagem()`: a árvore de
  orientações, que é literalmente o que um legado acadêmico é — um tronco em
  1996 que se ramifica em quatro gerações, com a espessura caindo conforme se
  afasta da raiz. Não é gráfico de dados; a contagem real está no texto.

### Uma terceira contagem de defesas, declarada

As coletas registram **292 defesas** entre 2013 e 2025. Ao lado das duas que
`indicadores.html` já registra — 94 com evidência nominal no Lattes (2021–2026)
e 48 teses + 118 dissertações do painel APCN —, é uma terceira medida, de fonte
e recorte diferentes. As três seguem declaradas, e nenhuma foi escolhida em
silêncio.

### Verificação

15 páginas sem erro de JavaScript e sem 404 próprio; 8 pontos de quebra × 15
páginas sem scroll horizontal; 48 cartões, 5 fases, 29 blocos de títulos, 9
marcadores de grafia, 6 notas de proveniência; filtros conferidos (17 de 48 em
"passaram pelo Programa", 6 de 48 na busca por "uemg", 1 na busca por
"hidrometalurgia"); acentos recuperados confirmados em tela (Antônio, Cláudio,
Kátia, Bragança, Álvares).

### Pendente da coordenação

- **A lista é automática; a homenagem é uma decisão.** O painel inclui todos os
  docentes das coletas, sem seleção editorial — critério defensável para um
  script, mas destacar ou escrever sobre uma pessoa é juízo institucional.
  Acréscimos, ausências e homenagens específicas devem passar pelo Colegiado.
- **Acentuação de 9 nomes.**
- **Fotos e autorização de imagem**, inclusive de quem já deixou o Programa —
  contato e autorização são trabalho da coordenação.
- **Anterior a 2013:** dezessete anos de orientações, publicações e projetos
  estão fora dos números. Recuperar depende de fonte que não está neste
  conjunto.

---

## Versão 4.8 — 03/09/2026

O mapa de colaborações muda de página, e três erros que a mudança revelou.

### O mapa vai para Internacionalização

A seção **Alcance geográfico — Mapa de colaborações no mundo** saiu de
`producao-lattes.html` e entrou em `internacionalizacao.html`, logo abaixo de
"Países com vínculos registrados". É o mesmo assunto em outra forma: a lista diz
quais países, o mapa mostra onde — e é ali que o visitante procura alcance
geográfico, não na página de produção.

Foram junto o Leaflet (CSS e JS), o `mapa-geo-dados.js`, as 31 linhas de HTML da
seção e as 128 linhas de JavaScript que a movem. O bloco era autossuficiente —
usa apenas `REDEMAT`, os componentes compartilhados e `window.MAPA_GEO` — o que
tornou a mudança um recorte, não uma reescrita.

Dois ajustes de acabamento: a alternância de faixas claras e escuras foi
recomposta nas duas páginas (a seção que saiu era clara e deixou três faixas
escuras seguidas em `producao-lattes.html`), e a página de produção ganhou um
ponteiro para o mapa, já que ainda exibe o número de países com coautoria.

### Três erros que só apareceram ao testar

**O mapa dizia 20 países; são 19.** O indicador contava
`l.codigo_pais || l.pais`, e um registro — o *Advanced Light Source*, em
Berkeley — estava com `codigo_pais: null`. Aquele local caía na chave "United
States" enquanto os outros usavam "US", e os Estados Unidos entravam duas vezes.
Corrigido nas duas pontas: o código do país foi preenchido no dado, e a
contagem passou a usar o **nome** do país, que nunca falta.

**"Publicações em coautoria: 731" media outra coisa.** A legenda logo acima diz
275 publicações com DOI resolvido — e 731 é a soma de vínculos por instituição:
um artigo assinado com três instituições estrangeiras conta três vezes. Publicar
731 sob o rótulo "publicações" é exatamente o erro do "202". O indicador passou
a se chamar **"Coautorias com instituição"**, e a página agora explica as duas
contagens lado a lado, com o aviso de que as duas medidas são legítimas e o que
não seria legítimo é publicar uma sob o rótulo da outra.

**O mapa inicializava duas vezes.** O gancho de carga dispara por dois caminhos
— o `load` do script do Leaflet e o `load` da janela — e o Leaflet recusa o
mesmo contêiner duas vezes, com "Map container is already initialized" no
console. Uma guarda tornou a chamada idempotente. O erro vinha de antes da
mudança de página; a movimentação só o trouxe à luz.

### Verificação

O Leaflet vem de CDN, que o ambiente de verificação não alcança — então o mapa
foi testado servindo o Leaflet 1.9.4 local no lugar do CDN e um tile de 1×1 no
lugar do OpenStreetMap. Com isso, os dois caminhos foram conferidos:

- **com Leaflet:** 257 marcadores e linhas desenhados, 128 instituições, 19
  países, 731 coautorias; o filtro por docente responde (Taíse Matte
  Manhabosco → 24 instituições, 4 países, 62 coautorias) e o filtro de ano
  compõe com ele (2025 → 6 / 1 / 9); 25 docentes e 7 anos nos seletores;
- **sem Leaflet:** a degradação documentada entra em ação — a lista por país
  substitui o mapa, os indicadores continuam corretos e nada quebra.

Nenhum erro de JavaScript nas duas situações. 14 páginas e 8 pontos de quebra
sem regressão.

---

## Versão 4.7 — 03/09/2026

Sai do portal o nome do docente fora do conjunto publicado. A explicação do
número fica.

### O que saiu

A página de pessoas trazia um aviso — "Exclusão formal. Guilherme Jorge
Brigolini Silva não integra o conjunto de 24 docentes utilizado nesta versão do
portal" — e o nome reaparecia em outros dois lugares públicos:

| Onde | O que dizia |
|---|---|
| `pessoas.html` | o aviso "Exclusão formal", com o nome |
| `indicadores.html`, conflito "Número de docentes permanentes" | "com a exclusão formal de Guilherme Jorge Brigolini Silva, o conjunto é de 24" |
| `reconhecimentos.html` | "Um dos dez prêmios (Melhor Palestrante, SEMTECH 2026) pertence ao docente formalmente excluído" |

O terceiro não trazia o nome, e identificava a pessoa de todo modo: o prêmio
tem título e ano, e é pesquisável.

### O que ficou

Os números que essas frases explicavam continuam explicados — sem apontar
ninguém:

- o aviso de `pessoas.html` foi **removido por completo**; nada naquela página
  afirma 25, então 24 não precisava de ressalva ali;
- o conflito de contagem passou a dizer "a página oficial lista 25 registros de
  docentes; o conjunto adotado nesta versão do portal é de 24 — 21 permanentes
  e 3 colaboradores";
- o aviso dos prêmios passou de "Um prêmio não aparece nesta lista" para "Nove
  dos dez prêmios registrados", e o texto agora diz que o décimo "consta de
  currículo fora do conjunto de 24 docentes adotado nesta versão do portal",
  sem o título do prêmio.

O campo `docentes.exclusao` deu lugar a `docentes.conjunto_nota`, cujo texto é
sobre contagem e não sobre pessoa. O motivo está escrito no comentário do
campo: nomear alguém como excluído é uma afirmação pública sobre essa pessoa, e
o portal não precisa fazê-la para explicar um número.

### Uma ocorrência que permanece, e por quê

`assets/js/mapa-geo-dados.js` traz o nome em três listas de **coautores** de
publicações. É fato de autoria vindo do Lattes, não afirmação sobre vínculo com
o Programa — e remover um coautor de uma lista de autores falsearia o registro.

Vale registrar, porém, que essas listas **não são exibidas em nenhuma página**:
o mapa usa apenas as contagens. São 797 nomes distintos, 26 KB dos 118 KB do
arquivo, que todo visitante baixa e ninguém vê. Retirá-las é decisão da
coordenação — não é remoção de dado publicado, é remoção de dado que trafega
sem uso.

### Verificação

As três páginas conferidas em navegador: o nome não aparece no texto nem no HTML
gerado, nenhuma delas imprime "undefined" onde havia o campo antigo, os 13
cartões de conflito seguem renderizando e não há erro de JavaScript. 14 páginas
e 8 pontos de quebra sem regressão.

---

## Versão 4.6 — 03/09/2026

Repositório Git preparado para <https://github.com/matheusjsmatos/redemat>, e
mais seis fotos de docentes.

### O repositório

`git init` na pasta do projeto, branch `main`, endereço remoto configurado e
primeiro commit com **268 arquivos, 16 MB**. O envio sai do Windows — o
ambiente onde o assistente trabalha não tem rede para o GitHub. O passo a passo
está em `docs/publicar-no-github.md`.

`.gitignore` deixa de fora o que é regenerável ou de trabalho:
`scriptlattes.bak/` (o script de sincronização recria a pasta a cada execução),
`assets/img/originais/` e `assets/img/pessoas/originais/` (imagens antes de
reencodar), além do lixo de Windows, macOS, Dropbox e editores.

`.gitattributes` normaliza fim de linha (`* text=auto`) e marca os binários,
para que editar no Windows e no Linux não produza diff de arquivo inteiro.

### Preparado para o GitHub Pages

- **`.nojekyll`** na raiz — sem ele o GitHub processa o site como Jekyll e
  ignora arquivos e pastas iniciadas por sublinhado.
- **Nenhum caminho absoluto**, conferido: Pages serve em `/redemat/`, não na
  raiz do domínio, e um `src="/assets/..."` quebraria.
- **`noindex` automático no github.io.** Enquanto o endereço for
  `matheusjsmatos.github.io`, cada página declara `noindex, nofollow`: são duas
  cópias do mesmo conteúdo na internet, e a que não deve aparecer na busca é a
  prévia. Não é controle de acesso — quem tem o link abre. A verificação é pelo
  hostname, então **se desliga sozinha** no domínio definitivo; não há nada
  para lembrar de remover. Verificado em navegador nos três casos: ausente em
  `localhost`, ausente em domínio `ufop.br`, presente em `github.io`.

### Decisão registrada: repositório público com as fotos

O repositório é **público** e inclui as fotos de pessoas, por decisão da
vice-coordenação. Fica registrado que:

- as 10 fotos hoje na pasta vão para uma página pública, e **9 delas são de
  outras pessoas** — 6 docentes, 2 pós-doutorandos e o secretário;
- não há autorização de imagem registrada para nenhuma delas: a coluna
  `autorizacao` do `assets/img/pessoas/LISTA-DE-FOTOS.csv` está em branco;
- **o Git guarda histórico.** Remover uma foto num commit futuro não a apaga
  dos commits anteriores, que seguem acessíveis. Tirar uma imagem do histórico
  exige reescrever a história e forçar o push.

A autorização de imagem permanece como pendência, agora com o agravante de que
a publicação precede a coleta.

### Seis fotos novas, e a mesma armadilha de novo

Chegaram Ana Paula Moreira Barboza, Dalila Chaves Sicupira, Ive Silvestre de
Almeida e Taíse Matte Manhabosco (docentes), Gustavo Henrique Silvestre
(pós-doutorando) e Rodrigo Cesário Lourenço (secretário) — **10 fotos no total**.

Duas vinham com extensão `.gif` e eram JPEG por dentro, exatamente como na v4.4.
O `conferir-fotos.py`, que passou a ler os primeiros bytes justamente por causa
disso, apontou as duas. Renomeadas para `.jpg`.

A de Dalila tinha **2257 KB** em 3088×2316 — um retrato de câmera inteiro para
exibir num círculo de 48 px. Reencodada: **70 KB**. A de Ana Paula, 449 KB →
61 KB. Os arquivos de origem ficaram em `assets/img/pessoas/originais/`, fora do
repositório.

### Observação para a Fase 4

`pages/normas.html` aponta para PDFs hospedados em
`redemat.ufop.br/sites/default/files/...` — endereços do site OpenScholar atual,
que **deixarão de existir** quando o domínio for substituído. A pasta local
`normas/` tem 23 documentos e entrou no repositório; ligar os links a ela é
trabalho de Fase 4, e dois arquivos precisarão de nome sem acento e sem espaço.

---

## Versão 4.5 — 03/09/2026

Foto aérea do campus na página de laboratórios, e um erro de rótulo que ela
fez aparecer.

### A figura: onde os laboratórios ficam

`pages/laboratorios.html` abre a lista com uma vista aérea do campus da UFOP,
com parte dos prédios da Escola de Minas — logo abaixo das notas de método e
antes da busca por técnica. É onde a imagem responde a uma pergunta real do
visitante, em vez de servir de textura atrás do título.

A figura é montada a partir dos dados (`laboratorios.foto`), com legenda e
crédito. `<picture>` serve o WebP e guarda o JPG para navegador que não o abra
— mesma imagem, um download só. A altura é limitada a `clamp(220px, 30vw,
420px)` com recorte pelo centro: em 1160 px de largura uma foto 16:9 ocuparia
650 px de altura e engoliria a tela; o recorte tira céu e mata das bordas, que
não são o assunto.

Tirar a foto do ar é apagar o bloco `foto` em `site-data.js` — a página trata a
ausência e se remove sozinha, sem edição de HTML.

O PNG original tinha **1,3 MB**. Reencodado: **108 KB** em WebP e 125 KB em
JPG, no tamanho nativo de 970×545. O original ficou em
`assets/img/originais/`.

### Autorização de uso: declarada como pendente, não presumida

A imagem vem da página "Apoio à EM-UFOP" da Fundação Gorceix, que não credita
fotógrafo e cujo rodapé reserva todos os direitos. **Atribuir a fonte não é o
mesmo que ter permissão.** O campo `autorizacao: 'PENDENTE'` registra isso, e a
página imprime o estado enquanto ele não for `'OK'`.

É a mesma regra já aplicada aos logos dos parceiros: fonte declarada não
autoriza publicação. Antes da substituição no domínio (Fase 4), ou há
autorização escrita da Fundação Gorceix, ou a foto é trocada por imagem do
acervo da própria UFOP.

### O erro que a foto revelou: `PARCIAL` não existia no vocabulário

Ao passar `C.badge('PENDENTE')`, o selo saiu escrito **"Em definição"** — e
investigar isso mostrou que `STATUS_MAP` em `components.js` não tinha
`PARCIAL`, que os dados usam em dois lugares. A página de prêmios vinha
imprimindo **"Em definição" onde o dado diz "Parcial"** desde a v4.3: um valor
publicado sob o rótulo errado, a mesma classe do erro do "202".

Corrigido nos dois sentidos:

- `PARCIAL` → "Parcial" e `PENDENTE` → "Pendente" entraram no mapa;
- estado desconhecido continua caindo para "Em definição" para não quebrar a
  página, mas agora **grita no console** com o nome do estado e onde corrigir.
  Cair em silêncio é como o erro durou duas versões.

### Verificação

14 páginas sem erro de JavaScript e sem 404 próprio; a figura conferida em
1440, 768 e 390 px (1160×420, 728×230 e 350×220, sem scroll horizontal);
`Parcial` agora impresso corretamente em `reconhecimentos.html`; 8 pontos de
quebra × 14 páginas sem scroll horizontal; sistema de fotos de pessoas intacto
nos seis formatos.

---

## Versão 4.4 — 03/09/2026

Fotos de secretaria e pós-doutorandos, seis formatos de imagem aceitos, e um
manifesto que evita mais de cem requisições inúteis por página.

### Quem aparece com foto: 28 pessoas em três populações

A pergunta era se secretaria e pós-doutorandos poderiam ter foto. Podiam desde
o começo — `pages/pessoas.html` já renderizava o componente de avatar para
todos os cartões. O que faltava era ficar **visível** que podiam: a aba se
chamava "Equipe técnica", o cargo de secretário não aparecia na lista de
conferência, e como ninguém tem foto ainda, todos os cartões mostravam
iniciais. Não havia como distinguir "não é suportado" de "não há arquivo".

Passou a estar explícito:

| População | Pessoas | Onde aparece |
|---|---|---|
| Docentes permanentes e colaboradores | 24 | `pessoas.html`, aba Docentes |
| Pós-doutorandos | 3 | `pessoas.html`, aba Pós-doutorandos |
| Secretaria e equipe técnica | 1 | `pessoas.html`, aba Secretaria e equipe |

A aba mudou de "Equipe técnica" para **"Secretaria e equipe"**, e a seção para
"Secretaria e equipe técnica". O `scripts/conferir-fotos.py` passou a mostrar o
**cargo** de cada pessoa quando existe — Rodrigo Cesário Lourenço aparece como
"Secretário da REDEMAT", não como uma linha genérica de equipe.

Os cartões de coordenação em `pages/programa.html` também ganharam foto: antes
mostravam só as iniciais, com marcação própria. Foi preciso declarar o slug à
mão em `programa.coordenacao`, porque o nome ali carrega título — o portal
geraria `profa-dra-dalila-...` a partir de "Profa. Dra. Dalila Chaves
Sicupira", que não corresponde a arquivo nenhum.

### Seis formatos, não um

O portal aceitava **só** `.jpg`: o nome do arquivo estava fixo no código. Uma
foto em PNG na pasta simplesmente não aparecia, sem nenhum aviso.

Agora aceita, nesta ordem de preferência: **jpg · jpeg · png · webp · gif ·
avif**. Basta um por pessoa; havendo mais de um, vence o primeiro da ordem e o
script avisa da duplicata, porque dois arquivos para a mesma pessoa costuma ser
troca de foto feita pela metade.

Sobre **GIF**, que foi o formato perguntado: funciona, inclusive animado. Vale
saber de uma limitação antes de escolher — **o portal não consegue pausá-lo**.
CSS não interrompe a animação de um GIF, nem para quem configurou
`prefers-reduced-motion` no sistema por sensibilidade a movimento. Para retrato
institucional a recomendação é imagem estática; se for animado, curto e
discreto. Está escrito no `LEIA-ME.md` da pasta.

Sobre **WebP** e **AVIF**: pesam bem menos com a mesma qualidade e qualquer
navegador atual abre. É a melhor escolha para quem vai gerar as imagens.

### O manifesto, e por que ele não é opcional

Aceitar seis formatos cria um problema que não existia com um só: o portal não
sabe qual arquivo pedir. Sondar um a um custaria **6 formatos × 28 pessoas =
até 168 requisições 404** em cada carregamento de `pessoas.html` — enquanto
ninguém tem foto, que é o estado de hoje.

Então `scripts/conferir-fotos.py --manifesto` varre a pasta e grava
`assets/img/pessoas/fotos.js` com um `window.FOTOS = {slug: formato}`. Com ele
o portal sabe de antemão quem tem foto e em que formato: **zero requisição
desperdiçada**, e quem não tem vai direto para as iniciais sem nem gerar a
`<img>`.

O manifesto vale sempre que o arquivo existe — inclusive vazio. A consequência
é real e está documentada: **foto largada na pasta sem regerar o manifesto não
aparece**. Para que isso não vire mistério, o portal escreve no console do
navegador, uma única vez, a linha de comando a rodar. E se `fotos.js` não
existir, o portal volta a sondar os formatos em cadeia — funciona para quem só
copiou arquivos, ao custo dos 404.

### Verificação

`scripts/verificar-fotos.py` (novo) faz a verificação em Chromium, servindo o
portal por HTTP:

- **14 páginas** sem erro de JavaScript e sem 404 de recurso próprio; 42
  avatares, todos com iniciais — o estado de entrega, sem foto nenhuma.
- **Os seis formatos renderizam no navegador**: png (docente), jpeg
  (coordenação), webp (pós-doc), gif (pós-doc), jpg (secretaria) e avif — cada
  um declarado no manifesto e conferido por `naturalWidth > 0` depois de
  `decode()`.
- **Manifesto vazio com foto solta na pasta**: 0 requisição de foto, aviso
  presente no console, nenhuma `<img>` gerada — o comportamento pretendido.
- **Sem `fotos.js`, com a foto só em `.gif`**: a sondagem em cadeia percorre
  jpg → jpeg → png → webp e resolve no gif, com as 27 pessoas sem foto caindo
  para as iniciais.
- **8 pontos de quebra × 14 páginas**: nenhum scroll horizontal.

Duas armadilhas de teste que valem registro, porque acusaram falha onde não
havia: as abas de pós-doc e secretaria começam `hidden` e as fotos são
`loading="lazy"` — dentro de painel escondido o navegador **não busca** a
imagem, então conferir essas fotos exige abrir a aba, como o visitante faz. E o
contêiner de verificação não tem saída para fonts.googleapis.com nem cdnjs, o
que gera erros de console que nada dizem sobre o portal. As duas ressalvas estão
escritas no cabeçalho do script, para a próxima pessoa não perder o tempo que se
perdeu aqui.

### As quatro primeiras fotos, e o que elas revelaram

Chegaram quatro fotos na pasta durante esta versão — Alan Barros de Oliveira,
Américo Tristão Bernardes, Matheus Josué de Souza Matos (docentes) e Leonardo
Villegas Lelovsky (pós-doutorando). Todas aparecem no portal. Duas coisas
apareceram com elas, e o `conferir-fotos.py` passou a detectar as duas:

**Extensão trocada não converte arquivo.** `alan-barros-de-oliveira.gif` e
`americo-tristao-bernardes.gif` eram **JPEG** por dentro. O Chrome fareja o
conteúdo e mostra a imagem mesmo assim, então o erro passa despercebido em
teste — mas basta o servidor enviar `X-Content-Type-Options: nosniff`, coisa
comum em hospedagem institucional, para a foto sumir. O script agora lê os
primeiros bytes de cada arquivo, compara com a extensão e diz o nome certo. Os
dois foram renomeados para `.jpg`.

**Peso.** `leonardo-villegas-lelovsky.png` tinha 620 KB para um retrato exibido
em círculo de 48 px. Reencodado para JPG de qualidade 82 em 599×800: **47 KB**,
sem diferença visível no cartão. O PNG original ficou em
`assets/img/pessoas/originais/`. O script agora avisa acima de 300 KB.

Nenhuma das quatro é recorte quadrado, e isso não é problema: `object-fit:
cover` com `object-position: center top` recorta pelo alto, que é o
enquadramento certo para retrato.

### Pendente do lado da coordenação

Os arquivos de foto das 28 pessoas e, para cada uma, a **autorização escrita
de uso de imagem** (LGPD). A coluna `autorizacao` do
`assets/img/pessoas/LISTA-DE-FOTOS.csv` fica em branco de propósito: o portal
não sabe quem autorizou, e publicar sem isso é decisão de quem publica.

---

## Versão 4.3 — 03/09/2026

Mural com as duas primeiras notícias, prêmios, oportunidades para estudantes,
laboratórios, patentes detalhadas, composição institucional e ilustrações.

### Mural: duas notícias, cada afirmação com fonte

**Artigo na Nature Nanotechnology** — "Pressure tuning of minibands in
MoS₂/WSe₂ heterostructures revealed by moiré phonons", Nature Nanotechnology
**18**, 1147–1153 (2023), DOI 10.1038/s41565-023-01413-3. Autoria da REDEMAT:
Matheus J. S. Matos (DEFIS/UFOP), num trabalho liderado pelo MIT com UNAM,
UFMG e UFF. O cartão traz a citação completa, a coautoria e os links para o
MIT News, o Phys.org e a página de métricas — fica marcado como **modelo
editorial** para as próximas divulgações de artigo.

**Menção Honrosa no EOSBF 2026** — Igor Ferreira Curvelo, Prêmio de Melhor
Pôster na área de Física de Materiais, pelo trabalho sobre modulação do efeito
Zeeman de vale por pressão e defeitos em dicalcogenetos de tungstênio dopados
com vanádio. O cartão registra também os outros dois participantes do encontro.

Os cartões com detalhe passaram de `<a>` para `<article>` com links próprios:
link dentro de link é HTML inválido e quebra a navegação por teclado.

### Prêmios e reconhecimentos — `pages/reconhecimentos.html`

**9 prêmios e títulos** do corpo docente, 2021–2026, do bloco Pm-0 do
ScriptLattes. O relatório traz o campo `membros_ids` com o índice do membro, e
não o nome: cada prêmio foi mapeado ao docente pelo índice em `membros.html`.

O relatório registra 10 prêmios; um deles (Melhor Palestrante, SEMTECH 2026) é
do docente formalmente excluído do conjunto de 24 e **não** é publicado. A
diferença está declarada na própria página.

A página inclui os prêmios de estudantes — hoje um, o do EOSBF — com a ressalva
de que prêmio de discente não fica no currículo do orientador e por isso não é
capturado automaticamente.

### Patentes: 8 com aplicação descrita, 47 no inventário

A página institucional de patentes traz 7 patentes e 1 software, cada um com
descrição de aplicação escrita pelo Programa. São exatamente os 8 destaques de
PI da entrega consolidada. O portal publica os 8 com número INPI, situação,
inventores e aplicação, e explica por que não são 47: as outras 39 constam no
Lattes **sem** descrição de aplicação, e o portal não inventa uma.

Situação de cada processo permanece "conforme escrito no Lattes" — validação no
INPI/DIRPA segue pendente e o portal não a afirma.

### Oportunidades para estudantes — `pages/oportunidades.html`

A pergunta que a página responde é "como eu entro". Com dado, não com promessa:

| | Concluídas | Em andamento |
|---|---|---|
| Iniciação científica | **150** | 24 |
| Trabalho de conclusão de curso | **97** | 6 |
| Dissertação de mestrado | 125 | 57 |
| Tese de doutorado | 52 | **79** |
| Supervisão de pós-doutorado | 11 | 3 |
| Monografia de especialização | 5 | — |
| Outras naturezas | 31 | 6 |
| **Total** | **471** | **175** |

Concluídas e em andamento vêm de blocos **separados** do ScriptLattes (OC* e
OA*): são populações distintas, nenhuma é subconjunto da outra, e a página diz
isso em vez de somar.

**As agências que financiaram as 150 iniciações**: CNPq 48, FAPEMIG 24, UFOP 14,
UEMG 4, UFMG 2, ArcelorMittal 1 — e 53 sem agência declarada no currículo, que
podem ser projeto voluntário ou registro incompleto; o portal não escolhe qual.

**Os cursos de onde vêm os bolsistas de IC** mostram a multidisciplinaridade na
prática: Física 36, Química Industrial 26, Engenharia Metalúrgica 26,
Engenharia Civil 20, Design de Produto 8, Design de Moda 5, e mais seis cursos.

Também **97 projetos de pesquisa** declarados nos currículos — com o aviso de
que é outra contagem que a do painel de captação (108 projetos únicos), porque
a fonte e o critério são diferentes.

### Laboratórios — `pages/laboratorios.html`

Os **15 laboratórios** da página institucional, com **64 equipamentos** e 45
técnicas distintas. Cada cartão traz responsável e e-mail quando existem — e
diz "não informado na página institucional" quando não existem, em vez de
deduzir. Busca livre por equipamento, técnica, responsável ou localização:
digitar "MEV" filtra para o NANOLAB.

A seção de infraestrutura de `pesquisa.html` deixou de exibir estado vazio.

### Composição institucional na home

A home passa a dizer **quem forma a rede**: na UFOP, os Departamentos de Física
e de Química (ICEB) e o Departamento de Engenharia Metalúrgica e de Materiais
(DEMET), da Escola de Minas, onde funciona a secretaria; na UEMG, a Escola de
Design. Com link para em.ufop.br e para a Escola de Design.

É a informação que explica por que a mesma rede orienta trabalho em aço
microligado e em design de moda — e isso está escrito na página.

### Ilustrações: 20 SVG desenhados a partir da física

Não é possível baixar imagens nesta sessão, e banco de imagens sobre "ciência"
é genérico ou de licença duvidosa. **`scripts/gerar-ilustracoes.py`** (novo)
desenha as ilustrações a partir do próprio objeto:

- a **super-rede moiré** vem da matemática de duas redes triangulares giradas
  de 5,5°, com período `a/(2·sen(θ/2))` — é o objeto do artigo da notícia;
- a **microestrutura** é um diagrama de Voronoi de verdade, recortado por
  meio-plano (Sutherland-Hodgman), com curva de resfriamento contínuo;
- a **curva de fadiga**, a **poça de fusão a laser**, a **coluna de separação**,
  a **folha 2D sobre eletrodos**, o **ciclo de economia circular** e a
  **bancada de caracterização** seguem a mesma regra: a forma é a forma certa.

Cada ilustração é gravada em duas versões — completa, com rótulos, para cartão
e figura; e `-hero`, **sem nenhum `<text>`**, para fundo de hero, onde o texto
do desenho competiria com o título da página.

SVG, não bitmap: escalam em qualquer tela e a maior pesa 50 KB.

### Correções de layout

- **`url()` em variável CSS resolve pela folha de estilo, não pela página.**
  `--hero-img: url('../assets/img/...')` num atributo `style` de
  `/pages/x.html` era resolvido de `/assets/css/` e virava
  `/assets/assets/img/...` — 404 silencioso. Passou a `../img/...`.
- **Nono item no menu não cabia em 1280px.** O hambúrguer subiu de 1080 para
  1180px e a faixa 1181–1400px aperta espaçamento e fonte do nav. Sem scroll
  horizontal em nenhum dos 8 pontos de quebra.
- **`display:block` nos spans da composição** — sem isso, nome do departamento,
  unidade e papel saíam na mesma linha.
- A barra de busca dos laboratórios usava `.filter-in`, que no design é a
  classe do *contêiner* e não do campo; ganhou classe própria.

### Verificação

14 páginas sem erro de JavaScript e sem 404 (exceto as fotos ainda não
enviadas); 8 pontos de quebra sem scroll horizontal; 15 cartões de laboratório
com busca funcional; 9 prêmios na linha do tempo; 8 cartões de patente;
7 linhas na tabela de orientações; 2 cartões de mural com 5 links de
repercussão e nenhum link aninhado.

---

## Versão 4.2 — 02/09/2026

Auditoria número por número contra a entrega consolidada, a partir de um
apontamento da coordenação. Nove indicadores publicados estavam errados.

### O apontamento

> "Confira o número de publicação com discentes. De onde você tirou esse
> número 202? Se esse número tá errado os outros também podem estar?"

Estava errado, e a suspeita estava certa: outros estavam também, pela **mesma
causa**.

### A causa: uma unidade de contagem trocada pela outra

Todo indicador de produção pode ser contado de dois modos:

- **produto único** — cada artigo conta uma vez no Programa;
- **soma por docente** — cada artigo conta uma vez para cada docente coautor.

São medidas diferentes e legítimas. Publicar uma com o rótulo da outra é erro
de fato. Foi o que aconteceu com o 202: ele é a soma das contagens por docente
(`06/resumo_por_docente_2021_2026.csv`); o número de **artigos únicos** com
coautoria de discente ou egresso é **168**
(`06/resumo_anual_2021_2026.csv`).

Procurada a mesma classe de erro em todos os indicadores de produção, ela
apareceu em mais três. O checklist completo:

| Indicador | Publicado até a v4.1 | Entrega consolidada | Veredito |
|---|---|---|---|
| Artigos únicos 2021–2026 | 310 | **308** | corrigido |
| Registros docente–artigo | 370 | **366** | corrigido |
| Artigos com DOI distinto | 289 | 289 | ok |
| Periódicos distintos | 204 | 204 | ok |
| Artigos únicos em Q1 | 92 | **85** | corrigido |
| Artigos únicos em Q2 | 55 | **47** | corrigido |
| Artigos únicos em Q3 | 32 | **21** | corrigido |
| Artigos únicos em Q4 | 4 | 4 | ok |
| Artigos sem quartil Scopus | 127 | **146 + 5 NE** | corrigido |
| Artigos com coautoria discente/egresso | 202 | **168 únicos** | corrigido |
| Projetos únicos no recorte | 119 | **108** | corrigido |
| Valor sob coordenação | R$ 29.410.319,49 | **R$ 44.381.317,50** | corrigido |
| Valor global sem dupla contagem | R$ 118.205.303,36 | R$ 118.205.303,36 | ok |
| Vínculos professor–projeto | 129 | 129 | ok |
| Pendências documentais | 73 | 73 | ok |

A distribuição Scopus estava errada por essa exata razão: os números
publicados vinham de contagem por registro docente–artigo, com o rótulo
"artigos únicos". Agora as duas contagens são publicadas, cada uma com o seu
nome (`unicos` e `vinculos` em `producao.scopus`).

### O checklist virou código

**`scripts/auditar-numeros.py`** (novo) lê os números publicados direto do
`site-data.js`, recalcula cada um a partir da entrega consolidada e imprime
veredito por item (`OK` / `DIVERGENTE`), gravando `data/checklist-numeros.csv`.
Para cada indicador imprime **sempre as duas contagens**, para que a troca de
unidade não passe outra vez.

```bash
python3 scripts/auditar-numeros.py ~/Dropbox/codex/apcn/10_analises/entrega_atualizada_lattes_20260829
```

### Três medidas de coautoria discente, não uma

O portal passa a publicar as três, porque as três circulam e medem coisas
diferentes:

- **168 artigos únicos** (2021–2026) — coautoria de pessoa confirmada como
  discente ou egresso em base institucional;
- **96 artigos** no critério estrito — o docente coautor é também o orientador
  principal comprovado daquele discente (17 docentes);
- **69 de 253 artigos (27,3%)** no recorte oficial do quadriênio 2021–2024.

E a soma por docente (202) fica registrada como o que é.

### Qualis: existia para um subconjunto e estava sendo omitido

A v4.1 declarava o Qualis `NAO_DISPONIVEL`. Correto para o conjunto completo —
o campo vem vazio do Lattes. Mas a auditoria DPIDE2 da entrega consolidada
**tem estrato atribuído** aos 69 artigos com coautoria discente do quadriênio:
A1 12 · A2 9 · A3 20 · A4 5 · B1 13 · B2 1 · B3 2 · B4 2 · C 5.

Passa a ser publicado, com o escopo impresso e um aviso explícito: **este
recorte não representa o perfil Qualis do Programa** e extrapolá-lo seria
inventar dado.

### Dados que faltavam no portal

- **Patentes** (bloco novo): 47 patentes únicas declaradas nos currículos
  (todos os anos), 48 declarações docente–patente, 8 produtos de PI
  destacados, 6 únicas no quadriênio. Extraídas do HTML bruto do cache Lattes,
  porque o campo de patentes dos JSON consolidados vem vazio. Depósito e
  concessão constam como escritos no Lattes; a situação atual exige validação
  no INPI/DIRPA e o portal não a afirma.
- **Defesas com evidência nominal**: 34 teses + 60 dissertações = **94**
  (2021–2026), com título, discente, orientador e ano. O painel APCN registra
  48 teses e 118 dissertações no mesmo período — recorte mais amplo, sem a
  mesma evidência. Os dois ficam declarados; a conciliação é da Secretaria.
- **Série oficial 2021–2024** (99/49/55/50 = 253 artigos únicos) registrada ao
  lado da série Lattes (62/48/57/49). Divergem sobretudo em 2021 — 99 contra
  62 — e a conciliação é pendência da Comissão de Produção.
- **Projetos**: entram `vinculos_recorte` (118), `vinculos_valor_conhecido`
  (105), `valor_participacao` (R$ 134,2 mi), `valor_atribuivel` (R$ 45,0 mi),
  `coordenacao_recorte` (74) e `participacoes_recorte` (44), com a leitura de
  que **nenhum desses valores é o "caixa" do Programa**.

### Percentil Scopus: o que faltava e por quê

O Chemical Physics Letters não aparecia na lista de Q1 porque o snapshot
automático do Scopus **não localizou o título** — e ausência no snapshot não é
ausência de métrica. Na interface do Scopus ele tem CiteScore 5,8 e percentil
80 (48/248 em General Physics and Astronomy). Entrou na tabela por consulta
manual, marcado com `m`.

**Não é possível raspar o Scopus.** `scopus.com` bloqueia acesso automatizado
por robots.txt e as páginas de fonte exigem sessão — tentativa registrada e
falhou com `ROBOTS_DISALLOWED`. O caminho confiável é a interface, inclusive o
botão "Download Scopus Source List", que entrega CiteScore e percentil de todos
os títulos numa planilha. Ficam prontos para isso:

- `data/percentis-scopus-pendentes.csv` — os 83 periódicos sem percentil,
  ordenados por número de artigos (é onde a consulta manual rende mais);
- `data/percentis-scopus-manuais.csv` — onde a consulta entra, com procedência
  (fonte, data, quem conferiu);
- `scripts/importar-percentis-scopus.py` — aplica no mapa e marca cada título
  preenchido por essa via, para que percentil conferido à mão não se misture
  com percentil de snapshot automático.

A tabela de Q1 ganhou **coluna de CiteScore** e passou de 70 para 71 títulos.

### Fotos das pessoas

**`scripts/conferir-fotos.py`** (novo) lista as 28 pessoas do portal — 24
docentes, 3 pós-doutorandos e 1 técnico — com o nome de arquivo exato que cada
uma espera, calculado do mesmo modo que o portal calcula em tempo de execução.
Com `--csv` grava `assets/img/pessoas/LISTA-DE-FOTOS.csv`, que traz uma coluna
`autorizacao` em branco: o script não sabe quem autorizou o uso de imagem, e
publicar sem isso é decisão de quem publica.

### Correção de cadastro aplicada

`09/07_cadastro_site_correcoes.csv` aponta que **Hana Hitomi Koga** não tem
orientador no cadastro público, mas a orientação por Dalila Chaves Sicupira
está confirmada no Lattes. Aplicada, com o campo `orientador_fonte: 'LATTES'`
marcando de onde vem. Os registros sem orientador caem de 23 para 22.

### Verificação

11 páginas sem erro de JavaScript e sem recurso 404 (exceto as fotos ainda não
enviadas); 8 pontos de quebra sem scroll horizontal; Qualis do subconjunto
renderizado com os 69 artigos; tabela de Q1 com 71 linhas, 7 colunas e o
Chemical Physics Letters marcado como consulta manual; distribuição Scopus
somando 308.

---

## Versão 4.1 — 02/09/2026

Grafo de colaborações importado para o portal, caminho da pasta do ScriptLattes
corrigido e recursos externos do relatório substituídos.

### O grafo de colaborações não estava no portal

A seção "Grafo de colaborações" mostrava apenas contadores e mandava o leitor
para o relatório ScriptLattes. Lá, o grafo existe em duas formas, e nenhuma
serve a um portal público:

- **imagem PNG com mapa de área clicável** — não escala, não tem texto
  selecionável, não responde a teclado, ilegível no celular;
- **applet Java** (`grafoDeColaboracoesInterativo.html`) — nenhum navegador
  atual executa applet; a página abre em branco.

O portal passa a redesenhar o **mesmo grafo em SVG**, a partir dos dados brutos
do `grafoDeColaboracoesComPesos.dot`. Não é uma reinterpretação: são os mesmos
24 nós, as mesmas 26 arestas e os mesmos pesos.

**`scripts/gerar-grafo.py`** (novo) lê o `.dot` e a tabela de Collaboration
Rank, casa cada nó com o docente pelo ID Lattes de 16 dígitos (nome canônico e
linha de pesquisa vêm do `site-data.js`), calcula o layout e escreve
`assets/js/grafo-dados.js`.

Decisões do desenho, todas com motivo:

- **Layout com semente fixa.** Fruchterman-Reingold com semente constante:
  rodar de novo com os mesmos dados dá exatamente o mesmo desenho. Um layout
  que muda a cada execução faria o leitor achar que o dado mudou.
- **Três faixas em vez de uma nuvem.** O núcleo conectado (14 docentes) ocupa a
  área principal; os 5 que aparecem em 2 grupos sem ligação com o núcleo ficam
  numa faixa própria; os 5 sem coautoria interna no período, em outra. Deixar a
  força espalhar nós desconectados sugeriria proximidade que o dado não afirma.
- **Separação de rótulos.** Além de afastar os círculos, o gerador afasta os
  *retângulos de texto* — nome sobre nome é o defeito clássico de grafo
  gerado. Verificado: zero sobreposições de rótulo.
- **Nome abreviado no desenho, completo no painel.** "Víctor Oliveira" no nó,
  "Víctor de Andrade Alvarenga Oliveira" ao selecioná-lo. As 24 abreviações são
  únicas — conferido.

Interação: seleção por lista ou clique no nó, navegação por teclado
(`Tab`/`Enter`/`Esc`), painel com parceiros e pesos, alternância de exibição
dos pesos, e a tabela de grau de colaboração dos 24 docentes — que não depende
do desenho.

### Um número que estava errado por dupla contagem

A primeira versão do painel de cada docente somava os pesos das arestas e
chamava o resultado de "produções em coautoria interna". Está errado: uma
produção assinada por três membros do Programa conta em cada um dos três pares.
Para Geraldo Lúcio de Faria a soma dava 34, e o valor correto — o que o
ScriptLattes registra no nó — é 27.

O painel passa a exibir o valor do nó, e a tabela de parceiros ganhou a
ressalva de que a coluna não soma o total. A soma dos pesos (86) continua nos
dados, com o nome explícito `soma_pesos_arestas` e o comentário de que **não é
contagem de produções**.

### Divergência de arestas registrada, não silenciada

A execução do ScriptLattes de 28/08/2026 indicava 29 arestas; a de 31/08/2026
fecha em 26. A diferença é de recoleta de currículos, não de critério. O portal
publica o número da execução mais recente — a mesma que alimenta o desenho — e
`colaboracao.interna.execucao_anterior` guarda o valor anterior com sua data.

### Caminho da pasta do ScriptLattes

O script apontava para `~/Documentos/softwares/scriptLattes/redemat/teste-01`
e para a cópia em `codex/apcn/10_analises/...`. Os dados estão em
**`C:\Users\mateu\Dropbox\claude\redemat\teste-01`**. Corrigido no script,
no README e no `scriptlattes/LEIA-ME.md`.

### Recursos externos que quebravam o relatório

A saída do ScriptLattes carrega, em 82 páginas, um `<script>` de
`sorttable.js` hospedado por **http://** num servidor de terceiro. Servido por
HTTPS, o navegador bloqueia como conteúdo misto: a ordenação das tabelas morre
sem mensagem de erro. Pior, o relatório passa a depender de um site que não é
nosso. A sincronização agora instala uma **cópia local equivalente**
(`js/sorttable-local.js`, escrita para o portal: clique ou `Enter` no cabeçalho
ordena, com `aria-sort`), reescreve os links do Lattes para `https://` e troca
a página do applet por um aviso que aponta para o grafo em SVG.

### O script de sincronização não dependia mais de apagar arquivo

O passo de backup fazia `rm -rf` + `mv`, e a exclusão do docente fora do
conjunto de 24 fazia `rm -f`. Em ambiente onde remover arquivo não é permitido,
o script abortava no meio. Agora o backup é cópia, a exclusão é feita no filtro
do `rsync`, e — se o arquivo ainda existir e não puder ser removido — a página
individual é substituída por um aviso. Nos três cenários o currículo fora do
conjunto deixa de ser publicado.

### Caixa alta em cabeçalho de linha

`.tbl th` aplicava fundo navy e caixa alta a **todo** `th`, inclusive ao
`th scope="row"` — o nome do docente saía "GERALDO LÚCIO DE FARIA". O estilo foi
restrito a `thead th`; `tbody th` virou rótulo de conteúdo, com zebra e hover.

### Verificação

11 páginas sem erro de JavaScript e sem recurso 404 (exceto as fotos ainda não
enviadas, cujo avatar cai para iniciais por projeto); 8 pontos de quebra
(1920→360 px) sem scroll horizontal; grafo com 24 nós, 26 arestas, 26 rótulos
de peso e 2 faixas; seleção por lista, por clique e por teclado; navegação
entre parceiros pela tabela; docente sem coautoria interna com mensagem
própria; tabela de grau com 24 linhas. Sincronização testada de ponta a ponta.

---

## Versão 4.0 — 02/09/2026

Lista completa de discentes (exigência CAPES), mapa geolocalizado de
colaborações, slots de foto, periódicos Q1 por impacto e correção do endereço.

### Correção de bug

**O mapa "Onde cada docente publica" não funcionava.** A causa: os dados vinham
por `fetch('../data/mapa-publicacoes.json')`, e navegadores bloqueiam leitura de
arquivo local quando a página é aberta por `file://`. Quem abrisse o `index.html`
com dois cliques via o mapa vazio.

Corrigido na raiz: os dados passaram a ser carregados por `<script>`, em
`assets/js/mapa-pub-dados.js`, que define `window.MAPA_PUB`. Agora funciona nos
dois modos — servido por HTTP e aberto direto do disco. O mesmo tratamento foi
aplicado ao mapa geolocalizado (`assets/js/mapa-geo-dados.js`).

### Correção de fato

**Endereço.** A secretaria funciona na **Escola de Minas, Campus Morro do
Cruzeiro**. O endereço da Praça Tiradentes, 20, que consta no cadastro do site
institucional, passou a ser exibido separadamente como endereço de
correspondência. As duas informações aparecem no rodapé e na página de ingresso,
identificadas.

### Corpo discente — exigência CAPES

Nova página `pages/discentes.html` com a **relação nominal completa dos 117
discentes**: nome, nível, orientador, coorientador, situação de bolsa, data de
ingresso e prazo regulamentar.

- 63 doutorandos e 54 mestrandos
- 39 com bolsa CAPES, 7 com FAPEMIG, 71 sem bolsa
- 24 orientadores distintos
- Ordenação por qualquer coluna, filtros por nível, bolsa e orientador, busca por nome
- Gráfico de orientações por docente, marcando os 5 orientadores externos ao
  quadro atual de 24 docentes

Três ressalvas ficaram explícitas na página:

1. **O prazo é calculado**, somando 24 meses no mestrado e 48 no doutorado à
   data de ingresso. Não é data de defesa nem considera prorrogações — os
   registros com prazo vencido recebem asterisco e uma nota explicando isso.
2. **23 registros não têm orientador** no cadastro da página institucional —
   pendência na origem, sinalizada como tal.
3. **E-mails de discentes não foram republicados**: não são necessários para a
   finalidade de transparência.

### Mapa geolocalizado de colaborações

Incorporado da pasta `Dropbox\claude\redemat`: mapa Leaflet com **128
instituições coautoras em 19 países e 299 conexões**, a partir de 275
publicações com DOI resolvido no OpenAlex. Filtros por docente, por ano e busca
por instituição, cidade ou país.

A auditoria de 01/09/2026 que acompanha os dados está resumida na página,
incluindo o que foi corrigido à mão — Gerdau Ouro Branco confundida com Rio
Branco Institute, a própria REDEMAT confundida com instituição de Portugal,
fragmentos de resumo interpretados como instituições. Os 7 DOI sem registro no
OpenAlex ficaram **fora** do mapa em vez de receber afiliação inferida.

Sem conexão, o mapa vira uma lista de instituições por país e a barra de filtros
se esconde — controles sem efeito não ficam na tela.

### Periódicos Q1 por parâmetro de impacto

Nova seção com os **70 periódicos Q1** que receberam produção do corpo docente,
ordenados pelo percentil Scopus 2025. O primeiro é ACS Nano, percentil 99.

A página explica o que o percentil mede: um artigo em periódico de percentil 95
não é, por isso, um artigo de alto impacto — é um artigo publicado em veículo de
alto impacto. A distinção importa e estava faltando.

### Fotos de pessoas

Slot de foto para docentes, pós-doutorandos e técnicos. O arquivo vai em
`assets/img/pessoas/<slug>.jpg`, com o slug derivado do nome. Sem o arquivo, o
cartão mostra as iniciais sobre a cor da linha de pesquisa — **o layout não
muda**, então o portal nunca fica com buracos.

Nenhuma foto acompanha o pacote: cada pessoa precisa autorizar o uso da própria
imagem. `assets/img/pessoas/LEIA-ME.md` traz a especificação e a tabela de
slugs. Discentes não têm slot de foto — a lista atende transparência e não
requer imagem.

### Novo pós-doutorando

**Adarlêne Moreira Silva**, supervisão do Prof. Versiane Albis Leão. Doutorado e
mestrado em Engenharia de Materiais pela REDEMAT-UFOP, graduação em Química
Industrial pela UFOP. Atuação em hidrometalurgia — tratamento de efluentes
líquidos, remoção de sulfato e manganês de água de mina visando reúso.

O total de pós-doutorandos passou a 3.

### ScriptLattes independente

A separação entre portal e relatório ficou explícita na página de produção: o
ScriptLattes entra como bloco autocontido em `scriptlattes/`, com HTML, CSS e
JavaScript próprios. O portal não reescreve esse conteúdo — apenas injeta uma
folha de legibilidade e um link de retorno. Atualizar o relatório não mexe no
site; mudar o site não altera o relatório.

### Logos

`docs/logos-parceiros.md` traz a fonte oficial de cada logo, separando **órgãos
públicos e fundações** (FAPEMIG, CNPq, CAPES, FINEP, EMBRAPII, CETENE, Gorceix —
com manual de identidade visual público) das **empresas** (que exigem
autorização do titular).

`scripts/preparar-logos.py` casa os arquivos baixados com o slug de cada
parceiro pelo nome, redimensiona para 120 px de altura, remove fundo branco e
grava no lugar certo. Roda em simulação por padrão; grava só com `--aplicar`.

Nenhum logo de terceiro foi incluído no pacote.

### Correções de layout

- Barras com rótulo longo (nomes de orientador) passam a empilhar em telas
  pequenas — resolvia scroll horizontal em 480 e 360 px
- Avatares da página inicial passaram a usar o componente com slot de foto
- Item duplicado "Ingresso" removido do menu (o botão de ação já cobria)
- Menu hambúrguer entra a partir de 1080 px, não 860 — com 8 itens e o logo
  maior, a barra não cabia mais a 1024 px

---

## Versão 3.0 — 02/09/2026

Incorporação da identidade visual institucional, das páginas indispensáveis do
Programa, do mapa dinâmico de publicações e do fluxo de atualização do
ScriptLattes. Duas correções de fato relevantes.

### Correções de fato

**1. O curso de Doutorado ESTÁ em funcionamento**

A versão 2.0 afirmava que o Doutorado não existia, interpretando a proposta APCN
("Criação do curso de Doutorado Acadêmico", "Nova proposta de curso") como prova
de que o curso não estava em operação. Isso estava errado.

Evidência em contrário, em três fontes:

- a página `/doutorado` do site oficial descreve o curso em operação: 8
  semestres, 34 créditos (9 obrigatórios + 21 eletivos + 4 de estágio de
  docência + 1 de qualificação + 3 de defesa), seleção anual única, exigência de
  2 artigos publicados ou submetidos, bolsas de até 48 meses;
- a página de discentes lista **63 doutorandos matriculados**, com ingressos de
  2012 a 2026;
- o site informa 132 teses defendidas.

O portal agora trata os dois assuntos separadamente: o Doutorado vigente na
página de cursos e no processo seletivo; a proposta APCN 2026 (curso em forma
associativa UFOP-UEMG) em seção própria, com aviso explícito de que não altera a
oferta atual. A relação formal entre os dois — substituição, reformulação ou
curso adicional — foi registrada como pendência da Comissão APCN.

**2. O endereço é Praça Tiradentes, 20**

A versão 2.0 informava "Campus Universitário Morro do Cruzeiro" por inferência.
O endereço institucional, confirmado nas páginas de docentes, técnicos e
credenciamento, é **Praça Tiradentes, 20 — Centro, Ouro Preto — MG, 35400-084**,
telefone **(31) 3559-1596**.

### Dados novos publicados

**Quartil Scopus 2025 da produção** — dado que existia no mapa de publicações e
havia sido declarado indisponível na 2.0. Dos 310 artigos únicos de 2021–2026:

| Estrato | Artigos | % dos que têm quartil |
|---|---|---|
| Q1 | 92 | 50% |
| Q2 | 55 | 30% |
| Q3 | 32 | 17% |
| Q4 | 4 | 2% |
| Sem quartil Scopus | 127 | — |

183 dos 310 artigos (59%) estão em periódicos com quartil atribuído; os 127
restantes concentram-se em periódicos nacionais sem indexação Scopus. O portal
declara isso e calcula os percentuais só sobre os 183.

**Qualis CAPES segue não publicado** — é classificação distinta do Scopus e o
campo continua vazio nos registros Lattes.

**Total de artigos ajustado de 308 para 310**, adotando a contagem do mapa de
publicações (mesma metodologia de deduplicação, fonte curada usada também para o
cruzamento Scopus). A diferença de 2 vem da normalização de títulos sem DOI.

**Números de projetos do painel integrado** (corte 29/08/2026): 119 projetos
únicos, 95 contabilizáveis, R$ 118.205.303,36 de valor global, R$ 29.410.319,49
sob coordenação, 23 coordenadores, 41 projetos alcançando 2026, concentração de
73,1% no top 3. Redes: INCT/CNPq INEO (R$ 14,9 mi), INCT MIDAS (R$ 9,1 mi), INCT
Nanocarbono (R$ 5,2 mi). Por IES: UFOP 60 projetos / R$ 27,3 mi, UEMG 12
projetos / R$ 2,1 mi. A divergência com a planilha (R$ 80,6 mi) foi declarada.

**Comunidade** — 117 discentes (63 doutorado + 54 mestrado), 2 pós-doutorandos e
a secretaria do Programa. Nomes de discentes não são republicados: o portal
publica só o agregado e aponta para a página institucional.

**Antônio Valadão Cardoso** registrado como bolsista de produtividade pela UEMG,
elevando o total a 12 bolsistas (11 CNPq + 1 UEMG).

### Identidade visual

- Logos institucionais de UFOP, UEMG e REDEMAT incorporados
- Logo modernizado da REDEMAT no header, sobre fundo claro — para preservar o
  amarelo da marca em vez de filtrá-lo para branco
- Logo histórico (azul vertical) preservado em `assets/img/`
- Faixa institucional no rodapé de todas as páginas
- Seção dedicada às duas universidades na página inicial
- Favicon derivado do poliedro da marca
- Aviso, na home, de que a identidade está em transição, com link para
  `ufop.br/logomarca`

### Páginas novas

**`pages/normas.html`** — 10 grupos de normas em acordeão (37 documentos),
seção de credenciamento docente, atas do Colegiado organizadas por ano (6 atas
de 2024–2025 com link direto), formulários, modelos e link para o apoio
psicológico da PRACE/UFOP.

**`pages/producao-lattes.html`** — distribuição por quartil Scopus, **mapa
dinâmico docente × periódico** em dois modos (docente → periódicos e periódico →
docentes), tabela dos periódicos mais utilizados com percentil, índice do
relatório ScriptLattes em 12 blocos e métricas do grafo de colaborações.

### Páginas expandidas

**`pages/pessoas.html`** ganhou quatro abas: Docentes (com os filtros e a busca
já existentes), Pós-doutorandos, Discentes e Equipe técnica. A barra de filtros
some fora da aba de docentes.

**`index.html`** ganhou o **mural** — notícias, artigos, patentes e produtos,
eventos, trabalhos de estudantes, extensão, oportunidades e processo seletivo em
8 categorias filtráveis —, cartões de redes sociais, parceiros com slot de logo
e a seção institucional.

**`pages/cursos.html`** reescrita para o Doutorado ativo, com seção separada
para a proposta APCN e suas 7 pendências críticas.

### Redes sociais

YouTube `@REDEMAT`, Instagram `@redemat.ufop` e LinkedIn `REDEMAT UFOP-UEMG`
no rodapé de todas as páginas e em cartões na home.

### Automação

**`scripts/atualizar-scriptlattes.sh`** — sincroniza a saída do ScriptLattes em
7 etapas: valida a origem, faz backup, copia, aplica a exclusão formal do
docente fora do conjunto publicado, troca o rótulo `teste-01` por `REDEMAT`,
injeta folha de legibilidade e link de retorno ao portal, e grava `SYNC.json`
com o inventário.

**`scripts/extrair-dados.py`** — recalcula os agregados a partir dos JSON dos
currículos e do mapa de publicações. **Não escreve em `site-data.js`**: imprime
um bloco para conferir e colar, porque todo número publicado passa por
conferência humana.

### Parceiros

17 parceiros catalogados com tipo (Empresa, Institucional, Fomento) e número de
projetos quando conhecido. **Nenhum logo incluído**: são marcas registradas de
terceiros e o uso requer autorização. Os cartões exibem o nome e passam a exibir
o logo automaticamente quando o arquivo for adicionado em
`assets/img/parceiros/<slug>.png`.

### Robustez

- Fallback de gráfico: sem a biblioteca Chart.js, cada gráfico vira tabela
  acessível com os dados reais — inclusive o perfil de quartis da seleção do
  mapa, que se atualiza a cada troca
- Mapa de publicações com mensagem explicativa quando aberto por `file://`
- CSS de abas movida para o design system (era duplicada inline)
- Correções de layout a 360px: `min-width: 0` em itens de grid,
  `overflow-wrap: anywhere` em e-mails e URLs, `max-width` no contêiner de
  tabela

---

## Versão 2.0 — 02/09/2026

Reconstrução do portal a partir das fontes primárias fornecidas: página oficial
de docentes, currículos Lattes via ScriptLattes, painel analítico APCN, proposta
APCN de Doutorado, proposta de estrutura curricular e planilha de captação.

### Correções críticas de dado

**1. Corpo docente integralmente substituído**

A versão 1.0 apresentava uma lista de docentes que não correspondia ao corpo
docente real do Programa. Nomes, e-mails, linhas de pesquisa e bolsas estavam
incorretos.

A lista foi substituída pelos 24 docentes obtidos da página oficial
(`redemat.ufop.br/docentes-1`), cruzada com a tabela de corpo docente da
proposta APCN e com os identificadores Lattes de 16 dígitos extraídos do
ScriptLattes. Guilherme Jorge Brigolini Silva foi excluído conforme instrução.

Consequência: todos os identificadores Lattes agora apontam para currículos
reais; os e-mails são os institucionais publicados.

**2. Conflito do número de docentes resolvido**

O conflito documentado na v1.0 (21 vs. 24 vs. 25 permanentes) tinha explicação
simples, que as fontes cruzadas revelaram:

- a página oficial lista 25 registros;
- excluindo Guilherme Jorge Brigolini Silva: 24 docentes;
- desses, 21 permanentes e 3 colaboradores (Antônio Valadão Cardoso,
  Heloisa Nazaré dos Santos, Ive Silvestre de Almeida);
- o valor "21" do site referia-se apenas aos permanentes;
- o "24" do painel APCN é o núcleo total.

Os três valores estavam corretos; mediam coisas diferentes. Registrado como
RESOLVIDO em `data/data_conflicts.csv`.

**3. Estrutura de áreas e linhas corrigida**

A v1.0 apresentava 3 áreas (Biomateriais e Compósitos / Materiais Avançados /
Tecnologia Mineral). A proposta APCN 2026 define **2 áreas de concentração e
4 linhas de pesquisa**, substituindo as 17 linhas históricas apontadas como
fragmentadas na Avaliação Quadrienal 2021–2024.

Estrutura adotada, marcada PRELIMINAR por aguardar aprovação no Colegiado:

- **Área 1 — Processamento, Estrutura e Desempenho de Materiais**
  - Linha 1.1 — Processamento, Manufatura e Engenharia de Superfícies
  - Linha 1.2 — Estrutura, Propriedades, Degradação, Modelagem e Integridade
- **Área 2 — Materiais Estratégicos, Funcionais e Sustentáveis**
  - Linha 2.1 — Recursos Minerais, Minerais Críticos e Economia Circular
  - Linha 2.2 — Materiais Funcionais, Biomateriais, Transição Energética,
    Desenvolvimento de Novos Materiais e Inovação Tecnológica

**4. Produção científica apurada da fonte**

A v1.0 exibia estimativas de produção sem base verificável ("~350 artigos",
"~65% Q1+Q2"). Substituídas por contagem apurada dos 24 currículos Lattes:

| Ano | Artigos únicos | Soma por docente |
|---|---|---|
| 2021 | 62 | 75 |
| 2022 | 48 | 58 |
| 2023 | 57 | 66 |
| 2024 | 49 | 56 |
| 2025 | 53 | 65 |
| 2026* | 39 | 50 |
| **Total** | **308** | **370** |

\* ano em curso, coleta até agosto de 2026

Deduplicação por DOI (289 dos 308 registros, 94%) e, na ausência de DOI, por
título normalizado. A diferença entre 308 e 370 decorre de coautoria interna ao
Programa — declarada no portal.

**5. Distribuição Qualis removida**

A v1.0 exibia uma distribuição estimada (Q1 40%, Q2 25%, Q3 20%, Q4 15%) sem
qualquer base na fonte. O campo Qualis está **vazio em 100%** dos registros
Lattes coletados.

A seção agora exibe "não disponível" e explica que a comprovação de percentil
Scopus/WoS consta como pendência crítica da proposta APCN.

**6. Lista de laboratórios removida**

A v1.0 apresentava 15 laboratórios com siglas, descrições e responsáveis
nominais que não foram confirmados em nenhuma fonte. A seção agora exibe
"inventário em processo de atualização" e cita a única informação com fonte:
a infraestrutura da UEMG descrita na ficha da instituição associada.

**7. Valores de bolsa removidos**

A v1.0 publicava valores mensais de bolsa (R$ 1.500 / R$ 2.200). Valores de
bolsa são definidos nacionalmente pelas agências e mudam periodicamente; o
portal agora remete às tabelas oficiais da CAPES e do CNPq.

**8. Doutorado reposicionado como proposta**

A v1.0 tratava o Doutorado como curso em funcionamento, com vagas e bolsas.
O Doutorado **não existe**: é proposta em elaboração (APCN/CAPES 2026), com
núcleo previsto de 12 a 13 docentes e 10 vagas por seleção sujeitas a decisão
colegiada. O portal agora avisa explicitamente que nenhuma inscrição está aberta.

**9. Dados novos incorporados**

- Código CAPES: 32007019007P3
- Nome do Programa em inglês
- Missão, visão e valor gerado (minutas da proposta)
- Comissão APCN (6 membros)
- Timeline ampliada: 1995, 1996, 1998, 1999, 2014, 2018, 2026
- Nucleação de quadros docentes: IFMG, CEFET-MG, UNIFEI, UFSJ, Unileste
- Alcance regional: Carajás, São Luís, Marabá, Vitória, Ipatinga, Araxá
- Formação 2021–2026: 118 dissertações, 48 teses, 133 orientações ativas
- Projetos: 110 únicos no recorte, R$ 80,6 mi sem dupla contagem, 73 pendências
- Financiadores: FAPEMIG, CNPq, FINEP, Embrapii, Vale, Gerdau, ArcelorMittal e outros
- Internacionalização: 13 de 24 docentes, 7 países, 45 vínculos
- Colaboração: 24 nós e 29 arestas internas, 797 coautores externos
- Estrutura curricular: 39 disciplinas (10 núcleo comum + 29 específicas)
- Créditos: mestrado 18 (8+10), doutorado 30 (8+22)
- Eixos transversais (5)
- Autoavaliação: histórico, ciclo anual, governança de dados
- ATD auditado do quadriênio: 0,472

### Dados deliberadamente não publicados

Presentes nas fontes, mantidos fora do portal:

- CPF constante da ficha de coordenação da proposta APCN (LGPD)
- `score_interno_0a100` por docente (painel APCN) — instrumento interno
- `h_index_scopus_proxy` por docente — evita ranking público
- Contagens individuais de artigos e valores individuais de captação
- Cenários prospectivos de composição do núcleo doutoral
- Pendências e criticidade por docente

### Mudanças de arquitetura de código

- Dados separados da apresentação: `assets/js/site-data.js` é fonte única
- Design system compartilhado em `assets/css/styles.css`
- Header, footer e selos de proveniência em `assets/js/components.js`
- Selo de status visível ao lado de cada indicador
- Responsivo verificado nos 8 pontos de quebra
- Acessibilidade: skip-nav, landmarks, ARIA, teclado, reduced-motion, impressão
