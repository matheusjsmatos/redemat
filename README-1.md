# Portal REDEMAT — Novo Site

Portal institucional do Programa de Pós-Graduação em Engenharia de Materiais
(REDEMAT — UFOP · UEMG), reconstruído a partir de dados com proveniência declarada.

**Versão:** 4.9 · **Data:** 08/09/2026

---

## Como abrir

**Sirva a pasta por HTTP** — é o modo recomendado:

```bash
python3 -m http.server 8080
```

e abra <http://localhost:8080/>.

Abrir `index.html` direto por `file://` também funciona: desde a versão 4.0 os
dados dos mapas são carregados por `<script>`, não por `fetch()`, justamente
para não depender de servidor. Só os links do relatório ScriptLattes podem
falhar por `file://`, dependendo do navegador. Não há processo de build — o
portal é HTML, CSS e JavaScript estáticos.

> **Importante:** mantenha a pasta inteira junta. As páginas usam caminhos
> relativos para `assets/css/`, `assets/js/` e `pages/`.

Dois recursos externos são carregados da internet (com degradação graciosa se
indisponíveis): as fontes Inter e Source Serif 4 (Google Fonts) e a biblioteca
Chart.js (cdnjs). Sem internet, o portal funciona com fontes do sistema e sem
os gráficos.

---

## Estrutura de arquivos

```
redemat-portal/
├── index.html                      Página inicial
├── README.md                       Este arquivo
│
├── assets/
│   ├── css/
│   │   └── styles.css              Design system completo (tokens, componentes, responsivo)
│   ├── img/
│   │   ├── pessoas/                Fotos de docentes, pós-docs e secretaria (vazio; 6 formatos)
│   │   ├── campus-ufop-aereo.webp  Vista aérea do campus (autorização pendente — ver abaixo)
│   │   ├── campus-ufop-aereo.jpg   O mesmo, alternativa para navegador sem WebP
│   │   ├── originais/              Arquivos como chegaram, antes de reencodar
│   │   ├── redemat-logo.png        Logo institucional modernizado
│   │   ├── redemat-logo-historico.png  Logo histórico (azul vertical)
│   │   ├── ufop-logo.png           Logo UFOP
│   │   ├── uemg-logo.png           Logo UEMG
│   │   ├── favicon.png             Ícone do navegador
│   │   └── parceiros/              Logos de parceiros (vazio — ver abaixo)
│   └── js/
│       ├── site-data.js            ⭐ CAMADA DE DADOS com proveniência
│       ├── discentes-data.js       Relação nominal dos 117 discentes
│       ├── mapa-pub-dados.js       Matriz docente × periódico (quartil Scopus)
│       ├── mapa-geo-dados.js       Mapa geolocalizado (128 instituições, 19 países)
│       └── components.js           Header, footer, selos, avatares, redes sociais
│
├── pages/
│   ├── programa.html               História, missão, visão, governança, autoavaliação
│   ├── pesquisa.html               2 áreas de concentração + 4 linhas + eixos transversais
│   ├── pessoas.html                Docentes, pós-doutorandos, discentes, secretaria e equipe
│   ├── oportunidades.html          IC, TCC, bolsas, orientações e projetos — porta de entrada
│   ├── laboratorios.html           15 laboratórios com responsável, equipamento e técnica
│   ├── reconhecimentos.html        Prêmios do corpo docente e de estudantes; patentes e software
│   ├── discentes.html              Relação nominal completa (exigência CAPES)
│   ├── cursos.html                 Mestrado, Doutorado e a proposta APCN
│   ├── normas.html                 Normas, credenciamento e atas do Colegiado
│   ├── indicadores.html            Dashboard: produção, formação, projetos, metodologia
│   ├── producao-lattes.html        Mapa dinâmico docente × periódico + relatório ScriptLattes
│   ├── internacionalizacao.html    Vínculos no exterior, mapa de colaborações, parceiros
│   ├── historico.html              Memória do corpo docente: 48 docentes desde o primeiro quadro
│   └── processo-seletivo.html      Etapas, documentos, escolha de orientador
│
├── scripts/
│   ├── atualizar-scriptlattes.sh   Sincroniza a saída do ScriptLattes
│   ├── gerar-grafo.py              Converte o .dot do ScriptLattes no grafo SVG do portal
│   ├── gerar-ilustracoes.py        Desenha as ilustrações do portal em SVG
│   ├── gerar-historico.py          Apura as 13 coletas CAPES no painel histórico
│   ├── auditar-numeros.py          ⭐ Confere cada número publicado contra a entrega consolidada
│   ├── importar-percentis-scopus.py  Completa o percentil de periódicos por consulta manual
│   ├── conferir-fotos.py           Fotos: lista o esperado por pessoa e gera o manifesto
│   ├── verificar-fotos.py          Confere fotos, 404, erro de JS e os 8 pontos de quebra
│   ├── extrair-dados.py            Recalcula os agregados das fontes primárias
│   └── preparar-logos.py           Casa logos baixados com o slug de cada parceiro
│
├── scriptlattes/                   Destino do relatório ScriptLattes (ver LEIA-ME.md)
│
├── data/
│   ├── mapa-publicacoes.json       Matriz docente × periódico com quartil Scopus
│   ├── data_conflicts.csv          Conflitos entre fontes e resolução adotada
│   ├── fontes.csv                  Inventário de fontes de dados
│   └── extracao-*.json             Saídas brutas das extrações
│
└── docs/
    ├── metodologia-dados.md        Pipeline RAW → PUBLIC, regras, LGPD
    ├── mapa-site-atual.md          Auditoria da estrutura vigente
    ├── mapa-site-proposto.md       Arquitetura de informação nova
    ├── redirect-map.csv            Mapa de redirecionamentos 301
    └── CHANGELOG.md                Correções aplicadas nesta versão
```

