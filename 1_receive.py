import socket
import struct
import sys
import time
import json
import ast
import threading 

id_receive = 'pc1'
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
        print "durasi melebihi limit waktu"
        exit()
        

def checkBatasHop(jumlah_hop,batas_hop):
    if(jumlah_hop > batas_hop):
        print 'Jumlah hop melebihi batas'
        exit()

def checkId(id_dari):
    if(id_dari == id_receive):
        return 1
    else:
        return 0

def receiveWhileSending():
    multicast_group = multicast_ip
    server_address = ('', port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        data, address = sock.recvfrom(1024)
        if(data == "0"):
            print "ternyata sudah ada receive yang sudah sampai tujuan"
            exit()
        sock.sendto('-1', address)


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
        print 'terdapat pesan baru !'
        print 'isi pesan : ', message[0]

        getCheckId = checkId(message[1])

        print 'mengirim konfirmasi ke ', address
        sock.sendto(str(getCheckId), address)

        #cek jumlah hop
        jumlah_hop = message[5]
        batas_hop = message[2]
        checkBatasHop(jumlah_hop,batas_hop)

        #penambahan hop apabila berhasil
        message[5] = message[5] + 1

        #pengecekan waktu
        checkWaktu(message[3],message[4])

        #cek apakah receiver ini tujuan awal 
        if(getCheckId == 1):
            print 'receive telah sesuai dengan tujuan awal'
            exit()
        else:
            check = 0
            while(check != 1):
                checkWaktu(int(message[3]),float(message[4]))
                # check = send(str(message))
                t1 = threading.Thread(target=receiveWhileSending) 
                t2 = threading.Thread(target=send, args=(str(message),)) 
                t1.start() 
                t2.start() 
                t1.join() 
                t2.join() 



if __name__ == "__main__":
    receive()