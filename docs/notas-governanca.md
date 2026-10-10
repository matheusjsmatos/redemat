# Notas de governança — registro interno

Retiradas das páginas públicas em 09/10/2026, por decisão da coordenação.
**As regras continuam valendo.** O que saiu foi o texto que as anunciava.

## 1. Procedência dos dados do diretório de docentes

> Nomes, e-mails e identificadores Lattes provêm da página oficial de docentes
> (`https://redemat.ufop.br/docentes-1`). Categoria, instituição, carga horária
> e bolsa provêm da tabela de corpo docente da proposta APCN 2026. O asterisco
> (*) na linha de pesquisa indica vinculação inferida da responsabilidade por
> disciplina na proposta curricular.

O asterisco **continua** na página. Sem a legenda, ele vira um símbolo sem
significado: quem o vir não tem como saber que marca inferência. Ver pendência
P-07.

## 2. O que não é publicado

> Este diretório não apresenta contagens individuais de produção, captação de
> recursos, índice h ou qualquer pontuação por docente. Análises individuais
> integram instrumento interno de planejamento e não constituem avaliação
> pública do corpo docente.

> E-mails de discentes não constam: não são necessários para a finalidade de
> transparência. Títulos de trabalho em andamento, histórico escolar e qualquer
> avaliação individual também não são publicados.

**Isto é regra de projeto, não texto de página.** O portal segue sem publicar
nada disso, e os scripts que geram os dados seguem filtrando esses campos. O
que mudou é que o visitante deixou de ser informado da política.

## 3. Autorização de uso de imagem

> Cada pessoa precisa autorizar o uso da própria imagem antes da publicação — o
> portal funciona sem foto e exibe as iniciais. Recomenda-se registrar a
> autorização por escrito, conforme a LGPD, antes de publicar a foto de
> docentes, pós-doutorandos e técnicos.

A exigência **permanece**. A coluna `autorizacao` em
`assets/img/pessoas/LISTA-DE-FOTOS.csv` continua em branco para todas as fotos,
e continua sendo o controle. Ver pendência P-02.

## 4. Vinculação de docente a linha de pesquisa

> A arquitetura de duas áreas e quatro linhas está aprovada. A vinculação
> individual, porém, só está nomeada para nove docentes; para os demais, a
> linha exibida foi inferida da responsabilidade por disciplina.

A inferência continua sendo feita e continua sendo exibida — agora sem aviso.
Ver pendência P-07.

---

Retiradas em 10/10/2026, na mesma decisão. Novamente: **o que saiu foi o texto,
não a regra.**

## 5. Vínculos institucionais no exterior

> Vínculos institucionais no exterior extraídos da seção "Atuação Profissional"
> dos currículos Lattes do corpo docente. Contagem de vínculos, não de acordos
> formais vigentes.

O mapa de internacionalização continua contando **vínculos de currículo**, não
convênios. Sem a nota, um leitor pode ler o número como acordos vigentes da
REDEMAT. O dado em si não mudou: `R.paises` segue vindo do Lattes.

## 6. Parceiros: relação histórica e uso de marcas

> **Relação histórica, não portfólio vigente.** Relação de cooperação histórica
> e de financiadores identificados nos projetos do período. O portfólio de
> instrumentos vigentes, com objeto, vigência e resultados, consta como
> pendência e será publicado após consolidação.

> **Sobre os logos.** [aviso de uso de marca registrada de terceiros]

Duas consequências a vigiar:

1. A lista de parceiros segue sendo **histórica**. Se alguém a citar como rede
   ativa em documento de avaliação, o número não sustenta a afirmação.
2. A regra de **não exibir logo de terceiro sem autorização continua valendo**.
   O portal exibe nomes, não marcas. Ver `docs/pendencias.md`.

## 7. Rede de coautoria

> Rede de coautoria entre os docentes do Programa — evidência de integração
> prévia do corpo docente. O desenho e os dados por docente ficam em
> `assets/js/grafo-dados.js`, gerado por `scripts/gerar-grafo.py`.

O grafo continua no ar. O que saiu foi a explicação de que ele mede
**coautoria entre docentes**, e não produção individual.

## 8. Infraestrutura

> **Infraestrutura da instituição associada.** [ficha da UEMG na proposta
> aprovada — PRELIMINAR]

> [aviso de que o inventário de laboratórios não está consolidado]

> Para equipamentos multiusuários e agendamento de análises, o contato é o
> responsável do laboratório — os e-mails estão na página de laboratórios — ou
> a secretaria.

O inventário de laboratórios **segue incompleto**, e a ficha da UEMG segue
sendo PRELIMINAR. O caminho de quem procura equipamento passou a ser só o link
para a página de laboratórios, que permanece na página.

## 9. Prêmios: atribuição, cobertura e o que a lista não é

> **Como os nomes foram atribuídos.** [atribuição por índice de membro no
> relatório ScriptLattes — VALIDADO]

> **Nove dos dez prêmios registrados.** [um prêmio fora do conjunto publicado]

> **O que esta lista não é.** Não é ranking nem medida de desempenho
> individual: prêmio depende de área, de existir premiação na especialidade e
> de quem indica. A ausência de um docente aqui não diz nada sobre o trabalho
> dele.

> **Faltam prêmios aqui?** Provavelmente sim. Prêmio de estudante não fica
> registrado no currículo do orientador, e por isso não é capturado
> automaticamente. A secretaria cadastra caso a caso.

A regra de **não publicar ranking nem desempenho individual continua valendo** —
é a mais importante das que ficaram sem texto. A lista de prêmios de discentes
continua **parcial** por construção: ela depende de informe do orientador.

## 10. Patentes: situação no INPI e por que 8 e não 47

> **Situação de cada processo.** [aviso sobre estágio dos pedidos no INPI]

> **Por que 8 e não 47.** O inventário do Lattes tem 47 patentes únicas. Destas,
> 8 têm descrição de aplicação escrita pelo Programa e são as que aparecem com
> detalhe. As outras constam no currículo sem essa descrição — existem, mas o
> portal não inventaria uma aplicação que ninguém escreveu.

Risco concreto: a página mostra **8** patentes e o Lattes registra **47**. Sem a
nota, a diferença fica sem explicação — e, num processo avaliativo, um número
menor sem justificativa pesa contra o Programa. Recomenda-se decidir entre
publicar as 47 com rótulo de "sem descrição de aplicação" ou reinserir a nota.
Ver `docs/pendencias.md`.