---

## Onde editar cada coisa

### Para alterar qualquer dado exibido

**Edite apenas `assets/js/site-data.js`.**

Toda informação do portal vem desse arquivo. As páginas HTML são casca e
renderização — não contêm números, nomes nem afirmações factuais no markup.
Isso significa que:

- atualizar o número de docentes muda a homepage, a página de pessoas e o
  dashboard de uma só vez;
- não existe risco de dois lugares do site discordarem entre si;
- cada dado carrega `fonte`, `ref`, `coleta` e `status` — a proveniência viaja
  junto com o valor.

### Para alterar a aparência

**Edite `assets/css/styles.css`**, preferencialmente apenas os tokens no
bloco `:root` do topo. Cores institucionais, tipografia, espaçamentos e raios
de borda estão todos ali.

### Para alterar a navegação

**Edite o array `NAV` no topo de `assets/js/components.js`.** O header e o
footer de todas as páginas se atualizam juntos.

### Para publicar no mural da página inicial

Adicione itens ao array `mural.itens` em `assets/js/site-data.js`:

```js
mural: {
  itens: [
    {
      categoria: 'artigo',              // id de uma das 8 categorias configuradas
      titulo: 'Artigo na Physical Review B',
      texto: 'Breve descrição de uma ou duas frases.',
      data: '2026-09-15',               // AAAA-MM-DD
      url: 'https://doi.org/...',       // opcional; externo abre em nova aba
      imagem: '../assets/img/mural/foo.jpg',  // opcional
      imagemAlt: 'Descrição da imagem para leitores de tela'
    }
  ]
}
```

Categorias disponíveis: `noticia`, `artigo`, `patente`, `evento`, `estudante`,
`extensao`, `oportunidade`, `selecao`. Com a lista vazia, o mural mostra um
estado que explica o mecanismo — nunca conteúdo fictício.

### Fotos de pessoas

Aparecem com foto **28 pessoas**: os 24 docentes, os 3 pós-doutorandos e a
secretaria, nas abas de `pessoas.html`, mais os dois cartões de coordenação em
`programa.html`.

Salve como `assets/img/pessoas/<slug>.<formato>`, com o slug derivado do nome
(`Taíse Matte Manhabosco` → `taise-matte-manhabosco`). Formatos aceitos, nesta
ordem de preferência: `jpg` · `jpeg` · `png` · `webp` · `gif` · `avif` — basta
um. Para conferir o slug exato de alguém, `RC.slugFoto('Nome Completo')` no
console do navegador; para a lista toda, `conferir-fotos.py --csv`.

