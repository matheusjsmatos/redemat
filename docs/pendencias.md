# Pendências do portal REDEMAT

Atualizado em 09/10/2026. Cada item diz **o que falta**, **quem resolve** e
**o que acontece enquanto não for resolvido**. A última coluna importa: sem ela
a lista vira inventário, e ninguém sabe o que é urgente.

Ordenado por consequência, não por esforço.

---

## Alta — algo publicado está errado ou incompleto

### P-01 · O edital contradiz a estrutura aprovada
O **Edital REDEMAT nº 7/2026**, publicado em 08/10, descreve no item 3.1 **três
áreas de concentração** (Processos de Fabricação; Análise e Seleção de
Materiais; Engenharia de Superfícies). O Colegiado aprovou **duas áreas e
quatro linhas**, que é o que o portal publica.
**Quem resolve:** Colegiado / Coordenação — retificação do edital, ou nota
pública explicando o descompasso.
**Enquanto isso:** um candidato que leia os dois documentos encontra a
divergência no meio da inscrição, e o edital é o que prevalece.

### P-02 · 29 discentes sem orientador do quadro atual no cadastro
22 registros com o campo vazio e 7 apontando para docentes que já deixaram o
Programa (Gilberto Henrique Tavares Álvares da Silva, Cláudio Batista Vieira,
Vagner Roberto Botaro, Adilson Rodrigues da Costa e Margareth Spangler
Andrade).
**Quem resolve:** Secretaria — atualizar a orientação no cadastro institucional.
**Enquanto isso:** a página mostra "—" nesses 29 registros. A orientação segue
válida até a titulação; o que falta é o registro.

### P-03 · Ata da aprovação do Colegiado
Os campos `areas`, `curriculo` e `apcn` registram `fonte: 'COLEGIADO'` com a
data em que a aprovação foi informada — **sem número nem data da reunião**.
**Quem resolve:** Secretaria — referência da ata.
**Enquanto isso:** o portal afirma "aprovado pelo Colegiado" sem a procedência
que ele exige de todo o resto dos seus dados.

### P-04 · Nome de docente fora do conjunto publicado ainda está no ar
Auditoria de 03/10/2026: o nome aparece em `docs/CHANGELOG.md`,
`docs/CHANGELOG-1.md`, `docs/metodologia-dados.md` e `data/lattes-resumos.csv`,
além do histórico do git.
**Quem resolve:** Coordenação decide; a limpeza é técnica.
**Enquanto isso:** a regra de não nomear ninguém como excluído vale nas páginas
e não vale nos arquivos ao lado delas.

---

## Média — falta conteúdo que o portal promete

### P-05 · 18 normas sem arquivo carregado
Resoluções CEPE 7465 e 8016, CONPEP 57, Portaria PROPPI 8/2024, Guia de
Normalização do SISBIN, diretrizes do PROAP, formulários eletrônicos de registro
e de avaliação, documento de indicação de coorientador, critérios de pontuação
de currículo, entre outros.
**Quem resolve:** Secretaria — fornecer os PDFs.
**Enquanto isso:** cada item aparece listado com "arquivo ainda não carregado
neste portal".

### P-06 · 7 das 39 disciplinas sem docente responsável
Seminários e os três Tópicos Avançados constam como "coordenação rotativa";
Tribologia, *Innovative Biomass* e Resistência à Fratura não aparecem na seção
8.3 do documento aprovado com esse nome.
**Quem resolve:** Colegiado.
**Enquanto isso:** o catálogo publica a disciplina sem responsável.

### P-07 · Vinculação docente–linha só está nomeada para 9 dos 24
Para os outros 15, a linha exibida é **inferida** da disciplina pela qual o
docente responde. O asterisco que marcava a inferência continua na página; a
legenda que o explicava saiu em 09/10/2026.
**Quem resolve:** Colegiado — vinculação nominal.
**Enquanto isso:** o portal exibe um asterisco sem legenda e uma inferência sem
aviso.

