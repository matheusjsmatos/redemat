# Pasta `scriptlattes/`

Esta pasta recebe o **relatório ScriptLattes completo**, gerado fora do portal e
sincronizado para dentro dele. Enquanto estiver vazia (só com este arquivo), os
links do bloco "Relatório ScriptLattes" em `pages/producao-lattes.html`
retornam 404 — o que é esperado, não um defeito.

## Como sincronizar

```bash
./scripts/atualizar-scriptlattes.sh ~/Dropbox/claude/redemat/teste-01
```

O caminho é a **pasta de saída do ScriptLattes**. Hoje ela fica em
`C:\Users\mateu\Dropbox\claude\redemat\teste-01` (no WSL/Git Bash,
`~/Dropbox/claude/redemat/teste-01`). A saída original do ScriptLattes fica em
`~/Documentos/softwares/scriptLattes/redemat/teste-01` no WSL — os dois
caminhos servem.

## O que a sincronização faz

1. Valida que a pasta tem cara de saída do ScriptLattes (`index.html`,
   `membros.html`, páginas `membro-*.html`)
2. Copia a versão anterior para `scriptlattes.bak/`
3. Copia o relatório para cá, **já sem** a página do docente formalmente
   excluído do conjunto de 24
4. Troca o rótulo técnico `teste-01` por `REDEMAT` nos títulos
5. Substitui recursos externos que quebram o relatório:
   - `sorttable.js` servido por `http://` de terceiro → cópia local
     `js/sorttable-local.js` (o original é bloqueado como conteúdo misto
     quando o site é servido por HTTPS, e a ordenação morre em silêncio)
   - links `http://lattes.cnpq.br` → `https://`
   - grafo interativo em *applet* Java → aviso apontando para o grafo em SVG
     do portal (nenhum navegador atual executa applet)
6. Injeta `portal-redemat.css` e o link de volta ao portal em cada página
7. Escreve `SYNC.json` com data, origem e inventário
8. Regenera `assets/js/grafo-dados.js` a partir do
   `grafoDeColaboracoesComPesos.dot` desta coleta

## Por que o relatório é independente

O ScriptLattes é um programa próprio (<https://scriptlattes.sourceforge.net/>)
que lê os currículos Lattes e gera o relatório completo. Ele entra no portal
como um **bloco autocontido**: HTML, CSS e JavaScript próprios. O portal não
reescreve nem reinterpreta esse conteúdo — apenas injeta a folha de
legibilidade e o link de retorno.

Consequência prática: atualizar o relatório não mexe no site, e mudar o site
não altera o relatório. O portal publica agregados conferidos; o ScriptLattes
preserva a evidência item a item, com DOI e coautores. É essa separação que
permite auditar qualquer número do portal até o registro de origem no currículo.

## O que a sincronização NÃO faz

- Não roda o ScriptLattes nem baixa currículos. Rode o ScriptLattes antes,
  confira a saída, e só então sincronize.
- Não atualiza os números publicados em `assets/js/site-data.js`. Se a coleta
  mudou os agregados, o script avisa no terminal e a decisão de publicar é da
  coordenação — todo número do portal passa por conferência humana.
- Não apaga arquivos: a exclusão do docente fora do conjunto é feita no filtro
  da cópia, para o script funcionar também onde remover arquivo não é
  permitido.