**Depois de copiar os arquivos, rode `conferir-fotos.py --manifesto`.** O
portal lê `assets/img/pessoas/fotos.js` para saber quem tem foto e em que
formato; sem regerar, a foto nova não aparece (e o portal avisa no console).

Recorte quadrado, mínimo 400×400 px, rosto e ombros, fundo neutro; 40–120 KB
bastam. Sem arquivo, o cartão mostra as iniciais sobre a cor da linha de
pesquisa — o layout não muda.

**Cada pessoa precisa autorizar por escrito o uso da própria imagem**, conforme
a LGPD. Ver `assets/img/pessoas/LEIA-ME.md`.

### Fotos e imagens de terceiros

Imagem segue a mesma regra dos dados: fonte declarada, e nada publicado sem
base. Cada imagem de terceiro é registrada em `site-data.js` com `fonte`,
`ref`, `coleta`, `credito` e — o campo que decide — `autorizacao`.

`autorizacao: 'PENDENTE'` significa que temos a fonte mas **não** temos
permissão escrita. A página exibe a imagem durante o desenvolvimento e imprime
o estado; antes da substituição no domínio (Fase 4) o campo tem de estar em
`'OK'` ou a imagem sai. Atribuir a fonte não substitui permissão.

Hoje há uma nessa condição: a vista aérea do campus em `laboratorios.html`,
obtida da página "Apoio à EM-UFOP" da Fundação Gorceix, sem crédito de
fotógrafo na origem e sob rodapé de direitos reservados.

Para tirar a imagem do ar, apague o bloco `foto` do respectivo dado — a página
trata a ausência e se remove sozinha, sem edição de HTML.

### Logos de parceiros

A pasta `assets/img/parceiros/` vem **vazia de propósito**. Os logos das
empresas e instituições são marcas registradas de seus titulares e o uso no
portal requer autorização prévia de cada um.

Para adicionar um logo depois de obter a autorização, salve o arquivo como
`assets/img/parceiros/<slug>.png` — o `slug` de cada parceiro está em
`site-data.js`, no array `parceiros.itens`. O cartão passa a exibir o logo
automaticamente; sem o arquivo, exibe apenas o nome.

**`docs/logos-parceiros.md`** lista a fonte oficial de cada logo, separando
órgãos públicos (que têm manual de identidade visual aberto) das empresas
(que exigem autorização). Depois de baixar tudo numa pasta:

```bash
python3 scripts/preparar-logos.py ~/Downloads/logos            # simulação
python3 scripts/preparar-logos.py ~/Downloads/logos --aplicar   # grava
```

### Atualizar o relatório ScriptLattes

```bash
./scripts/atualizar-scriptlattes.sh ~/Dropbox/claude/redemat/teste-01
```

A pasta de saída do ScriptLattes fica hoje em
`C:\Users\mateu\Dropbox\claude\redemat\teste-01` (a saída original no WSL,
`~/Documentos/softwares/scriptLattes/redemat/teste-01`, serve igualmente).

Além de copiar o relatório, o script substitui os recursos externos que o
quebrariam — o `sorttable.js` servido por `http://` de terceiro, que o
navegador bloqueia como conteúdo misto sob HTTPS, e o grafo em *applet* Java,
que nenhum navegador atual executa — e regenera `assets/js/grafo-dados.js`.
Ver `scriptlattes/LEIA-ME.md` para o detalhamento.

Sincronizar o relatório **não** atualiza os indicadores — use
`scripts/extrair-dados.py` para recalcular os agregados e conferir antes de
publicar.

### Auditar os números publicados

```bash
python3 scripts/auditar-numeros.py ~/Dropbox/codex/apcn/10_analises/entrega_atualizada_lattes_20260829
```

Lê os números direto do `site-data.js`, recalcula cada um a partir da entrega
consolidada e imprime veredito por item, gravando `data/checklist-numeros.csv`.

**Rode isto depois de qualquer atualização de dados.** Existe por causa de um
erro real: o portal publicou 202 como "artigos com coautoria de discentes e
egressos", quando 202 era a soma das contagens por docente e o número de
artigos únicos é 168. O mesmo tipo de troca afetava outros quatro indicadores.
Para cada um, o script imprime **as duas contagens** — produto único e soma por
docente — para que a confusão não volte.

