#!/usr/bin/env bash
# Roda a importação do acervo até o fim, em segundo plano, com registro.
#
# O servidor do portal antigo bloqueia por ~20 min depois de poucas
# requisições seguidas, então a importação completa leva horas. Este
# invólucro existe para que ela rode sozinha e sobreviva a quedas: se o
# processo morrer, basta chamar de novo — o importador é retomável.
#
#   bash scripts/importar-acervo.sh          # inicia
#   tail -f importacao.log                   # acompanha
set -u
cd "$(dirname "$0")/.."
nohup python3 -u scripts/importar-noticias-antigas.py --ate-acabar --pausa 25 \
      >> importacao.log 2>&1 &
echo "importação iniciada (pid $!). Acompanhe com: tail -f importacao.log"
