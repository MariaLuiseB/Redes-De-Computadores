import socket

# Configuração do servidor de nomes
PORT = 65000  # Porta para comunicação de broadcasting
BUFFER_SIZE = 1024  # Tamanho do buffer para receber mensagens

# Cria um socket TCP para broadcasting
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# Permite que o socket seja reutilizado pelo SO para evitar erros de endereço em uso
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server_socket.bind(('', PORT))
server_socket.listen(1) 

print("Servidor de Nomes iniciado. Aguardando registros...")

while True:
    # Aguarda uma conexão TCP
    client_conn, client_addr = server_socket.accept()
    print(f"Conexão estabelecida com {client_addr}")

    # Recebe dados do cliente
    data = client_conn.recv(BUFFER_SIZE).decode()
    print(f"Recebido registro de {client_addr}: {data}")

    # Aqui você pode adicionar lógica para processar o registro recebido e responder, se necessário.
    # Por exemplo, você pode enviar uma mensagem de confirmação de registro de volta ao cliente.
    response = "Registro bem-sucedido!"
    client_conn.send(response.encode())

    # Fecha a conexão com o cliente
    client_conn.close()