### Completar o percentil Scopus de um periódico

```bash
python3 scripts/importar-percentis-scopus.py --listar     # o que falta
# preencha data/percentis-scopus-manuais.csv na interface do Scopus
python3 scripts/importar-percentis-scopus.py --aplicar    # grava
```

O snapshot automático não cobre todos os títulos: o Chemical Physics Letters,
por exemplo, tem CiteScore 5,8 e percentil 80 no Scopus e não foi localizado
pela busca. `scopus.com` bloqueia acesso automatizado, então o caminho é a
interface — de preferência o botão "Download Scopus Source List", que traz
tudo de uma vez. Cada título preenchido por essa via fica marcado no portal.

### Adicionar ou conferir as fotos das pessoas

```bash
python3 scripts/conferir-fotos.py --csv          # o que cada pessoa espera
# copie os arquivos para assets/img/pessoas/
python3 scripts/conferir-fotos.py --manifesto    # OBRIGATÓRIO depois de mexer
```

Cobre as 28 pessoas que o portal exibe em cartão: 24 docentes, 3
pós-doutorandos e a secretaria. Formatos aceitos, nesta ordem de preferência:
`jpg` · `jpeg` · `png` · `webp` · `gif` · `avif` — basta um por pessoa.

`--csv` grava `LISTA-DE-FOTOS.csv` com o slug exato de cada pessoa e uma coluna
`autorizacao` em branco: cada pessoa precisa autorizar por escrito o uso da
própria imagem antes de a foto ir ao ar.

`--manifesto` grava `assets/img/pessoas/fotos.js`, que declara quem tem foto e
em que formato. **Não é opcional.** O portal confia no manifesto — foto na
pasta sem ele regerado não aparece. A alternativa seria sondar os seis formatos
para cada pessoa, até 168 requisições 404 por carregamento de página enquanto
ninguém tem foto. Se esquecer, o portal escreve o comando no console do
navegador.

Detalhes de formato, incluindo por que GIF animado não é ideal para retrato
institucional, em `assets/img/pessoas/LEIA-ME.md`.

### Regenerar só o grafo de colaborações

```bash
python3 scripts/gerar-grafo.py ~/Dropbox/claude/redemat/teste-01
```

Lê `grafoDeColaboracoesComPesos.dot` e a tabela de Collaboration Rank do
ScriptLattes, casa cada nó com o docente pelo ID Lattes de 16 dígitos, calcula
o layout com semente fixa (mesmos dados = mesmo desenho) e escreve
`assets/js/grafo-dados.js`. Não escreve em `site-data.js`: se o número de nós
ou arestas mudou, avisa no terminal e a decisão de publicar é da coordenação.

---

## Regras de governança de dados

Estas regras são estruturais, não estilísticas. Foram embutidas no código e
não devem ser afrouxadas sem decisão da coordenação.

### 1. Nenhum dado sem origem rastreável

Todo valor no portal tem fonte declarada. Se você adicionar um dado, adicione
também de onde ele veio.

### 2. Status obrigatório

| Status | Significado | Aparece no portal? |
|---|---|---|
| `VALIDADO` | Conferido em ≥2 fontes ou confirmado por documento oficial | Sim, com selo verde |
| `PRELIMINAR` | Coletado, aguarda validação formal | Sim, **sempre** com aviso |
| `DIVERGENTE` | Fontes conflitam | Valor **não** publicado; conflito é declarado |
| `EM_DEFINICAO` | Decisão institucional pendente | Sim, como "em definição" |
| `NAO_PUBLICAR` | Dado interno ou sensível | **Nunca** |

### 3. Dado ausente não é dado inventado

Quando falta informação validada, o portal exibe
**"Dado em processo de atualização"**. Nenhum valor estimado, arredondado por
conveniência ou plausível-mas-não-verificado ocupa esse lugar.

### 4. O que nunca é publicado

- CPF, telefone pessoal, endereço residencial, remuneração
- Pontuação, índice h ou ranking por docente
- Contagens individuais de produção ou de captação de recursos
- Respostas individuais de autoavaliação
- Estimativas de Qualis ou percentil não comprovadas na base de origem
- Inventários e acordos não confirmados com os responsáveis

