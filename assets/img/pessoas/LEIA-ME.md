# Fotos de pessoas

Esta pasta guarda as fotos de **docentes**, **pós-doutorandos** e da
**secretaria e equipe técnica** — as três populações que o portal exibe em
cartão com foto.

## Nome do arquivo

`<slug>.<formato>`, onde o slug é o nome sem acentos, em minúsculas, com
hífens:

| Pessoa | Papel | Arquivo |
|---|---|---|
| Geraldo Lúcio de Faria | Docente | `geraldo-lucio-de-faria.jpg` |
| Taíse Matte Manhabosco | Docente | `taise-matte-manhabosco.jpg` |
| Adarlêne Moreira Silva | Pós-doutoranda | `adarlene-moreira-silva.webp` |
| Rodrigo Cesário Lourenço | Secretário | `rodrigo-cesario-lourenco.png` |

Para ver a lista completa, com o slug exato de cada pessoa:

```bash
python3 scripts/conferir-fotos.py --csv
```

## Formatos aceitos

`jpg` · `jpeg` · `png` · `webp` · `gif` · `avif`

Basta **um** deles por pessoa. Se houver mais de um arquivo para a mesma
pessoa, o portal usa o primeiro dessa ordem e o script avisa da duplicata —
dois arquivos para a mesma pessoa costuma ser troca de foto feita pela metade.

Sobre **GIF**: funciona, inclusive animado. Mas o portal **não consegue
pausá-lo** — CSS não interrompe a animação de um GIF, nem para quem pediu
`prefers-reduced-motion` no sistema. Para retrato institucional, prefira
imagem estática; se usar animado, que seja curto e discreto.

Sobre **WebP** e **AVIF**: pesam menos com a mesma qualidade e são suportados
por qualquer navegador atual. Boa escolha se você estiver gerando as imagens.

## Depois de adicionar ou trocar fotos

```bash
python3 scripts/conferir-fotos.py --manifesto
```

Isso regrava `fotos.js`, que declara quem tem foto e em que formato.

**Esse passo não é opcional.** O portal confia no manifesto: quem não está
declarado ali vai direto para as iniciais, e uma foto largada na pasta **não
aparece** até o script rodar de novo. A alternativa — sondar os seis formatos
para cada uma das 28 pessoas — custaria mais de cem requisições 404 em cada
carregamento de página enquanto ninguém tiver foto, e foi por isso que se
escolheu o manifesto.

Se esquecer, o próprio portal avisa: com o manifesto vazio ele escreve no
console do navegador a linha de comando a rodar.

## Duas armadilhas que o script pega

**Renomear a extensão não converte o arquivo.** Salvar um JPEG como `.gif` faz
a foto funcionar no Chrome — que fareja o conteúdo — e falhar em servidor que
envia `X-Content-Type-Options: nosniff`, coisa comum em hospedagem
institucional. O script lê os primeiros bytes e diz qual é o formato de
verdade. Para converter mesmo, use um editor de imagem ou:

```bash
python3 -c "from PIL import Image; Image.open('foto.gif').convert('RGB').save('foto.jpg', quality=82)"
```

**Peso.** O cartão mostra a foto num círculo de 48 px. Um retrato de 600 KB
gasta banda de todo visitante e não fica mais nítido. O script avisa acima de
300 KB.

## Especificação

- Recorte **quadrado**, mínimo 400×400 px — mas não é obrigatório: o portal
  recorta pelo alto (`object-fit: cover` com `object-position: center top`), que
  é o enquadramento certo para retrato. Foto em pé funciona bem.
- Enquadramento de rosto e ombros, fundo neutro. Foto de corpo inteiro ou de
  palestra fica com o rosto pequeno no círculo de 48 px.
- Arquivos de 40–120 KB dão conta (JPG qualidade 80–85, ou WebP)

## Antes de publicar

Cada pessoa precisa **autorizar por escrito o uso da própria imagem**, conforme
a LGPD. A coluna `autorizacao` do `LISTA-DE-FOTOS.csv` existe para isso e fica
em branco de propósito: o portal não sabe quem autorizou.

O portal funciona sem foto nenhuma — quem não tiver arquivo aparece com as
iniciais sobre a cor da sua linha de pesquisa, sem alteração de layout.

## Arquivos gerados

- `fotos.js` — manifesto lido pelo portal. **Não editar à mão.**
- `LISTA-DE-FOTOS.csv` — a lista para conferência e controle de autorização.
