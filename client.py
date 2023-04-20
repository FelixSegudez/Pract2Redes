#imports para clientes
import socket


#configuración del cliente
HOST = '127.0.0.1'  #dirección IP del cliente
PORT = 12345  #puerto utilizado por el servidor
audio_enviar = 'audio1.mp3'  #nombre del archivo de audio a enviar


#creamos el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

#ponemos el socket como no bloqueante y permite realizar múltiples operaciones

client_socket.setblocking(0)

#Se lee el archivo de audio
with open(audio_enviar, 'rb') as f:  #abrimos el archivo solo para lectura en formato binario
    data = f.read()

#se envia el archivo de audio al servidor
try:
    client_socket.sendall(data) #asegura que se envíen todos los datos, o hasta que ocurra un error
    print(f'Archivo de audio {audio_enviar} enviado al servidor {HOST}:{PORT}')
    
    #se lee la confirmación del servidor
    data = client_socket.recv(1024)
    print(data.decode())
except socket.error:
    pass

#Se cierra el socket
client_socket.close()