O painel analítico APCN, que contém métricas individuais, é **instrumento
interno de planejamento** e não deve ser vinculado a partir do portal público.

---

## Acessibilidade

- **WCAG 2.2 AA** como alvo: contraste ≥4.5:1 em texto, ≥3:1 em componentes
- Navegação completa por teclado; `skip-nav` para o conteúdo principal
- HTML semântico com landmarks (`header`, `nav`, `main`, `footer`)
- `aria-current`, `aria-pressed`, `aria-selected`, `aria-live` nos componentes interativos
- Abas navegáveis por setas do teclado
- Rótulos em todos os campos de formulário; `aria-label` em gráficos
- `prefers-reduced-motion` respeitado — animações e contadores desligam
- Foco visível com `:focus-visible`
- Folha de impressão dedicada

---

## Responsividade

Testado nos oito pontos de quebra pedidos:
**1920 · 1440 · 1280 · 1024 · 768 · 640 · 480 · 360 px**

Menu colapsa em hambúrguer a partir de 860px. Tabelas e gráficos rolam
horizontalmente dentro do próprio contêiner — o corpo da página nunca rola na
horizontal.

---

## Bilinguismo (pendente)

A estrutura está preparada: `<html lang="pt-BR">`, tags `hreflang` no
`index.html` e todo o texto de dado vindo de `site-data.js`.

Para implementar `en`:

1. Duplicar as chaves de texto em `site-data.js` com sufixo `_en`
2. Criar `assets/js/i18n.js` com o seletor de idioma
3. Gerar `/en/` espelhando a estrutura de `pages/`

**Não usar tradução automática** — o texto institucional precisa de revisão
humana, especialmente termos técnicos da área e nomes de linhas de pesquisa.

---

## Identidade visual

O portal usa os logos institucionais da UFOP, da UEMG e da REDEMAT. As versões
oficiais do logo da UFOP estão em <https://www.ufop.br/logomarca/>.

A REDEMAT usa historicamente um logo vertical azul com detalhes amarelos
(preservado em `assets/img/redemat-logo-historico.png`). Este portal adota a
versão modernizada da marca — poliedro amarelo com tipografia navy — mantendo a
paleta institucional. O logo aparece no header sobre fundo claro, para preservar
o amarelo da marca em vez de filtrá-lo para branco.

A faixa institucional no rodapé de todas as páginas reúne UFOP, UEMG e REDEMAT,
e a página inicial tem uma seção dedicada às duas universidades.

---

## Pendências conhecidas

Estas são pendências de **dado**, não de código. O portal já as exibe
honestamente como "em definição" ou "preliminar".

| Pendência | Impacto no portal | Responsável |
|---|---|---|
| Categoria formal de cada docente (Lattes 21+3 vs. oficial 2024 19+4) | Conflito declarado em `/indicadores#conflitos` | Secretaria |
| Comprovação de percentil Scopus/WoS | Distribuição Qualis não publicada | Comissão de Produção |
| Conferência de produção e formação na Sucupira | Indicadores marcados PRELIMINAR | Comissão de Produção |
| 73 pendências documentais de projetos | Captação marcada PRELIMINAR | Comissão de Projetos |
| Inventário de laboratórios e equipamentos | Seção exibe "em atualização" | Responsáveis de laboratório |
| Portfólio de acordos internacionais vigentes | Seção exibe "em definição" | Comissão de Internacionalização |
| Composição do Colegiado com mandatos | Seção exibe "em definição" | Secretaria |
| Aprovação das 2 áreas e 4 linhas no Colegiado | Estrutura marcada PRELIMINAR | Colegiado |
| Aprovação do catálogo de 39 disciplinas | Catálogo marcado EM_DEFINICAO | GT curricular / Colegiado |
| Totais históricos 430/132 vs. Sucupira | Marcados PRELIMINAR | Secretaria |
| Relação entre o Doutorado vigente e a proposta APCN | Tratados em seções separadas | Comissão APCN |
| Autorização de uso dos logos de parceiros | Cartões exibem só o nome | Comunicação |
| Divergência de captação: R$ 118,2 mi vs. R$ 80,6 mi | Publicado o valor do painel, com aviso | Comissão de Projetos |
| Nova coleta do ScriptLattes | Rodar `atualizar-scriptlattes.sh` após cada coleta | Coordenação |
| Conteúdo editorial do mural | Estado vazio explicativo | Secretaria |

