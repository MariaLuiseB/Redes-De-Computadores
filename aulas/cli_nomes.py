from socket import *
import sys
import json

porta = 65000
ip = "10.1.17.103"

if len(sys.argv) < 2:
    print("Uso: {sys.argv[0]} <tipo de requisicao>")
    print("INFO\nLIST\nINSERT <nome>\nRESOLVE <nome>")
    sys.exit(1)

serv_socket = socket(AF_INET, SOCK_DGRAM)
cmd = sys.argv[1].upper()

if cmd.startswith("INFO") or cmd.startswith("LIST"):
    msg = cmd
    print(f"[Enviando {msg}]")
    serv_socket.sendto(msg.encode(), (ip, porta))
    msg, end_servidor = serv_socket.recvfrom(1024)
    print(f"[Resposta de {end_servidor}: {msg.decode()}]")

elif cmd.startswith("INSERT") or cmd.startswith("RESOLVE"):
    msg = cmd + " " + sys.argv[2]  # recebe o segundo argumento
    serv_socket.sendto(msg.encode(), (ip, porta))  # envia para a msg o ip e porta
    print(f"[Enviando {msg}]")
    msg, end_servidor = serv_socket.recvfrom(1024)  #
    print(f"[Resposta de {end_servidor}: {msg.decode()}]")

else:
    print(f"[Comando Inválido: {cmd}]")
    sys.exit(1)


# gera uma requisicao LIST e imprime o resultado na tela
# while 1:
#     msg = input
#     if msg == 'INFO':
#         msg = serv_socket.recvfrom(1024)
#         serv_socket.sendto(msg.encode(), (ip,porta))


serv_socket.close()
