import socket


server_ip = '172.20.10.9'  
server_port = 12345  
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))
print("Starting sever...")
while True:
    data, addr = server_socket.recvfrom(1024) 
    print(f'Received data from the client')
print('The graph has been put on the Desktop server')



    






