import socket
import threading
import os

# Endereço e porta do servidor de nomes
name_server_address = ('localhost', 12345)

# Endereço e porta do servidor
server_address = ('192.168.1.110', 65000)

# Pasta para salvar os arquivos recebidos e enviados
received_files_folder = "received_files"

# Função para lidar com a conexão de um cliente


def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        if request.startswith("SEND"):  # SEND nome_do_arquivo
            _, file_name = request.split()
            save_file(client_socket, file_name)
        elif request.startswith("CONNECT"):  # CONNECT nome_do_cliente
            client_name = request.split()[1]
            client_sockets[client_name] = client_socket
            print(f"Cliente '{client_name}' conectado.")
    except Exception as e:
        print(f"Erro ao lidar com o cliente: {str(e)}")
    finally:
        client_socket.close()


def register_with_name_server():
    # Cria um socket UDP para broadcasting
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Envia uma mensagem de broadcast
    request = f"REGISTER ATA {server_address[0]} {server_address[1]}"
    broadcast_socket.sendto(request.encode('utf-8'), name_server_address)
    print("Mensagem de broadcast enviada.\n")
    # Aguarda uma resposta do servidor de nomes
    data, _ = broadcast_socket.recvfrom(1024)
    # Decodifica a mensagem do servidor de nomes
    response = data.decode('utf-8')
    # Verifica se o servidor de nomes respondeu com o endereço e a porta do servidor ATA
    if response.startswith("ATA"):
        _, ata_ip, ata_port = response.split()
        ata_port = int(ata_port)
        ata_server_address = (ata_ip, ata_port)
        print(f"Servidor ATA encontrado no endereço {ata_server_address}.\n")
    else:
        print("Servidor ATA não encontrado.\n")


def list_registered_names():
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Envia uma mensagem de broadcast
    request = f"LIST"
    try:
        serv_socket.sendto(request.encode('utf-8'), name_server_address)
        # Aguarda uma resposta do servidor de nomes
        data, _ = serv_socket.recvfrom(1024)
        # Decodifica a mensagem do servidor de nomes
        response = data.decode('utf-8')
        print(response)
        serv_socket.close()
    except Exception as e:
        print(f"Erro ao listar nomes registrados: {str(e)}")
        serv_socket.close()


def save_file(client_socket, file_name):
    try:
        file_path = os.path.join(received_files_folder, file_name)
        file_name = os.path.basename(file_name)
        print(f"Recebendo arquivo '{file_name}'...")
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"Arquivo '{file_name}' recebido e salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao receber e salvar o arquivo '{file_name}': {str(e)}")


def send_files():
    # Consultar cliente_name no servidor de nomes
    client_name = "192.168.1.119"
    print(client_name)
    file_name = input(
        "Digite o caminho completo do arquivo local que deseja enviar:\n")
    if os.path.exists(file_name):
        # Enviar o arquivo para o cliente
        with open(file_name, 'rb') as file:
            print(
                f"Enviando arquivo '{file_name}' para {client_name}.")
            file_name = os.path.basename(file_name)
            client_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((client_name, 65000))
            print(
                f"Enviando arquivo '{file_name}' para {client_name}.")
            client_socket.send(f"SEND {file_name}".encode('utf-8'))
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)
            client_socket.send(f"SEND {file_name}".encode('utf-8'))
            print(
                f"Arquivo '{file_name}' enviado com sucesso para {client_name}.")

    else:
        print("O arquivo local não existe.")


def accept_connections():
    # Configurar a pasta para salvar os arquivos recebidos
    if not os.path.exists(received_files_folder):
        os.makedirs(received_files_folder)

    # Configurar o socket do servidor TCP para receber conexões
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(server_address)
        server_socket.listen(5)
        print("Servidor TCP aguardando conexões para transferência de arquivos...\n")

        while True:
            client_socket, _ = server_socket.accept()
            client_handler_thread = threading.Thread(
                target=handle_client, args=(client_socket,))
            client_handler_thread.start()

# Função principal do servidor


def resolve():
    # faz consulta no dns e resolve o nome do servidor
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(5)
    nome = input("Digite o nome que deseja resolver: ")
    request = f"RESOLVE {nome}"
    udp_socket.sendto(request.encode('utf-8'), name_server_address)
    response, _ = udp_socket.recvfrom(1024)
    print("\nResposta do servidor:\n", response.decode('utf-8'))
    return response.decode('utf-8')
    udp_socket.close()


def cadastrar():
    # Cadastra o nome do servidor no servidor de nomes
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(5)

    client_name = input("Digite o nome que deseja registrar: ")
    client_ip = input("Digite o IP associado ao nome: ")
    request = f"REGISTER {client_name} {client_ip}"
    # Envia a solicitação para o servidor de nomes
    udp_socket.sendto(request.encode('utf-8'), name_server_address)

    # Recebe a resposta do servidor
    response, _ = udp_socket.recvfrom(1024)
    print("\nResposta do servidor:\n", response.decode('utf-8'))
    udp_socket.close()


def main():
    # Iniciar a thread para aceitar conexões de clientes
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.start()

    # Cria um socket UDP para broadcasting
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Envia uma mensagem de broadcast
    request = f"REGISTER"
    ata_server_address = ('localhost', 12345)
    ata_name = 'ATA'
    request = f"REGISTER {ata_name} {ata_server_address[0]}"
    udp_socket.sendto(request.encode('utf-8'), name_server_address)

    udp_socket.close()

    while True:
        print("----------------------------------------------")
        print("\nEscolha uma opção:\n")
        print("1. Registrar Nome")
        print("2. Resolver Nome")
        print("3. Listar Nomes Registrados")
        print("4. Enviar Arquivo")
        print("5. Sair")
        print("----------------------------------------------")
        choice = input("Escolha uma opção (1/2/3/4/5): \n\n")

        if choice == '1':
            cadastrar()
        elif choice == '2':
            resolve()
        elif choice == '3':
            list_registered_names()
            request = f"LIST"
        elif choice == '4':
            send_files()
        elif choice == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")
            continue
    # Encerrar a thread para aceitar conexões de clientes
    accept_thread.join()
    print("Servidor encerrado.")


if __name__ == "__main__":
    main()
