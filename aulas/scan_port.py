#!/usr/bin/env python3
from socket import *
import sys

if len(sys.argv) != 2:
    print("Uso: scan_port.py <servidor>")
    sys.exit(1)

alvo = sys.argv[1]

print("--" * 50)
print("Scan Port V 0.1b")

# scanport vai tentar conectar com as portas de um servidor
# através de uma conexao TCP

for porta in range(70, 1024):  # tentar conectar com portas de 1 até 1024
    # um socket IPV4 e TCP
    sock = socket(AF_INET, SOCK_STREAM)
    sock.settimeout(1)
    # se o socket não responder nada, o servidor assume que a porta está fechada
    # estabelecimento de conexão(handshake)
    codigo = sock.connect_ex((alvo, porta))  # pedindo pro servidor

    if codigo == 0:
        servico = getservbyport(porta)
        print(f"[Porta {porta} - {servico}: aberta]")
    else:
        print(f"Porta {porta}: Fechada")
    sock.close()
