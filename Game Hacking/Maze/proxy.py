import socket
import select
import time
import sys
import os
import json
from threading import Thread

class color():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    N = '\033[0m'


senddobble = False
##Standard Variables
dbg_http_ts = False #HTTP Debugging output to server
dbg_http_tc = False #HTTP Debugging output to client
dbg_udp_tc = False  #UDP Debugging output to client
dbg_udp_ts = False  #UDP Debuging output to server
httpport = 80
remoteHost = "147.75.85.99"

print("{}[*]{} Client{} to{} Server{} HTTP port is: {}".format(color.GREEN, color.CYAN, color.N, color.RED, color.N, httpport))
print("{}[*]{} Server{} is {}{}{}".format(color.GREEN, color.RED, color.N, color.YELLOW, remoteHost, color.N))



class tcpproxy:
    class Proxy2Server(Thread):

        def __init__(self, host, port):
            super(tcpproxy.Proxy2Server, self).__init__()
            self.game = None
            self.port = port
            self.host = host
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect((host, port))

        def run(self):
          while True:
                data = self.server.recv(4096)
                if data:
                    if dbg_http_tc == True:
                        print("[{}] {}<- {}{}".format(self.port, color.BLUE, data[:], color.N))
                    # forward to client
                    self.game.sendall(data)

    class Game2Proxy(Thread):

        def __init__(self, host, port):
            super(tcpproxy.Game2Proxy, self).__init__()
            self.server = None
            self.port = port
            self.host = host
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(1)
            self.game, addr = sock.accept()

        def run(self):
            while True:
                data = self.game.recv(4096)
                if data:
                    if dbg_http_ts == True:
                        print("[{}]{} -> {}{}".format(self.port, color.YELLOW, data[:], color.N))
                    self.server.sendall(data)

    class Proxy(Thread):

        def __init__(self, from_host, to_host, port):
            super(tcpproxy.Proxy, self).__init__()
            self.from_host = from_host
            self.to_host = to_host
            self.port = port

        def run(self):
            while True:
                print("{}[proxy({})]{} setting up".format(color.GREEN, self.port, color.N))
                self.g2p = tcpproxy.Game2Proxy(self.from_host, self.port) # waiting for a client
                self.p2s = tcpproxy.Proxy2Server(self.to_host, self.port)
                print("{}[proxy({})]{} connection established".format(color.GREEN, self.port, color.N))
                self.g2p.server = self.p2s.server
                self.p2s.game = self.g2p.game
                self.g2p.start()
                self.p2s.start()
 
class udpproxy:
    class ProxyUdp(Thread):

        def __init__(self, fromhost, tohost, toport):
            super(udpproxy.ProxyUdp, self).__init__()
            self.fromhost = fromhost
            self.tohost = tohost
            self.toport = toport
        def run(self):
            try:
	            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	            s.bind(('', self.toport))
            except:
	            print("{}[!] Failed to bind UDP socket with Port: {}{}{}".format(color.RED, color.YELLOW, self.toport, color.N))
            print("{}[UDP({})]{} started".format(color.GREEN, self.toport, color.N))
            knownClient = None
            knownServer = (self.tohost, self.toport)            
            while True:
                #32768
                data, addr = s.recvfrom(65565)
                if knownClient is None:
                    knownClient = addr
                if addr == knownClient:
                    s.sendto(data, knownServer)
                    if dbg_udp_ts == True:
                        print("{}[{}]{} -> {}{}".format(color.GREEN, self.toport, color.RED, data[:].hex(), color.N))
                else:
                    s.sendto(data, knownClient)
                    if dbg_udp_tc == True:
                        print("[{}]{} -> {}{}".format(self.toport, color.YELLOW, data[:].hex(), color.N))
######################################################################################################################
http = tcpproxy.Proxy('0.0.0.0', remoteHost, httpport)
http.start()

game_servers = []
for port in range(1337, 1357):
    _game_server = udpproxy.ProxyUdp('0.0.0.0', remoteHost, port)
    _game_server.start()
    game_servers.append(_game_server)
time.sleep(0.5)

