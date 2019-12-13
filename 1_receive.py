import socket
import struct
import sys
import time
import json
import ast
from geopy.distance import geodesic

id_receive = 'pc1'
port = 10000
multicast_ip = '224.3.29.71'
#perak surabaya
lat_current = -7.228549
long_current = 112.731391



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
        #print "tidak ada respon"
        sock.close()
        return 0
    else:
        print "pesan berhasil dikirim"
        sock.close()
        return 1


def checkWaktu(batas_waktu, timestamp):
    waktuSekarang = time.time()
    if(waktuSekarang - timestamp > batas_waktu):
        print "durasi melebihi limit waktu"
        exit()
        

def checkBatasHop(jumlah_hop,batas_hop):
    if(jumlah_hop > batas_hop):
        print 'Jumlah hop melebihi batas'
        exit()

def cekJarak(lat_from,long_from,maximal_jarak):
    coords_1 = (lat_from, long_from)
    coords_2 = (lat_current, long_current)
    jarak = geodesic(coords_1, coords_2).km
    print "jaraknya adalah " + str(jarak)
    
    print maximal_jarak
    if(jarak > float(maximal_jarak)):
        print maximal_jarak
        print "jarak melebihi batas"
        exit()

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
        cekJarak(message[6],message[7],message[8])
        print 'terdapat pesan baru !'
        print 'isi pesan : ', message[0]
        print 'mengirim konfirmasi ke ', address
        sock.sendto('ack', address)


        message[5] = message[5] + 1


        #cek jumlah hop
        jumlah_hop = message[5]
        batas_hop = message[2]
        checkBatasHop(jumlah_hop,batas_hop)

        #penambahan hop apabila berhasil
        # message[5] = message[5] + 1

        #pengecekan waktu
        checkWaktu(message[3],message[4])

        #cek maximal jarak
        # cekJarak(message[6],message[7],message[8])

        #cek apakah receiver ini tujuan awal 
        if(message[1] == id_receive):
            print 'receive telah sesuai dengan tujuan awal'
            exit()
        else:
            check = 0
            while(check != 1):
                checkWaktu(int(message[3]),float(message[4]))
                check = send(str(message))
            exit()

if __name__ == "__main__":
    receive()
