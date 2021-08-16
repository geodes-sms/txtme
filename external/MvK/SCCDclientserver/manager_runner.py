import sys
import select

import mvkmanager
from python_runtime.statecharts_core import Event

controller = mvkmanager.Controller()
controller.start()
listenport = controller.addOutputListener('output')

events = frozenset(["start", "startrange", "monitor", "kill", "restart", "quit", "setmem", ""])

while True:
    if listenport.fetch() is not None:
        break
    else:
        if len(select.select([sys.stdin], [], [], 1)[0]) > 0:
            # New input, cut of trailing newline
            inp = sys.stdin.readline()[:-1]
            splitted = inp.split(" ")

            params = [] if len(splitted) == 1 else splitted[1:]
            event_name = splitted[0].upper() if splitted[0].lower() in events else 'UNKNOWN'
            event_name = "RETURN" if event_name == "" else event_name

            controller.addInput(Event(event_name, "input", params))

controller.stop()
