# Mapa do Site Proposto

**Versão 2.0 · 02/09/2026**

---

## Arquitetura implementada nesta entrega

```
/                                   Home
│   Hero · KPIs · Sobre + timeline · 2 áreas e 4 linhas ·
│   Mini-dashboard de produção · Docentes · Internacionalização ·
│   Parceiros · CTA de ingresso
│
├── /programa                       ✅ implementado
│     Ficha institucional · História · Nucleação de quadros ·
│     Missão, visão e valor gerado · Coordenação e Comissão APCN ·
│     Forma associativa UFOP-UEMG · Autoavaliação
│
├── /pesquisa                       ✅ implementado
│     Princípios de organização · 2 áreas de concentração ·
│     4 linhas com escopo e palavras-chave · 5 eixos transversais ·
│     Rede de colaboração · Infraestrutura (em atualização)
│
├── /pessoas                        ✅ implementado
│     24 docentes com filtros (categoria, IES, linha) e busca ·
│     Distribuição por linha · Composição institucional
│
├── /cursos                         ✅ implementado
│     Mestrado · Proposta de Doutorado · Comparativo dos níveis ·
│     Créditos · Catálogo de 39 disciplinas · Bolsas
│
├── /indicadores                    ✅ implementado
│     Abas: Produção · Formação · Projetos e captação ·
│     Corpo docente · Autoavaliação · Metodologia
│     Inclui: pipeline de dados, inventário de fontes,
│     conflitos declarados, o que não é publicado
│
├── /internacionalizacao            ✅ implementado
│     Experiência formativa no exterior · Países com vínculos ·
│     Rede de colaboração · Parceiros · Financiadores · Metas
│
├── /processo-seletivo              ✅ implementado
│     Situação atual · Etapas · Documentos ·
│     Escolha de linha e orientador · Doutorado · Contato
│
├── /alunos                         ⏳ fase 2
│     Área do matriculado · Defesas agendadas · Normas
│
├── /noticias                       ⏳ fase 2
│     Arquivo e notícia individual
│
├── /contato                        ⏳ fase 2
│     Mapa · Formulário · Material para imprensa
│
└── /en/                            ⏳ fase 3
      Espelho bilíngue completo
```

---

## Princípios de organização

1. **Público-alvo explícito por seção** — candidato, estudante, comunidade
   científica, avaliador CAPES
2. **Nada relevante além de dois cliques** da home
3. **Dados agregados apenas** — nenhuma análise individual de docente
4. **Proveniência visível** — selo de status ao lado de cada indicador
5. **URLs semânticas e estáveis** — sem IDs numéricos, sem parâmetros de query
6. **Separação admin/público** — o painel APCN permanece instrumento interno e
   não é vinculado do portal
7. **Dado separado de interface** — `site-data.js` é fonte única; páginas HTML
   não contêm números no markup

---

## Roadmap

| Fase | Escopo | Status |
|---|---|---|
| **1** | Home, Programa, Pesquisa, Pessoas, Cursos, Indicadores, Internacionalização, Processo Seletivo | ✅ Concluída |
| **2** | Área do aluno, Notícias, Contato com formulário, páginas de laboratório individuais | ⏳ Depende de validação de dados |
| **3** | Bilinguismo pt-BR ↔ en com revisão humana | ⏳ Planejada |
| **4** | Integração com CMS, substituição do OpenScholar no domínio, redirects 301 | ⏳ Planejada |

---

## Antes de substituir o site atual

- [ ] Validar corpo docente e categorias com a secretaria
- [ ] Aprovar as 2 áreas e 4 linhas no Colegiado
- [ ] Conferir produção e formação na Plataforma Sucupira
- [ ] Resolver as 73 pendências documentais de projetos
- [ ] Confirmar inventário de laboratórios com responsáveis
- [ ] Aplicar o mapa de redirects (`docs/redirect-map.csv`)
- [ ] Testar Lighthouse (alvo ≥90 em performance, acessibilidade, SEO)
- [ ] Validar HTML no W3C e contraste no WAVE
- [ ] Configurar HTTPS e certificado no domínio
