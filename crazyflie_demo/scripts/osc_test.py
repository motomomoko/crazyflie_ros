import time, threading
import OSC

server_address = ("192.168.11.102", 8000)
server = OSC.OSCServer(server_address)
server.addDefaultHandlers()

def msgPrint(addr, tags, data, client_address):

    print addr
    print data

server.addMsgHandler("/pos", msgPrint)
#server.addMsgHandler("/pos1", msgPrint)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

try :
    while True :
        pass
except KeyboardInterrupt :
    server.close()
    server_thread.join()
