#import socket module
import socket
import os
import threading


def handle_client(client_socket): #Definerer handle_client, tar inn client socket som parameter. Funksjonen handle_client handler kommunikasjon med klienten ved å ta inn en HTTP request og sjekke om filen klienten ber om finnes. Dersom
    #filen finnes vil vi returnere en respons med status 200, men dersom filen ikke finnes vil vi sende en 404 error i stedet.

    request_data = client_socket.recv(1024).decode() #Tar inn HTTP request fra klienten

    request_lines = request_data.split('\r\n') # Splitter HTTP request i individuelle linjer.
    request_line = request_lines[0] # Registrerer første linje i HTTP requesten som request_line.
    request_method, file_path, _ = request_line.split(' ') # Henter request method og file_path fra request_line.

    file_path = '.' + file_path # Legger til en "." i file_path (/index.html blir til ./index.html)

    if os.path.exists(file_path): # Sjekker om file_path finnes.
        with open(file_path, 'rb') as file: # Åpner file_path
            file_content = file.read() # Legger innhold i file_content

        # Sender en respons med status 200-OK.
        response_headers = "HTTP/1.1 200 OK\r\n" # Angir HTTP-responsens statuslinje med status 200.
        response_headers += "Content-Type: text/html\r\n" # Legger til Content-Type header i HTTP responsen, innholdet er av typen text/html.
        response_headers += "Content-Length: {}\r\n\r\n".format(len(file_content)) # Legger til Content-Length header i HTTP-responsen, dette angir lengden på innholdet i bytes.
        response = response_headers.encode() + file_content # Kombinerer alle headers for å danne den endelige HTTP responsen.
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode() # Sender en 404 respons dersom filen ikke finnes.

    client_socket.sendall(response) # Sender HTTP respons til klienten
    client_socket.close() #Lukker klient socket


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Lager server socket
    server_socket.bind(('localhost', 8080)) # Binder socket til localhost:8080

    server_socket.listen(5) # Hører etter tilkoblinger, 5 her er maks tilkoblinger.
    print("Listening on port 8080...") # Printer "Listening on port 8080..."

    while True:
        client_socket, client_address = server_socket.accept() #Aksepterer tilkobling fra klient.
        print("Accepted connection from:", client_address) # Printer "Accepted connection from:" og addressen til klienten.

        client_thread = threading.Thread(target=handle_client, args=(client_socket,)) # Oppretter en ny tråd som skal utføre handle_client-funksjonen. Tar inn handle_client og klient-socketen som argumenter.
        client_thread.start() # Starter tråden for å håndtere kommunikasjon med klienten.


if __name__ == "__main__":
    main()
