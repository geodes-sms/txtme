# Statechart compiler by Glenn De Jonghe
#
# Date:   Mon Oct  6 13:09:24 2014

# Model author: Yentl Van Tendeloo
# Model name:   MvK Client interface
# Model description:
"""
    MvK Client interface that sends events over the network using XMLHTTPRequests
"""

from python_runtime.statecharts_core import ObjectManagerBase, Event, InstanceWrapper, RuntimeClassBase, Association
import urllib
import urllib2
import sys

sys.path.append("../")
from mvk.impl.python.util.jsonserializer import MvKEncoder
from mvk.impl.python.datavalue import StringValue
from mvk.impl.client.jsondeserializer import MvKDecoder


class MvKClient(RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_main = 1
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
    
    def start(self):
        super(MvKClient, self).start()
        self.enter_Root_main()
    
    #The actual constructor
    def __init__(self, controller):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        self.server_id = 0
        self.client_id = 1
        #self.requesturl = "http://studento.ua.ac.be/~s0090165/mvk.php?server_id=" + str(self.server_id) + "&client_id=" + str(self.client_id)
        self.requesturl = "http://localhost:8000/?server_id=0&client_id=1"
        self.encoder = MvKEncoder()
        self.decoder = MvKDecoder()
        self.history = []
        self.future = []
    
    # User defined method
    def requestGET(self, function, data):
        query = "&func=" + function + "&args=" + urllib.quote(data)
        response = urllib2.urlopen(self.requesturl + query)
        response = response.read()
        return self.decoder.decode(response)
        
    # User defined method
    def requestPOST(self, function, data):
        query = "func=" + function + "&args=" + str(data) + "&client_id=" + str(self.client_id)
        response = urllib2.urlopen(self.requesturl, query)
        return self.decoder.decode(response.read())
        
    # User defined method
    def undo(self):
        print("START UNDO")
        if len(self.history) == 0:
            return None
        command, changelog = self.history.pop()
        self.future.append(command)
        logs = []
        for reverse_action in changelog.get_inverse():
            logs.append(self.requestPOST(reverse_action[0], self.encoder.encode(reverse_action[1])))
        print("END UNDO")
        return logs
        
    # User defined method
    def redo(self):
        if len(self.future) == 0:
            return None
        command = self.future.pop()
        changelog = self.requestPOST(command[0], command[1])
        self.history.append((command, changelog))
        return changelog
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_main(self):
        self.current_state[self.Root].append(self.Root_main)
    
    def exit_Root_main(self):
        self.current_state[self.Root] = []
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_main:
                catched = self.transition_Root_main(event)
        return catched
    
    def transition_Root_main(self, event) :
        catched = False
        enableds = []
        if event.name == "read" and event.getPort() == "request" :
            enableds.append(1)
        
        if event.name == "create" and event.getPort() == "request" :
            enableds.append(2)
        
        if event.name == "update" and event.getPort() == "request" :
            enableds.append(3)
        
        if event.name == "delete" and event.getPort() == "request" :
            enableds.append(4)
        
        if event.name == "clear" and event.getPort() == "request" :
            enableds.append(5)
        
        if event.name == "conforms_to" and event.getPort() == "request" :
            enableds.append(6)
        
        if event.name == "evaluate" and event.getPort() == "request" :
            enableds.append(7)
        
        if event.name == "backup" and event.getPort() == "request" :
            enableds.append(8)
        
        if event.name == "restore" and event.getPort() == "request" :
            enableds.append(9)
        
        if event.name == "run" and event.getPort() == "request" :
            enableds.append(10)
        
        if event.name == "execute" and event.getPort() == "request" :
            enableds.append(11)
        
        if event.name == "apply" and event.getPort() == "request" :
            enableds.append(12)
        
        if event.name == "undo" and event.getPort() == "request" :
            enableds.append(13)
        
        if event.name == "redo" and event.getPort() == "request" :
            enableds.append(14)
        
        if event.name == "unbind" and event.getPort() == "request" :
            enableds.append(15)
        
        if event.name == "get_files" and event.getPort() == "request" :
            enableds.append(16)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                data = parameters[0]
                self.exit_Root_main()
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestGET('read', self.encoder.encode(data))]))
                self.enter_Root_main()
            elif enabled == 2 :
                parameters = event.getParameters()
                data = parameters[0]
                self.exit_Root_main()
                encoded_data = self.encoder.encode(data)
                changelog = self.requestPOST("create", encoded_data)
                self.history.append((("create", encoded_data), changelog))
                self.future = []
                self.controller.outputEvent(Event("reply", port="", parameters = [changelog]))
                self.enter_Root_main()
            elif enabled == 3 :
                parameters = event.getParameters()
                data = parameters[0]
                self.exit_Root_main()
                encoded_data = self.encoder.encode(data)
                changelog = self.requestPOST("update", encoded_data)
                self.history.append((("update", encoded_data), changelog))
                self.future = []
                self.controller.outputEvent(Event("reply", port="", parameters = [changelog]))
                self.enter_Root_main()
            elif enabled == 4 :
                parameters = event.getParameters()
                data = parameters[0]
                self.exit_Root_main()
                encoded_data = self.encoder.encode(data)
                changelog = self.requestPOST("delete", encoded_data)
                self.history.append((("delete", encoded_data), changelog))
                self.future = []
                self.controller.outputEvent(Event("reply", port="", parameters = [changelog]))
                self.enter_Root_main()
            elif enabled == 5 :
                self.exit_Root_main()
                self.history = []
                self.future = []
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestPOST('clear', [[], {}])]))
                self.enter_Root_main()
            elif enabled == 6 :
                parameters = event.getParameters()
                model = parameters[0]
                type_model = parameters[1]
                self.exit_Root_main()
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestPOST('conforms_to', '[[' + self.encoder.encode(model) + ', ' + self.encoder.encode(type_model) + '], {}]')]))
                self.enter_Root_main()
            elif enabled == 7 :
                parameters = event.getParameters()
                args = parameters[0]
                kwargs = parameters[1]
                self.exit_Root_main()
                self.history = []
                self.future = []
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestPOST('evaluate', '[' + self.encoder.encode(args) + ', ' + self.encoder.encode(kwargs) + ']')]))
                self.enter_Root_main()
            elif enabled == 8 :
                parameters = event.getParameters()
                filename = parameters[0]
                self.exit_Root_main()
                filename = StringValue(str(self.server_id) + '/' + filename.get_value())
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestPOST('backup', '[[' + self.encoder.encode(filename) + '], {}]')]))
                self.enter_Root_main()
            elif enabled == 9 :
                parameters = event.getParameters()
                filename = parameters[0]
                self.exit_Root_main()
                filename = StringValue(str(self.server_id) + '/' + filename.get_value())
                self.history = []
                self.future = []
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestPOST('restore', '[[' + self.encoder.encode(filename) + '], {}]')]))
                self.enter_Root_main()
            elif enabled == 10 :
                parameters = event.getParameters()
                opname = parameters[0]
                kwargs = parameters[1]
                self.exit_Root_main()
                self.history = []
                self.future = []
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestPOST('run', '[[' + self.encoder.encode(opname) + '], {' + self.encoder.encode(kwargs) + '}]')]))
                self.enter_Root_main()
            elif enabled == 11 :
                parameters = event.getParameters()
                location = parameters[0]
                args = parameters[1]
                self.exit_Root_main()
                new_args = [location]
                new_args.extend(args)
                self.history = []
                self.future = []
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestPOST('execute', '[' + self.encoder.encode(new_args) + ', {}]')]))
                self.enter_Root_main()
            elif enabled == 12 :
                parameters = event.getParameters()
                params = parameters[0]
                self.exit_Root_main()
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestPOST('apply', '[[' + self.encoder.encode(params) + '], {}]')]))
                self.enter_Root_main()
            elif enabled == 13 :
                self.exit_Root_main()
                self.controller.outputEvent(Event("reply", port="", parameters = [self.undo()]))
                self.enter_Root_main()
            elif enabled == 14 :
                self.exit_Root_main()
                self.controller.outputEvent(Event("reply", port="", parameters = [self.redo()]))
                self.enter_Root_main()
            elif enabled == 15 :
                self.exit_Root_main()
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestGET('unbind', '')]))
                self.enter_Root_main()
            elif enabled == 16 :
                self.exit_Root_main()
                self.controller.outputEvent(Event("reply", port="", parameters = [self.requestGET('get_files', '[[' + self.encoder.encode(StringValue(str(self.server_id))) + '], {}]')]))
                self.enter_Root_main()
            catched = True
        
        return catched
    
    # Execute transitions
    def transition(self, event = Event("")):
        self.state_changed = self.transition_Root(event)
    # inState method for statechart
    def inState(self, nodes):
        for actives in self.current_state.itervalues():
            nodes = [node for node in nodes if node not in actives]
            if not nodes :
                return True
        return False
    
class ObjectManager (ObjectManagerBase):
    def __init__(self, controller):
        super(ObjectManager, self).__init__(controller)
    
    def instantiate(self, class_name, construct_params):
        associations = []
        if class_name == "MvKClient" :
            instance =  MvKClient(self.controller, *construct_params)
        if instance:
            return InstanceWrapper(instance, associations)
        else :
            return None

from python_runtime.statecharts_core import ThreadsControllerBase
class Controller(ThreadsControllerBase):
    def __init__(self, keep_running = True):
        super(Controller, self).__init__(ObjectManager(self), keep_running)
        self.addInputPort("request")
        self.addOutputPort("reply")
        self.object_manager.createInstance("MvKClient", [])
        
def main():
    controller = Controller()
    controller.start()

if __name__ == "__main__":
    main()
