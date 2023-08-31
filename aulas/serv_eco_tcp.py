from socket import *

# um socket que usa IPV4 e TCP
sock = socket(AF_INET, SOCK_STREAM)
end = ("", 3000)
sock.bind(end)

sock.listen(5)

print(f"[Servidor pronto e aguardando requisições: {end}...]")
while True:
    #estabelecimento de conexao (HandShake)
    con, end_cliente = sock.accept()
    print(f"[Conexão Estabelecida com {end_cliente}]")

    # recebe msg de 1024 bytes
    msg = con.recv(1024)
    
    print(f"Mensagem de {end_cliente}: {msg.decode()}")
    con.send(msg.upper())
    con.close()
