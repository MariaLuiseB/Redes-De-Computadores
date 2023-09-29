import socket

# Endereço e porta do servidor de nomes
server_address = ('localhost', 12345)

# Criação de um socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    print("\nEscolha uma opção:\n")
    print("1. Registrar Nome")
    print("2. Resolver Nome")
    print("3. Listar Nomes Registrados")
    print("4. Enviar Arquivo")
    print("5. Sair")
    choice = input("Escolha uma opção (1/2/3/4/5): \n\n")

    if choice == '1':
        client_name = input("Digite o nome que deseja registrar: ")
        client_ip = input("Digite o IP associado ao nome: ")
        request = f"REGISTER {client_name} {client_ip}"
    elif choice == '2':
        client_name = input("Digite o nome que deseja resolver: ")
        request = f"RESOLVE {client_name}"
    elif choice == '3':
        request = f"LIST"
    elif choice == '4':
        client_file = input("Digite o nome do arquivo que deseja enviar: ")
        request = f"SEND {client_file}"
    elif choice == '5':
        break
    else:
        print("Opção inválida. Tente novamente.")
        continue

    # Envia a solicitação para o servidor de nomes
    client_socket.sendto(request.encode('utf-8'), server_address)

    # Recebe a resposta do servidor
    response, _ = client_socket.recvfrom(1024)
    print("\nResposta do servidor:\n", response.decode('utf-8'))

# Fecha o socket do cliente
client_socket.close()