while True:
    try:
        cmd = input('$ ')
        if cmd[:4] == 'quit':
            os._exit(0)
        if cmd[:5] == 'clear':
            os.system('clear')
        ######UDP-Debugging
        if cmd[:9] == 'udp-tson':
            print("{}[i]{} UDP Debugging to Server{} on{}".format(color.GREEN, color.N, color.RED, color.N))
            dbg_udp_ts = True
        if cmd[:10] == 'udp-tsoff':
            print("{}[i]{} UDP Debugging to Server{} off{}".format(color.GREEN, color.N, color.BLUE, color.N))
            dbg_udp_ts = False
        if cmd[:9] == 'udp-tcon':
            print("{}[i]{} UDP Debugging to Client{} on{}".format(color.GREEN, color.N, color.RED, color.N))
            dbg_udp_tc = True
        if cmd[:10] == 'udp-tcoff':
            dbg_udp_tc = False
            print("{}[i]{} UDP Debugging to Client{} off{}".format(color.GREEN, color.N, color.BLUE, color.N))
        if cmd[:10] == 'udp-allon':
            print("{}[i]{} UDP Debugging completly{} on{}".format(color.GREEN, color.N, color.RED, color.N))
            dbg_udp_tc = True
            dbg_udp_ts = True
        if cmd[:11] == 'udp-alloff':
            print("{}[i]{} UDP Debugging completly{} off{}".format(color.GREEN, color.N, color.BLUE, color.N))
            dbg_udp_tc = False
            dbg_udp_ts = False

        #######  HTTP-Debugging    
        if cmd[:9] == 'http-tson':
            print("{}[i]{} HTTP Debugging to Server{} on{}".format(color.GREEN, color.N, color.RED, color.N))
            dbg_http_ts = True
        if cmd[:10] == 'http-tsoff':
            print("{}[i]{} HTTP Debugging to Server{} off{}".format(color.GREEN, color.N, color.BLUE, color.N))
            dbg_http_ts = False
        if cmd[:9] == 'http-tcon':
            print("{}[i]{} HTTP Debugging to Client{} on{}".format(color.GREEN, color.N, color.RED, color.N))
            dbg_http_tc = True
        if cmd[:10] == 'http-tcoff':
            dbg_http_tc = False
            print("{}[i]{} HTTP Debugging to Client{} off{}".format(color.GREEN, color.N, color.BLUE, color.N))
        if cmd[:10] == 'http-allon':
            print("{}[i]{} HTTP Debugging completly{} on{}".format(color.GREEN, color.N, color.RED, color.N))
            dbg_http_tc = True
            dbg_http_ts = True
        if cmd[:11] == 'http-alloff':
            print("{}[i]{} HTTP Debugging completly{} off{}".format(color.GREEN, color.N, color.BLUE, color.N))
            dbg_http_tc = False
            dbg_http_ts = False
        ####### / HTTP-Debugging
        if cmd[:4] == 'help':
            print("{}[{}Command Help{}]{}".format(color.RED, color.YELLOW, color.RED, color.N))
            print("{}[-]{} quit{}        Exit program and kill all listeners/proxys{}".format(color.RED, color.CYAN, color.MAGENTA, color.N))
            print("{}[-]{} clear{}       Clears the entire screen{}".format(color.RED, color.CYAN, color.MAGENTA, color.N))
            print("{}[-]{} help{}        Displays this help menu{}".format(color.RED, color.CYAN, color.MAGENTA, color.N))
            print("{}[{}UDP-Debugging{}]{}".format(color.RED, color.YELLOW, color.RED, color.N))
            print("{}[-]{} udp-tson{}    Turn the UDP Debugging to server {}on{}".format(color.RED, color.CYAN, color.MAGENTA, color.RED, color.N))
            print("{}[-]{} udp-tsoff{}   Turn the UDP Debugging to server {}off{}".format(color.RED, color.CYAN, color.MAGENTA, color.BLUE, color.N))
            print("{}[-]{} udp-tcon{}    Turn the UDP Debugging to client {}on{}".format(color.RED, color.CYAN, color.MAGENTA, color.RED, color.N))
            print("{}[-]{} udp-tcoff{}   Turn the UDP Debugging to client {}off{}".format(color.RED, color.CYAN, color.MAGENTA, color.BLUE, color.N))
            print("{}[-]{} udp-allon{}   Turn the UDP Debugging completly {}on{}".format(color.RED, color.CYAN, color.MAGENTA, color.RED, color.N))        
            print("{}[-]{} udp-alloff{}  Turn the UDP Debugging completly {}off{}".format(color.RED, color.CYAN, color.MAGENTA, color.BLUE, color.N))            
            print("{}[{}HTTP-Debugging{}]{}".format(color.RED, color.YELLOW, color.RED, color.N))
            print("{}[-]{} http-tson{}   Turn the HTTP Debugging to server {}on{}".format(color.RED, color.CYAN, color.MAGENTA, color.RED, color.N))
            print("{}[-]{} http-tsoff{}  Turn the HTTP Debugging to server {}off{}".format(color.RED, color.CYAN, color.MAGENTA, color.BLUE, color.N))
            print("{}[-]{} http-tcon{}   Turn the HTTP Debugging to client {}on{}".format(color.RED, color.CYAN, color.MAGENTA, color.RED, color.N))
            print("{}[-]{} http-tcoff{}  Turn the HTTP Debugging to client {}off{}".format(color.RED, color.CYAN, color.MAGENTA, color.BLUE, color.N))
            print("{}[-]{} http-allon{}  Turn the HTTP Debugging completly {}on{}".format(color.RED, color.CYAN, color.MAGENTA, color.RED, color.N))        
            print("{}[-]{} http-alloff{} Turn the HTTP Debugging completly {}off{}".format(color.RED, color.CYAN, color.MAGENTA, color.BLUE, color.N))
            
    except Exception as e:
        print(e)