---

## Publicar no GitHub

O repositório local está pronto para <https://github.com/matheusjsmatos/redemat>
(branch `main`, remoto configurado, primeiro commit feito). O passo a passo do
envio e da ativação do GitHub Pages está em **`docs/publicar-no-github.md`**.

## Correções relevantes

**Versão 4.9** criou a **memória do corpo docente** (`pages/historico.html`): os
48 docentes que passaram pela REDEMAT desde o primeiro quadro, apurados das 13
coletas CAPES por `scripts/gerar-historico.py`. Duas janelas distintas e
declaradas — o período no Programa é completo desde 06/09/1996, as contribuições
cobrem 2013–2025. Ordem cronológica, nunca por volume: é registro, não
classificação. Os relatórios CAPES guardam nome sem acento, então a grafia vem de
fonte (`data/nomes-docentes.csv`), com 9 nomes marcados como a conferir em vez de
receberem acento inventado.

**Versão 4.8** moveu o mapa de colaborações de `producao-lattes.html` para
`internacionalizacao.html`, abaixo da lista de países. Testar a mudança revelou
três erros: o mapa contava 20 países onde há 19 (um registro sem `codigo_pais`
fazia os Estados Unidos entrarem duas vezes), o indicador "Publicações em
coautoria" mostrava 731 quando as publicações distintas são 275 — soma por
instituição sob rótulo de publicação, o erro do "202" — e o mapa inicializava
duas vezes.

**Versão 4.7** retirou do portal o nome do docente fora do conjunto publicado.
Ele aparecia em três lugares — o aviso "Exclusão formal" em `pessoas.html`, o
conflito de contagem em `indicadores.html` e, sem o nome mas identificável pelo
título do prêmio, o aviso de `reconhecimentos.html`. Os números que essas frases
explicavam seguem explicados em termos de contagem, sem apontar ninguém.

**Versão 4.6** preparou o repositório Git (`.gitignore`, `.gitattributes`,
`.nojekyll`) e o GitHub Pages, incluindo um `noindex` que vale só no domínio
github.io — para a prévia não competir com redemat.ufop.br na busca — e que se
desliga sozinho no domínio definitivo. Chegaram seis fotos novas, totalizando 10;
duas vinham com extensão `.gif` sendo JPEG, e uma tinha 2,2 MB — o
`conferir-fotos.py` apontou as três.

**Versão 4.5** pôs uma vista aérea do campus na abertura da lista de
laboratórios, montada a partir dos dados com legenda e crédito, e reduziu a
imagem de 1,3 MB para 108 KB em WebP. A autorização de uso está declarada como
**pendente**: a foto vem do site da Fundação Gorceix, que reserva todos os
direitos, e atribuir a fonte não substitui permissão. No caminho apareceu um
erro de rótulo real — `PARCIAL` não constava em `STATUS_MAP` e a página de
prêmios imprimia "Em definição" onde o dado diz "Parcial" desde a v4.3; agora um
estado desconhecido avisa no console em vez de cair em silêncio.

**Versão 4.4** estendeu as fotos a todas as 28 pessoas que o portal exibe em
cartão — 24 docentes, 3 pós-doutorandos e a secretaria — e passou a aceitar seis
formatos (jpg, jpeg, png, webp, gif, avif) em vez de só jpg. Para não custar até
168 requisições 404 por página, `scripts/conferir-fotos.py --manifesto` gera
`assets/img/pessoas/fotos.js`, que declara quem tem foto e em que formato; rodar
esse comando depois de mexer na pasta não é opcional, e o portal avisa no console
quando ele está vazio.

**Versão 4.3** publicou as duas primeiras notícias do mural — o artigo na Nature
Nanotechnology e a Menção Honrosa no EOSBF 2026, cada afirmação com link para a
fonte — e criou três páginas: oportunidades para estudantes (150 iniciações
científicas, 97 TCCs, as agências que pagaram cada bolsa), laboratórios (15, com
64 equipamentos e busca por técnica) e prêmios e propriedade intelectual (9
prêmios do corpo docente e as 8 patentes com aplicação descrita). A home passou
a dizer quem forma a rede — DEFIS, DEQUI e DEMET na UFOP, Escola de Design na
UEMG. As 20 ilustrações são SVG desenhados a partir da própria física.

