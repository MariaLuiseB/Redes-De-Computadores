import socket
import os
import threading

# Endereço e porta do servidor de nomes
name_server_address = ('localhost', 12345)

# Endereço e porta do servidor ATA
ata_server_address = None

# Pasta para salvar os arquivos recebidos
received_files_folder = "received_files"

# Função para procurar e se registrar no servidor de nomes via broadcas
def register_with_name_server():
    # Cria um socket UDP para broadcasting
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # Envia uma mensagem de broadcast
    ata_nome = "ATA"
    ata_ip = "localhost"
    request = f"REGISTER {ata_nome} {ata_ip}"
    broadcast_socket.sendto(request.encode('utf-8'), name_server_address)
    
    print("Mensagem de broadcast enviada.")
    
    # Aguarda uma resposta do servidor de nomes
    data, _ = broadcast_socket.recvfrom(1024)
    print("Resposta do servidor de nomes recebida.")
    
    # Decodifica a mensagem do servidor de nomes
    response = data.decode('utf-8')
    
    # Verifica se o servidor de nomes respondeu com o endereço e a porta do servidor ATA
    if response.startswith("ATA"):
        _, ata_ip, ata_port = response.split()
        ata_port = int(ata_port)
        ata_server_address = (ata_ip, ata_port)
        print(f"Servidor ATA encontrado no endereço {ata_server_address}.")
    else:
        print("Servidor ATA não encontrado.")
    
    
# Função para listar nomes registrados no servidor de nomes
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
    
# Função para enviar arquivos para o servidor ATA
def send_file(file_name):
    # Cria um socket TCP para enviar o arquivo para um nome que será resolvido pelo servidor de nomes
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ata_client_socket:
        # Resolve o nome do servidor ATA
        ata_client_socket.connect(ata_server_address)
        print(f"Conexão estabelecida com {ata_server_address}.")
        
        # Envia o nome do arquivo para o servidor ATA
        ata_client_socket.send(file_name.encode('utf-8'))
        
        # Abre o arquivo a ser enviado
        with open(file_name, 'rb') as file:
            while True:
                # Lê os dados do arquivo
                data = file.read(1024)
                if not data:
                    break
                # Envia os dados para o servidor ATA
                ata_client_socket.sendall(data)
        print(f"Arquivo '{file_name}' enviado com sucesso.")
        ata_client_socket.close()
        

# Função para receber arquivos
def receive_file(client_socket, file_name):
    try:
        with open(os.path.join(received_files_folder, file_name), 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"Arquivo '{file_name}' recebido com sucesso.")
    except Exception as e:
        print(f"Erro ao receber o arquivo '{file_name}': {str(e)}")
    finally:
        client_socket.close()

# Função principal da thread de recepção de arquivos
def receive_files():
    if not os.path.exists(received_files_folder):
        os.makedirs(received_files_folder)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ata_server_socket:
        ata_server_socket.bind(('', 0))
        ata_server_socket.listen(5)
        print(f"Servidor ATA iniciado no endereço {ata_server_socket.getsockname()}.")

        while True:
            client_socket, client_address = ata_server_socket.accept()
            print(f"Conexão estabelecida com {client_address}.")

            file_name = client_socket.recv(1024).decode('utf-8')
            print(f"Recebido pedido de download do arquivo '{file_name}'.")

            file_thread = threading.Thread(target=receive_file, args=(client_socket, file_name))
            file_thread.start()
        
    
# Função principal do cliente ATA
def main():
    
    register_with_name_server()

    receiver_thread = threading.Thread(target=receive_files)
    receiver_thread.start()

    while True:
        print("\nEscolha uma opção:\n")
        print("1. Listar Nomes Registrados")
        print("2. Enviar Arquivo")
        print("3. Sair")
        choice = input("Escolha uma opção (1/2/3):\n\n")

        if choice == '1':
            list_registered_names()
        elif choice == '2':
            file_name = input("Digite o nome do arquivo local: ")
            send_file(file_name)
        elif choice == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
