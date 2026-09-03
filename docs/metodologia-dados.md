# Metodologia de Dados — Portal REDEMAT

**Versão 2.0 · 02/09/2026**

---

## Regra fundamental

**Nenhum dado é publicado sem origem rastreável.**

Todo número, nome, projeto, publicação, instituição, indicador ou afirmação
factual no portal carrega:

- **fonte** — qual documento ou sistema originou o dado
- **ref** — referência específica (URL, seção, tabela, arquivo)
- **coleta** — data em que o dado foi obtido
- **status** — nível de validação

Isso é implementado estruturalmente: `assets/js/site-data.js` é a única fonte de
dados do portal, e cada registro carrega esses campos. As páginas HTML não
contêm números nem afirmações factuais no markup.

---

## Pipeline

```
RAW  →  CLEANED  →  PRELIMINAR  →  VALIDADO  →  publicado
                          ↓
                     DIVERGENTE  →  valor suspenso, conflito declarado
```

| Estágio | Descrição | Publicado? |
|---|---|---|
| **RAW** | Dado como veio da fonte, sem tratamento | Não |
| **CLEANED** | Normalizado: unicode, formatação, deduplicação | Não |
| **PRELIMINAR** | Coletado e tratado, aguarda validação formal | Sim, **sempre com aviso** |
| **VALIDADO** | Conferido em ≥2 fontes ou confirmado por documento oficial | Sim, com selo |
| **DIVERGENTE** | Fontes conflitam entre si | Valor não publicado; conflito declarado |
| **EM_DEFINICAO** | Decisão institucional pendente | Sim, como "em definição" |
| **NAO_PUBLICAR** | Dado interno ou sensível | Nunca |

Os selos de status são visíveis ao lado de cada indicador no portal. Um leitor
consegue distinguir, sem sair da página, o que está confirmado do que ainda não.

---

## Dado ausente

Quando falta informação validada, o portal exibe:

> **"Dado em processo de atualização"**

Nenhum valor estimado, arredondado por conveniência ou plausível-mas-não-verificado
ocupa esse lugar. Isso vale inclusive quando a ausência é visualmente incômoda —
um dashboard com um cartão vazio é preferível a um dashboard com um número
inventado.

---

## Fontes

| ID | Fonte | Referência | Coleta |
|---|---|---|---|
| `SITE` | Site institucional REDEMAT | https://redemat.ufop.br/ | 01/09/2026 |
| `DOCENTES` | Página oficial de docentes | https://redemat.ufop.br/docentes-1 | 02/09/2026 |
| `LATTES` | Currículos Lattes via ScriptLattes | 25 currículos, saída de 28/08/2026 | 28/08/2026 |
| `APCN` | Painel analítico APCN (interno) | `portal_integrado_apcn_redemat_20260829` | 29/08/2026 |
| `PROPOSTA` | Esqueleto da Proposta APCN Doutorado v0.1 | Documento da Comissão APCN | 31/07/2026 |
| `CURRIC` | Proposta de estrutura curricular | Documento do GT curricular | 02/09/2026 |
| `CAPTACAO` | Panorama de captação (planilha deduplicada) | `REDEMAT_APCN_2026_Panorama...xlsx` | 29/08/2026 |

---

## Procedimentos de apuração

### Produção bibliográfica

1. Leitura dos 25 arquivos JSON do ScriptLattes (`scriptlattes/json/`)
2. Exclusão do currículo de Guilherme Jorge Brigolini Silva → 24 currículos
3. Filtro de `producao_bibliografica.artigos_periodicos` por ano ∈ [2021, 2026]
4. Deduplicação por DOI normalizado (minúsculas, sem espaços)
5. Na ausência de DOI, deduplicação por título normalizado (sem acentos, sem
   pontuação, minúsculas, 70 primeiros caracteres)
6. Resultado: **308 artigos únicos**, dos quais 289 (94%) com DOI

A soma das contagens por docente (**370**) é maior que o total único porque
artigos em coautoria entre docentes do Programa aparecem em mais de um currículo.
As duas séries são publicadas lado a lado, com a diferença explicada.

**Limitação declarada:** a deduplicação por título pode falhar em casos de
grafia divergente entre currículos. Estimativa de erro: baixa, dado que 94% dos
registros têm DOI.

### Qualis

O campo `qualis` está **vazio em 100%** dos registros coletados. Nenhuma
distribuição é publicada. A seção exibe "não disponível" e remete à pendência
de comprovação de percentil Scopus/WoS declarada na proposta APCN.

### Formação

Somatório de `orientacoes.concluidas.mestrado` e `.doutorado` no recorte
2021–2026, a partir do painel APCN (campos `orientacoes_m_concluidas_2021_2026`
e `orientacoes_d_concluidas_2021_2026`).