**Versão 4.2** auditou número por número contra a entrega consolidada, depois
de a coordenação questionar de onde vinha o "202" de artigos com coautoria
discente. Vinha da soma por docente — o número de artigos únicos é 168 — e a
mesma troca de unidade afetava o total de artigos (310 → 308), a distribuição
por quartil Scopus, as produções acima do P50 e os projetos únicos (119 → 108),
além do valor sob coordenação (R$ 29,4 mi → R$ 44,4 mi). Nove indicadores
corrigidos, seis confirmados. O Qualis, antes declarado indisponível, passou a
ser publicado para o subconjunto documentado que o tem. Entraram patentes (47),
defesas com evidência nominal (94) e a conferência automática do checklist.

**Versão 4.1** trouxe o grafo de colaborações para dentro do portal. Ele existia
só no relatório ScriptLattes, em duas formas que não servem a um site público —
imagem PNG com mapa de área e applet Java, que nenhum navegador atual executa.
O portal passa a redesenhar o mesmo grafo em SVG a partir do
`grafoDeColaboracoesComPesos.dot`: mesmos 24 nós, mesmas 26 arestas, mesmos
pesos, agora com seleção por docente, navegação por teclado e tabela
equivalente. No caminho, um número errado foi corrigido — o painel somava os
pesos das arestas e chamava isso de produções em coautoria interna, o que conta
em dobro toda produção assinada por três membros do Programa.

**Versão 4.0** publicou a relação nominal de discentes exigida pela CAPES,
integrou o mapa geolocalizado e corrigiu o mapa docente × periódico, que
carregava dados por `fetch()` e por isso não funcionava aberto por `file://`.

**Versão 3.0** corrigiu dois erros de fato da 2.0:

- **O Doutorado está em funcionamento.** A 2.0 o tratava como inexistente,
  interpretando a proposta APCN como prova de que o curso não existia. O site
  oficial descreve o curso (8 semestres, 34 créditos, seleção anual) e há 63
  doutorandos matriculados. A proposta APCN é um item separado, para um curso em
  forma associativa, e agora tem seção própria.
- **O endereço é Praça Tiradentes, 20**, confirmado em três páginas do site
  oficial. A 2.0 informava o Campus Morro do Cruzeiro por inferência.

A 3.0 também passou a publicar o **quartil Scopus 2025** da produção (dado que
existia no mapa de publicações e havia sido declarado indisponível), com o aviso
de que Scopus não é Qualis CAPES.

**Versão 2.0** substituiu integralmente uma lista de docentes que não
correspondia ao corpo docente real do Programa, e removeu 15 laboratórios com
responsáveis não confirmados, uma estimativa de Qualis sem base na fonte e
valores de bolsa que mudam por decisão das agências.

Ver `docs/CHANGELOG.md` para o detalhamento completo.

---

## Fontes de dados

| Fonte | Referência | Coleta |
|---|---|---|
| Site institucional REDEMAT | https://redemat.ufop.br/ | 01/09/2026 |
| Página oficial de docentes | https://redemat.ufop.br/docentes-1 | 02/09/2026 |
| Currículos Lattes via ScriptLattes | 25 currículos, saída de 28/08/2026 | 28/08/2026 |
| Painel analítico APCN (interno) | `portal_integrado_apcn_redemat_20260829` | 29/08/2026 |
| Esqueleto da Proposta APCN Doutorado v0.1 | Documento da Comissão APCN | 31/07/2026 |
| Proposta de estrutura curricular | Documento do GT curricular | 02/09/2026 |
| Panorama de captação (planilha deduplicada) | `REDEMAT_APCN_2026_Panorama_Captacao...xlsx` | 29/08/2026 |

---

## Contato

Secretaria REDEMAT — <redemat@ufop.edu.br>
Coordenação — <coordenacao.redemat.em@ufop.edu.br>
Vice-Coordenação — <vicecoordenacao.redemat.em@ufop.edu.br>
