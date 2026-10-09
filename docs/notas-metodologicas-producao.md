# Notas metodológicas da produção — registro interno

Retiradas das páginas públicas em 09/10/2026, por decisão da coordenação.
**Não são publicadas no portal.** Ficam aqui porque descrevem como cada número
foi apurado: sem elas, quem reconferir a produção daqui a um ano não tem como
refazer a conta nem saber o que cada medida cobre.

As páginas continuam publicando os números. O que saiu foi a explicação ao
lado deles.

---

## 1. Quartil Scopus não é Qualis CAPES

> Quartil Scopus NÃO é Qualis CAPES. A comprovação formal de percentil para a
> proposta APCN segue pendente.

São duas classificações distintas, de bases distintas. O portal mostra quartil
Scopus; quem ler "Q1" como "Qualis A1" lê errado.

## 2. Cobertura do quartil Scopus

> Quartil do periódico na base Scopus, na categoria de maior percentil. 157 dos
> 308 artigos únicos (51%) estão em periódicos com quartil atribuído; 5 aparecem
> como NE (não elegível) e 146 sem métrica, concentrados em periódicos nacionais
> fora da indexação Scopus. Percentuais calculados apenas sobre os artigos com
> quartil conhecido.

O snapshot Scopus cobre 98 dos 204 periódicos do conjunto. **Ausência de métrica
não é qualidade zero**: significa que o veículo não foi localizado na base.
106 periódicos seguem sem percentil — ver `data/percentis-scopus-manuais.csv`.

## 3. Escopo da distribuição Qualis

> A classificação Qualis CAPES não está preenchida nos registros Lattes, e por
> isso não existe distribuição Qualis do conjunto completo de artigos. Existe,
> porém, para um subconjunto documentado: os 69 artigos com coautoria de
> discente ou egresso do quadriênio 2021–2024, classificados na auditoria
> DPIDE2. É esse subconjunto — e só ele — que o portal publica por estrato.

O rótulo de escopo **permanece na página**, ao lado do gráfico. Um gráfico
chamado "distribuição Qualis" que cobre 69 de 308 artigos, sem dizer isso,
afirma algo que não é verdade — e isso é legenda de eixo, não ressalva.

## 4. Como o total foi apurado

> Artigos deduplicados por DOI (94% dos registros) e, na ausência de DOI, por
> título normalizado. Os 366 registros docente–artigo somam mais que os 308
> artigos únicos por causa da coautoria interna ao Programa: um artigo assinado
> por três docentes aparece em três registros e conta uma única vez no total do
> Programa. O ano de 2026 está em curso — a coleta cobre até agosto de 2026.

## 5. Pendência de percentil para a APCN

> A comprovação de percentil Scopus/Web of Science para a produção destacada e
> para ao menos 60% do núcleo docente consta como pendência formal antes da
> submissão da proposta APCN. Enquanto não concluída, o portal não publica
> distribuição por estrato do conjunto completo — só a do subconjunto auditado,
> com o escopo declarado.

Consta também em `apcn.pendencias_criticas`, agora rotulado como documentação
do trâmite na CAPES.

## 6. Percentil acima de 50

> Artigos em periódico com percentil Scopus acima de 50: 145 **registros
> docente–artigo** — soma por docente. Um artigo com três docentes coautores
> entra três vezes nesta soma.

Fonte: `09/01_producao_docente.csv`, coluna "Artigos P>50", somada nos 24
docentes.

## 7. Uma medida, dois números

> Todo indicador de produção pode ser contado por **produto único** (cada artigo
> uma vez no Programa) ou por **soma por docente** (cada artigo uma vez para
> cada docente coautor). No período, são 308 artigos únicos e 366 registros
> docente–artigo; 168 artigos únicos com coautoria de discente ou egresso, cuja
> soma por docente é 202. Num recorte mais exigente — em que o docente coautor é
> também o orientador principal comprovado do discente — são 96 artigos, de 17
> docentes. Os três números são corretos e medem coisas diferentes.

Esta é a distinção que já produziu um erro publicado: **202 era a soma por
docente e foi ao ar como se fosse o número de artigos**. Com a explicação fora
da página, a distinção passa a depender inteiramente de quem monta os números
saber dela. É o principal risco desta remoção.

## 8. Duas séries anuais que não coincidem

> A série oficial do quadriênio registra 99 artigos únicos em 2021; a coleta
> Lattes registra 62. A conciliação das duas séries é pendência da Comissão de
> Produção.

Série oficial 2021–2024 (coleta/ATD): 2021 → 99 · 2022 → 49 · 2023 → 55 ·
2024 → 50 · total 253.

---

## O que ficou nas páginas

- Os números, todos.
- O rótulo de escopo do gráfico Qualis (item 3).
- Livros e capítulos publicados no período.
- Os selos de procedência por campo (`VALIDADO`, `PARCIAL`, `DIVERGENTE`).
