import socket
import struct
import sys
import time
import json

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
        
if __name__ == "__main__":
    message = []

    # pesan = raw_input("Masukkan Pesan > ")
    # id_tujuan = raw_input("Masukkan ID Tujuan > ")
    # batas_hop = raw_input("Masukkan Batas Hop > ")
    # batas_waktu = raw_input("Masukkan Batas Waktu > ")
    # timestamp = time.time()

    pesan = "memek"
    id_tujuan = "pc1"
    batas_hop = "30"
    batas_waktu = "30"
    timestamp = time.time()

    #pesan
    message.insert(0, pesan)
    #id tujuan
    message.insert(1, id_tujuan)
    #batas hop
    message.insert(2, int(batas_hop))
    #batas waktu
    message.insert(3, int(batas_waktu))
    #timestamp
    message.insert(4, timestamp)

    check = 0
    while(check != 1):
        checkWaktu(int(batas_waktu), timestamp)
        check = send(str(message))
