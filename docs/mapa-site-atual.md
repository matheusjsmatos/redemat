# Mapa do Site Atual — Auditoria

**Fonte:** coleta em https://redemat.ufop.br/ · 01–02/09/2026
**Plataforma:** OpenScholar / Drupal

---

## Árvore de navegação identificada

```
/
├── /sobre-o-redemat
│   ├── /historico
│   ├── /regimento
│   ├── /colegiado
│   └── /coordenacao
├── /cursos
│   ├── /mestrado
│   └── /doutorado
├── /disciplinas
├── /docentes-1                     ← página real do corpo docente
├── /linhas-de-pesquisa
│   ├── /biom-e-matcomp
│   ├── /mat-avancados
│   └── /tecnologia-mineral
├── /laboratorios
├── /processo-seletivo
├── /indicadores
├── /parcerias
├── /noticias
└── /contato
```

---

## Problemas identificados

### Consistência de dados

| Problema | Evidência | Gravidade |
|---|---|---|
| Contagem de docentes ambígua entre páginas | `/indicadores` diz 21; `/docentes-1` lista 25 registros | Alta |
| Estrutura de linhas desatualizada | Site mostra 3 áreas; proposta APCN define 2 áreas e 4 linhas; avaliação aponta 17 linhas históricas | Alta |
| Ausência de data de atualização | Nenhuma página informa quando o dado foi apurado | Alta |
| Ausência de fonte dos indicadores | Números aparecem sem origem declarada | Alta |
| Doutorado com página própria | Pode sugerir curso existente quando é proposta em elaboração | Alta |

### Arquitetura de informação

| Problema | Impacto |
|---|---|
| Slug `/docentes-1` | Sugere página duplicada ou provisória; ruim para SEO e memorização |
| Sem área de estudante matriculado | Informação acadêmica dispersa |
| Sem seção de internacionalização | Oculta a inserção internacional real do corpo docente |
| Sem seção de egressos | Perde a evidência de impacto formativo (nucleação em IFMG, CEFET, UNIFEI) |
| Indicadores fragmentados em subpáginas | Dificulta leitura por avaliadores |
| Sem página de oportunidades (pós-doc, IC) | Perde captação de talentos |
| Sem versão em inglês | Barreira à visibilidade internacional; consta como meta na proposta APCN |

### Apresentação e técnica

| Problema | Impacto |
|---|---|
| Layout datado, herdado do tema OpenScholar | Percepção de programa pouco ativo |
| Responsividade limitada | Experiência ruim em telas pequenas |
| Sem dados estruturados (JSON-LD) | Menor visibilidade em buscadores |
| Sem hierarquia visual clara | Informação relevante compete com secundária |
| Sem indicação de status de dado | Leitor não distingue confirmado de provisório |

---

## O que o site atual faz bem

Registrado para não se perder na reforma:

- URLs semânticas na maior parte das seções
- Página de docentes com links Lattes corretos e e-mails institucionais
- Estrutura de menus reconhecível para quem já usa o site
- Conteúdo histórico do Programa preservado
