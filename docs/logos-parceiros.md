# Logos de parceiros e órgãos públicos

**Não consigo baixar os arquivos de imagem.** As ferramentas desta sessão leem
páginas web como texto — não trazem binários. Então este documento faz a parte
que dá para fazer: diz exatamente **onde** buscar cada logo, em que **formato**,
e como colocá-lo no lugar certo com um comando.

---

## Órgãos públicos e fundações — prioridade

Todos abaixo têm manual de identidade visual público e permitem uso
institucional com atribuição. Comece por eles.

| Instituição | Arquivo a salvar | Onde obter |
|---|---|---|
| **FAPEMIG** | `fapemig.png` | <https://fapemig.br/pt/comunicacao/logotipos/> — manual de aplicação e PNG/vetor |
| **CNPq** | `cnpq.png` | <https://www.gov.br/cnpq/pt-br/acesso-a-informacao/identidade-visual> |
| **CAPES** | `capes.png` | <https://www.gov.br/capes/pt-br/acesso-a-informacao/identidade-visual> |
| **FINEP** | `finep.png` | <https://www.finep.gov.br/a-finep-externo/identidade-visual> |
| **EMBRAPII** | `embrapii.png` | <https://embrapii.org.br/manual-de-marca/> |
| **UFOP** | já incluído | <https://www.ufop.br/logomarca/> — já está em `assets/img/ufop-logo.png` |
| **UEMG** | já incluído | <https://uemg.br/> — já está em `assets/img/uemg-logo.png` |
| **Fundação Gorceix** | `gorceix.png` | <https://www.gorceix.org.br/> — solicitar à comunicação |
| **CETENE / MCTI** | `cetene.png` | <https://www.gov.br/cetene/pt-br> |

Órgãos federais seguem o **Manual de Identidade Visual do Governo Federal**;
respeite a versão e a área de proteção definidas em cada manual.

---

## Empresas — exigem autorização

Marcas privadas são registradas. O uso no portal precisa de **autorização
prévia** de cada titular, normalmente pela assessoria de comunicação ou pelo
contato do convênio vigente.

| Empresa | Arquivo | Onde pedir |
|---|---|---|
| Vale | `vale.png` | Sala de imprensa / gestor do convênio |
| CEMIG | `cemig.png` | Comunicação corporativa |
| Gerdau | `gerdau.png` | Sala de imprensa |
| Samarco | `samarco.png` | Comunicação |
| ArcelorMittal | `arcelormittal.png` | Comunicação |
| Vallourec | `vallourec.png` | Comunicação |
| Sapura Navegação | `sapura.png` | Contato do projeto |
| CBMM | `cbmm.png` | Comunicação |
| Usiminas | `usiminas.png` | Sala de imprensa |
| Aperam | `aperam.png` | Comunicação |
| Nexa | `nexa.png` | Comunicação |

> Enquanto a autorização não vier, o cartão exibe **apenas o nome** da
> instituição. O portal não fica quebrado nem "faltando" — a ausência de logo é
> um estado previsto do layout.

---

## Especificação do arquivo

- **PNG com fundo transparente** (preferencial) ou SVG convertido para PNG
- Altura de **80 a 120 px**; largura livre
- Peso alvo: até 30 KB por arquivo
- Versão **colorida principal**; evite versões monocromáticas ou negativas
- Não recorte, distorça, gire nem altere as cores da marca

## Onde salvar

```
assets/img/parceiros/<slug>.png
```

O `slug` de cada parceiro está em `assets/js/site-data.js`, no array
`parceiros.itens`. Os cartões passam a exibir o logo automaticamente — nenhum
código precisa mudar.

## Comando para preparar os arquivos

Depois de baixar tudo numa pasta (por exemplo `~/Downloads/logos`), rode:

```bash
python3 scripts/preparar-logos.py ~/Downloads/logos
```

O script casa cada arquivo com o slug do parceiro pelo nome, redimensiona para
120 px de altura, remove fundo branco quando detectado, e grava em
`assets/img/parceiros/`. Ele mostra o que vai fazer antes de gravar.

---

## Registro de autorizações

Sugestão: manter uma planilha simples com quem autorizou o quê e quando.
Se a coordenação mudar, a autorização continua rastreável.

| Instituição | Autorizado por | Data | Escopo | Evidência |
|---|---|---|---|---|
| | | | | |