### P-08 · Fotos e autorização de uso de imagem
24 das 28 pessoas sem foto; a coluna `autorizacao` em
`assets/img/pessoas/LISTA-DE-FOTOS.csv` está em branco para todas as 11 fotos
existentes.
**Quem resolve:** cada pessoa autoriza; Secretaria recolhe.
**Enquanto isso:** o portal exibe iniciais, que é o comportamento correto.

### P-09 · Foto aérea do campus sem autorização
`autorizacao: 'PENDENTE'`. Origem: Fundação Gorceix, que não credita fotógrafo e
reserva todos os direitos.
**Quem resolve:** Coordenação — autorização escrita, ou troca por imagem do
acervo da própria UFOP.
**Enquanto isso:** a imagem está no ar com o estado impresso na página.

### P-10 · Acervo de notícias importado, ainda não publicado
107 das 109 notícias de 2019–2026 foram baixadas, com 48 anexos e 18 imagens.
Faltam: a página de arquivo, as abas por semestre de 2019.1 a 2026.2 e o mural
de destaques. Duas notícias não baixaram e 30 links internos seguem sem
equivalente local.
**Quem resolve:** técnico.
**Enquanto isso:** a notícia do EOSBF no mural ainda aponta para o site antigo —
que será desligado.

---

## Baixa — qualidade e manutenção

### P-11 · Nove arquivos duplicados "-1" no repositório
`README-1.md`, `docs/CHANGELOG-1.md`, `assets/js/site-data-1.js` (que é a v4.9,
com números defasados), `components-1.js`, `styles-1.css`, `programa-1.html`,
`gerar-ilustracoes-1.py`, `PB-1.html`, `area-1.svg`. Todos servidos
publicamente.
**Enquanto isso:** há duas versões dos mesmos números no ar, uma delas antiga e
sem aviso.

### P-12 · Google Fonts entrega o IP do visitante a terceiros
32 referências. Para site de instituição pública sob LGPD é o ponto clássico;
resolve-se hospedando as fontes no repositório.

### P-13 · Métricas individuais por docente publicadas em `scriptlattes/`
`metricas.html` (tabela por docente, exportável), `teste-01-authorRank.txt`
(ranking) e `publicacoesPorMembro.csv` estão no ar e linkados pelo portal,
enquanto o próprio portal declarava não publicar contagem individual.
**Quem resolve:** Coordenação — decidir entre tirar o relatório do ar ou
reescrever a regra.

### P-14 · Conciliações de número em aberto
Série Lattes × série oficial de 2021 (62 contra 99); captação de recursos
(R$ 118,2 mi / R$ 44,4 mi / R$ 45,0 mi contra R$ 80,6 mi); situação das 47
patentes no INPI; percentil Scopus de 83 periódicos.
**Quem resolve:** Comissão de Produção e Comissão de Projetos.

### P-15 · Nome do grupo de pesquisa em `nano.ufop.br`
`data/sites-docentes.json` tem a URL e não tem o nome do grupo.

### P-04 (atualizada em 10/10/2026)
O nome saiu do **arquivo atual** do CHANGELOG em 10/10/2026 — quatro ocorrências
substituídas por "[nome de docente]". **O histórico do git continua trazendo o
nome**: ele está nos commits antigos e qualquer pessoa com o repositório clonado
o recupera. Remover de verdade exige reescrever o histórico (`git filter-repo`)
e um push forçado, o que invalida todos os clones existentes.
**Quem resolve:** Coordenação — decidir se reescreve o histórico.

### P-16 · A página mostra 8 patentes e o Lattes registra 47
A nota que explicava a diferença saiu em 10/10/2026 (ver
`docs/notas-governanca.md`, §10). O número menor ficou sem justificativa
visível, e num processo avaliativo isso pesa contra o Programa.
**Quem resolve:** Coordenação — decidir entre publicar as 47 com rótulo de
"sem descrição de aplicação" ou reinserir a nota.

### P-17 · Mandato da representação discente no Colegiado vencido
Encerrado em 25/06/2026. A página de administração sinaliza o vencimento pela
data; a recondução ou nova eleição é que resolve.
**Quem resolve:** Secretaria e Colegiado.
