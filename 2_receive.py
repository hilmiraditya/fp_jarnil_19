import socket
import struct
import sys
import time
import json
import ast

id_receive = 'pc2'
port = 10000
multicast_ip = '224.3.29.71'

def send(message): 
    multicast_group = (multicast_ip, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(0.2)

    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    sock.sendto(message, multicast_group)
    print 'mengirimkan pesan... '

    try:
        sock.recvfrom(16)
    except:
        print "tidak ada respon"
        sock.close()
        return 0
    else:
        print "pesan berhasil dikirim"
        sock.close()
        return 1


def checkWaktu(batas_waktu, timestamp):
    waktuSekarang = time.time()
    if(waktuSekarang - timestamp > batas_waktu):
        print "durasi pengiriman melebihi limit waktu"
        exit()
        
def checkId(id_pengirim):
    if(id_pengirim == id_receive):
        print 'Receive telah sesuai dengan tujuan awal'
        return 1
    else:
        print 'Receive belum sesuai tujuan'
        return 0

def receive():
    multicast_group = multicast_ip
    server_address = ('', port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        print 'menunggu pesan..'
        data, address = sock.recvfrom(1024)
        message = ast.literal_eval(data)

        print >>sys.stderr, 'mengirim konfirmasi ke ', address
        sock.sendto('ack', address)

        cek_id = checkId(message[1])
        if(cek_id == 1):
            exit()
        else:
            check = 0
            while(check != 1):
                checkWaktu(int(message[3]),float(message[4]))
                check = send(str(message))

if __name__ == "__main__":
    receive()