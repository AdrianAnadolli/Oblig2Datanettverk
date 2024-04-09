#import socket module
from socket import *
import sys  # In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM) #Dette er hentet fra webserver-task1-skeleton-code.py, dette lager en ny socket objekt.

# Prepare a server socket
serverPort = 8080 #definerer port nummer til 8080
serverSocket.bind(('', serverPort)) #Binder IP adresse og portnummer til serverSocket
serverSocket.listen(1) #serverSocket hører etter tilkoblinger, her bruker vi 1 som argument, dette sørger for at serveren håndterer kun en tilkobling om gangen.

while True:
    # Establish the connection
    print('Ready to serve...') #Printer 'Ready to serve...'
    connectionSocket, addr = serverSocket.accept() #Aksepterer tilkobling fra klient, returnerer en ny socket objekt connectionSocket som brukes for kommunikasjon mellom klienten og adressen til klienten.
    print('Connected by', addr) #Printer "Connected by" også addresse
    try:
        message = connectionSocket.recv(1024) #Tar inn data fra klienten gjennom connectionSocket, argumentet 1024 sørger for at maksimalt buffer størrelse er på 1024 bytes.
        filename = message.split()[1].decode('latin-1').split('\x00')[0] #Splitter meldingen i ord, tar ordet med index 1 og registrerer dette som filename. .decode() dekoder data med latin-1 encoding, konverterer bytestring til unicode.
        # Her fikk jeg error "ValueError: embedded null character", så jeg måtte bruke .split(\x00)[0] til å splitte unicode ved å bruke '\x00' som separator.
        f = open(filename[1:]) #Hentet fra skeleton-code.py. Åpner filename, fjerner første karakter av strengen før den prøver å åpne filename.
        outputdata = f.read() #Leser av f og legger inn i outputdata

        # Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode()) #Sender en HTTP respons header med kode 200/OK

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)): #Dette her er også hentet fra skeleton-code.py. For løkke fra 0 til outputdata sin legde.
            connectionSocket.send(outputdata[i].encode()) #Sender outputdata til klient socket. Encode enkoderer outputdata til bytes
        connectionSocket.send("\r\n".encode())
        connectionSocket.close() #Lukk klient socket

    except IOError:
        #Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode()) #Dersom exception blir kastet ut, sender 404 respons.
        connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n'.encode()) #Dersom exception blir kastet ut, informerer bruker om 404 med bruk av HTML.
        connectionSocket.close() #Lukk klient socket

#Terminate the program after sending the corresponding data
serverSocket.close() #Lukk server socket
sys.exit() #terminer programmet
