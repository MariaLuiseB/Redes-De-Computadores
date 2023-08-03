import socket
# Um socket que usa ipv4 e UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
e = ("", 5001)
sock.bind(e)

print(f"Servidor pronto, aguardando requisições na porta {e}...")
while True:
    msg, cliente = sock.recvfrom(1024) # pega a mensagem e o cliente (tupla de ip e porta de destino) que mandou a mensagem 
    print(f"Mensagem do Cliente: {cliente}: {msg.decode()}")
    sock.sendto(msg.upper(), cliente) # manda mensagem de volta p/ cliente


