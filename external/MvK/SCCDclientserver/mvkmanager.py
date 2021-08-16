# Statechart compiler by Glenn De Jonghe
#
# Date:   Wed Aug 13 14:07:05 2014

# Model author: Yentl Van Tendeloo
# Model name:   MvK Manager
# Model description:
"""
    MvK Manager interface for managing several locally hosted MvK instances
"""

from python_runtime.statecharts_core import ObjectManagerBase, Event, InstanceWrapper, RuntimeClassBase, Association
from subprocess import check_output, check_call, CalledProcessError
import select
import sys
import os

serverfilename = "simple_http_server.py"
if __name__ == "__main__":
    print("ERROR: should not call the statechart directly")
    sys.exit(1)


class MvKManager(RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_main = 1
    Root_main_manager_state = 2
    Root_main_mem_watchdog = 3
    Root_main_cpu_watchdog = 4
    Root_main_manager_state_monitor = 5
    Root_main_manager_state_command = 6
    Root_main_manager_state_quit = 7
    Root_main_mem_watchdog_mem_watchdog = 8
    Root_main_cpu_watchdog_cpu_watchdog = 9
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_main] = []
        self.current_state[self.Root_main_manager_state] = []
        self.current_state[self.Root_main_mem_watchdog] = []
        self.current_state[self.Root_main_cpu_watchdog] = []
    
    def start(self):
        super(MvKManager, self).start()
        self.enterDefault_Root_main()
    
    #The actual constructor
    def __init__(self, controller):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        self.command_log = ["Initialized"]
        self.max_memory = 10
        self.cpu_times = {}
    
    # User defined method
    def kill_port(self, port):
        try:
            pid = int(check_output('ps aux | grep "' + str(serverfilename) + ' ' + str(port) + '" | grep -v grep | awk \'{print $2}\'', shell=True))
            self.command_log.append("Killing MvK at port " + str(port))
            self.kill_pid(pid)
        except:
            self.command_log.append("ERROR: no MvK at port " + str(port))
        
    # User defined method
    def kill_pid(self, pid):
        check_call("kill " + str(pid), shell=True)
        
    # User defined method
    def start_port(self, port):
        check_call("nohup python " + str(serverfilename) + " " + str(port) + " > server_" + str(port) + ".log &", shell=True)
        self.command_log.append("Starting MvK at port " + str(port))
        self.cpu_times[port] = 0
        
    # User defined method
    def get_all_mvks(self):
        try:
            mvks = check_output('ps aux | grep "' + str(serverfilename) + '" | grep -v grep | awk \'{print $2}\'', shell=True)
            return mvks.split("\n")[:-1]
        except CalledProcessError:
            return []
        
    # User defined method
    def printStatus(self):
        output = "\n"
        output += " === Current processes ===\n"
        output += "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\n"
        try:
            output += check_output('ps aux | grep ' + str(serverfilename) + ' | grep -v grep', shell=True) + "\n"
        except CalledProcessError:
            output += " ** No instances running **\n"
        output += "\n"
        output += " === Command log ===\n"
        if len(self.command_log) > 10:
            self.command_log = self.command_log[-5:]
        for log in self.command_log:
            output += log + "\n"
        output += "\n"
        os.system('clear')
        print(output)
        
    # User defined method
    def printCommands(self):
        print(" === Available commands ===")
        print(" monitor                            Go to monitoring state")
        print(" kill <port>                        Kill MvK at port")
        print(" start <port>                       Start MvK at port")
        print(" startrange <startport> <endport>   Start MvK port range (inclusive)")
        print(" restart <port>                     Restart MvK at port")
        print(" setmem <percentage>                Set the maximal memory percentage for the watchdog")
        print(" quit                               Stop all MvK's and stop")
        print("")
        print(" >>> "),
        sys.stdout.flush()
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_main(self):
        self.current_state[self.Root].append(self.Root_main)
    
    def exit_Root_main(self):
        self.exit_Root_main_manager_state()
        self.exit_Root_main_mem_watchdog()
        self.exit_Root_main_cpu_watchdog()
        self.current_state[self.Root] = []
    
    def enter_Root_main_manager_state(self):
        self.current_state[self.Root_main].append(self.Root_main_manager_state)
    
    def exit_Root_main_manager_state(self):
        if self.Root_main_manager_state_monitor in self.current_state[self.Root_main_manager_state] :
            self.exit_Root_main_manager_state_monitor()
        if self.Root_main_manager_state_command in self.current_state[self.Root_main_manager_state] :
            self.exit_Root_main_manager_state_command()
        if self.Root_main_manager_state_quit in self.current_state[self.Root_main_manager_state] :
            self.exit_Root_main_manager_state_quit()
        self.current_state[self.Root_main] = []
    
    def enter_Root_main_mem_watchdog(self):
        self.current_state[self.Root_main].append(self.Root_main_mem_watchdog)
    
    def exit_Root_main_mem_watchdog(self):
        if self.Root_main_mem_watchdog_mem_watchdog in self.current_state[self.Root_main_mem_watchdog] :
            self.exit_Root_main_mem_watchdog_mem_watchdog()
        self.current_state[self.Root_main] = []
    
    def enter_Root_main_cpu_watchdog(self):
        self.current_state[self.Root_main].append(self.Root_main_cpu_watchdog)
    
    def exit_Root_main_cpu_watchdog(self):
        if self.Root_main_cpu_watchdog_cpu_watchdog in self.current_state[self.Root_main_cpu_watchdog] :
            self.exit_Root_main_cpu_watchdog_cpu_watchdog()
        self.current_state[self.Root_main] = []
    
    def enter_Root_main_manager_state_monitor(self):
        self.timers[0] = 5.0
        self.printStatus()
        print(" == Press RETURN for command interface == ")
        self.current_state[self.Root_main_manager_state].append(self.Root_main_manager_state_monitor)
    
    def exit_Root_main_manager_state_monitor(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_main_manager_state] = []
    
    def enter_Root_main_manager_state_command(self):
        self.timers[1] = 10.0
        self.printStatus()
        self.printCommands()
        self.current_state[self.Root_main_manager_state].append(self.Root_main_manager_state_command)
    
    def exit_Root_main_manager_state_command(self):
        self.timers.pop(1, None)
        self.current_state[self.Root_main_manager_state] = []
    
    def enter_Root_main_manager_state_quit(self):
        print("Shutting down manager")
        self.current_state[self.Root_main_manager_state].append(self.Root_main_manager_state_quit)
    
    def exit_Root_main_manager_state_quit(self):
        self.current_state[self.Root_main_manager_state] = []
    
    def enter_Root_main_mem_watchdog_mem_watchdog(self):
        self.timers[2] = 5.0
        try:
            output = check_output('ps aux | grep ' + str(serverfilename) + ' | grep -v grep | awk \'{print $4 " " $13}\'', shell=True)
            if len(output) > 1:
                output = output.split("\n")[:-1]
                for process in output:
                    mem_usage = float(process.split(" ")[0])
                    if mem_usage >= self.max_memory:
                        # Process is using more than max_memory percent of available memory
                        # So kill it
                        port = process.split(" ")[1]
                        self.command_log.append("WATCHDOG kills port " + str(port) + " (mem% was " + str(mem_usage) + ")")
                        self.kill_port(port)
        except CalledProcessError:
            # No MvKs are running
            pass
        self.current_state[self.Root_main_mem_watchdog].append(self.Root_main_mem_watchdog_mem_watchdog)
    
    def exit_Root_main_mem_watchdog_mem_watchdog(self):
        self.timers.pop(2, None)
        self.current_state[self.Root_main_mem_watchdog] = []
    
    def enter_Root_main_cpu_watchdog_cpu_watchdog(self):
        self.timers[3] = 10.0
        try:
            output = check_output('ps aux | grep ' + str(serverfilename) + ' | grep -v grep | awk \'{print $10 " " $13}\'', shell=True)
            if len(output) > 1:
                output = output.split("\n")[:-1]
                for process in output:
                    cpu_min, cpu_sec = process.split(" ")[0].split(":")
                    cpu_time = int(cpu_min) * 60 + int(cpu_sec)
                    port = process.split(" ")[1]
                    if cpu_time - self.cpu_times.get(port, 0) >= 9:
                        # CPU was running 9 out of 10 seconds for this process
                        # So kill it
                        self.command_log.append("WATCHDOG kills port " + str(port) + " (cpu time was " + str(cpu_time) + "s)")
                        self.kill_port(port)
                    self.cpu_times[port] = self.cpu_times.get(port, 0) + cpu_time
        except CalledProcessError:
            # No MvKs are running
            pass
        self.current_state[self.Root_main_cpu_watchdog].append(self.Root_main_cpu_watchdog_cpu_watchdog)
    
    def exit_Root_main_cpu_watchdog_cpu_watchdog(self):
        self.timers.pop(3, None)
        self.current_state[self.Root_main_cpu_watchdog] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_main(self):
        self.enter_Root_main()
        self.enterDefault_Root_main_manager_state()
        self.enterDefault_Root_main_mem_watchdog()
        self.enterDefault_Root_main_cpu_watchdog()
    
    def enterDefault_Root_main_manager_state(self):
        self.enter_Root_main_manager_state()
        self.enter_Root_main_manager_state_monitor()
    
    def enterDefault_Root_main_mem_watchdog(self):
        self.enter_Root_main_mem_watchdog()
        self.enter_Root_main_mem_watchdog_mem_watchdog()
    
    def enterDefault_Root_main_cpu_watchdog(self):
        self.enter_Root_main_cpu_watchdog()
        self.enter_Root_main_cpu_watchdog_cpu_watchdog()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_main:
                catched = self.transition_Root_main(event)
        return catched
    
    def transition_Root_main(self, event) :
        catched = False
        if not catched :
            catched = self.transition_Root_main_manager_state(event) or catched
            catched = self.transition_Root_main_mem_watchdog(event) or catched
            catched = self.transition_Root_main_cpu_watchdog(event) or catched
        return catched
    
    def transition_Root_main_manager_state(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_main_manager_state][0] == self.Root_main_manager_state_monitor:
                catched = self.transition_Root_main_manager_state_monitor(event)
            elif self.current_state[self.Root_main_manager_state][0] == self.Root_main_manager_state_command:
                catched = self.transition_Root_main_manager_state_command(event)
            elif self.current_state[self.Root_main_manager_state][0] == self.Root_main_manager_state_quit:
                catched = self.transition_Root_main_manager_state_quit(event)
        return catched
    
    def transition_Root_main_manager_state_monitor(self, event) :
        catched = False
        enableds = []
        if event.name == "RETURN" and event.getPort() == "input" :
            enableds.append(1)
        
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_manager_state_monitor. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_main_manager_state_monitor()
                self.enter_Root_main_manager_state_command()
            elif enabled == 2 :
                self.exit_Root_main_manager_state_monitor()
                self.enter_Root_main_manager_state_monitor()
            catched = True
        
        return catched
    
    def transition_Root_main_manager_state_command(self, event) :
        catched = False
        enableds = []
        if event.name == "START" and event.getPort() == "input" :
            enableds.append(1)
        
        if event.name == "STARTRANGE" and event.getPort() == "input" :
            enableds.append(2)
        
        if event.name == "KILL" and event.getPort() == "input" :
            enableds.append(3)
        
        if event.name == "RETURN" and event.getPort() == "input" :
            enableds.append(4)
        
        if event.name == "RESTART" and event.getPort() == "input" :
            enableds.append(5)
        
        if event.name == "QUIT" and event.getPort() == "input" :
            enableds.append(6)
        
        if event.name == "SETMEM" and event.getPort() == "input" :
            enableds.append(7)
        
        if event.name == "MONITOR" and event.getPort() == "input" :
            enableds.append(8)
        
        if event.name == "_1after" and event.getPort() == "" :
            enableds.append(9)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_manager_state_command. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                port = parameters[0]
                self.exit_Root_main_manager_state_command()
                self.start_port(port)
                self.enter_Root_main_manager_state_command()
            elif enabled == 2 :
                parameters = event.getParameters()
                startport = parameters[0]
                endport = parameters[1]
                self.exit_Root_main_manager_state_command()
                for port in range(int(startport), int(endport)+1):
                    self.start_port(port)
                self.enter_Root_main_manager_state_command()
            elif enabled == 3 :
                parameters = event.getParameters()
                port = parameters[0]
                self.exit_Root_main_manager_state_command()
                self.kill_port(port)
                self.enter_Root_main_manager_state_command()
            elif enabled == 4 :
                self.exit_Root_main_manager_state_command()
                self.enter_Root_main_manager_state_command()
            elif enabled == 5 :
                parameters = event.getParameters()
                port = parameters[0]
                self.exit_Root_main_manager_state_command()
                self.kill_port(port)
                self.start_port(port)
                self.enter_Root_main_manager_state_command()
            elif enabled == 6 :
                self.exit_Root_main_manager_state_command()
                mvks = self.get_all_mvks()
                for mvk in mvks:
                    self.kill_pid(mvk)
                self.controller.outputEvent(Event("STOP", port="", parameters = []))
                self.enter_Root_main_manager_state_quit()
            elif enabled == 7 :
                parameters = event.getParameters()
                maxmem = parameters[0]
                self.exit_Root_main_manager_state_command()
                self.max_memory = float(maxmem)
                self.command_log.append("Changed max memory for watchdog to " + str(self.max_memory) + "%")
                self.enter_Root_main_manager_state_command()
            elif enabled == 8 :
                self.exit_Root_main_manager_state_command()
                self.enter_Root_main_manager_state_monitor()
            elif enabled == 9 :
                self.exit_Root_main_manager_state_command()
                self.enter_Root_main_manager_state_monitor()
            catched = True
        
        return catched
    
    def transition_Root_main_manager_state_quit(self, event) :
        catched = False
        return catched
    
    def transition_Root_main_mem_watchdog(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_main_mem_watchdog][0] == self.Root_main_mem_watchdog_mem_watchdog:
                catched = self.transition_Root_main_mem_watchdog_mem_watchdog(event)
        return catched
    
    def transition_Root_main_mem_watchdog_mem_watchdog(self, event) :
        catched = False
        enableds = []
        if event.name == "_2after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_mem_watchdog_mem_watchdog. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_main_mem_watchdog_mem_watchdog()
                self.enter_Root_main_mem_watchdog_mem_watchdog()
            catched = True
        
        return catched
    
    def transition_Root_main_cpu_watchdog(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_main_cpu_watchdog][0] == self.Root_main_cpu_watchdog_cpu_watchdog:
                catched = self.transition_Root_main_cpu_watchdog_cpu_watchdog(event)
        return catched
    
    def transition_Root_main_cpu_watchdog_cpu_watchdog(self, event) :
        catched = False
        enableds = []
        if event.name == "_3after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_cpu_watchdog_cpu_watchdog. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_main_cpu_watchdog_cpu_watchdog()
                self.enter_Root_main_cpu_watchdog_cpu_watchdog()
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
        if class_name == "MvKManager" :
            instance =  MvKManager(self.controller, *construct_params)
        if instance:
            return InstanceWrapper(instance, associations)
        else :
            return None

from python_runtime.statecharts_core import ThreadsControllerBase
class Controller(ThreadsControllerBase):
    def __init__(self, keep_running = True):
        super(Controller, self).__init__(ObjectManager(self), keep_running)
        self.addInputPort("input")
        self.addOutputPort("output")
        self.object_manager.createInstance("MvKManager", [])
        
def main():
    controller = Controller()
    controller.start()

if __name__ == "__main__":
    main()
