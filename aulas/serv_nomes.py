from socket import *
import platform 
import json 

porta = 65001
serv_socket = socket(AF_INET, SOCK_DGRAM)
serv_socket.bind(('', porta))
print(f"Servidor de nomes iniciado: {serv_socket.getsockname()}")

host={}
host['maria'] = '10.1.17.43'
host['taina'] = '5.10.7.88'

def get_2nd_arg(msg):
    parts = msg.split()[1]
    if len(parts) == 2: # msg vai ter duas partes 
        return parts[1].strip()

while True:
    msg, end_cli = serv_socket.recvfrom(2048) # retorna lista com dois argumentos: a msg e o end do cliente 
    print(f"Recebido de: {end_cli}: {msg.decode()}")
    if msg.decode().upper().strip() == 'INFO':
        resposta = "10 - OK para INFO"
        resposta += json.dumps(platform.uname()._asdict())

    elif msg.decode().upper().strip() == 'LIST':
        resposta = "10 OK para LIST"
        resposta += json.dumps(host)

    elif msg.decode().upper().startswith('INSERT '): 
        nome = get_2nd_arg(msg) 
        if get_2nd_arg(msg) in host: 
            resposta = "10 OK \n"
            resposta += host[nome]
        else: 
            "0 - Nome não encontrado\n"
        


    elif msg.decode().upper().startswith('RESOLVE '): 
        resposta = "10 OK para RESOLVE"
    else:
        resposta = '[ERRO] 13 - Requisição Inválida\n'

    #enviar respota
    serv_socket.sendto(resposta.encode(), end_cli)