**Limitação declarada:** inclui orientações realizadas pelos docentes em outros
programas de pós-graduação. O número de titulados pela REDEMAT especificamente
depende de conferência na Plataforma Sucupira. Os totais históricos do site
atual (430 dissertações, 132 teses) são exibidos separadamente, com aviso, e
não devem ser somados nem confundidos com o recorte.

### Projetos e captação

Planilha `Panorama de Captação`, aba `Projetos únicos`:

- Unidade de análise: projeto único, identificado por ID canônico
- Recorte: projeto entra quando sua vigência intersecta 2021–2026
- Regra de valor: valor integral do projeto, **sem rateio anual**
- Deduplicação: cada ID de projeto conta uma vez, mesmo com vários docentes

Resultado: **110 projetos únicos no recorte**, **R$ 80.643.902,79** sem dupla
contagem, **R$ 45.722.742,87** sob coordenação ou liderança.

**Limitação declarada:** 73 pendências documentais ativas (valor não informado,
divergência de papel entre fontes, ou parcela atribuível ao docente não
informada). Por isso o indicador permanece PRELIMINAR. **Valores individuais
por docente não são publicados.**

### Internacionalização

Extração de `atuacao_profissional[].instituicao_pais` dos currículos, filtrando
países diferentes de Brasil.

**Limitações declaradas:**
- conta **vínculos**, não acordos formais vigentes
- um docente pode ter vínculos em mais de um país
- registros com ruído (nomes de instituições brasileiras no campo país) foram
  descartados manualmente

O número de docentes com pós-doutorado ou experiência internacional (13 de 24)
vem do painel APCN (`posdoc_ou_exterior_3m_proxy`).

### Colaboração

Grafo `grafo_de_colaboracoes.gexf` do ScriptLattes: 25 nós e 29 arestas
(24 nós após exclusão). Lista de coautores externos: `colaboradores.txt`,
797 identificadores Lattes distintos.

**Limitação declarada:** homonímia e variações de grafia podem afetar a contagem.

### Corpo docente

Cruzamento de três fontes:

| Campo | Fonte |
|---|---|
| Nome, e-mail, link Lattes | Página oficial de docentes |
| ID Lattes de 16 dígitos | Nomes dos arquivos JSON do ScriptLattes |
| Categoria, IES, carga horária, bolsa PQ/DT | Tabela de corpo docente da proposta APCN |
| Vinculação de linha (9 docentes) | Tabela de cenário 12A da proposta APCN |
| Vinculação de linha (14 docentes) | Responsabilidade por disciplina na proposta curricular |

Docentes cuja linha foi **inferida** da responsabilidade por disciplina recebem
`linhaStatus: 'PRELIMINAR'` e são marcados com asterisco no portal. Um docente
sem vinculação documentada recebe `EM_DEFINICAO`.

---

## Dados nunca publicados

### Por LGPD

- CPF (presente na ficha de coordenação da proposta APCN)
- Telefone pessoal, endereço residencial
- Remuneração ou dados financeiros individuais

### Por decisão de governança

- `score_interno_0a100` por docente (painel APCN)
- `h_index_scopus_proxy` por docente
- Contagem individual de artigos por docente
- Valor individual de captação por docente
- Cenários prospectivos de composição do núcleo doutoral
- Pendências e criticidade por docente
- Respostas individuais de autoavaliação — somente sínteses agregadas

**Justificativa:** o painel analítico APCN é instrumento interno de apoio ao
planejamento. O score que apresenta não corresponde a nota oficial da CAPES e
não constitui avaliação pública do corpo docente. Transformá-lo em ranking
público distorceria sua função e exporia docentes a comparação indevida.

### Por falta de validação

- Distribuição Qualis (campo vazio na fonte)
- Inventário de laboratórios e equipamentos (não confirmado com responsáveis)
- Portfólio de acordos internacionais (pendência declarada na proposta)
- Composição do Colegiado com mandatos (não confirmada pela secretaria)
- Valores de bolsa (definidos nacionalmente, mudam periodicamente)
- Número de vagas fora da vigência de um edital

---

## Ciclo de atualização

| Dado | Frequência | Responsável |
|---|---|---|
| Notícias e editais | Sob demanda | Secretaria |
| Processo seletivo | Por semestre | Coordenação |
| Corpo docente | A cada alteração | Coordenação |
| Produção e formação | Anual, após Sucupira | Comissão de Produção |
| Projetos e captação | Semestral | Comissão de Projetos |
| Infraestrutura | A cada alteração | Responsáveis de laboratório |
| Discentes e egressos | Anual | Secretaria / Comissão de Egressos |
| Impacto e patentes | Anual | Docentes / NIT |

---

## Como reportar erro de dado

Divergências, correções e validações devem ser encaminhadas à secretaria:
<redemat@ufop.edu.br>

Ao reportar, informe: o dado, a página onde aparece, o valor correto e a fonte
que o comprova. Correções são aplicadas em `assets/js/site-data.js`, com
atualização do campo `coleta` e, quando aplicável, promoção do `status`.
