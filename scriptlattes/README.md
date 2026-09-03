# Visualizar a tabela de colaborações

Na raiz do projeto, inicie um servidor HTTP local com Python:

```bash
python3 -m http.server 8000 --directory teste-01
```

Depois, acesse no navegador:

<http://localhost:8000/tabela-colaboracoes.html>

Para encerrar o servidor, volte ao terminal e pressione `Ctrl+C`.

## Alternativa

Também é possível entrar primeiro na pasta do site:

```bash
cd teste-01
python3 -m http.server 8000
```

Se a porta `8000` já estiver ocupada, use outra porta, por exemplo `8080`, tanto no comando quanto no endereço do navegador.
