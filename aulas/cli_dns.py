#!/usr/bin/env python3
import sys
import socket 

name = sys.argv[1]

if len(sys.argv) != 2:
    print("Uso: cli_dns.py <none>")
    sys.exit(1)
#obtem o endereço IP do nome 


try:
    ip = socket.gethostbyname(name)
except socket.error:
    print(f"Não foi possivel resolver o nome: {name}")
    sys.exit(1)

print(f"{name}: {ip}")
