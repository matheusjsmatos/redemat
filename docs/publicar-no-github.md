# Publicar o portal no GitHub

Repositório: <https://github.com/matheusjsmatos/redemat> · branch `main`

O repositório local **já está pronto**: `git init` feito, `.gitignore` no lugar,
primeiro commit criado e o endereço remoto configurado. Falta só o envio, que
tem de sair do Windows — o ambiente onde o assistente trabalha não tem rede
para o GitHub.

---

## Passo 0 — ver o que já existe na máquina

Abra o **PowerShell** (tecla Windows, digite `powershell`) e cole:

```powershell
git --version
```

- **Respondeu algo como `git version 2.x`** → o git está instalado. Pode seguir
  pelo Caminho A (GitHub Desktop, se o tiver) ou pelo Caminho B (linha de
  comando).
- **Deu erro "não é reconhecido"** → o git não está instalado. O Caminho A
  instala o que precisa junto.

Para saber se o GitHub Desktop está instalado, procure "GitHub Desktop" no menu
Iniciar.

---

## Caminho A — GitHub Desktop (mais simples)

Recomendado se você não usa git no dia a dia: a autenticação acontece dentro do
aplicativo, sem token nem senha no terminal.

1. Se não tiver, instale de <https://desktop.github.com> e entre com sua conta
   do GitHub.
2. **File → Add local repository…**
3. Aponte para `C:\Users\mateu\Dropbox\claude\redemat-portal` e confirme.
   O Desktop reconhece o repositório existente — não crie um novo.
4. No topo aparecerá **Push origin** (e não "Publish repository", porque o
   endereço remoto já está configurado). Clique.

Pronto. O primeiro envio leva alguns minutos: são 16 MB.

---

## Caminho B — linha de comando

No PowerShell:

```powershell
cd "$env:USERPROFILE\Dropbox\claude\redemat-portal"
git push -u origin main
```

Na primeira vez o Git abre o navegador para você autorizar a conta. Depois disso
ele lembra.

> Se pedir usuário e senha no terminal, **cancele** (Ctrl+C) e instale o Git
> Credential Manager, ou use o Caminho A. Senha do GitHub não funciona mais
> para push, e token colado no terminal fica gravado no histórico.

---

## Passo 1 — limpar 10 MB de arquivos temporários

O repositório foi preparado num ambiente que não tem permissão para apagar
arquivos, e o git deixou 271 arquivos temporários dentro de `.git/`. São
inertes — o `git fsck` não aponta erro — mas ocupam 10 MB e o Dropbox
sincroniza cada um deles.

Depois do primeiro push, rode uma vez:

```powershell
cd "$env:USERPROFILE\Dropbox\claude\redemat-portal"
git gc --prune=now
```

---

## Passo 2 — ativar o GitHub Pages

No repositório, **Settings → Pages**:

- **Source:** Deploy from a branch
- **Branch:** `main` · pasta `/ (root)` → **Save**

Em um ou dois minutos o portal fica em:

**<https://matheusjsmatos.github.io/redemat/>**

O que já está preparado para isso:

- **`.nojekyll`** na raiz — sem ele o GitHub tenta processar o site como Jekyll
  e ignora arquivos e pastas que começam com sublinhado.
- **Nenhum caminho absoluto.** Pages serve o site em `/redemat/`, não na raiz do
  domínio; um `src="/assets/..."` quebraria. Todos os caminhos do portal são
  relativos — conferido.
- **`noindex` automático no github.io.** Enquanto o endereço for
  `matheusjsmatos.github.io`, cada página declara `noindex, nofollow`: são duas
  cópias do mesmo conteúdo na internet, e a que não deve aparecer na busca é a
  prévia. Quem tem o link abre normalmente — não é controle de acesso. A
  verificação é pelo domínio, então **se desliga sozinha** quando o portal for
  para redemat.ufop.br. Está em `assets/js/components.js`, no topo.

---

## Enviar alterações depois

**GitHub Desktop:** as mudanças aparecem na aba Changes; escreva um resumo,
clique em **Commit to main** e depois em **Push origin**.

**Linha de comando:**

```powershell
cd "$env:USERPROFILE\Dropbox\claude\redemat-portal"
git add -A
git commit -m "descreva o que mudou"
git push
```

---

## Duas ressalvas que valem saber

**O repositório está dentro do Dropbox.** Funciona, e é conveniente ter backup
automático, mas Dropbox e git escrevem nos mesmos arquivos de controle. Editar a
mesma pasta em duas máquinas ao mesmo tempo pode corromper o `.git`. Se isso
acontecer, o conserto é clonar de novo do GitHub — que é justamente para o que
o repositório serve. Trabalhando em uma máquina por vez, não há problema.

**O que está publicado é público.** O repositório é público por escolha, com as
fotos de pessoas incluídas — decisão registrada em `docs/CHANGELOG.md`. Vale
lembrar de duas coisas:

- O Git **guarda histórico**: remover uma foto num commit futuro não a apaga dos
  commits anteriores, que continuam acessíveis. Tirar uma imagem do histórico
  exige reescrever a história do repositório e forçar o push.
- As pessoas fotografadas provavelmente não sabem que suas fotos estão numa
  página pública. Um aviso por e-mail resolve, e é o momento natural de colher a
  autorização de imagem que a coluna `autorizacao` do
  `assets/img/pessoas/LISTA-DE-FOTOS.csv` existe para registrar.
