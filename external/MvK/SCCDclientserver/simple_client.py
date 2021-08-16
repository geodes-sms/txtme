import client
from python_runtime.statecharts_core import Event

from mvk.impl.python.datavalue import LocationValue, StringValue, MappingValue
from mvk.impl.python.constants import CreateConstants

controller = client.Controller()
listener = controller.addOutputListener("reply")
controller.start()

requests = [["clear", ""],
            ["read", [LocationValue("protected")]],
            ["create", [MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'), CreateConstants.LOCATION_KEY: LocationValue('formalisms'), CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})})]],
            ["evaluate", [[StringValue("__eq__"), LocationValue("protected.formalisms"), LocationValue("protected.formalisms")], {}]],
            ["evaluate", [[StringValue("__ne__"), LocationValue("protected.formalisms"), LocationValue("protected.formalisms")], {}]],
            ["read", [LocationValue("formalisms")]],
            ["backup", [StringValue("my_backup")]],
            ["clear", ""],
            ["read", [LocationValue("formalisms")]],
            ["restore", [StringValue("my_backup")]],
            ["read", [LocationValue("formalisms")]],
            ["create", [MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'), CreateConstants.LOCATION_KEY: LocationValue('formalisms'), CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})})]],
            ["undo", ""],
            ["redo", ""],
            ["get_files", ""],
            ["unbind", ""]
            ]

for request in requests:
    print("Make request " + str(request))
    controller.addInput(Event(request[0], "request", request[1]))
    print("Reply: " + str(listener.fetch(-1).getParameters()[0]))

controller.stop()
