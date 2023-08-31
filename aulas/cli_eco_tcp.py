import socket
import sys 

if len(sys.argv) != 3:
    print("Uso: cli_eco_tcp.py <ip> <porta>")
    sys.exit(1)
ip = sys.argv[1]
porta = int(sys.argv[2])

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, porta)) # estabelecimento de conexao com esse ip e essa porta 
msg = input("Mensagem:")
msg = msg + "\n"
sock.send(msg.encode())
 # recebe os dados do buffer com tamanho 1024 
 # e fica travado esperando a resposta 
 # ate o servidor responder
dados = sock.recv(1024) 
sock.close()

