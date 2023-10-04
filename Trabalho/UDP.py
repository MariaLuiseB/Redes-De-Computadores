import socket

# Dicionário para armazenar os registros de nome e IP
name_to_ip = {}

# Endereço e porta do servidor de nomes
server_address = ('localhost', 12345)

# Criação de um socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Vincula o socket ao endereço e à porta do servidor
server_socket.bind(server_address)

print("Servidor de nomes iniciado. Aguardando conexões...")

while True:
    # Espera por solicitações dos clientes
    data, client_address = server_socket.recvfrom(1024)

    # Decodifica a mensagem do cliente
    request = data.decode('utf-8')

    # Verifica o tipo de solicitação do cliente
    if request.startswith("REGISTER"):
        # Formato da solicitação: REGISTER nome_do_cliente ip_do_cliente
        _, client_name, client_ip = request.split()

        # Verifica se o nome já está em uso
        if client_name in name_to_ip:
            response = "\nNome já registrado para outro IP, tente novamente.\n."
        else:
            name_to_ip[client_name] = client_ip
            response = "Registro bem-sucedido."
    elif request.startswith("RESOLVE"):
        # Formato da solicitação: RESOLVE nome_do_cliente
        _, client_name = request.split()

        # Tenta encontrar o IP associado ao nome
        if client_name in name_to_ip:
            response = name_to_ip[client_name]
        else:
            response = "Nome não encontrado."

    elif request.startswith("LIST"):

        # Formato da solicitação: LIST
        response = "\n"

        # Lista todos os nomes registrados
        for name, ip in name_to_ip.items():
            response += f"{name} {ip}\n"

    else:
        response = "Comando inválido."

    server_socket.sendto(response.encode('utf-8'), client_address)

    try:
        # Espera por solicitações dos clientes
        data, client_address = server_socket.recvfrom(1024)

        # Decodifica a mensagem do cliente
        request = data.decode('utf-8')

        # Verifica o tipo de solicitação do cliente
        if request.startswith("REGISTER"):
            # Formato da solicitação: REGISTER nome_do_cliente ip_do_cliente
            _, client_name, client_ip = request.split()

            # Verifica se o nome já está em uso
            if client_name in name_to_ip:
                response = "\nNome já registrado para outro IP, tente novamente.\n."
            else:
                name_to_ip[client_name] = client_ip
                response = "Registro bem-sucedido."
        elif request.startswith("RESOLVE"):
            # Formato da solicitação: RESOLVE nome_do_cliente
            _, client_name = request.split()

            # Tenta encontrar o IP associado ao nome
            if client_name in name_to_ip:
                response = name_to_ip[client_name]
            else:
                response = "Nome não encontrado."

        elif request.startswith("LIST"):

            # Formato da solicitação: LIST
            response = "\n"

            # Lista todos os nomes registrados
            for name, ip in name_to_ip.items():
                response += f"{name} {ip}\n"

        else:
            response = "Comando inválido."

        server_socket.sendto(response.encode('utf-8'), client_address)

    except Exception as e:
        print(f"Erro ao processar a solicitação do cliente: {e}")
        
        # Fecha o socket do servidor    
        server_socket.close()
        break
    
    # Fecha o socket do servidor    
    server_socket.close()
