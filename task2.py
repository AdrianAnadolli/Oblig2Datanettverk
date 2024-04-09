#import socket module
import socket
import argparse

# Bruk dette for å kjøre programmet: python .venv/Client/task2.py -i 127.0.0.1 -p 8080 -f /index.html (kjør server først)
def send_request(server_ip, server_port, filename): #Definerer send_request, tar inn server_ip, server_port og filename som parametere.
    # Denne funksjonen sender en HTTP GET request for filename. Funksjonen får en respons fra serveren og den printer dette ut.

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Lager en ny socket objekt.

    try:
        client_socket.connect((server_ip, server_port)) #Initierer en tilkobling fra klient til server.

        request = f"GET {filename} HTTP/1.1\r\nHost: {server_ip}\r\n\r\n" #Lager en HTTP GET request med filnavn og server IP.
        client_socket.sendall(request.encode()) #Sender HTTP fra klient til server, enkoder i bytes.

        response = client_socket.recv(4096).decode() #Responsen vi får fra server. 4096 er maks størrelse i bytes. Decode dekoderer fra bytes til string.
        print("Server response:") #Printer "Server response"
        print(response) #Printer selve responsen.

    except Exception as e: #Exeption dersom filen ikke finnes.
        print(f"Error: {e}") #Print feilmeldingen.

    finally:
        client_socket.close() #Lukk socket.

def main():

    parser = argparse.ArgumentParser(description='HTTP Client') # Lager en ArgumentParser
    parser.add_argument('-i', '--server_ip', type=str, help='Server IP address or hostname', required=True) # Parser command-line argumenter (IP)
    parser.add_argument('-p', '--server_port', type=int, help='Server port', required=True) # Parser command-line argumenter (Port)
    parser.add_argument('-f', '--filename', type=str, help='Path of the requested file on the server', required=True) # Parser command-line argumenter (filename)
    args = parser.parse_args() #Parser command-line argumentene til args

    send_request(args.server_ip, args.server_port, args.filename) # Sender HTTP request til serveren ved å bruke send_request funksjonen.

if __name__ == "__main__":
    main()