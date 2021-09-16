from xmlrpc.server import SimpleXMLRPCServer

def wipeThePc(pcNumber):
    # wiping the pc
    return 'pc is now wiped'


def is_even(va):
    print("got the variabe"+va)
    return va 

server = SimpleXMLRPCServer(("localhost", 8001))
print("Listening on port 8001...")
server.register_function(is_even, "is_even")
server.register_function(wipeThePc, "wipe")
server.serve_forever()