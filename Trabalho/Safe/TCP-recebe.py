import socket
import threading
import os

# Endereço e porta do servidor
server_address = ('192.168.1.110', 65000)

# Pasta para salvar os arquivos recebidos
received_files_folder = "received_files"

# Dicionário para mapear nomes de clientes para seus sockets
client_sockets = {
    'taina': ('192.168.1.119', 65000)
}

# Função para enviar arquivos para um cliente

# Função para enviar arquivos para um cliente
def send_file(client_socket, file_name):
    try:
        file_path = os.path.join(received_files_folder, file_name)
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)
        print(f"Arquivo '{file_name}' enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar o arquivo '{file_name}': {str(e)}")
    finally:
        client_socket.close()

# Função para lidar com a conexão de um cliente
def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        if request.startswith("SEND"):
            _, file_name = request.split()
            save_file(client_socket, file_name)
        elif request.startswith("CONNECT"):
            client_name = request.split()[1]
            client_sockets[client_name] = client_socket
            print(f"Cliente '{client_name}' conectado.")
        elif request.startswith("LIST"):
            client_list = ", ".join(client_sockets.keys())
            client_socket.send(client_list.encode('utf-8'))
        elif request.startswith("UPLOAD"):
            _, file_name = request.split()
            save_file(client_socket, file_name)
    except Exception as e:
        print(f"Erro ao lidar com o cliente: {str(e)}")
    finally:
        client_socket.close()

# Função para receber e salvar arquivos do cliente
def save_file(client_socket, file_name):
    try:
        file_path = os.path.join(received_files_folder, file_name)
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print(f"Arquivo '{file_name}' recebido e salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao receber e salvar o arquivo '{file_name}': {str(e)}")

# Função para permitir que o usuário envie arquivos
def send_files():
    while True:
        print("\nClientes conectados:")
        for client_name in client_sockets.keys():
            print(client_name)
        client_name = input(
            "Digite o nome do cliente para enviar o arquivo (ou 'LIST' para listar clientes): ")

        if client_name == 'LIST':
            list_clients()
        elif client_name in client_sockets:
            file_name = input(
                "Digite o nome do arquivo local que deseja enviar: ")
            if os.path.exists(file_name):
                # Enviar o arquivo para o cliente
                with open(file_name, 'rb') as file:
                    file_name = os.path.basename(file_name)
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect(client_sockets[client_name])
                    client_socket.send(f"SEND {file_name}".encode('utf-8'))
                    print(f"Enviando arquivo '{file_name}' para {client_name}.")
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        client_socket.send(data)
                    print(f"Arquivo '{file_name}' enviado com sucesso para {client_name}.")
                    
            else:
                print("O arquivo local não existe.")
        else:
            print("Cliente não encontrado. Verifique o nome e tente novamente.")

# Função para listar clientes conectados
def list_clients():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp_socket:
        temp_socket.connect(server_address)
        temp_socket.send(b"LIST")
        data = temp_socket.recv(1024).decode('utf-8')
        print(f"Clientes conectados: {data}")

# Função para aceitar conexões de clientes
def accept_connections():
    # Configurar a pasta para salvar os arquivos recebidos
    if not os.path.exists(received_files_folder):
        os.makedirs(received_files_folder)

    # Configurar o socket do servidor TCP para receber conexões
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(server_address)
        server_socket.listen(5)
        print("Servidor TCP aguardando conexões para transferência de arquivos...")

        while True:
            client_socket, _ = server_socket.accept()
            client_handler_thread = threading.Thread(
                target=handle_client, args=(client_socket,))
            client_handler_thread.start()

# Função principal do servidor
def main():
    # Iniciar a thread para aceitar conexões de clientes
    accept_thread = threading.Thread(target=accept_connections)
    accept_thread.start()

    # Iniciar a thread para permitir o envio de arquivos pelo usuário
    send_thread = threading.Thread(target=send_files)
    send_thread.start()

if __name__ == "__main__":
    main()