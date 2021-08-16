import threading

def _recv(socket, func):
    total = ""
    while 1:
        data = socket.recv(1024)
        if not data:
            break
        print("Got data: " + str(data))
        if data[-1] == "\0":
            total += data[:-1]
            break
        total += data
    func(total)

def _accept(socket, func):
    conn, addr = socket.accept()
    func(conn)

def wait_for_receive_on_socket(socket, func):
    # As soon as recv on socket does something, call func with the parameter
    # This immediately returns
    thrd = threading.Thread(target=_recv, args=[socket, func])
    thrd.deamon = True
    thrd.start()

def wait_for_accept_on_socket(socket, func):
    # As soon as accept is done, call func with the socket
    thrd = threading.Thread(target=_accept, args=[socket, func])
    thrd.daemon = True
    thrd.start()
