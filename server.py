#librerias que ocupamos
import socket
import os


#configuración de nuestro servidor

HOST = '172.20.10.5'  #direccion de la interfaz de loopback estándar (localhost) Dirección IP del servidor
PORT = 12345  #puerto utilizado por el servidor Puerto que usa el cliente (los puertos sin provilegios son > 1023)
DIRECTORY = './audio_files/'  #directorio donde se guardarán los archivos de audio recibidos
buffer_size = 1024 #tamaño del buffer



#crear el socket del servidor

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creamos nuestro socket
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Creamos nuestro socket
socket_server.bind((HOST, PORT)) #creamos el canal de comunicación entre el puerto y el socket
socket_server.listen() #pone el estado del protocolo en listo, empieza a aceptar las conecciones y recibir las solicitudes

print(f'Servidor escuchando en {HOST}:{PORT}...') #comprobacion si el servidor esta escuchando

#configuracion del socket a socket no bloqueante
socket_server.setblocking(0)

#lista de clientes conectados
clients = []

while True:
    #aceptar nuevas conexiones de clientes
    #ocupamos un "try" por si llega a ocurrir un error de bucle
    try:
        client_socket, address = socket_server.accept() #aqui generamos la conexion
        print(f'Conexión aceptada de {address}')
        
        #configuramos SOCKET CLIENTE A NO BLOQUEANTE
        client_socket.setblocking(0)
        
        #agregamos el cliente a la lista de clientes
        clients.append(client_socket)
    except socket.error:
        pass



    #Se lee datos de los clientes conectados
    for client_socket in clients:
        try:
            audio = client_socket.recv(buffer_size)
            if audio:

                # Recibir un archivo de audio
                # getpeername -- > retorna la dirección [0] a la que está conectado el socket y el puerto [1]
                audio_recibido = os.path.join(DIRECTORY, f'{client_socket.getpeername()[0]}_{client_socket.getpeername()[1]}.mp3')
                # Ocupé os.path para poder darles un nombre a los archivos que se están recibiendo os.path.join es para juntar rutas
                with open(audio_recibido, 'wb') as f:
                    f.write(audio)
                print(f'Archivo de audio recibido de {client_socket.getpeername()} y guardado en {audio_recibido}')
                # Enviar una confirmación al cliente de que se recibio el audio
                client_socket.sendall(b'Archivo de audio recibido y guardado correctamente\n')
            else:

                # Si no hay datos, el cliente se desconecta
                print(f'{client_socket.getpeername()} desconectado')
                client_socket.close()
                clients.remove(client_socket)
        except socket.error:
            pass

