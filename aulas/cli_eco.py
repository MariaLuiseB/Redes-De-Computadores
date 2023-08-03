import socket
import sys 

if len(sys.argv) != 3:
    print("Uso: cli_eco.py <ip> <porta>")
    sys.exit(1)
ip = sys.argv[1]
porta = int(sys.argv[2])

sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
    msg = input("Mensagem: ")
    if msg == "s":
        break
    sock.sendto(msg.encode(), (ip, porta))
    msg, end_servidor = sock.recvfrom(1024)
    print(f"Resposta de {end_servidor}: {msg.decode()}")
sock.close()

