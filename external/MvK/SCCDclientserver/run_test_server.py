import test_server
import test_socket_event
from python_runtime.statecharts_core import Event

controller = test_server.Controller()
listener = controller.addOutputListener("socket_out")
controller.start()

while 1:
    evt = listener.fetch(-1)
    name, params = evt.getName(), evt.getParameters()
    print("Got event " + str(evt))
    if name == "accept_socket":
        print("Accepting")
        test_socket_event.wait_for_accept_on_socket(params[0], lambda i: controller.addInput(Event("accepted_socket", "socket_in", [i])))
    elif name == "recv_socket":
        print("Receiving")
        test_socket_event.wait_for_receive_on_socket(params[0], lambda i: controller.addInput(Event("received_socket", "socket_in", [i])))

controller.stop()
