# Statechart compiler by Glenn De Jonghe
#
# Date:   Thu Sep 04 13:59:19 2014

# Model author: Simon Van Mierlo
# Model name:   MvK Frontend
# Model description:
"""
    Tkinter frontend for the Modelverse.
"""

from python_runtime.statecharts_core import ObjectManagerBase, Event, InstanceWrapper, RuntimeClassBase, Association
import time
import re
import os
import urllib
import urllib2
import sys
import random

import Tkinter as tk
import mvk.impl.client.object as client_object

from util_classes import *
from mvk.impl.python.util.jsonserializer import MvKEncoder
from mvk.impl.client.jsondeserializer import MvKDecoder        
from mvk.impl.python.datavalue import *
from mvk.impl.python.datatype import *
from mvk.impl.python.constants import CreateConstants, UpdateConstants

sys.path.append("../")


class MvKFrontend(MvKWidget, tk.Tk, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_running = 2
    Root_root_running_main_behaviour = 3
    Root_root_running_cd_behaviour = 4
    Root_root_running_listening_client = 5
    Root_root_running_main_behaviour_initializing = 6
    Root_root_running_main_behaviour_asking_id = 7
    Root_root_running_main_behaviour_creating_client = 8
    Root_root_running_main_behaviour_initializing_windows = 9
    Root_root_running_main_behaviour_running = 10
    Root_root_running_cd_behaviour_waiting = 11
    Root_root_running_cd_behaviour_creating = 12
    Root_root_running_cd_behaviour_starting = 13
    Root_root_running_cd_behaviour_check_nr_of_windows = 14
    Root_root_running_listening_client_listening_client = 15
    Root_root_stopped = 16
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_running] = []
        self.current_state[self.Root_root_running_main_behaviour] = []
        self.current_state[self.Root_root_running_cd_behaviour] = []
        self.current_state[self.Root_root_running_listening_client] = []
    
    def start(self):
        super(MvKFrontend, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        tk.Tk.__init__(self)
        MvKWidget.__init__(self, self.controller)
        self.fixed_update_time = 5
        self.prev_time = time.time()
        self.update_self()
        self.withdraw()
        self.nr_of_windows = 0
        self.initialized = False
    
    # User defined method
    def update_self(self):
        curr_time = time.time()
        self.controller.update(curr_time - self.prev_time)
        self.prev_time = curr_time
        self.scheduled_update_id = self.after(self.fixed_update_time, self.update_self)
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_running in self.current_state[self.Root_root] :
            self.exit_Root_root_running()
        if self.Root_root_stopped in self.current_state[self.Root_root] :
            self.exit_Root_root_stopped()
        self.current_state[self.Root] = []
    
    def enter_Root_root_running(self):
        self.current_state[self.Root_root].append(self.Root_root_running)
    
    def exit_Root_root_running(self):
        self.exit_Root_root_running_main_behaviour()
        self.exit_Root_root_running_cd_behaviour()
        self.exit_Root_root_running_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_running_main_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_main_behaviour)
    
    def exit_Root_root_running_main_behaviour(self):
        if self.Root_root_running_main_behaviour_initializing in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_initializing()
        if self.Root_root_running_main_behaviour_asking_id in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_asking_id()
        if self.Root_root_running_main_behaviour_creating_client in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_creating_client()
        if self.Root_root_running_main_behaviour_initializing_windows in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_initializing_windows()
        if self.Root_root_running_main_behaviour_running in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_running()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_cd_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_cd_behaviour)
    
    def exit_Root_root_running_cd_behaviour(self):
        if self.Root_root_running_cd_behaviour_waiting in self.current_state[self.Root_root_running_cd_behaviour] :
            self.exit_Root_root_running_cd_behaviour_waiting()
        if self.Root_root_running_cd_behaviour_creating in self.current_state[self.Root_root_running_cd_behaviour] :
            self.exit_Root_root_running_cd_behaviour_creating()
        if self.Root_root_running_cd_behaviour_starting in self.current_state[self.Root_root_running_cd_behaviour] :
            self.exit_Root_root_running_cd_behaviour_starting()
        if self.Root_root_running_cd_behaviour_check_nr_of_windows in self.current_state[self.Root_root_running_cd_behaviour] :
            self.exit_Root_root_running_cd_behaviour_check_nr_of_windows()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_listening_client(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_listening_client)
    
    def exit_Root_root_running_listening_client(self):
        if self.Root_root_running_listening_client_listening_client in self.current_state[self.Root_root_running_listening_client] :
            self.exit_Root_root_running_listening_client_listening_client()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_main_behaviour_initializing(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_initializing)
    
    def exit_Root_root_running_main_behaviour_initializing(self):
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_asking_id(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_asking_id)
    
    def exit_Root_root_running_main_behaviour_asking_id(self):
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_creating_client(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_creating_client)
    
    def exit_Root_root_running_main_behaviour_creating_client(self):
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_initializing_windows(self):
        self.timers[0] = 0.1
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_initializing_windows)
    
    def exit_Root_root_running_main_behaviour_initializing_windows(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_running(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_running)
    
    def exit_Root_root_running_main_behaviour_running(self):
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_cd_behaviour_waiting(self):
        self.current_state[self.Root_root_running_cd_behaviour].append(self.Root_root_running_cd_behaviour_waiting)
    
    def exit_Root_root_running_cd_behaviour_waiting(self):
        self.current_state[self.Root_root_running_cd_behaviour] = []
    
    def enter_Root_root_running_cd_behaviour_creating(self):
        self.current_state[self.Root_root_running_cd_behaviour].append(self.Root_root_running_cd_behaviour_creating)
    
    def exit_Root_root_running_cd_behaviour_creating(self):
        self.current_state[self.Root_root_running_cd_behaviour] = []
    
    def enter_Root_root_running_cd_behaviour_starting(self):
        self.current_state[self.Root_root_running_cd_behaviour].append(self.Root_root_running_cd_behaviour_starting)
    
    def exit_Root_root_running_cd_behaviour_starting(self):
        self.current_state[self.Root_root_running_cd_behaviour] = []
    
    def enter_Root_root_running_cd_behaviour_check_nr_of_windows(self):
        self.current_state[self.Root_root_running_cd_behaviour].append(self.Root_root_running_cd_behaviour_check_nr_of_windows)
    
    def exit_Root_root_running_cd_behaviour_check_nr_of_windows(self):
        self.current_state[self.Root_root_running_cd_behaviour] = []
    
    def enter_Root_root_running_listening_client_listening_client(self):
        self.current_state[self.Root_root_running_listening_client].append(self.Root_root_running_listening_client_listening_client)
    
    def exit_Root_root_running_listening_client_listening_client(self):
        self.current_state[self.Root_root_running_listening_client] = []
    
    def enter_Root_root_stopped(self):
        self.current_state[self.Root_root].append(self.Root_root_stopped)
    
    def exit_Root_root_stopped(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enterDefault_Root_root_running()
    
    def enterDefault_Root_root_running(self):
        self.enter_Root_root_running()
        self.enterDefault_Root_root_running_main_behaviour()
        self.enterDefault_Root_root_running_cd_behaviour()
        self.enterDefault_Root_root_running_listening_client()
    
    def enterDefault_Root_root_running_main_behaviour(self):
        self.enter_Root_root_running_main_behaviour()
        self.enter_Root_root_running_main_behaviour_initializing()
    
    def enterDefault_Root_root_running_cd_behaviour(self):
        self.enter_Root_root_running_cd_behaviour()
        self.enter_Root_root_running_cd_behaviour_waiting()
    
    def enterDefault_Root_root_running_listening_client(self):
        self.enter_Root_root_running_listening_client()
        self.enter_Root_root_running_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_running:
                catched = self.transition_Root_root_running(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_stopped:
                catched = self.transition_Root_root_stopped(event)
        return catched
    
    def transition_Root_root_running(self, event) :
        catched = False
        enableds = []
        if event.name == "stop" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running()
                self.destroy()
                self.enter_Root_root_stopped()
            catched = True
        
        if not catched :
            catched = self.transition_Root_root_running_main_behaviour(event) or catched
            catched = self.transition_Root_root_running_cd_behaviour(event) or catched
            catched = self.transition_Root_root_running_listening_client(event) or catched
        return catched
    
    def transition_Root_root_running_main_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_initializing:
                catched = self.transition_Root_root_running_main_behaviour_initializing(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_asking_id:
                catched = self.transition_Root_root_running_main_behaviour_asking_id(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_creating_client:
                catched = self.transition_Root_root_running_main_behaviour_creating_client(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_initializing_windows:
                catched = self.transition_Root_root_running_main_behaviour_initializing_windows(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_running:
                catched = self.transition_Root_root_running_main_behaviour_running(event)
        return catched
    
    def transition_Root_root_running_main_behaviour_initializing(self, event) :
        catched = False
        enableds = []
        enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_initializing()
                self.addEvent(Event("create_window", parameters = [{'class_name': 'InputWindow', 'constructor_parameters': {'option_names': ['UserID']}}]))
                self.enter_Root_root_running_main_behaviour_asking_id()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_asking_id(self, event) :
        catched = False
        enableds = []
        if event.name == "input_given" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_asking_id. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                given_input = parameters[0]
                self.exit_Root_root_running_main_behaviour_asking_id()
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "client","MvKClient",given_input['UserID']]))
                self.enter_Root_root_running_main_behaviour_initializing_windows()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_asking_id()
                print 'closed window!'
                self.addEvent(Event("stop", parameters = []))
                self.enter_Root_root_running_main_behaviour_asking_id()
            elif enabled == 3 :
                self.exit_Root_root_running_main_behaviour_asking_id()
                print 'error'
                self.enter_Root_root_running_main_behaviour_asking_id()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_client(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_main_behaviour_creating_client()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                self.enter_Root_root_running_main_behaviour_initializing_windows()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_initializing_windows(self, event) :
        catched = False
        enableds = []
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_initializing_windows. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_initializing_windows()
                self.addEvent(Event("create_window", parameters = [{'class_name': 'ModelEditor', 'constructor_parameters': {}}]))
                self.initialized = True
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_running(self, event) :
        catched = False
        enableds = []
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters["event_name"] == "create_window" :
                enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                self.addEvent(Event("create_window", parameters = [event_parameters]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_cd_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_cd_behaviour][0] == self.Root_root_running_cd_behaviour_waiting:
                catched = self.transition_Root_root_running_cd_behaviour_waiting(event)
            elif self.current_state[self.Root_root_running_cd_behaviour][0] == self.Root_root_running_cd_behaviour_creating:
                catched = self.transition_Root_root_running_cd_behaviour_creating(event)
            elif self.current_state[self.Root_root_running_cd_behaviour][0] == self.Root_root_running_cd_behaviour_starting:
                catched = self.transition_Root_root_running_cd_behaviour_starting(event)
            elif self.current_state[self.Root_root_running_cd_behaviour][0] == self.Root_root_running_cd_behaviour_check_nr_of_windows:
                catched = self.transition_Root_root_running_cd_behaviour_check_nr_of_windows(event)
        return catched
    
    def transition_Root_root_running_cd_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "create_window" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_cd_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_cd_behaviour_waiting()
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "windows",event_parameters["class_name"],event_parameters["constructor_parameters"]]))
                self.enter_Root_root_running_cd_behaviour_creating()
            elif enabled == 2 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_cd_behaviour_waiting()
                self.nr_of_windows -= 1
                print "in delete_window %s" % self.nr_of_windows
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, association_name]))
                self.enter_Root_root_running_cd_behaviour_check_nr_of_windows()
            catched = True
        
        return catched
    
    def transition_Root_root_running_cd_behaviour_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_cd_behaviour_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_cd_behaviour_creating()
                self.nr_of_windows += 1
                print "in create_window %s" % self.nr_of_windows
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                self.enter_Root_root_running_cd_behaviour_starting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_cd_behaviour_starting(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_started" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_cd_behaviour_starting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_cd_behaviour_starting()
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.addEvent(Event("window_started", parameters = [association_name]))
                self.enter_Root_root_running_cd_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_cd_behaviour_check_nr_of_windows(self, event) :
        catched = False
        enableds = []
        if self.nr_of_windows == 0 and self.initialized :
            enableds.append(1)
        
        if self.nr_of_windows != 0 or not self.initialized :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_cd_behaviour_check_nr_of_windows. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_cd_behaviour_check_nr_of_windows()
                self.addEvent(Event("stop", parameters = []))
                self.enter_Root_root_running_cd_behaviour_check_nr_of_windows()
            elif enabled == 2 :
                self.exit_Root_root_running_cd_behaviour_check_nr_of_windows()
                self.enter_Root_root_running_cd_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_listening_client][0] == self.Root_root_running_listening_client_listening_client:
                catched = self.transition_Root_root_running_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_running_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            parameters = event.getParameters()
            association_name = parameters[0]
            data = parameters[1]
            if data['event_name'] == 'read' :
                enableds.append(1)
        
        if event.name == "client_request" and event.getPort() == "" :
            parameters = event.getParameters()
            association_name = parameters[0]
            data = parameters[1]
            if data['event_name'] == 'create' :
                enableds.append(2)
        
        if event.name == "client_request" and event.getPort() == "" :
            parameters = event.getParameters()
            association_name = parameters[0]
            data = parameters[1]
            if data['event_name'] == 'delete' :
                enableds.append(3)
        
        if event.name == "client_request" and event.getPort() == "" :
            parameters = event.getParameters()
            association_name = parameters[0]
            data = parameters[1]
            if data['event_name'] == 'update' :
                enableds.append(4)
        
        if event.name == "client_request" and event.getPort() == "" :
            parameters = event.getParameters()
            association_name = parameters[0]
            data = parameters[1]
            if data['event_name'] == 'evaluate' :
                enableds.append(5)
        
        if event.name == "client_request" and event.getPort() == "" :
            parameters = event.getParameters()
            association_name = parameters[0]
            data = parameters[1]
            if data['event_name'] == 'backup' :
                enableds.append(6)
        
        if event.name == "client_request" and event.getPort() == "" :
            parameters = event.getParameters()
            association_name = parameters[0]
            data = parameters[1]
            if data['event_name'] == 'restore' :
                enableds.append(7)
        
        if event.name == "client_request" and event.getPort() == "" :
            parameters = event.getParameters()
            association_name = parameters[0]
            data = parameters[1]
            if data['event_name'] == 'validate' :
                enableds.append(8)
        
        if event.name == "client_request" and event.getPort() == "" :
            parameters = event.getParameters()
            association_name = parameters[0]
            data = parameters[1]
            if data['event_name'] == 'get_files' :
                enableds.append(9)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_running_listening_client_listening_client()
                send_event = Event("read", parameters = ['parent' + '/' + association_name,data['request_parameters']])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'client' , send_event]))
                self.enter_Root_root_running_listening_client_listening_client()
            elif enabled == 2 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_running_listening_client_listening_client()
                send_event = Event("create", parameters = ['parent' + '/' + association_name,data['request_parameters']])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'client' , send_event]))
                self.enter_Root_root_running_listening_client_listening_client()
            elif enabled == 3 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_running_listening_client_listening_client()
                send_event = Event("delete", parameters = ['parent' + '/' + association_name,data['request_parameters']])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'client' , send_event]))
                self.enter_Root_root_running_listening_client_listening_client()
            elif enabled == 4 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_running_listening_client_listening_client()
                send_event = Event("update", parameters = ['parent' + '/' + association_name,data['request_parameters']])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'client' , send_event]))
                self.enter_Root_root_running_listening_client_listening_client()
            elif enabled == 5 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_running_listening_client_listening_client()
                send_event = Event("evaluate", parameters = ['parent' + '/' + association_name,data['request_parameters']['args'],data['request_parameters']['kwargs']])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'client' , send_event]))
                self.enter_Root_root_running_listening_client_listening_client()
            elif enabled == 6 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_running_listening_client_listening_client()
                send_event = Event("backup", parameters = ['parent' + '/' + association_name,data['request_parameters']['file_name']])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'client' , send_event]))
                self.enter_Root_root_running_listening_client_listening_client()
            elif enabled == 7 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_running_listening_client_listening_client()
                send_event = Event("restore", parameters = ['parent' + '/' + association_name,data['request_parameters']['file_name']])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'client' , send_event]))
                self.enter_Root_root_running_listening_client_listening_client()
            elif enabled == 8 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_running_listening_client_listening_client()
                print 'sending conforms_to to client'
                send_event = Event("conforms_to", parameters = ['parent' + '/' + association_name,data['request_parameters']['model'],data['request_parameters']['type_model']])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'client' , send_event]))
                self.enter_Root_root_running_listening_client_listening_client()
            elif enabled == 9 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_running_listening_client_listening_client()
                send_event = Event("get_files", parameters = ['parent' + '/' + association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'client' , send_event]))
                self.enter_Root_root_running_listening_client_listening_client()
            catched = True
        
        return catched
    
    def transition_Root_root_stopped(self, event) :
        catched = False
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
    

class MvKClient(RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_main = 1
    Root_main_keepalive = 2
    Root_main_main = 3
    Root_main_keepalive_loop = 4
    Root_main_main_main = 5
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_main] = []
        self.current_state[self.Root_main_keepalive] = []
        self.current_state[self.Root_main_main] = []
    
    def start(self):
        super(MvKClient, self).start()
        self.enterDefault_Root_main()
    
    #The actual constructor
    def __init__(self, controller, UserID):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        random.seed()
        self.client_id = random.randint(0, 9999999)
        self.server_id = UserID
        #self.requesturl = "http://studento.ua.ac.be/~s0090165/mvk.php?server_id=" + str(self.server_id) + "&client_id=" + str(self.client_id)
        self.requesturl = "http://127.0.0.1:8000/?server_id=%s&client_id=%s" % (self.server_id, self.client_id)
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
        # Send the client_id in the POST data too, in case it is a localhost method
        query = "func=" + function + "&args=" + str(data) + "&client_id=" + str(self.client_id)
        response = urllib2.urlopen(self.requesturl, query)
        return self.decoder.decode(response.read())
        
    # User defined method
    def undo(self):
        if len(self.history) == 0:
            return None
        command, changelog = self.history.pop()
        self.future.append(command)
        logs = []
        for reverse_action in changelog.get_inverse():
            logs.append(self.requestPOST(reverse_action[0], self.encoder.encode(reverse_action[1])))
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
        self.exit_Root_main_keepalive()
        self.exit_Root_main_main()
        self.current_state[self.Root] = []
    
    def enter_Root_main_keepalive(self):
        self.current_state[self.Root_main].append(self.Root_main_keepalive)
    
    def exit_Root_main_keepalive(self):
        if self.Root_main_keepalive_loop in self.current_state[self.Root_main_keepalive] :
            self.exit_Root_main_keepalive_loop()
        self.current_state[self.Root_main] = []
    
    def enter_Root_main_main(self):
        self.current_state[self.Root_main].append(self.Root_main_main)
    
    def exit_Root_main_main(self):
        if self.Root_main_main_main in self.current_state[self.Root_main_main] :
            self.exit_Root_main_main_main()
        self.current_state[self.Root_main] = []
    
    def enter_Root_main_keepalive_loop(self):
        self.timers[0] = 1
        self.current_state[self.Root_main_keepalive].append(self.Root_main_keepalive_loop)
    
    def exit_Root_main_keepalive_loop(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_main_keepalive] = []
    
    def enter_Root_main_main_main(self):
        self.current_state[self.Root_main_main].append(self.Root_main_main_main)
    
    def exit_Root_main_main_main(self):
        self.current_state[self.Root_main_main] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_main(self):
        self.enter_Root_main()
        self.enterDefault_Root_main_keepalive()
        self.enterDefault_Root_main_main()
    
    def enterDefault_Root_main_keepalive(self):
        self.enter_Root_main_keepalive()
        self.enter_Root_main_keepalive_loop()
    
    def enterDefault_Root_main_main(self):
        self.enter_Root_main_main()
        self.enter_Root_main_main_main()
    
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
            catched = self.transition_Root_main_keepalive(event) or catched
            catched = self.transition_Root_main_main(event) or catched
        return catched
    
    def transition_Root_main_keepalive(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_main_keepalive][0] == self.Root_main_keepalive_loop:
                catched = self.transition_Root_main_keepalive_loop(event)
        return catched
    
    def transition_Root_main_keepalive_loop(self, event) :
        catched = False
        enableds = []
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_keepalive_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_main_keepalive_loop()
                # Send a keepalive packet to the server
                self.requestGET("keepalive", '')
                self.enter_Root_main_keepalive_loop()
            catched = True
        
        return catched
    
    def transition_Root_main_main(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_main_main][0] == self.Root_main_main_main:
                catched = self.transition_Root_main_main_main(event)
        return catched
    
    def transition_Root_main_main_main(self, event) :
        catched = False
        enableds = []
        if event.name == "read" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "create" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "update" and event.getPort() == "" :
            enableds.append(3)
        
        if event.name == "delete" and event.getPort() == "" :
            enableds.append(4)
        
        if event.name == "clear" and event.getPort() == "" :
            enableds.append(5)
        
        if event.name == "conforms_to" and event.getPort() == "" :
            enableds.append(6)
        
        if event.name == "evaluate" and event.getPort() == "" :
            enableds.append(7)
        
        if event.name == "backup" and event.getPort() == "" :
            enableds.append(8)
        
        if event.name == "restore" and event.getPort() == "" :
            enableds.append(9)
        
        if event.name == "run" and event.getPort() == "" :
            enableds.append(10)
        
        if event.name == "execute" and event.getPort() == "" :
            enableds.append(11)
        
        if event.name == "apply" and event.getPort() == "" :
            enableds.append(12)
        
        if event.name == "undo" and event.getPort() == "" :
            enableds.append(13)
        
        if event.name == "redo" and event.getPort() == "" :
            enableds.append(14)
        
        if event.name == "get_files" and event.getPort() == "" :
            enableds.append(15)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_main_main. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_main_main_main()
                send_event = Event("client_response", parameters = [self.requestGET('read', self.encoder.encode(data))])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 2 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_main_main_main()
                encoded_data = self.encoder.encode(data)
                changelog = self.requestPOST("create", encoded_data)
                self.history.append((("create", encoded_data), changelog))
                self.future = []
                send_event = Event("client_response", parameters = [changelog])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 3 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_main_main_main()
                encoded_data = self.encoder.encode(data)
                changelog = self.requestPOST("update", encoded_data)
                self.history.append((("update", encoded_data), changelog))
                self.future = []
                send_event = Event("client_response", parameters = [changelog])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 4 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_main_main_main()
                encoded_data = self.encoder.encode(data)
                changelog = self.requestPOST("delete", encoded_data)
                self.history.append((("delete", encoded_data), changelog))
                self.future = []
                send_event = Event("client_response", parameters = [changelog])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 5 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_main_main_main()
                self.history = []
                self.future = []
                send_event = Event("client_response", parameters = [self.requestPOST('clear', [[], {}])])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 6 :
                parameters = event.getParameters()
                association_name = parameters[0]
                model = parameters[1]
                type_model = parameters[2]
                self.exit_Root_main_main_main()
                send_event = Event("client_response", parameters = [self.requestPOST('conforms_to', '[[' + self.encoder.encode(model) + ', ' + self.encoder.encode(type_model) + '], {}]')])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 7 :
                parameters = event.getParameters()
                association_name = parameters[0]
                args = parameters[1]
                kwargs = parameters[2]
                self.exit_Root_main_main_main()
                send_event = Event("client_response", parameters = [self.requestPOST('evaluate', '[' + self.encoder.encode(args) + ', ' + self.encoder.encode(kwargs) + ']')])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 8 :
                parameters = event.getParameters()
                association_name = parameters[0]
                filename = parameters[1]
                self.exit_Root_main_main_main()
                filename = StringValue(str(self.server_id) + '/' + filename.get_value())
                send_event = Event("client_response", parameters = [self.requestPOST('backup', '[[' + self.encoder.encode(filename) + '], {}]')])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 9 :
                parameters = event.getParameters()
                association_name = parameters[0]
                filename = parameters[1]
                self.exit_Root_main_main_main()
                filename = StringValue(str(self.server_id) + '/' + filename.get_value())
                self.history = []
                self.future = []
                send_event = Event("client_response", parameters = [self.requestPOST('restore', '[[' + self.encoder.encode(filename) + '], {}]')])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 10 :
                parameters = event.getParameters()
                association_name = parameters[0]
                opname = parameters[1]
                kwargs = parameters[2]
                self.exit_Root_main_main_main()
                self.history = []
                self.future = []
                send_event = Event("client_response", parameters = [self.requestPOST('run', '[[' + self.encoder.encode(opname) + '], {' + self.encoder.encode(kwargs) + '}]')])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 11 :
                parameters = event.getParameters()
                association_name = parameters[0]
                location = parameters[1]
                args = parameters[2]
                self.exit_Root_main_main_main()
                new_args = [location]
                new_args.extend(args)
                send_event = Event("client_response", parameters = [self.requestPOST('execute', '[' + self.encoder.encode(new_args) + ', {}]')])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 12 :
                parameters = event.getParameters()
                association_name = parameters[0]
                params = parameters[1]
                self.exit_Root_main_main_main()
                send_event = Event("client_response", parameters = [self.requestPOST('apply', '[[' + self.encoder.encode(params) + '], {}]')])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 13 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_main_main_main()
                send_event = Event("client_response", parameters = [self.undo()])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 14 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_main_main_main()
                send_event = Event("client_response", parameters = [self.redo()])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
            elif enabled == 15 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_main_main_main()
                send_event = Event("client_response", parameters = [self.requestGET('get_files', '[[' + self.encoder.encode(StringValue(str(self.server_id))) + '], {}]')])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_main_main_main()
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
    

class Window(MvKWidget, tk.Toplevel, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_idle = 1
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
    
    def start(self):
        super(Window, self).start()
        self.enter_Root_idle()
    
    #The actual constructor
    def __init__(self, controller):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        tk.Toplevel.__init__(self)
        MvKWidget.__init__(self, self.controller)
    
    # User defined destructor
    def __del__(self):
        self.destroy()
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_idle(self):
        self.current_state[self.Root].append(self.Root_idle)
    
    def exit_Root_idle(self):
        self.current_state[self.Root] = []
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_idle:
                catched = self.transition_Root_idle(event)
        return catched
    
    def transition_Root_idle(self, event) :
        catched = False
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
    

class NewInstanceAttributeEditor(Window, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_main_behaviour = 2
    Root_root_main_behaviour_creating_editors = 3
    Root_root_main_behaviour_packing_widgets = 4
    Root_root_main_behaviour_window_behaviour = 5
    Root_root_main_behaviour_listening = 6
    Root_root_main_behaviour_listening_client = 7
    Root_root_initializing = 8
    Root_root_main_behaviour_creating_editors_loop = 9
    Root_root_main_behaviour_creating_editors_creating = 10
    Root_root_main_behaviour_creating_editors_running = 11
    Root_root_main_behaviour_packing_widgets_packing = 12
    Root_root_main_behaviour_window_behaviour_waiting = 13
    Root_root_main_behaviour_listening_listening = 14
    Root_root_main_behaviour_listening_checking_input = 15
    Root_root_main_behaviour_listening_client_listening_client = 16
    Root_root_deleting = 17
    Root_root_stopped = 18
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_main_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
        self.current_state[self.Root_root_main_behaviour_window_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_listening] = []
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def start(self):
        super(NewInstanceAttributeEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        Window.__init__(self, self.controller)
        self.minsize(width=256, height=256)
        self.t = constructor_parameters['type']
        self.type_location = constructor_parameters['type_location']
        if 'attribute_values' in constructor_parameters:
            self.attribute_values = constructor_parameters['attribute_values']
        else:
            self.attribute_values = {}
        self.title('Create New %s Instance' % self.t.name)
        
        self.attribute_frames = []
        self.attr_to_editor = {}
        self.loc = constructor_parameters['location'] if 'location' in constructor_parameters else None
        
        if isinstance(self.t, client_object.Model):
            self.attribute_frames = [tk.Frame(master=self)]
            self.editors = [{'class_name': 'LocationEditor', 'constructor_parameters': {'parent': self.attribute_frames[0], 'attr_name': StringValue('location'), 'attr_type': LocationType, 'value': self.attribute_values[StringValue('location')] if StringValue('location') in self.attribute_values else ''}}]
        elif isinstance(self.t, client_object.Association):
            self.attribute_frames = [tk.Frame(master=self), tk.Frame(master=self)]
            self.editors = [{'class_name': 'LocationEditor', 'constructor_parameters': {'parent': self.attribute_frames[0], 'attr_name': self.t.from_multiplicity.port_name, 'attr_type': LocationType, 'value': self.attribute_values[self.t.from_multiplicity.port_name] if self.t.from_multiplicity.port_name in self.attribute_values else ''}},
                            {'class_name': 'LocationEditor', 'constructor_parameters': {'parent': self.attribute_frames[1], 'attr_name': self.t.to_multiplicity.port_name, 'attr_type': LocationType, 'value': self.attribute_values[self.t.to_multiplicity.port_name] if self.t.to_multiplicity.port_name in self.attribute_values else ''}}]
        else:
            self.editors = []
        
        for a in self.t.attributes:
            if a.potency > IntegerValue(0):
                class_name = None
                the_type = a.the_type
                class_name = None
                if isinstance(the_type, StringType):
                    class_name = 'StringEditor'
                elif isinstance(the_type, LocationType):
                    class_name = 'LocationEditor'
                elif isinstance(the_type, BooleanType):
                    class_name = 'BooleanEditor'
                elif isinstance(the_type, IntegerType):
                    class_name = 'IntegerEditor'
                elif isinstance(the_type, FloatType):
                    class_name = 'FloatEditor'
                elif isinstance(the_type, AnyType):
                    class_name = 'AnyEditor'
                elif isinstance(the_type, EnumType):
                    class_name = 'EnumEditor'
                elif isinstance(the_type, TypeType):
                    class_name = 'TypeEditor'
                elif the_type == UnionType(SequenceValue([IntegerType(), InfiniteType()])):
                    class_name = 'IntInfEditor'
                self.attribute_frames.append(tk.Frame(master=self))
                self.editors.append({'class_name': class_name, 'constructor_parameters': {'parent': self.attribute_frames[len(self.attribute_frames) - 1], 'attr_name': a.short_location, 'attr_type': a.the_type, 'value': self.attribute_values[a.name] if a.name in self.attribute_values else a.default}})
        self.buttons = [{'class_name': 'Button', 'constructor_parameters': {'parent': self, 'visual': TextVisual('OK'), 'tooltip_text': 'Create Instance', 'event_parameters': {'event_name': 'user_confirmed'}}}]
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        if self.Root_root_deleting in self.current_state[self.Root_root] :
            self.exit_Root_root_deleting()
        if self.Root_root_stopped in self.current_state[self.Root_root] :
            self.exit_Root_root_stopped()
        self.current_state[self.Root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.exit_Root_root_main_behaviour_creating_editors()
        self.exit_Root_root_main_behaviour_packing_widgets()
        self.exit_Root_root_main_behaviour_window_behaviour()
        self.exit_Root_root_main_behaviour_listening()
        self.exit_Root_root_main_behaviour_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_editors(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_creating_editors)
    
    def exit_Root_root_main_behaviour_creating_editors(self):
        if self.Root_root_main_behaviour_creating_editors_loop in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_loop()
        if self.Root_root_main_behaviour_creating_editors_creating in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_creating()
        if self.Root_root_main_behaviour_creating_editors_running in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_running()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_packing_widgets(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_packing_widgets)
    
    def exit_Root_root_main_behaviour_packing_widgets(self):
        if self.Root_root_main_behaviour_packing_widgets_packing in self.current_state[self.Root_root_main_behaviour_packing_widgets] :
            self.exit_Root_root_main_behaviour_packing_widgets_packing()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_window_behaviour(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_window_behaviour)
    
    def exit_Root_root_main_behaviour_window_behaviour(self):
        if self.Root_root_main_behaviour_window_behaviour_waiting in self.current_state[self.Root_root_main_behaviour_window_behaviour] :
            self.exit_Root_root_main_behaviour_window_behaviour_waiting()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening)
    
    def exit_Root_root_main_behaviour_listening(self):
        if self.Root_root_main_behaviour_listening_listening in self.current_state[self.Root_root_main_behaviour_listening] :
            self.exit_Root_root_main_behaviour_listening_listening()
        if self.Root_root_main_behaviour_listening_checking_input in self.current_state[self.Root_root_main_behaviour_listening] :
            self.exit_Root_root_main_behaviour_listening_checking_input()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_client(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client(self):
        if self.Root_root_main_behaviour_listening_client_listening_client in self.current_state[self.Root_root_main_behaviour_listening_client] :
            self.exit_Root_root_main_behaviour_listening_client_listening_client()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_editors_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_loop)
    
    def exit_Root_root_main_behaviour_creating_editors_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_creating)
    
    def exit_Root_root_main_behaviour_creating_editors_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_running)
    
    def exit_Root_root_main_behaviour_creating_editors_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets].append(self.Root_root_main_behaviour_packing_widgets_packing)
    
    def exit_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
    
    def enter_Root_root_main_behaviour_window_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour].append(self.Root_root_main_behaviour_window_behaviour_waiting)
    
    def exit_Root_root_main_behaviour_window_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_listening(self):
        self.current_state[self.Root_root_main_behaviour_listening].append(self.Root_root_main_behaviour_listening_listening)
    
    def exit_Root_root_main_behaviour_listening_listening(self):
        self.current_state[self.Root_root_main_behaviour_listening] = []
    
    def enter_Root_root_main_behaviour_listening_checking_input(self):
        self.current_state[self.Root_root_main_behaviour_listening].append(self.Root_root_main_behaviour_listening_checking_input)
    
    def exit_Root_root_main_behaviour_listening_checking_input(self):
        self.current_state[self.Root_root_main_behaviour_listening] = []
    
    def enter_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client].append(self.Root_root_main_behaviour_listening_client_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def enter_Root_root_deleting(self):
        self.timers[0] = 0.05
        self.current_state[self.Root_root].append(self.Root_root_deleting)
    
    def exit_Root_root_deleting(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_stopped(self):
        self.current_state[self.Root_root].append(self.Root_root_stopped)
    
    def exit_Root_root_stopped(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_main_behaviour(self):
        self.enter_Root_root_main_behaviour()
        self.enterDefault_Root_root_main_behaviour_creating_editors()
        self.enterDefault_Root_root_main_behaviour_packing_widgets()
        self.enterDefault_Root_root_main_behaviour_window_behaviour()
        self.enterDefault_Root_root_main_behaviour_listening()
        self.enterDefault_Root_root_main_behaviour_listening_client()
    
    def enterDefault_Root_root_main_behaviour_creating_editors(self):
        self.enter_Root_root_main_behaviour_creating_editors()
        self.enter_Root_root_main_behaviour_creating_editors_loop()
    
    def enterDefault_Root_root_main_behaviour_packing_widgets(self):
        self.enter_Root_root_main_behaviour_packing_widgets()
        self.enter_Root_root_main_behaviour_packing_widgets_packing()
    
    def enterDefault_Root_root_main_behaviour_window_behaviour(self):
        self.enter_Root_root_main_behaviour_window_behaviour()
        self.enter_Root_root_main_behaviour_window_behaviour_waiting()
    
    def enterDefault_Root_root_main_behaviour_listening(self):
        self.enter_Root_root_main_behaviour_listening()
        self.enter_Root_root_main_behaviour_listening_listening()
    
    def enterDefault_Root_root_main_behaviour_listening_client(self):
        self.enter_Root_root_main_behaviour_listening_client()
        self.enter_Root_root_main_behaviour_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_deleting:
                catched = self.transition_Root_root_deleting(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_stopped:
                catched = self.transition_Root_root_stopped(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                self.grab_set()
                self.enterDefault_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
        enableds = []
        if event.name == "close" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "window-close" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'widgets']))
                self.enter_Root_root_deleting()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'widgets']))
                self.enter_Root_root_deleting()
            catched = True
        
        if not catched :
            catched = self.transition_Root_root_main_behaviour_creating_editors(event) or catched
            catched = self.transition_Root_root_main_behaviour_packing_widgets(event) or catched
            catched = self.transition_Root_root_main_behaviour_window_behaviour(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening_client(event) or catched
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_loop:
                catched = self.transition_Root_root_main_behaviour_creating_editors_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_creating:
                catched = self.transition_Root_root_main_behaviour_creating_editors_creating(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_running:
                catched = self.transition_Root_root_main_behaviour_creating_editors_running(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_loop(self, event) :
        catched = False
        enableds = []
        if self.editors :
            enableds.append(1)
        
        if not self.editors and self.buttons :
            enableds.append(2)
        
        if not self.editors and not self.buttons :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_editors_loop()
                ctor_parameters = self.editors.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "widgets",ctor_parameters["class_name"],ctor_parameters["constructor_parameters"]]))
                self.enter_Root_root_main_behaviour_creating_editors_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_editors_loop()
                ctor_parameters = self.buttons.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "widgets",ctor_parameters["class_name"],ctor_parameters["constructor_parameters"]]))
                self.enter_Root_root_main_behaviour_creating_editors_creating()
            elif enabled == 3 :
                self.exit_Root_root_main_behaviour_creating_editors_loop()
                self.enter_Root_root_main_behaviour_creating_editors_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_editors_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_running(self, event) :
        catched = False
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_packing_widgets][0] == self.Root_root_main_behaviour_packing_widgets_packing:
                catched = self.transition_Root_root_main_behaviour_packing_widgets_packing(event)
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets_packing(self, event) :
        catched = False
        enableds = []
        if event.name == "editor_created" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "button_created" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_packing_widgets_packing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                editor = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                editor.master.pack(side=tk.TOP, pady=5)
                tk.Label(master=editor.master, text=str(editor.attr_name) + ': ').pack(side=tk.LEFT)
                editor.pack(side=tk.LEFT)
                self.attr_to_editor[editor.attr_name] = editor
                print self.attr_to_editor
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            elif enabled == 2 :
                parameters = event.getParameters()
                button = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                button.pack(side=tk.TOP, fill=tk.Y)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_window_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_window_behaviour][0] == self.Root_root_main_behaviour_window_behaviour_waiting:
                catched = self.transition_Root_root_main_behaviour_window_behaviour_waiting(event)
        return catched
    
    def transition_Root_root_main_behaviour_window_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "grab_focus" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_window_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_window_behaviour_waiting()
                self.grab_set()
                self.enter_Root_root_main_behaviour_window_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening][0] == self.Root_root_main_behaviour_listening_listening:
                catched = self.transition_Root_root_main_behaviour_listening_listening(event)
            elif self.current_state[self.Root_root_main_behaviour_listening][0] == self.Root_root_main_behaviour_listening_checking_input:
                catched = self.transition_Root_root_main_behaviour_listening_checking_input(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_listening(self, event) :
        catched = False
        enableds = []
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] == 'user_confirmed' :
                enableds.append(1)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] != 'user_confirmed' :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_listening. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_listening_listening()
                attrs = {}
                self.input_ok = True
                self.input_check_result = ""
                for k, v in self.attr_to_editor.iteritems():
                    if not v.validate():
                        self.input_ok = False
                        self.input_check_result += 'Invalid entry for attribute %s.\n' % k
                self.enter_Root_root_main_behaviour_listening_checking_input()
            elif enabled == 2 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_listening_listening()
                send_event = Event("button_pressed", parameters = [event_parameters])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_listening()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_checking_input(self, event) :
        catched = False
        enableds = []
        if self.input_ok :
            enableds.append(1)
        
        if not self.input_ok :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_checking_input. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_listening_checking_input()
                attrs = {}
                for k, v in self.attr_to_editor.iteritems():
                    if k != StringValue('location') or not isinstance(self.t, client_object.Model):
                        attrs[k] = v.get_value()
                loc = self.attr_to_editor[StringValue('location')].get_value() if StringValue('location') in self.attr_to_editor else self.loc
                send_event = Event("instance_details_entered", parameters = [MappingValue({CreateConstants.TYPE_KEY: self.type_location, CreateConstants.LOCATION_KEY: loc, CreateConstants.ATTRS_KEY: MappingValue(attrs)})])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_listening_listening()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_listening_checking_input()
                send_event = Event("error", parameters = [797,self.input_check_result])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_listening_listening()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening_client][0] == self.Root_root_main_behaviour_listening_client_listening_client:
                catched = self.transition_Root_root_main_behaviour_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_main_behaviour_listening_client_listening_client()
                send_event = Event("client_request", parameters = [self.association_name + '/' + association_name,data])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_client_listening_client()
            catched = True
        
        return catched
    
    def transition_Root_root_deleting(self, event) :
        catched = False
        enableds = []
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_deleting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_deleting()
                send_event = Event("delete_window", parameters = [self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_stopped()
            catched = True
        
        return catched
    
    def transition_Root_root_stopped(self, event) :
        catched = False
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
    

class InstanceAttributeEditor(Window, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_main_behaviour = 2
    Root_root_main_behaviour_creating_editors = 3
    Root_root_main_behaviour_packing_widgets = 4
    Root_root_main_behaviour_window_behaviour = 5
    Root_root_main_behaviour_listening = 6
    Root_root_main_behaviour_listening_client = 7
    Root_root_initializing = 8
    Root_root_main_behaviour_creating_editors_waiting_client = 9
    Root_root_main_behaviour_creating_editors_loop_out_subclasses = 10
    Root_root_main_behaviour_creating_editors_waiting_client_read = 11
    Root_root_main_behaviour_creating_editors_waiting_client_subclasses = 12
    Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions = 13
    Root_root_main_behaviour_creating_editors_loop = 14
    Root_root_main_behaviour_creating_editors_creating = 15
    Root_root_main_behaviour_creating_editors_running = 16
    Root_root_main_behaviour_packing_widgets_packing = 17
    Root_root_main_behaviour_packing_widgets_done = 18
    Root_root_main_behaviour_window_behaviour_waiting = 19
    Root_root_main_behaviour_listening_listening = 20
    Root_root_main_behaviour_listening_checking_input = 21
    Root_root_main_behaviour_listening_client_listening_client = 22
    Root_root_deleting = 23
    Root_root_stopped = 24
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_main_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
        self.current_state[self.Root_root_main_behaviour_window_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_listening] = []
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def start(self):
        super(InstanceAttributeEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        Window.__init__(self, self.controller)
        self.minsize(width=256, height=256)
        self.instance = constructor_parameters['instance']
        self.instance_location = self.instance.location
        self.title('Edit %s Instance' % self.instance.name)
        
        self.attribute_frames = []
        self.attr_to_editor = {}
        
        self.editors = []
        
        for a in self.instance.attributes:
            if a.potency == IntegerValue(0):
                class_name = None
                the_type = a.the_type
                class_name = None
                if isinstance(the_type, StringType):
                    class_name = 'StringEditor'
                elif isinstance(the_type, LocationType):
                    class_name = 'LocationEditor'
                elif isinstance(the_type, BooleanType):
                    class_name = 'BooleanEditor'
                elif isinstance(the_type, IntegerType):
                    class_name = 'IntegerEditor'
                elif isinstance(the_type, FloatType):
                    class_name = 'FloatEditor'
                elif isinstance(the_type, AnyType):
                    class_name = 'AnyEditor'
                elif isinstance(the_type, EnumType):
                    class_name = 'EnumEditor'
                if isinstance(the_type, TypeType):
                    class_name = 'TypeEditor'
                elif the_type == UnionType(SequenceValue([IntegerType(), InfiniteType()])):
                    class_name = 'IntInfEditor'
                self.attribute_frames.append(tk.Frame(master=self))
                self.editors.append({'class_name': class_name, 'constructor_parameters': {'parent': self.attribute_frames[-1], 'attr_name': a.name, 'attr_type': a.the_type, 'value': a.value}})
        self.buttons = [{'class_name': 'Button', 'constructor_parameters': {'parent': self, 'visual': TextVisual('OK'), 'tooltip_text': 'Edit Instance', 'event_parameters': {'event_name': 'user_confirmed'}}}]
        self.compositions = []
        self.comp_loc_to_idx = {}
        self.curr_comp_idx = 0
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        if self.Root_root_deleting in self.current_state[self.Root_root] :
            self.exit_Root_root_deleting()
        if self.Root_root_stopped in self.current_state[self.Root_root] :
            self.exit_Root_root_stopped()
        self.current_state[self.Root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.exit_Root_root_main_behaviour_creating_editors()
        self.exit_Root_root_main_behaviour_packing_widgets()
        self.exit_Root_root_main_behaviour_window_behaviour()
        self.exit_Root_root_main_behaviour_listening()
        self.exit_Root_root_main_behaviour_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_editors(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_creating_editors)
    
    def exit_Root_root_main_behaviour_creating_editors(self):
        if self.Root_root_main_behaviour_creating_editors_waiting_client in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_waiting_client()
        if self.Root_root_main_behaviour_creating_editors_loop_out_subclasses in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_loop_out_subclasses()
        if self.Root_root_main_behaviour_creating_editors_waiting_client_read in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_waiting_client_read()
        if self.Root_root_main_behaviour_creating_editors_waiting_client_subclasses in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_waiting_client_subclasses()
        if self.Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions()
        if self.Root_root_main_behaviour_creating_editors_loop in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_loop()
        if self.Root_root_main_behaviour_creating_editors_creating in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_creating()
        if self.Root_root_main_behaviour_creating_editors_running in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_running()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_packing_widgets(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_packing_widgets)
    
    def exit_Root_root_main_behaviour_packing_widgets(self):
        if self.Root_root_main_behaviour_packing_widgets_packing in self.current_state[self.Root_root_main_behaviour_packing_widgets] :
            self.exit_Root_root_main_behaviour_packing_widgets_packing()
        if self.Root_root_main_behaviour_packing_widgets_done in self.current_state[self.Root_root_main_behaviour_packing_widgets] :
            self.exit_Root_root_main_behaviour_packing_widgets_done()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_window_behaviour(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_window_behaviour)
    
    def exit_Root_root_main_behaviour_window_behaviour(self):
        if self.Root_root_main_behaviour_window_behaviour_waiting in self.current_state[self.Root_root_main_behaviour_window_behaviour] :
            self.exit_Root_root_main_behaviour_window_behaviour_waiting()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening)
    
    def exit_Root_root_main_behaviour_listening(self):
        if self.Root_root_main_behaviour_listening_listening in self.current_state[self.Root_root_main_behaviour_listening] :
            self.exit_Root_root_main_behaviour_listening_listening()
        if self.Root_root_main_behaviour_listening_checking_input in self.current_state[self.Root_root_main_behaviour_listening] :
            self.exit_Root_root_main_behaviour_listening_checking_input()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_client(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client(self):
        if self.Root_root_main_behaviour_listening_client_listening_client in self.current_state[self.Root_root_main_behaviour_listening_client] :
            self.exit_Root_root_main_behaviour_listening_client_listening_client()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_editors_waiting_client(self):
        # TODO: Models!
        loc = self.instance.linguistic_type
        print loc
        send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'evaluate', 'request_parameters': {'args': [StringValue('get_all_out_associations'), loc], 'kwargs': {}}}])
        self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_waiting_client)
    
    def exit_Root_root_main_behaviour_creating_editors_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_loop_out_subclasses(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_loop_out_subclasses)
    
    def exit_Root_root_main_behaviour_creating_editors_loop_out_subclasses(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_waiting_client_read(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_waiting_client_read)
    
    def exit_Root_root_main_behaviour_creating_editors_waiting_client_read(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_waiting_client_subclasses(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_waiting_client_subclasses)
    
    def exit_Root_root_main_behaviour_creating_editors_waiting_client_subclasses(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions)
    
    def exit_Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_loop)
    
    def exit_Root_root_main_behaviour_creating_editors_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_creating)
    
    def exit_Root_root_main_behaviour_creating_editors_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_running)
    
    def exit_Root_root_main_behaviour_creating_editors_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets].append(self.Root_root_main_behaviour_packing_widgets_packing)
    
    def exit_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
    
    def enter_Root_root_main_behaviour_packing_widgets_done(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets].append(self.Root_root_main_behaviour_packing_widgets_done)
    
    def exit_Root_root_main_behaviour_packing_widgets_done(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
    
    def enter_Root_root_main_behaviour_window_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour].append(self.Root_root_main_behaviour_window_behaviour_waiting)
    
    def exit_Root_root_main_behaviour_window_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_listening(self):
        self.current_state[self.Root_root_main_behaviour_listening].append(self.Root_root_main_behaviour_listening_listening)
    
    def exit_Root_root_main_behaviour_listening_listening(self):
        self.current_state[self.Root_root_main_behaviour_listening] = []
    
    def enter_Root_root_main_behaviour_listening_checking_input(self):
        self.current_state[self.Root_root_main_behaviour_listening].append(self.Root_root_main_behaviour_listening_checking_input)
    
    def exit_Root_root_main_behaviour_listening_checking_input(self):
        self.current_state[self.Root_root_main_behaviour_listening] = []
    
    def enter_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client].append(self.Root_root_main_behaviour_listening_client_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def enter_Root_root_deleting(self):
        self.timers[0] = 0.05
        self.current_state[self.Root_root].append(self.Root_root_deleting)
    
    def exit_Root_root_deleting(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_stopped(self):
        self.current_state[self.Root_root].append(self.Root_root_stopped)
    
    def exit_Root_root_stopped(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_main_behaviour(self):
        self.enter_Root_root_main_behaviour()
        self.enterDefault_Root_root_main_behaviour_creating_editors()
        self.enterDefault_Root_root_main_behaviour_packing_widgets()
        self.enterDefault_Root_root_main_behaviour_window_behaviour()
        self.enterDefault_Root_root_main_behaviour_listening()
        self.enterDefault_Root_root_main_behaviour_listening_client()
    
    def enterDefault_Root_root_main_behaviour_creating_editors(self):
        self.enter_Root_root_main_behaviour_creating_editors()
        self.enter_Root_root_main_behaviour_creating_editors_waiting_client()
    
    def enterDefault_Root_root_main_behaviour_packing_widgets(self):
        self.enter_Root_root_main_behaviour_packing_widgets()
        self.enter_Root_root_main_behaviour_packing_widgets_packing()
    
    def enterDefault_Root_root_main_behaviour_window_behaviour(self):
        self.enter_Root_root_main_behaviour_window_behaviour()
        self.enter_Root_root_main_behaviour_window_behaviour_waiting()
    
    def enterDefault_Root_root_main_behaviour_listening(self):
        self.enter_Root_root_main_behaviour_listening()
        self.enter_Root_root_main_behaviour_listening_listening()
    
    def enterDefault_Root_root_main_behaviour_listening_client(self):
        self.enter_Root_root_main_behaviour_listening_client()
        self.enter_Root_root_main_behaviour_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_deleting:
                catched = self.transition_Root_root_deleting(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_stopped:
                catched = self.transition_Root_root_stopped(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                self.grab_set()
                self.enterDefault_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
        enableds = []
        if event.name == "close" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "window-close" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'widgets']))
                self.enter_Root_root_deleting()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'widgets']))
                self.enter_Root_root_deleting()
            catched = True
        
        if not catched :
            catched = self.transition_Root_root_main_behaviour_creating_editors(event) or catched
            catched = self.transition_Root_root_main_behaviour_packing_widgets(event) or catched
            catched = self.transition_Root_root_main_behaviour_window_behaviour(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening_client(event) or catched
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_waiting_client:
                catched = self.transition_Root_root_main_behaviour_creating_editors_waiting_client(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_loop_out_subclasses:
                catched = self.transition_Root_root_main_behaviour_creating_editors_loop_out_subclasses(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_waiting_client_read:
                catched = self.transition_Root_root_main_behaviour_creating_editors_waiting_client_read(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_waiting_client_subclasses:
                catched = self.transition_Root_root_main_behaviour_creating_editors_waiting_client_subclasses(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions:
                catched = self.transition_Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_loop:
                catched = self.transition_Root_root_main_behaviour_creating_editors_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_creating:
                catched = self.transition_Root_root_main_behaviour_creating_editors_creating(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_running:
                catched = self.transition_Root_root_main_behaviour_creating_editors_running(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_waiting_client()
                for a in response[StringValue("result")]:
                    print a.name
                    if a.potency > IntegerValue(0) and isinstance(a, client_object.Composition):
                        self.comp_loc_to_idx[a.location] = len(self.compositions)
                        self.compositions.append({'item': a, 'name': a.name, 'location': a.location, 'out_class': a.to_multiplicity.node, 'subclasses': [], 'children': []})
                self.enter_Root_root_main_behaviour_creating_editors_loop_out_subclasses()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_waiting_client()
                send_event = Event("error", parameters = [response.get_status_code(),response.get_status_message()])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_creating_editors_waiting_client()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_loop_out_subclasses(self, event) :
        catched = False
        enableds = []
        if self.curr_comp_idx < len(self.compositions) :
            enableds.append(1)
        
        if self.curr_comp_idx == len(self.compositions) :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_loop_out_subclasses. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_editors_loop_out_subclasses()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': self.compositions[self.curr_comp_idx]['out_class']}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, "parent" , send_event]))
                self.enter_Root_root_main_behaviour_creating_editors_waiting_client_read()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_editors_loop_out_subclasses()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'evaluate', 'request_parameters': {'args': [StringValue('get_out_associations'), self.instance_location], 'kwargs': {}}}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_waiting_client_read(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_waiting_client_read. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_waiting_client_read()
                self.compositions[self.curr_comp_idx]['out_class'] = response[StringValue('item')]
                if not response[StringValue('item')].abstract:
                    self.compositions[self.curr_comp_idx]['subclasses'].append(response[StringValue('item')].location)
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'evaluate', 'request_parameters': {'args': [StringValue('get_all_specialise_classes'), self.compositions[self.curr_comp_idx]['out_class'].location], 'kwargs': {}}}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, "parent" , send_event]))
                self.enter_Root_root_main_behaviour_creating_editors_waiting_client_subclasses()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_waiting_client_read()
                send_event = Event("error", parameters = [response.get_status_code(),response.get_status_message()])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_creating_editors_waiting_client_read()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_waiting_client_subclasses(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_waiting_client_subclasses. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_waiting_client_subclasses()
                print response
                for subclass in response[StringValue("result")]:
                    if not subclass.abstract:
                        self.compositions[self.curr_comp_idx]['subclasses'].append(subclass.location)
                self.curr_comp_idx += 1
                self.enter_Root_root_main_behaviour_creating_editors_loop_out_subclasses()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_waiting_client_subclasses()
                send_event = Event("error", parameters = [response.get_status_code(),response.get_status_message()])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_creating_editors_waiting_client_subclasses()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions()
                print response
                for a in response[StringValue("result")]:
                    if isinstance(a, client_object.Composition) and a.potency == IntegerValue(0):
                        self.compositions[self.comp_loc_to_idx[a.linguistic_type]]['children'].append({'location': a.to_multiplicity.node})
                for c in self.compositions:
                    self.attribute_frames.append(tk.Frame(master=self))
                    self.editors.append({'class_name': 'CompositionEditor', 'constructor_parameters': {'parent': self.attribute_frames[-1], 'location': self.instance.location, 'children': c['children'], 'subclasses': c['subclasses'], 'composition_name': c['name'], 'composition': c['item'], 'class_location': c['out_class'].location, 'class': c['out_class']}})
                self.enter_Root_root_main_behaviour_creating_editors_loop()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions()
                send_event = Event("error", parameters = [response.get_status_code(),response.get_status_message()])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_creating_editors_waiting_client_instance_compositions()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_loop(self, event) :
        catched = False
        enableds = []
        if self.editors :
            enableds.append(1)
        
        if not self.editors and self.buttons :
            enableds.append(2)
        
        if not self.editors and not self.buttons :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_editors_loop()
                ctor_parameters = self.editors.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "widgets",ctor_parameters["class_name"],ctor_parameters["constructor_parameters"]]))
                self.enter_Root_root_main_behaviour_creating_editors_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_editors_loop()
                ctor_parameters = self.buttons.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "widgets",ctor_parameters["class_name"],ctor_parameters["constructor_parameters"]]))
                self.enter_Root_root_main_behaviour_creating_editors_creating()
            elif enabled == 3 :
                self.exit_Root_root_main_behaviour_creating_editors_loop()
                self.enter_Root_root_main_behaviour_creating_editors_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_editors_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_running(self, event) :
        catched = False
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_packing_widgets][0] == self.Root_root_main_behaviour_packing_widgets_packing:
                catched = self.transition_Root_root_main_behaviour_packing_widgets_packing(event)
            elif self.current_state[self.Root_root_main_behaviour_packing_widgets][0] == self.Root_root_main_behaviour_packing_widgets_done:
                catched = self.transition_Root_root_main_behaviour_packing_widgets_done(event)
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets_packing(self, event) :
        catched = False
        enableds = []
        if event.name == "editor_created" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "button_created" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_packing_widgets_packing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                editor = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                editor.master.pack(side=tk.TOP, pady=5)
                if isinstance(editor, Editor):
                    tk.Label(master=editor.master, text=str(editor.attr_name) + ': ').pack(side=tk.LEFT)
                    self.attr_to_editor[editor.attr_name] = editor
                editor.pack(side=tk.LEFT)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            elif enabled == 2 :
                parameters = event.getParameters()
                button = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                button.pack(side=tk.TOP, fill=tk.Y)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets_done(self, event) :
        catched = False
        return catched
    
    def transition_Root_root_main_behaviour_window_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_window_behaviour][0] == self.Root_root_main_behaviour_window_behaviour_waiting:
                catched = self.transition_Root_root_main_behaviour_window_behaviour_waiting(event)
        return catched
    
    def transition_Root_root_main_behaviour_window_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "grab_focus" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_window_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_window_behaviour_waiting()
                self.grab_set()
                self.enter_Root_root_main_behaviour_window_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening][0] == self.Root_root_main_behaviour_listening_listening:
                catched = self.transition_Root_root_main_behaviour_listening_listening(event)
            elif self.current_state[self.Root_root_main_behaviour_listening][0] == self.Root_root_main_behaviour_listening_checking_input:
                catched = self.transition_Root_root_main_behaviour_listening_checking_input(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_listening(self, event) :
        catched = False
        enableds = []
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] == 'user_confirmed' :
                enableds.append(1)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] != 'user_confirmed' :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_listening. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_listening_listening()
                attrs = {}
                self.input_ok = True
                self.input_check_result = ""
                for k, v in self.attr_to_editor.iteritems():
                    if not v.validate():
                        self.input_ok = False
                        self.input_check_result += 'Invalid entry for attribute %s.\n' % k
                self.enter_Root_root_main_behaviour_listening_checking_input()
            elif enabled == 2 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_listening_listening()
                send_event = Event("button_pressed", parameters = [event_parameters])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_listening()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_checking_input(self, event) :
        catched = False
        enableds = []
        if self.input_ok :
            enableds.append(1)
        
        if not self.input_ok :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_checking_input. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_listening_checking_input()
                attrs = {}
                for k, v in self.attr_to_editor.iteritems():
                    attrs[k] = v.get_value()
                send_event = Event("instance_details_entered", parameters = [MappingValue({UpdateConstants.TYPE_KEY: self.instance.linguistic_type, UpdateConstants.LOCATION_KEY: self.instance_location, UpdateConstants.ATTRS_KEY: MappingValue(attrs)})])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_listening_listening()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_listening_checking_input()
                send_event = Event("error", parameters = [797,self.input_check_result])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_listening_listening()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening_client][0] == self.Root_root_main_behaviour_listening_client_listening_client:
                catched = self.transition_Root_root_main_behaviour_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_main_behaviour_listening_client_listening_client()
                send_event = Event("client_request", parameters = [self.association_name + '/' + association_name,data])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_client_listening_client()
            catched = True
        
        return catched
    
    def transition_Root_root_deleting(self, event) :
        catched = False
        enableds = []
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_deleting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_deleting()
                send_event = Event("delete_window", parameters = [self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_stopped()
            catched = True
        
        return catched
    
    def transition_Root_root_stopped(self, event) :
        catched = False
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
    

class InputWindow(Window, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_main_behaviour = 2
    Root_root_main_behaviour_creating_editors = 3
    Root_root_main_behaviour_packing_widgets = 4
    Root_root_main_behaviour_window_behaviour = 5
    Root_root_main_behaviour_listening = 6
    Root_root_main_behaviour_listening_client = 7
    Root_root_initializing = 8
    Root_root_main_behaviour_creating_editors_loop = 9
    Root_root_main_behaviour_creating_editors_creating = 10
    Root_root_main_behaviour_creating_editors_running = 11
    Root_root_main_behaviour_packing_widgets_packing = 12
    Root_root_main_behaviour_window_behaviour_waiting = 13
    Root_root_main_behaviour_listening_listening = 14
    Root_root_main_behaviour_listening_checking_input = 15
    Root_root_main_behaviour_listening_client_listening_client = 16
    Root_root_deleting = 17
    Root_root_stopped = 18
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_main_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
        self.current_state[self.Root_root_main_behaviour_window_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_listening] = []
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def start(self):
        super(InputWindow, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        Window.__init__(self, self.controller)
        self.title('Enter Input')
        self.minsize(width=256, height=256)
        self.option_names = constructor_parameters["option_names"]
        self.editors = []
        self.input_frames = []
        self.attr_to_editor = {}
        
        for n in self.option_names:
            self.input_frames.append(tk.Frame(master=self))
            self.editors.append({'class_name': 'StringEditor', 'constructor_parameters': {'parent': self.input_frames[-1], 'attr_name': n, 'attr_type': StringType(), 'value': ''}})
        self.buttons = [{'class_name': 'Button', 'constructor_parameters': {'parent': self, 'visual': TextVisual('OK'), 'tooltip_text': 'OK', 'event_parameters': {'event_name': 'user_confirmed'}}}]
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        if self.Root_root_deleting in self.current_state[self.Root_root] :
            self.exit_Root_root_deleting()
        if self.Root_root_stopped in self.current_state[self.Root_root] :
            self.exit_Root_root_stopped()
        self.current_state[self.Root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.exit_Root_root_main_behaviour_creating_editors()
        self.exit_Root_root_main_behaviour_packing_widgets()
        self.exit_Root_root_main_behaviour_window_behaviour()
        self.exit_Root_root_main_behaviour_listening()
        self.exit_Root_root_main_behaviour_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_editors(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_creating_editors)
    
    def exit_Root_root_main_behaviour_creating_editors(self):
        if self.Root_root_main_behaviour_creating_editors_loop in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_loop()
        if self.Root_root_main_behaviour_creating_editors_creating in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_creating()
        if self.Root_root_main_behaviour_creating_editors_running in self.current_state[self.Root_root_main_behaviour_creating_editors] :
            self.exit_Root_root_main_behaviour_creating_editors_running()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_packing_widgets(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_packing_widgets)
    
    def exit_Root_root_main_behaviour_packing_widgets(self):
        if self.Root_root_main_behaviour_packing_widgets_packing in self.current_state[self.Root_root_main_behaviour_packing_widgets] :
            self.exit_Root_root_main_behaviour_packing_widgets_packing()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_window_behaviour(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_window_behaviour)
    
    def exit_Root_root_main_behaviour_window_behaviour(self):
        if self.Root_root_main_behaviour_window_behaviour_waiting in self.current_state[self.Root_root_main_behaviour_window_behaviour] :
            self.exit_Root_root_main_behaviour_window_behaviour_waiting()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening)
    
    def exit_Root_root_main_behaviour_listening(self):
        if self.Root_root_main_behaviour_listening_listening in self.current_state[self.Root_root_main_behaviour_listening] :
            self.exit_Root_root_main_behaviour_listening_listening()
        if self.Root_root_main_behaviour_listening_checking_input in self.current_state[self.Root_root_main_behaviour_listening] :
            self.exit_Root_root_main_behaviour_listening_checking_input()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_client(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client(self):
        if self.Root_root_main_behaviour_listening_client_listening_client in self.current_state[self.Root_root_main_behaviour_listening_client] :
            self.exit_Root_root_main_behaviour_listening_client_listening_client()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_editors_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_loop)
    
    def exit_Root_root_main_behaviour_creating_editors_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_creating)
    
    def exit_Root_root_main_behaviour_creating_editors_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_creating_editors_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors].append(self.Root_root_main_behaviour_creating_editors_running)
    
    def exit_Root_root_main_behaviour_creating_editors_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_editors] = []
    
    def enter_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets].append(self.Root_root_main_behaviour_packing_widgets_packing)
    
    def exit_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
    
    def enter_Root_root_main_behaviour_window_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour].append(self.Root_root_main_behaviour_window_behaviour_waiting)
    
    def exit_Root_root_main_behaviour_window_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_listening(self):
        self.current_state[self.Root_root_main_behaviour_listening].append(self.Root_root_main_behaviour_listening_listening)
    
    def exit_Root_root_main_behaviour_listening_listening(self):
        self.current_state[self.Root_root_main_behaviour_listening] = []
    
    def enter_Root_root_main_behaviour_listening_checking_input(self):
        self.current_state[self.Root_root_main_behaviour_listening].append(self.Root_root_main_behaviour_listening_checking_input)
    
    def exit_Root_root_main_behaviour_listening_checking_input(self):
        self.current_state[self.Root_root_main_behaviour_listening] = []
    
    def enter_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client].append(self.Root_root_main_behaviour_listening_client_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def enter_Root_root_deleting(self):
        self.timers[0] = 0.05
        self.current_state[self.Root_root].append(self.Root_root_deleting)
    
    def exit_Root_root_deleting(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_stopped(self):
        self.current_state[self.Root_root].append(self.Root_root_stopped)
    
    def exit_Root_root_stopped(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_main_behaviour(self):
        self.enter_Root_root_main_behaviour()
        self.enterDefault_Root_root_main_behaviour_creating_editors()
        self.enterDefault_Root_root_main_behaviour_packing_widgets()
        self.enterDefault_Root_root_main_behaviour_window_behaviour()
        self.enterDefault_Root_root_main_behaviour_listening()
        self.enterDefault_Root_root_main_behaviour_listening_client()
    
    def enterDefault_Root_root_main_behaviour_creating_editors(self):
        self.enter_Root_root_main_behaviour_creating_editors()
        self.enter_Root_root_main_behaviour_creating_editors_loop()
    
    def enterDefault_Root_root_main_behaviour_packing_widgets(self):
        self.enter_Root_root_main_behaviour_packing_widgets()
        self.enter_Root_root_main_behaviour_packing_widgets_packing()
    
    def enterDefault_Root_root_main_behaviour_window_behaviour(self):
        self.enter_Root_root_main_behaviour_window_behaviour()
        self.enter_Root_root_main_behaviour_window_behaviour_waiting()
    
    def enterDefault_Root_root_main_behaviour_listening(self):
        self.enter_Root_root_main_behaviour_listening()
        self.enter_Root_root_main_behaviour_listening_listening()
    
    def enterDefault_Root_root_main_behaviour_listening_client(self):
        self.enter_Root_root_main_behaviour_listening_client()
        self.enter_Root_root_main_behaviour_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_deleting:
                catched = self.transition_Root_root_deleting(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_stopped:
                catched = self.transition_Root_root_stopped(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                self.grab_set()
                self.enterDefault_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
        enableds = []
        if event.name == "close" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "window-close" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'widgets']))
                self.enter_Root_root_deleting()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'widgets']))
                self.enter_Root_root_deleting()
            catched = True
        
        if not catched :
            catched = self.transition_Root_root_main_behaviour_creating_editors(event) or catched
            catched = self.transition_Root_root_main_behaviour_packing_widgets(event) or catched
            catched = self.transition_Root_root_main_behaviour_window_behaviour(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening_client(event) or catched
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_loop:
                catched = self.transition_Root_root_main_behaviour_creating_editors_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_creating:
                catched = self.transition_Root_root_main_behaviour_creating_editors_creating(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_editors][0] == self.Root_root_main_behaviour_creating_editors_running:
                catched = self.transition_Root_root_main_behaviour_creating_editors_running(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_loop(self, event) :
        catched = False
        enableds = []
        if self.editors :
            enableds.append(1)
        
        if not self.editors and self.buttons :
            enableds.append(2)
        
        if not self.editors and not self.buttons :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_editors_loop()
                ctor_parameters = self.editors.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "widgets",ctor_parameters["class_name"],ctor_parameters["constructor_parameters"]]))
                self.enter_Root_root_main_behaviour_creating_editors_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_editors_loop()
                ctor_parameters = self.buttons.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "widgets",ctor_parameters["class_name"],ctor_parameters["constructor_parameters"]]))
                self.enter_Root_root_main_behaviour_creating_editors_creating()
            elif enabled == 3 :
                self.exit_Root_root_main_behaviour_creating_editors_loop()
                self.enter_Root_root_main_behaviour_creating_editors_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_editors_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_editors_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_editors_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_editors_running(self, event) :
        catched = False
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_packing_widgets][0] == self.Root_root_main_behaviour_packing_widgets_packing:
                catched = self.transition_Root_root_main_behaviour_packing_widgets_packing(event)
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets_packing(self, event) :
        catched = False
        enableds = []
        if event.name == "editor_created" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "button_created" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_packing_widgets_packing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                editor = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                editor.master.pack(side=tk.TOP, pady=5)
                tk.Label(master=editor.master, text=str(editor.attr_name) + ': ').pack(side=tk.LEFT)
                editor.pack(side=tk.LEFT)
                self.attr_to_editor[editor.attr_name] = editor
                print self.attr_to_editor
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            elif enabled == 2 :
                parameters = event.getParameters()
                button = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                button.pack(side=tk.TOP, fill=tk.Y)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_window_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_window_behaviour][0] == self.Root_root_main_behaviour_window_behaviour_waiting:
                catched = self.transition_Root_root_main_behaviour_window_behaviour_waiting(event)
        return catched
    
    def transition_Root_root_main_behaviour_window_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "grab_focus" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_window_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_window_behaviour_waiting()
                self.grab_set()
                self.enter_Root_root_main_behaviour_window_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening][0] == self.Root_root_main_behaviour_listening_listening:
                catched = self.transition_Root_root_main_behaviour_listening_listening(event)
            elif self.current_state[self.Root_root_main_behaviour_listening][0] == self.Root_root_main_behaviour_listening_checking_input:
                catched = self.transition_Root_root_main_behaviour_listening_checking_input(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_listening(self, event) :
        catched = False
        enableds = []
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] == 'user_confirmed' :
                enableds.append(1)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] != 'user_confirmed' :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_listening. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_listening_listening()
                attrs = {}
                self.input_ok = True
                self.input_check_result = ""
                for k, v in self.attr_to_editor.iteritems():
                    if not v.validate():
                        self.input_ok = False
                        self.input_check_result += 'Invalid entry for attribute %s.\n' % k
                self.enter_Root_root_main_behaviour_listening_checking_input()
            elif enabled == 2 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_listening_listening()
                send_event = Event("button_pressed", parameters = [event_parameters])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_listening()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_checking_input(self, event) :
        catched = False
        enableds = []
        if self.input_ok :
            enableds.append(1)
        
        if not self.input_ok :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_checking_input. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_listening_checking_input()
                attrs = {}
                for k, v in self.attr_to_editor.iteritems():
                    attrs[k] = v.get_value()
                send_event = Event("input_given", parameters = [attrs])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_listening_listening()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_listening_checking_input()
                send_event = Event("error", parameters = [797,self.input_check_result])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_listening_listening()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening_client][0] == self.Root_root_main_behaviour_listening_client_listening_client:
                catched = self.transition_Root_root_main_behaviour_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_main_behaviour_listening_client_listening_client()
                send_event = Event("client_request", parameters = [self.association_name + '/' + association_name,data])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_client_listening_client()
            catched = True
        
        return catched
    
    def transition_Root_root_deleting(self, event) :
        catched = False
        enableds = []
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_deleting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_deleting()
                send_event = Event("delete_window", parameters = [self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_stopped()
            catched = True
        
        return catched
    
    def transition_Root_root_stopped(self, event) :
        catched = False
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
    

class Editor(RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_idle = 1
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
    
    def start(self):
        super(Editor, self).start()
        self.enter_Root_idle()
    
    #The actual constructor
    def __init__(self, controller, attr_name, attr_type):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        self.attr_name = attr_name
        self.attr_type = attr_type
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_idle(self):
        self.current_state[self.Root].append(self.Root_idle)
    
    def exit_Root_idle(self):
        self.current_state[self.Root] = []
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_idle:
                catched = self.transition_Root_idle(event)
        return catched
    
    def transition_Root_idle(self, event) :
        catched = False
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
    

class EntryEditor(Editor, tk.Entry, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_idle = 1
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
    
    def start(self):
        super(EntryEditor, self).start()
        self.enter_Root_idle()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        tk.Entry.__init__(self, constructor_parameters['parent'])
        self.insert(0, constructor_parameters['value'])
        Editor.__init__(self, self.controller, constructor_parameters['attr_name'], constructor_parameters['attr_type'])
        self.insert(0, '')
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_idle(self):
        self.current_state[self.Root].append(self.Root_idle)
    
    def exit_Root_idle(self):
        self.current_state[self.Root] = []
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_idle:
                catched = self.transition_Root_idle(event)
        return catched
    
    def transition_Root_idle(self, event) :
        catched = False
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
    

class AnyEditor(EntryEditor, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_main_behaviour = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(AnyEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        EntryEditor.__init__(self, self.controller, constructor_parameters)
    
    # User defined method
    def get_value(self):
        val = self.get().strip()
        if val.find('Value(') != -1:
            return eval(val)
        else:
            return AnyValue()
        
    # User defined method
    def validate(self):
        val = self.get().strip()
        try:
            if val.find('Value(') != -1:
                eval(val)
        except:
            return False
        return True
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("editor_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
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
    

class BooleanEditor(EntryEditor, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_main_behaviour = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(BooleanEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        EntryEditor.__init__(self, self.controller, constructor_parameters)
    
    # User defined method
    def get_value(self):
        val = self.get().strip()
        if val.find('BooleanValue(') == 0:
            return eval(val)
        else:
            if val == 'True':
                val = 1
            elif val == 'False':
                val = 0
            return BooleanValue(int(val))
        
    # User defined method
    def validate(self):
        val = self.get().strip()
        return val == 'True' or val == 'False' or re.search("^-?[0-9]+$|^BooleanValue\((-?[0-9]+|True|False)\)$", self.get().strip())
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("editor_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
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
    

class EnumEditor(EntryEditor, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_main_behaviour = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(EnumEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        EntryEditor.__init__(self, self.controller, constructor_parameters)
    
    # User defined method
    def get_value(self):
        val = self.get().strip()
        return self.attr_type.get_val(StringValue(val))
        
    # User defined method
    def validate(self):
        val = self.get().strip()
        try:
            self.attr_type.get_val(StringValue(val))
            return True
        except:
            return False
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("editor_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
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
    

class FloatEditor(EntryEditor, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_main_behaviour = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(FloatEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        EntryEditor.__init__(self, self.controller, constructor_parameters)
    
    # User defined method
    def get_value(self):
        val = self.get().strip()
        if val.find('Value(') != -1:
            return eval(val)
        else:
            return FloatValue(float(val))
        
    # User defined method
    def validate(self):
        return re.search("^-?[0-9]*?(.[0-9]+)$|^FloatValue\(-?[0-9]*?(.[0-9]+)\)$", self.get().strip())
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("editor_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
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
    

class IntInfEditor(EntryEditor, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_main_behaviour = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(IntInfEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        EntryEditor.__init__(self, self.controller, constructor_parameters)
    
    # User defined method
    def get_value(self):
        val = self.get().strip()
        if val.find('inf') == 0 or val.find('inf') == 1:
            return InfiniteValue(val)
        else:
            return IntegerValue(int(val))
        
    # User defined method
    def validate(self):
        return re.search("^-?[0-9]+$|^IntegerValue\(-?[0-9]+\)$|^(-|\+)?inf$", self.get().strip())
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("editor_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
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
    

class IntegerEditor(EntryEditor, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_main_behaviour = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(IntegerEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        EntryEditor.__init__(self, self.controller, constructor_parameters)
    
    # User defined method
    def get_value(self):
        val = self.get().strip()
        if val.find('Value(') != -1:
            return eval(val)
        else:
            return IntegerValue(int(val))
        
    # User defined method
    def validate(self):
        return re.search("^-?[0-9]+$|^IntegerValue\(-?[0-9]+\)$", self.get().strip())
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("editor_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
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
    

class LocationEditor(EntryEditor, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_main_behaviour = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(LocationEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        EntryEditor.__init__(self, self.controller, constructor_parameters)
    
    # User defined method
    def get_value(self):
        val = self.get().strip()
        if val.find('LocationValue(') == 0:
            return eval(val)
        else:
            return LocationValue(val)
        
    # User defined method
    def validate(self):
        return re.search("^[a-zA-Z0-9]*$|^([a-zA-Z0-9]+\.[a-zA-Z0-9]+)+$|^LocationValue\(\'([a-zA-Z0-9]*|([a-zA-Z0-9]+\.[a-zA-Z0-9]+)+)\'\)$", self.get().strip())
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("editor_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
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
    

class StringEditor(EntryEditor, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_main_behaviour = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(StringEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        EntryEditor.__init__(self, self.controller, constructor_parameters)
    
    # User defined method
    def get_value(self):
        val = self.get().strip()
        if (val.startswith("StringValue('") or val.startswith("LocationValue('")) and val.endswith("')"):
            return eval(val)
        else:
            return StringValue(val)
        
    # User defined method
    def validate(self):
        return True
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("editor_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
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
    

class TypeEditor(EntryEditor, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_main_behaviour = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(TypeEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        EntryEditor.__init__(self, self.controller, constructor_parameters)
    
    # User defined method
    def get_value(self):
        val = self.get().strip()
        return eval(val + '()')
        
    # User defined method
    def validate(self):
        val = self.get().strip()
        try:
            eval(val + '()')
        except:
            return False
        return True
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("editor_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
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
    

class CompositionEditor(tk.Frame, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_main_behaviour = 2
    Root_root_main_behaviour_running = 3
    Root_root_main_behaviour_running_editing_child = 4
    Root_root_main_behaviour_running_creating_child = 5
    Root_root_main_behaviour_label_behaviour = 6
    Root_root_main_behaviour_packing_widgets = 7
    Root_root_main_behaviour_error_behaviour = 8
    Root_root_main_behaviour_window_behaviour = 9
    Root_root_main_behaviour_listening_client = 10
    Root_root_initializing = 11
    Root_root_main_behaviour_running_creating_button = 12
    Root_root_main_behaviour_running_creating_labels = 13
    Root_root_main_behaviour_running_waiting = 14
    Root_root_main_behaviour_running_waiting_for_second = 15
    Root_root_main_behaviour_running_waiting_client_read = 16
    Root_root_main_behaviour_running_editing_child_entering_instance_details = 17
    Root_root_main_behaviour_running_editing_child_waiting_client = 18
    Root_root_main_behaviour_running_editing_child_waiting_client_read = 19
    Root_root_main_behaviour_running_creating_child_choosing_subclass = 20
    Root_root_main_behaviour_running_creating_child_waiting_close = 21
    Root_root_main_behaviour_running_creating_child_reading_type = 22
    Root_root_main_behaviour_running_creating_child_entering_instance_details = 23
    Root_root_main_behaviour_running_creating_child_waiting_client = 24
    Root_root_main_behaviour_running_creating_child_reading_new_child = 25
    Root_root_main_behaviour_running_creating_child_entering_composition_details = 26
    Root_root_main_behaviour_running_creating_child_waiting_client_composition = 27
    Root_root_main_behaviour_label_behaviour_waiting = 28
    Root_root_main_behaviour_label_behaviour_creating_label = 29
    Root_root_main_behaviour_packing_widgets_packing = 30
    Root_root_main_behaviour_error_behaviour_waiting = 31
    Root_root_main_behaviour_window_behaviour_waiting = 32
    Root_root_main_behaviour_window_behaviour_creating = 33
    Root_root_main_behaviour_window_behaviour_starting = 34
    Root_root_main_behaviour_listening_client_listening_client = 35
    Root_root_deleting = 36
    Root_root_stopped = 37
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_main_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_running] = []
        self.current_state[self.Root_root_main_behaviour_running_editing_child] = []
        self.current_state[self.Root_root_main_behaviour_running_creating_child] = []
        self.current_state[self.Root_root_main_behaviour_label_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
        self.current_state[self.Root_root_main_behaviour_error_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_window_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def start(self):
        super(CompositionEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        tk.Frame.__init__(self, constructor_parameters['parent'], borderwidth=1)
        self.composition_name = constructor_parameters['composition_name']
        self.composition = constructor_parameters['composition']
        self.class_location = constructor_parameters['class_location']
        self.clazz = constructor_parameters['class']
        self.assoc_children = constructor_parameters['children']
        self.subclasses = constructor_parameters['subclasses']
        self.location = constructor_parameters['location']
        self.curr_child_idx = 0
        
        self.class_name = self.class_location.substring(start=self.class_location.rfind(StringValue('.')) + IntegerValue(1))
        self.add_button = {"class_name": "Button", "parent": self, "visual": TextVisual('Add %s' % self.class_name), "tooltip_text": 'Add %s' % self.class_name, "event_parameters": {"event_name": "create_child"}}
        tk.Label(master=self, text=str(self.composition_name) + ': ', pady=10).pack(side=tk.TOP, expand=True, fill=tk.X)
        self.inner_frame = tk.Frame(self, pady=10, bg="white", width=250, height=50)
        self.inner_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.labels = []
        for c in self.assoc_children:
            print c["location"]
            self.labels.append({'parent': self.inner_frame, 'text': c["location"].substring(start=c["location"].rfind(StringValue('.')) + IntegerValue(1))})
        
        self.name_to_assoc = {}
        self.curr_name = None
        self.curr_label_idx = 0
        self.loc_to_label = {}
        self.text = None
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        if self.Root_root_deleting in self.current_state[self.Root_root] :
            self.exit_Root_root_deleting()
        if self.Root_root_stopped in self.current_state[self.Root_root] :
            self.exit_Root_root_stopped()
        self.current_state[self.Root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.exit_Root_root_main_behaviour_running()
        self.exit_Root_root_main_behaviour_label_behaviour()
        self.exit_Root_root_main_behaviour_packing_widgets()
        self.exit_Root_root_main_behaviour_error_behaviour()
        self.exit_Root_root_main_behaviour_window_behaviour()
        self.exit_Root_root_main_behaviour_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_running(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_running)
    
    def exit_Root_root_main_behaviour_running(self):
        if self.Root_root_main_behaviour_running_creating_button in self.current_state[self.Root_root_main_behaviour_running] :
            self.exit_Root_root_main_behaviour_running_creating_button()
        if self.Root_root_main_behaviour_running_creating_labels in self.current_state[self.Root_root_main_behaviour_running] :
            self.exit_Root_root_main_behaviour_running_creating_labels()
        if self.Root_root_main_behaviour_running_waiting in self.current_state[self.Root_root_main_behaviour_running] :
            self.exit_Root_root_main_behaviour_running_waiting()
        if self.Root_root_main_behaviour_running_waiting_for_second in self.current_state[self.Root_root_main_behaviour_running] :
            self.exit_Root_root_main_behaviour_running_waiting_for_second()
        if self.Root_root_main_behaviour_running_waiting_client_read in self.current_state[self.Root_root_main_behaviour_running] :
            self.exit_Root_root_main_behaviour_running_waiting_client_read()
        if self.Root_root_main_behaviour_running_editing_child in self.current_state[self.Root_root_main_behaviour_running] :
            self.exit_Root_root_main_behaviour_running_editing_child()
        if self.Root_root_main_behaviour_running_creating_child in self.current_state[self.Root_root_main_behaviour_running] :
            self.exit_Root_root_main_behaviour_running_creating_child()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_running_editing_child(self):
        self.current_state[self.Root_root_main_behaviour_running].append(self.Root_root_main_behaviour_running_editing_child)
    
    def exit_Root_root_main_behaviour_running_editing_child(self):
        if self.Root_root_main_behaviour_running_editing_child_entering_instance_details in self.current_state[self.Root_root_main_behaviour_running_editing_child] :
            self.exit_Root_root_main_behaviour_running_editing_child_entering_instance_details()
        if self.Root_root_main_behaviour_running_editing_child_waiting_client in self.current_state[self.Root_root_main_behaviour_running_editing_child] :
            self.exit_Root_root_main_behaviour_running_editing_child_waiting_client()
        if self.Root_root_main_behaviour_running_editing_child_waiting_client_read in self.current_state[self.Root_root_main_behaviour_running_editing_child] :
            self.exit_Root_root_main_behaviour_running_editing_child_waiting_client_read()
        self.current_state[self.Root_root_main_behaviour_running] = []
    
    def enter_Root_root_main_behaviour_running_creating_child(self):
        self.current_state[self.Root_root_main_behaviour_running].append(self.Root_root_main_behaviour_running_creating_child)
    
    def exit_Root_root_main_behaviour_running_creating_child(self):
        if self.Root_root_main_behaviour_running_creating_child_choosing_subclass in self.current_state[self.Root_root_main_behaviour_running_creating_child] :
            self.exit_Root_root_main_behaviour_running_creating_child_choosing_subclass()
        if self.Root_root_main_behaviour_running_creating_child_waiting_close in self.current_state[self.Root_root_main_behaviour_running_creating_child] :
            self.exit_Root_root_main_behaviour_running_creating_child_waiting_close()
        if self.Root_root_main_behaviour_running_creating_child_reading_type in self.current_state[self.Root_root_main_behaviour_running_creating_child] :
            self.exit_Root_root_main_behaviour_running_creating_child_reading_type()
        if self.Root_root_main_behaviour_running_creating_child_entering_instance_details in self.current_state[self.Root_root_main_behaviour_running_creating_child] :
            self.exit_Root_root_main_behaviour_running_creating_child_entering_instance_details()
        if self.Root_root_main_behaviour_running_creating_child_waiting_client in self.current_state[self.Root_root_main_behaviour_running_creating_child] :
            self.exit_Root_root_main_behaviour_running_creating_child_waiting_client()
        if self.Root_root_main_behaviour_running_creating_child_reading_new_child in self.current_state[self.Root_root_main_behaviour_running_creating_child] :
            self.exit_Root_root_main_behaviour_running_creating_child_reading_new_child()
        if self.Root_root_main_behaviour_running_creating_child_entering_composition_details in self.current_state[self.Root_root_main_behaviour_running_creating_child] :
            self.exit_Root_root_main_behaviour_running_creating_child_entering_composition_details()
        if self.Root_root_main_behaviour_running_creating_child_waiting_client_composition in self.current_state[self.Root_root_main_behaviour_running_creating_child] :
            self.exit_Root_root_main_behaviour_running_creating_child_waiting_client_composition()
        self.current_state[self.Root_root_main_behaviour_running] = []
    
    def enter_Root_root_main_behaviour_label_behaviour(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_label_behaviour)
    
    def exit_Root_root_main_behaviour_label_behaviour(self):
        if self.Root_root_main_behaviour_label_behaviour_waiting in self.current_state[self.Root_root_main_behaviour_label_behaviour] :
            self.exit_Root_root_main_behaviour_label_behaviour_waiting()
        if self.Root_root_main_behaviour_label_behaviour_creating_label in self.current_state[self.Root_root_main_behaviour_label_behaviour] :
            self.exit_Root_root_main_behaviour_label_behaviour_creating_label()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_packing_widgets(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_packing_widgets)
    
    def exit_Root_root_main_behaviour_packing_widgets(self):
        if self.Root_root_main_behaviour_packing_widgets_packing in self.current_state[self.Root_root_main_behaviour_packing_widgets] :
            self.exit_Root_root_main_behaviour_packing_widgets_packing()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_error_behaviour(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_error_behaviour)
    
    def exit_Root_root_main_behaviour_error_behaviour(self):
        if self.Root_root_main_behaviour_error_behaviour_waiting in self.current_state[self.Root_root_main_behaviour_error_behaviour] :
            self.exit_Root_root_main_behaviour_error_behaviour_waiting()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_window_behaviour(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_window_behaviour)
    
    def exit_Root_root_main_behaviour_window_behaviour(self):
        if self.Root_root_main_behaviour_window_behaviour_waiting in self.current_state[self.Root_root_main_behaviour_window_behaviour] :
            self.exit_Root_root_main_behaviour_window_behaviour_waiting()
        if self.Root_root_main_behaviour_window_behaviour_creating in self.current_state[self.Root_root_main_behaviour_window_behaviour] :
            self.exit_Root_root_main_behaviour_window_behaviour_creating()
        if self.Root_root_main_behaviour_window_behaviour_starting in self.current_state[self.Root_root_main_behaviour_window_behaviour] :
            self.exit_Root_root_main_behaviour_window_behaviour_starting()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_client(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client(self):
        if self.Root_root_main_behaviour_listening_client_listening_client in self.current_state[self.Root_root_main_behaviour_listening_client] :
            self.exit_Root_root_main_behaviour_listening_client_listening_client()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_running_creating_button(self):
        self.object_manager.addEvent(Event("create_instance", parameters = [self, "buttons",self.add_button["class_name"],self.add_button]))
        self.current_state[self.Root_root_main_behaviour_running].append(self.Root_root_main_behaviour_running_creating_button)
    
    def exit_Root_root_main_behaviour_running_creating_button(self):
        self.current_state[self.Root_root_main_behaviour_running] = []
    
    def enter_Root_root_main_behaviour_running_creating_labels(self):
        self.current_state[self.Root_root_main_behaviour_running].append(self.Root_root_main_behaviour_running_creating_labels)
    
    def exit_Root_root_main_behaviour_running_creating_labels(self):
        self.current_state[self.Root_root_main_behaviour_running] = []
    
    def enter_Root_root_main_behaviour_running_waiting(self):
        self.current_state[self.Root_root_main_behaviour_running].append(self.Root_root_main_behaviour_running_waiting)
    
    def exit_Root_root_main_behaviour_running_waiting(self):
        self.current_state[self.Root_root_main_behaviour_running] = []
    
    def enter_Root_root_main_behaviour_running_waiting_for_second(self):
        self.timers[0] = 0.3
        self.current_state[self.Root_root_main_behaviour_running].append(self.Root_root_main_behaviour_running_waiting_for_second)
    
    def exit_Root_root_main_behaviour_running_waiting_for_second(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root_main_behaviour_running] = []
    
    def enter_Root_root_main_behaviour_running_waiting_client_read(self):
        self.current_state[self.Root_root_main_behaviour_running].append(self.Root_root_main_behaviour_running_waiting_client_read)
    
    def exit_Root_root_main_behaviour_running_waiting_client_read(self):
        self.current_state[self.Root_root_main_behaviour_running] = []
    
    def enter_Root_root_main_behaviour_running_editing_child_entering_instance_details(self):
        self.current_state[self.Root_root_main_behaviour_running_editing_child].append(self.Root_root_main_behaviour_running_editing_child_entering_instance_details)
    
    def exit_Root_root_main_behaviour_running_editing_child_entering_instance_details(self):
        self.current_state[self.Root_root_main_behaviour_running_editing_child] = []
    
    def enter_Root_root_main_behaviour_running_editing_child_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_running_editing_child].append(self.Root_root_main_behaviour_running_editing_child_waiting_client)
    
    def exit_Root_root_main_behaviour_running_editing_child_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_running_editing_child] = []
    
    def enter_Root_root_main_behaviour_running_editing_child_waiting_client_read(self):
        self.current_state[self.Root_root_main_behaviour_running_editing_child].append(self.Root_root_main_behaviour_running_editing_child_waiting_client_read)
    
    def exit_Root_root_main_behaviour_running_editing_child_waiting_client_read(self):
        self.current_state[self.Root_root_main_behaviour_running_editing_child] = []
    
    def enter_Root_root_main_behaviour_running_creating_child_choosing_subclass(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child].append(self.Root_root_main_behaviour_running_creating_child_choosing_subclass)
    
    def exit_Root_root_main_behaviour_running_creating_child_choosing_subclass(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child] = []
    
    def enter_Root_root_main_behaviour_running_creating_child_waiting_close(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child].append(self.Root_root_main_behaviour_running_creating_child_waiting_close)
    
    def exit_Root_root_main_behaviour_running_creating_child_waiting_close(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child] = []
    
    def enter_Root_root_main_behaviour_running_creating_child_reading_type(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child].append(self.Root_root_main_behaviour_running_creating_child_reading_type)
    
    def exit_Root_root_main_behaviour_running_creating_child_reading_type(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child] = []
    
    def enter_Root_root_main_behaviour_running_creating_child_entering_instance_details(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child].append(self.Root_root_main_behaviour_running_creating_child_entering_instance_details)
    
    def exit_Root_root_main_behaviour_running_creating_child_entering_instance_details(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child] = []
    
    def enter_Root_root_main_behaviour_running_creating_child_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child].append(self.Root_root_main_behaviour_running_creating_child_waiting_client)
    
    def exit_Root_root_main_behaviour_running_creating_child_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child] = []
    
    def enter_Root_root_main_behaviour_running_creating_child_reading_new_child(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child].append(self.Root_root_main_behaviour_running_creating_child_reading_new_child)
    
    def exit_Root_root_main_behaviour_running_creating_child_reading_new_child(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child] = []
    
    def enter_Root_root_main_behaviour_running_creating_child_entering_composition_details(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child].append(self.Root_root_main_behaviour_running_creating_child_entering_composition_details)
    
    def exit_Root_root_main_behaviour_running_creating_child_entering_composition_details(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child] = []
    
    def enter_Root_root_main_behaviour_running_creating_child_waiting_client_composition(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child].append(self.Root_root_main_behaviour_running_creating_child_waiting_client_composition)
    
    def exit_Root_root_main_behaviour_running_creating_child_waiting_client_composition(self):
        self.current_state[self.Root_root_main_behaviour_running_creating_child] = []
    
    def enter_Root_root_main_behaviour_label_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_label_behaviour].append(self.Root_root_main_behaviour_label_behaviour_waiting)
    
    def exit_Root_root_main_behaviour_label_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_label_behaviour] = []
    
    def enter_Root_root_main_behaviour_label_behaviour_creating_label(self):
        self.current_state[self.Root_root_main_behaviour_label_behaviour].append(self.Root_root_main_behaviour_label_behaviour_creating_label)
    
    def exit_Root_root_main_behaviour_label_behaviour_creating_label(self):
        self.current_state[self.Root_root_main_behaviour_label_behaviour] = []
    
    def enter_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets].append(self.Root_root_main_behaviour_packing_widgets_packing)
    
    def exit_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
    
    def enter_Root_root_main_behaviour_error_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_error_behaviour].append(self.Root_root_main_behaviour_error_behaviour_waiting)
    
    def exit_Root_root_main_behaviour_error_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_error_behaviour] = []
    
    def enter_Root_root_main_behaviour_window_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour].append(self.Root_root_main_behaviour_window_behaviour_waiting)
    
    def exit_Root_root_main_behaviour_window_behaviour_waiting(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour] = []
    
    def enter_Root_root_main_behaviour_window_behaviour_creating(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour].append(self.Root_root_main_behaviour_window_behaviour_creating)
    
    def exit_Root_root_main_behaviour_window_behaviour_creating(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour] = []
    
    def enter_Root_root_main_behaviour_window_behaviour_starting(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour].append(self.Root_root_main_behaviour_window_behaviour_starting)
    
    def exit_Root_root_main_behaviour_window_behaviour_starting(self):
        self.current_state[self.Root_root_main_behaviour_window_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client].append(self.Root_root_main_behaviour_listening_client_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def enter_Root_root_deleting(self):
        self.timers[1] = 0.05
        self.current_state[self.Root_root].append(self.Root_root_deleting)
    
    def exit_Root_root_deleting(self):
        self.timers.pop(1, None)
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_stopped(self):
        self.current_state[self.Root_root].append(self.Root_root_stopped)
    
    def exit_Root_root_stopped(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_main_behaviour(self):
        self.enter_Root_root_main_behaviour()
        self.enterDefault_Root_root_main_behaviour_running()
        self.enterDefault_Root_root_main_behaviour_label_behaviour()
        self.enterDefault_Root_root_main_behaviour_packing_widgets()
        self.enterDefault_Root_root_main_behaviour_error_behaviour()
        self.enterDefault_Root_root_main_behaviour_window_behaviour()
        self.enterDefault_Root_root_main_behaviour_listening_client()
    
    def enterDefault_Root_root_main_behaviour_running(self):
        self.enter_Root_root_main_behaviour_running()
        self.enter_Root_root_main_behaviour_running_creating_button()
    
    def enterDefault_Root_root_main_behaviour_running_editing_child(self):
        self.enter_Root_root_main_behaviour_running_editing_child()
        self.enter_Root_root_main_behaviour_running_editing_child_entering_instance_details()
    
    def enterDefault_Root_root_main_behaviour_running_creating_child(self):
        self.enter_Root_root_main_behaviour_running_creating_child()
        self.enter_Root_root_main_behaviour_running_creating_child_choosing_subclass()
    
    def enterDefault_Root_root_main_behaviour_label_behaviour(self):
        self.enter_Root_root_main_behaviour_label_behaviour()
        self.enter_Root_root_main_behaviour_label_behaviour_waiting()
    
    def enterDefault_Root_root_main_behaviour_packing_widgets(self):
        self.enter_Root_root_main_behaviour_packing_widgets()
        self.enter_Root_root_main_behaviour_packing_widgets_packing()
    
    def enterDefault_Root_root_main_behaviour_error_behaviour(self):
        self.enter_Root_root_main_behaviour_error_behaviour()
        self.enter_Root_root_main_behaviour_error_behaviour_waiting()
    
    def enterDefault_Root_root_main_behaviour_window_behaviour(self):
        self.enter_Root_root_main_behaviour_window_behaviour()
        self.enter_Root_root_main_behaviour_window_behaviour_waiting()
    
    def enterDefault_Root_root_main_behaviour_listening_client(self):
        self.enter_Root_root_main_behaviour_listening_client()
        self.enter_Root_root_main_behaviour_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_deleting:
                catched = self.transition_Root_root_deleting(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_stopped:
                catched = self.transition_Root_root_stopped(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                self.enterDefault_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
        enableds = []
        if event.name == "close" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "window-close" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'labels']))
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'buttons']))
                self.enter_Root_root_deleting()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'labels']))
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'buttons']))
                self.enter_Root_root_deleting()
            catched = True
        
        if not catched :
            catched = self.transition_Root_root_main_behaviour_running(event) or catched
            catched = self.transition_Root_root_main_behaviour_label_behaviour(event) or catched
            catched = self.transition_Root_root_main_behaviour_packing_widgets(event) or catched
            catched = self.transition_Root_root_main_behaviour_error_behaviour(event) or catched
            catched = self.transition_Root_root_main_behaviour_window_behaviour(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening_client(event) or catched
        return catched
    
    def transition_Root_root_main_behaviour_running(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_running][0] == self.Root_root_main_behaviour_running_creating_button:
                catched = self.transition_Root_root_main_behaviour_running_creating_button(event)
            elif self.current_state[self.Root_root_main_behaviour_running][0] == self.Root_root_main_behaviour_running_creating_labels:
                catched = self.transition_Root_root_main_behaviour_running_creating_labels(event)
            elif self.current_state[self.Root_root_main_behaviour_running][0] == self.Root_root_main_behaviour_running_waiting:
                catched = self.transition_Root_root_main_behaviour_running_waiting(event)
            elif self.current_state[self.Root_root_main_behaviour_running][0] == self.Root_root_main_behaviour_running_waiting_for_second:
                catched = self.transition_Root_root_main_behaviour_running_waiting_for_second(event)
            elif self.current_state[self.Root_root_main_behaviour_running][0] == self.Root_root_main_behaviour_running_waiting_client_read:
                catched = self.transition_Root_root_main_behaviour_running_waiting_client_read(event)
            elif self.current_state[self.Root_root_main_behaviour_running][0] == self.Root_root_main_behaviour_running_editing_child:
                catched = self.transition_Root_root_main_behaviour_running_editing_child(event)
            elif self.current_state[self.Root_root_main_behaviour_running][0] == self.Root_root_main_behaviour_running_creating_child:
                catched = self.transition_Root_root_main_behaviour_running_creating_child(event)
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_button(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_creating_button. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_button()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_running_creating_labels()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_labels(self, event) :
        catched = False
        enableds = []
        if self.curr_label_idx < len(self.labels) :
            enableds.append(1)
        
        if self.curr_label_idx == len(self.labels) :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_creating_labels. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_running_creating_labels()
                self.addEvent(Event("create_label", parameters = [self.labels[self.curr_label_idx]]))
                print self.labels[self.curr_label_idx]
                self.curr_label_idx += 1
                self.enter_Root_root_main_behaviour_running_creating_labels()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_running_creating_labels()
                send_event = Event("editor_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "label_pressed" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] == 'create_child' :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                text = parameters[0]
                self.exit_Root_root_main_behaviour_running_waiting()
                self.curr_text = text
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'labels' , send_event]))
                send_event = Event("highlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.name_to_assoc[StringValue(text)] , send_event]))
                self.enter_Root_root_main_behaviour_running_waiting_for_second()
            elif enabled == 2 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_running_waiting()
                self.addEvent(Event("create_window", parameters = [{"class_name": "SelectionWindow", "constructor_parameters": {"selection_text": "Subclass", "options": self.subclasses}}]))
                self.enterDefault_Root_root_main_behaviour_running_creating_child()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_waiting_for_second(self, event) :
        catched = False
        enableds = []
        if event.name == "label_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            text = parameters[0]
            if self.curr_text == text :
                enableds.append(1)
        
        if event.name == "label_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            text = parameters[0]
            if self.curr_text != text :
                enableds.append(2)
        
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_waiting_for_second. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                text = parameters[0]
                self.exit_Root_root_main_behaviour_running_waiting_for_second()
                self.curr_editing_location = self.location + StringValue('.%s' % text)
                print 'label pressed second time!'
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': self.curr_editing_location}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_waiting_client_read()
            elif enabled == 2 :
                parameters = event.getParameters()
                text = parameters[0]
                self.exit_Root_root_main_behaviour_running_waiting_for_second()
                self.curr_text = text
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'labels' , send_event]))
                send_event = Event("highlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.name_to_assoc[StringValue(text)] , send_event]))
                self.enter_Root_root_main_behaviour_running_waiting_for_second()
            elif enabled == 3 :
                self.exit_Root_root_main_behaviour_running_waiting_for_second()
                print 'going back to waiting'
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_waiting_client_read(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_waiting_client_read. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_waiting_client_read()
                self.addEvent(Event("create_window", parameters = [{"class_name": "InstanceAttributeEditor", "constructor_parameters": {"instance": response[StringValue("item")]}}]))
                self.enterDefault_Root_root_main_behaviour_running_editing_child()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_waiting_client_read()
                print response
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_editing_child(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_running_editing_child][0] == self.Root_root_main_behaviour_running_editing_child_entering_instance_details:
                catched = self.transition_Root_root_main_behaviour_running_editing_child_entering_instance_details(event)
            elif self.current_state[self.Root_root_main_behaviour_running_editing_child][0] == self.Root_root_main_behaviour_running_editing_child_waiting_client:
                catched = self.transition_Root_root_main_behaviour_running_editing_child_waiting_client(event)
            elif self.current_state[self.Root_root_main_behaviour_running_editing_child][0] == self.Root_root_main_behaviour_running_editing_child_waiting_client_read:
                catched = self.transition_Root_root_main_behaviour_running_editing_child_waiting_client_read(event)
        return catched
    
    def transition_Root_root_main_behaviour_running_editing_child_entering_instance_details(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_details_entered" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_editing_child_entering_instance_details. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                data = parameters[0]
                self.exit_Root_root_main_behaviour_running_editing_child_entering_instance_details()
                print 'Entered instance details! %s' % data
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'update', 'request_parameters': data}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                send_event = Event("grab_focus", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_editing_child_waiting_client()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_running_editing_child()
                print 'closed window!'
                send_event = Event("grab_focus", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_waiting()
            elif enabled == 3 :
                self.exit_Root_root_main_behaviour_running_editing_child()
                print 'error'
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_editing_child_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_editing_child_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_editing_child_waiting_client()
                print response
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': response[StringValue('location')]}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_editing_child_waiting_client_read()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_editing_child()
                print response
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_editing_child_waiting_client_read(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_editing_child_waiting_client_read. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_editing_child()
                print response
                item = response[StringValue("item")]
                if self.curr_editing_location != item.location:
                    self.loc_to_label[self.curr_editing_location].set_text(item.name)
                    self.loc_to_label[item.location] = self.loc_to_label[self.curr_editing_location]
                    del self.loc_to_label[self.curr_editing_location]
                    old_name = self.curr_editing_location.substring(start=self.curr_editing_location.rfind(StringValue('.')) + IntegerValue(1))
                    self.name_to_assoc[item.name] = self.name_to_assoc[old_name]
                    del self.name_to_assoc[old_name]
                self.enter_Root_root_main_behaviour_running_waiting()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_editing_child()
                print response
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_child(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_running_creating_child][0] == self.Root_root_main_behaviour_running_creating_child_choosing_subclass:
                catched = self.transition_Root_root_main_behaviour_running_creating_child_choosing_subclass(event)
            elif self.current_state[self.Root_root_main_behaviour_running_creating_child][0] == self.Root_root_main_behaviour_running_creating_child_waiting_close:
                catched = self.transition_Root_root_main_behaviour_running_creating_child_waiting_close(event)
            elif self.current_state[self.Root_root_main_behaviour_running_creating_child][0] == self.Root_root_main_behaviour_running_creating_child_reading_type:
                catched = self.transition_Root_root_main_behaviour_running_creating_child_reading_type(event)
            elif self.current_state[self.Root_root_main_behaviour_running_creating_child][0] == self.Root_root_main_behaviour_running_creating_child_entering_instance_details:
                catched = self.transition_Root_root_main_behaviour_running_creating_child_entering_instance_details(event)
            elif self.current_state[self.Root_root_main_behaviour_running_creating_child][0] == self.Root_root_main_behaviour_running_creating_child_waiting_client:
                catched = self.transition_Root_root_main_behaviour_running_creating_child_waiting_client(event)
            elif self.current_state[self.Root_root_main_behaviour_running_creating_child][0] == self.Root_root_main_behaviour_running_creating_child_reading_new_child:
                catched = self.transition_Root_root_main_behaviour_running_creating_child_reading_new_child(event)
            elif self.current_state[self.Root_root_main_behaviour_running_creating_child][0] == self.Root_root_main_behaviour_running_creating_child_entering_composition_details:
                catched = self.transition_Root_root_main_behaviour_running_creating_child_entering_composition_details(event)
            elif self.current_state[self.Root_root_main_behaviour_running_creating_child][0] == self.Root_root_main_behaviour_running_creating_child_waiting_client_composition:
                catched = self.transition_Root_root_main_behaviour_running_creating_child_waiting_client_composition(event)
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_child_choosing_subclass(self, event) :
        catched = False
        enableds = []
        if event.name == "option_selected" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_creating_child_choosing_subclass. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                selected_option = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child_choosing_subclass()
                self.selected_option = selected_option
                self.enter_Root_root_main_behaviour_running_creating_child_waiting_close()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_running_creating_child()
                print 'closed window!'
                send_event = Event("grab_focus", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_waiting()
            elif enabled == 3 :
                self.exit_Root_root_main_behaviour_running_creating_child()
                print 'error'
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_child_waiting_close(self, event) :
        catched = False
        enableds = []
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_creating_child_waiting_close. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_running_creating_child_waiting_close()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': LocationValue(self.selected_option)}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_creating_child_reading_type()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_child_reading_type(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_creating_child_reading_type. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child_reading_type()
                self.addEvent(Event("create_window", parameters = [{"class_name": "NewInstanceAttributeEditor", "constructor_parameters": {"type": response[StringValue("item")], "type_location": response[StringValue("item")].location, "location": self.location}}]))
                self.enter_Root_root_main_behaviour_running_creating_child_entering_instance_details()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child()
                print response
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_child_entering_instance_details(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_details_entered" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_creating_child_entering_instance_details. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                data = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child_entering_instance_details()
                print 'Entered instance details! %s' % data
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'create', 'request_parameters': data}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                send_event = Event("grab_focus", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_creating_child_waiting_client()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_running_creating_child()
                print 'closed window!'
                send_event = Event("grab_focus", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_waiting()
            elif enabled == 3 :
                self.exit_Root_root_main_behaviour_running_creating_child()
                print 'error'
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_child_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_creating_child_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child_waiting_client()
                print response
                text = ""
                if isinstance(response, mvk.interfaces.changelog.MvKCompositeLog):
                    found = False
                    for l in response.logs:
                        if found:
                            break
                        for a in l[StringValue('attributes')]:
                            print a
                            if a[StringValue('name')] == StringValue('name'):
                                self.text = a[StringValue('value')]
                            if a[StringValue('name')] == StringValue('class') and a[StringValue('value')] == self.class_location:
                                found = True
                else:
                    for a in response.value[StringValue("attributes")]:
                        print a
                        if a[StringValue('name')] == StringValue('name'):
                            self.text = a[StringValue('value')]
                location = self.location + StringValue('.') + self.text
                print 'Reading %s' % location
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': location}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_creating_child_reading_new_child()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child()
                print response
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_child_reading_new_child(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() and isinstance(response[StringValue('item')], client_object.Clabject) :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() and not isinstance(response[StringValue('item')], client_object.Clabject) :
                enableds.append(2)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_creating_child_reading_new_child. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child_reading_new_child()
                print 'created child == Clabject'
                self.addEvent(Event("create_window", parameters = [{"class_name": "NewInstanceAttributeEditor", "constructor_parameters": {"type": self.composition, "type_location": self.composition.location, "location": self.location, "attribute_values": {self.composition.from_multiplicity.port_name: self.location, self.composition.to_multiplicity.port_name: self.location + StringValue(".") + self.text}}}]))
                self.enter_Root_root_main_behaviour_running_creating_child_entering_composition_details()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child()
                print 'created child # Clabject'
                self.addEvent(Event("create_label", parameters = [{'parent': self.inner_frame, 'text': self.text}]))
                self.enter_Root_root_main_behaviour_running_waiting()
            elif enabled == 3 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child()
                print response
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_child_entering_composition_details(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_details_entered" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_creating_child_entering_composition_details. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                data = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child_entering_composition_details()
                print 'Entered instance details! %s' % data
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'create', 'request_parameters': data}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                send_event = Event("grab_focus", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_creating_child_waiting_client_composition()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_running_creating_child()
                print 'closed window!'
                send_event = Event("grab_focus", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_running_waiting()
            elif enabled == 3 :
                self.exit_Root_root_main_behaviour_running_creating_child()
                print 'error'
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_running_creating_child_waiting_client_composition(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_running_creating_child_waiting_client_composition. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child()
                print response
                self.addEvent(Event("create_label", parameters = [{'parent': self.inner_frame, 'text': self.text}]))
                self.enter_Root_root_main_behaviour_running_waiting()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_running_creating_child()
                print response
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_main_behaviour_running_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_label_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_label_behaviour][0] == self.Root_root_main_behaviour_label_behaviour_waiting:
                catched = self.transition_Root_root_main_behaviour_label_behaviour_waiting(event)
            elif self.current_state[self.Root_root_main_behaviour_label_behaviour][0] == self.Root_root_main_behaviour_label_behaviour_creating_label:
                catched = self.transition_Root_root_main_behaviour_label_behaviour_creating_label(event)
        return catched
    
    def transition_Root_root_main_behaviour_label_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "create_label" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_label_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                constructor_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_label_behaviour_waiting()
                self.curr_name = constructor_parameters['text']
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "labels","Label",constructor_parameters]))
                self.enter_Root_root_main_behaviour_label_behaviour_creating_label()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_label_behaviour_creating_label(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_label_behaviour_creating_label. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_label_behaviour_creating_label()
                self.name_to_assoc[self.curr_name] = association_name
                print self.name_to_assoc
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_label_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_packing_widgets][0] == self.Root_root_main_behaviour_packing_widgets_packing:
                catched = self.transition_Root_root_main_behaviour_packing_widgets_packing(event)
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets_packing(self, event) :
        catched = False
        enableds = []
        if event.name == "button_created" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "label_created" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_packing_widgets_packing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                widget = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                widget.pack(side=tk.TOP, fill=tk.X)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            elif enabled == 2 :
                parameters = event.getParameters()
                widget = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                self.loc_to_label[self.location + StringValue('.%s' % widget.cget('text'))] = widget
                widget.pack(side=tk.TOP, fill=tk.X)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_error_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_error_behaviour][0] == self.Root_root_main_behaviour_error_behaviour_waiting:
                catched = self.transition_Root_root_main_behaviour_error_behaviour_waiting(event)
        return catched
    
    def transition_Root_root_main_behaviour_error_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "error" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_error_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                error_code = parameters[0]
                error_message = parameters[1]
                self.exit_Root_root_main_behaviour_error_behaviour_waiting()
                print 'ERROR!!!!!'
                self.addEvent(Event("create_window", parameters = [{"class_name": "PopupMessage", "constructor_parameters": {"title": "ERROR", "message": "%s (%s)" % (error_message, error_code)}}]))
                self.enter_Root_root_main_behaviour_error_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_window_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_window_behaviour][0] == self.Root_root_main_behaviour_window_behaviour_waiting:
                catched = self.transition_Root_root_main_behaviour_window_behaviour_waiting(event)
            elif self.current_state[self.Root_root_main_behaviour_window_behaviour][0] == self.Root_root_main_behaviour_window_behaviour_creating:
                catched = self.transition_Root_root_main_behaviour_window_behaviour_creating(event)
            elif self.current_state[self.Root_root_main_behaviour_window_behaviour][0] == self.Root_root_main_behaviour_window_behaviour_starting:
                catched = self.transition_Root_root_main_behaviour_window_behaviour_starting(event)
        return catched
    
    def transition_Root_root_main_behaviour_window_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "create_window" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_window_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_window_behaviour_waiting()
                event_parameters["constructor_parameters"]["parent"] = self
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "windows",event_parameters["class_name"],event_parameters["constructor_parameters"]]))
                self.enter_Root_root_main_behaviour_window_behaviour_creating()
            elif enabled == 2 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_window_behaviour_waiting()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, association_name]))
                self.enter_Root_root_main_behaviour_window_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_window_behaviour_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_window_behaviour_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_window_behaviour_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                self.enter_Root_root_main_behaviour_window_behaviour_starting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_window_behaviour_starting(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_started" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_window_behaviour_starting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_window_behaviour_starting()
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_window_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening_client][0] == self.Root_root_main_behaviour_listening_client_listening_client:
                catched = self.transition_Root_root_main_behaviour_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_main_behaviour_listening_client_listening_client()
                send_event = Event("client_request", parameters = [self.association_name + '/' + association_name,data])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_client_listening_client()
            catched = True
        
        return catched
    
    def transition_Root_root_deleting(self, event) :
        catched = False
        enableds = []
        if event.name == "_1after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_deleting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_deleting()
                send_event = Event("delete_window", parameters = [self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_stopped()
            catched = True
        
        return catched
    
    def transition_Root_root_stopped(self, event) :
        catched = False
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
    

class SelectionWindow(Window, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_main_behaviour = 2
    Root_root_main_behaviour_creating_buttons = 3
    Root_root_main_behaviour_creating_buttons_running = 4
    Root_root_main_behaviour_creating_buttons_running_populating_frame = 5
    Root_root_main_behaviour_packing_widgets = 6
    Root_root_main_behaviour_listening_client = 7
    Root_root_initializing = 8
    Root_root_main_behaviour_creating_buttons_loop = 9
    Root_root_main_behaviour_creating_buttons_creating = 10
    Root_root_main_behaviour_creating_buttons_running_populating_frame_loop = 11
    Root_root_main_behaviour_creating_buttons_running_populating_frame_creating = 12
    Root_root_main_behaviour_creating_buttons_running_running = 13
    Root_root_main_behaviour_packing_widgets_packing = 14
    Root_root_main_behaviour_listening_client_listening_client = 15
    Root_root_deleting = 16
    Root_root_stopped = 17
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_main_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] = []
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def start(self):
        super(SelectionWindow, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        Window.__init__(self, self.controller)
        self.minsize(width=256, height=256)
        self.title('Select ' + constructor_parameters['selection_text'])
        
        self.buttons = [{"class_name": "Button", "parent": self, "visual": TextVisual('SELECT'), "tooltip_text": 'Select Option', "event_parameters": {"event_name": "select_option"}}]
        self.options = constructor_parameters['options']
        
        self.f = tk.Frame(self, pady=30, bg="white")
        self.f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.selected_option = None
        self.curr_option_idx = 0
        self.name_to_assoc = {}
        self.curr_name = None
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        if self.Root_root_deleting in self.current_state[self.Root_root] :
            self.exit_Root_root_deleting()
        if self.Root_root_stopped in self.current_state[self.Root_root] :
            self.exit_Root_root_stopped()
        self.current_state[self.Root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.exit_Root_root_main_behaviour_creating_buttons()
        self.exit_Root_root_main_behaviour_packing_widgets()
        self.exit_Root_root_main_behaviour_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_buttons(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_creating_buttons)
    
    def exit_Root_root_main_behaviour_creating_buttons(self):
        if self.Root_root_main_behaviour_creating_buttons_loop in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_loop()
        if self.Root_root_main_behaviour_creating_buttons_creating in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_creating()
        if self.Root_root_main_behaviour_creating_buttons_running in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_running()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_running)
    
    def exit_Root_root_main_behaviour_creating_buttons_running(self):
        if self.Root_root_main_behaviour_creating_buttons_running_populating_frame in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame()
        if self.Root_root_main_behaviour_creating_buttons_running_running in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_running()
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_populating_frame(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_populating_frame)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_populating_frame(self):
        if self.Root_root_main_behaviour_creating_buttons_running_populating_frame_loop in self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
        if self.Root_root_main_behaviour_creating_buttons_running_populating_frame_creating in self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating()
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_packing_widgets(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_packing_widgets)
    
    def exit_Root_root_main_behaviour_packing_widgets(self):
        if self.Root_root_main_behaviour_packing_widgets_packing in self.current_state[self.Root_root_main_behaviour_packing_widgets] :
            self.exit_Root_root_main_behaviour_packing_widgets_packing()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_client(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client(self):
        if self.Root_root_main_behaviour_listening_client_listening_client in self.current_state[self.Root_root_main_behaviour_listening_client] :
            self.exit_Root_root_main_behaviour_listening_client_listening_client()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_loop)
    
    def exit_Root_root_main_behaviour_creating_buttons_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_creating)
    
    def exit_Root_root_main_behaviour_creating_buttons_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame].append(self.Root_root_main_behaviour_creating_buttons_running_populating_frame_loop)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame].append(self.Root_root_main_behaviour_creating_buttons_running_populating_frame_creating)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_running)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets].append(self.Root_root_main_behaviour_packing_widgets_packing)
    
    def exit_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
    
    def enter_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client].append(self.Root_root_main_behaviour_listening_client_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def enter_Root_root_deleting(self):
        self.timers[0] = 0.05
        self.current_state[self.Root_root].append(self.Root_root_deleting)
    
    def exit_Root_root_deleting(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_stopped(self):
        self.current_state[self.Root_root].append(self.Root_root_stopped)
    
    def exit_Root_root_stopped(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_main_behaviour(self):
        self.enter_Root_root_main_behaviour()
        self.enterDefault_Root_root_main_behaviour_creating_buttons()
        self.enterDefault_Root_root_main_behaviour_packing_widgets()
        self.enterDefault_Root_root_main_behaviour_listening_client()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons(self):
        self.enter_Root_root_main_behaviour_creating_buttons()
        self.enter_Root_root_main_behaviour_creating_buttons_loop()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons_running(self):
        self.enter_Root_root_main_behaviour_creating_buttons_running()
        self.enterDefault_Root_root_main_behaviour_creating_buttons_running_populating_frame()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons_running_populating_frame(self):
        self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame()
        self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
    
    def enterDefault_Root_root_main_behaviour_packing_widgets(self):
        self.enter_Root_root_main_behaviour_packing_widgets()
        self.enter_Root_root_main_behaviour_packing_widgets_packing()
    
    def enterDefault_Root_root_main_behaviour_listening_client(self):
        self.enter_Root_root_main_behaviour_listening_client()
        self.enter_Root_root_main_behaviour_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_deleting:
                catched = self.transition_Root_root_deleting(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_stopped:
                catched = self.transition_Root_root_stopped(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                self.grab_set()
                self.enterDefault_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
        enableds = []
        if event.name == "close" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "window-close" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'labels']))
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'buttons']))
                self.enter_Root_root_deleting()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'labels']))
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'buttons']))
                self.enter_Root_root_deleting()
            catched = True
        
        if not catched :
            catched = self.transition_Root_root_main_behaviour_creating_buttons(event) or catched
            catched = self.transition_Root_root_main_behaviour_packing_widgets(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening_client(event) or catched
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_loop:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_creating:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_creating(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_running:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_loop(self, event) :
        catched = False
        enableds = []
        if self.buttons :
            enableds.append(1)
        
        if not self.buttons :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_loop()
                ctor_parameters = self.buttons.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "buttons",ctor_parameters["class_name"],ctor_parameters]))
                self.enter_Root_root_main_behaviour_creating_buttons_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_loop()
                self.enterDefault_Root_root_main_behaviour_creating_buttons_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_populating_frame:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_populating_frame(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_running:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_running(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_populating_frame(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame][0] == self.Root_root_main_behaviour_creating_buttons_running_populating_frame_loop:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame][0] == self.Root_root_main_behaviour_creating_buttons_running_populating_frame_creating:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(self, event) :
        catched = False
        enableds = []
        if self.curr_option_idx < len(self.options) :
            enableds.append(1)
        
        if self.curr_option_idx == len(self.options) :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_populating_frame_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
                text = str(self.options[self.curr_option_idx])
                self.curr_name = text
                ctor_parameters = {"parent": self.f, "text": text}
                self.curr_option_idx += 1
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "labels","Label",ctor_parameters]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame()
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_populating_frame_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating()
                self.name_to_assoc[self.curr_name] = association_name
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_running(self, event) :
        catched = False
        enableds = []
        if event.name == "label_pressed" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] == 'select_option' :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                text = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_running()
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'labels' , send_event]))
                send_event = Event("highlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.name_to_assoc[text] , send_event]))
                self.selected_option = text
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            elif enabled == 2 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_running()
                send_event = Event("option_selected", parameters = [self.selected_option])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_packing_widgets][0] == self.Root_root_main_behaviour_packing_widgets_packing:
                catched = self.transition_Root_root_main_behaviour_packing_widgets_packing(event)
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets_packing(self, event) :
        catched = False
        enableds = []
        if event.name == "button_created" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "label_created" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_packing_widgets_packing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                widget = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                widget.pack(side=tk.TOP, fill=tk.Y)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            elif enabled == 2 :
                parameters = event.getParameters()
                widget = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                widget.pack(side=tk.TOP, fill=tk.X)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening_client][0] == self.Root_root_main_behaviour_listening_client_listening_client:
                catched = self.transition_Root_root_main_behaviour_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_main_behaviour_listening_client_listening_client()
                send_event = Event("client_request", parameters = [self.association_name + '/' + association_name,data])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_client_listening_client()
            catched = True
        
        return catched
    
    def transition_Root_root_deleting(self, event) :
        catched = False
        enableds = []
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_deleting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_deleting()
                send_event = Event("delete_window", parameters = [self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_stopped()
            catched = True
        
        return catched
    
    def transition_Root_root_stopped(self, event) :
        catched = False
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
    

class PopupMessage(Window, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_running = 3
    Root_root_deleting = 4
    Root_root_stopped = 5
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(PopupMessage, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        Window.__init__(self, self.controller)
        self.minsize(width=256, height=64)
        self.title(constructor_parameters['title'])
        f = tk.Frame(self)
        f.pack()
        tk.Label(f, text=constructor_parameters['message'], pady=30, bg="yellow").pack()
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_running in self.current_state[self.Root_root] :
            self.exit_Root_root_running()
        if self.Root_root_deleting in self.current_state[self.Root_root] :
            self.exit_Root_root_deleting()
        if self.Root_root_stopped in self.current_state[self.Root_root] :
            self.exit_Root_root_stopped()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_running(self):
        self.current_state[self.Root_root].append(self.Root_root_running)
    
    def exit_Root_root_running(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_deleting(self):
        self.timers[0] = 0.05
        self.current_state[self.Root_root].append(self.Root_root_deleting)
    
    def exit_Root_root_deleting(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_stopped(self):
        self.current_state[self.Root_root].append(self.Root_root_stopped)
    
    def exit_Root_root_stopped(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_running:
                catched = self.transition_Root_root_running(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_deleting:
                catched = self.transition_Root_root_deleting(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_stopped:
                catched = self.transition_Root_root_stopped(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                self.grab_set()
                self.enter_Root_root_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running(self, event) :
        catched = False
        enableds = []
        if event.name == "window-close" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_running()
                self.enter_Root_root_deleting()
            catched = True
        
        return catched
    
    def transition_Root_root_deleting(self, event) :
        catched = False
        enableds = []
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_deleting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_deleting()
                send_event = Event("delete_window", parameters = [self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_stopped()
            catched = True
        
        return catched
    
    def transition_Root_root_stopped(self, event) :
        catched = False
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
    

class TypeModelBrowser(Window, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_main_behaviour = 2
    Root_root_main_behaviour_creating_buttons = 3
    Root_root_main_behaviour_creating_buttons_running = 4
    Root_root_main_behaviour_creating_buttons_running_populating_frame = 5
    Root_root_main_behaviour_packing_widgets = 6
    Root_root_main_behaviour_listening_client = 7
    Root_root_initializing = 8
    Root_root_main_behaviour_creating_buttons_loop = 9
    Root_root_main_behaviour_creating_buttons_creating = 10
    Root_root_main_behaviour_creating_buttons_running_getting_children = 11
    Root_root_main_behaviour_creating_buttons_running_waiting_client = 12
    Root_root_main_behaviour_creating_buttons_running_populating_frame_loop = 13
    Root_root_main_behaviour_creating_buttons_running_populating_frame_creating = 14
    Root_root_main_behaviour_creating_buttons_running_running = 15
    Root_root_main_behaviour_creating_buttons_running_waiting_for_second = 16
    Root_root_main_behaviour_creating_buttons_running_get_type_model = 17
    Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model = 18
    Root_root_main_behaviour_packing_widgets_packing = 19
    Root_root_main_behaviour_listening_client_listening_client = 20
    Root_root_deleting = 21
    Root_root_stopped = 22
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_main_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] = []
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def start(self):
        super(TypeModelBrowser, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        Window.__init__(self, self.controller)
        self.minsize(width=256, height=256)
        self.title('Browse Type Models')
        self.curr_location = LocationValue('.')
        
        self.buttons = [{"class_name": "Button", "parent": self, "visual": ImageVisual('icons/back-icon.png'), "tooltip_text": 'Go Up One Level', "event_parameters": {"event_name": "up_level"}},
                        {"class_name": "Button", "parent": self, "visual": TextVisual('SELECT'), "tooltip_text": 'Select Type Model', "event_parameters": {"event_name": "select_type_model"}}]
        
        self.f = tk.Frame(self, pady=30, bg="white")
        self.curr_location = LocationValue("")
        self.selected_location = LocationValue("")
        self.history = []
        self.append_history = True
        self.curr_children = []
        self.name_to_loc = {}
        self.name_to_assoc = {}
        self.curr_name = ""
        self.curr_b = 0
        self.instance_to_assoc = {}
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        if self.Root_root_deleting in self.current_state[self.Root_root] :
            self.exit_Root_root_deleting()
        if self.Root_root_stopped in self.current_state[self.Root_root] :
            self.exit_Root_root_stopped()
        self.current_state[self.Root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.exit_Root_root_main_behaviour_creating_buttons()
        self.exit_Root_root_main_behaviour_packing_widgets()
        self.exit_Root_root_main_behaviour_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_buttons(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_creating_buttons)
    
    def exit_Root_root_main_behaviour_creating_buttons(self):
        if self.Root_root_main_behaviour_creating_buttons_loop in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_loop()
        if self.Root_root_main_behaviour_creating_buttons_creating in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_creating()
        if self.Root_root_main_behaviour_creating_buttons_running in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_running()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_running)
    
    def exit_Root_root_main_behaviour_creating_buttons_running(self):
        if self.Root_root_main_behaviour_creating_buttons_running_getting_children in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_getting_children()
        if self.Root_root_main_behaviour_creating_buttons_running_waiting_client in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client()
        if self.Root_root_main_behaviour_creating_buttons_running_populating_frame in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame()
        if self.Root_root_main_behaviour_creating_buttons_running_running in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_running()
        if self.Root_root_main_behaviour_creating_buttons_running_waiting_for_second in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
        if self.Root_root_main_behaviour_creating_buttons_running_get_type_model in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_get_type_model()
        if self.Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model()
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_populating_frame(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_populating_frame)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_populating_frame(self):
        if self.Root_root_main_behaviour_creating_buttons_running_populating_frame_loop in self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
        if self.Root_root_main_behaviour_creating_buttons_running_populating_frame_creating in self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating()
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_packing_widgets(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_packing_widgets)
    
    def exit_Root_root_main_behaviour_packing_widgets(self):
        if self.Root_root_main_behaviour_packing_widgets_packing in self.current_state[self.Root_root_main_behaviour_packing_widgets] :
            self.exit_Root_root_main_behaviour_packing_widgets_packing()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_client(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client(self):
        if self.Root_root_main_behaviour_listening_client_listening_client in self.current_state[self.Root_root_main_behaviour_listening_client] :
            self.exit_Root_root_main_behaviour_listening_client_listening_client()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_loop)
    
    def exit_Root_root_main_behaviour_creating_buttons_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_creating)
    
    def exit_Root_root_main_behaviour_creating_buttons_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_getting_children(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_getting_children)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_getting_children(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_waiting_client)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame].append(self.Root_root_main_behaviour_creating_buttons_running_populating_frame_loop)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame].append(self.Root_root_main_behaviour_creating_buttons_running_populating_frame_creating)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_running)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_waiting_for_second(self):
        self.timers[0] = 0.3
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_waiting_for_second)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_waiting_for_second(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_get_type_model(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_get_type_model)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_get_type_model(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets].append(self.Root_root_main_behaviour_packing_widgets_packing)
    
    def exit_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
    
    def enter_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client].append(self.Root_root_main_behaviour_listening_client_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def enter_Root_root_deleting(self):
        self.timers[1] = 0.1
        self.current_state[self.Root_root].append(self.Root_root_deleting)
    
    def exit_Root_root_deleting(self):
        self.timers.pop(1, None)
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_stopped(self):
        self.current_state[self.Root_root].append(self.Root_root_stopped)
    
    def exit_Root_root_stopped(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_main_behaviour(self):
        self.enter_Root_root_main_behaviour()
        self.enterDefault_Root_root_main_behaviour_creating_buttons()
        self.enterDefault_Root_root_main_behaviour_packing_widgets()
        self.enterDefault_Root_root_main_behaviour_listening_client()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons(self):
        self.enter_Root_root_main_behaviour_creating_buttons()
        self.enter_Root_root_main_behaviour_creating_buttons_loop()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons_running(self):
        self.enter_Root_root_main_behaviour_creating_buttons_running()
        self.enter_Root_root_main_behaviour_creating_buttons_running_getting_children()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons_running_populating_frame(self):
        self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame()
        self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
    
    def enterDefault_Root_root_main_behaviour_packing_widgets(self):
        self.enter_Root_root_main_behaviour_packing_widgets()
        self.enter_Root_root_main_behaviour_packing_widgets_packing()
    
    def enterDefault_Root_root_main_behaviour_listening_client(self):
        self.enter_Root_root_main_behaviour_listening_client()
        self.enter_Root_root_main_behaviour_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_deleting:
                catched = self.transition_Root_root_deleting(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_stopped:
                catched = self.transition_Root_root_stopped(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                self.grab_set()
                self.enterDefault_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
        enableds = []
        if event.name == "close" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "window-close" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'labels']))
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'buttons']))
                self.enter_Root_root_deleting()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'labels']))
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'buttons']))
                self.enter_Root_root_deleting()
            catched = True
        
        if not catched :
            catched = self.transition_Root_root_main_behaviour_creating_buttons(event) or catched
            catched = self.transition_Root_root_main_behaviour_packing_widgets(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening_client(event) or catched
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_loop:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_creating:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_creating(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_running:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_loop(self, event) :
        catched = False
        enableds = []
        if self.buttons :
            enableds.append(1)
        
        if not self.buttons :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_loop()
                ctor_parameters = self.buttons.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "buttons",ctor_parameters["class_name"],ctor_parameters]))
                self.enter_Root_root_main_behaviour_creating_buttons_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_loop()
                self.enterDefault_Root_root_main_behaviour_creating_buttons_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_getting_children:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_getting_children(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_waiting_client:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_waiting_client(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_populating_frame:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_populating_frame(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_running:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_running(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_waiting_for_second:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_waiting_for_second(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_get_type_model:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_get_type_model(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_getting_children(self, event) :
        catched = False
        enableds = []
        enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_getting_children. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_getting_children()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': self.selected_location}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_waiting_client()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            result = parameters[0]
            if result.is_success() and hasattr(result[StringValue('item')], 'children') :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            if result.is_success() and not hasattr(result[StringValue('item')], 'children') :
                enableds.append(2)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            result = parameters[0]
            if not result.is_success() :
                enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                result = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client()
                if self.append_history:
                    self.history.append(self.curr_location)
                self.curr_location = self.selected_location
                self.curr_children = result[StringValue("item")].children
                self.curr_item = result[StringValue('item')]
                self.name_to_loc = {}
                self.name_to_assoc = {}
                for c in self.curr_children:
                    self.name_to_loc[c[0]] = c[1]
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'labels']))
                self.enterDefault_Root_root_main_behaviour_creating_buttons_running_populating_frame()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client()
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            elif enabled == 3 :
                parameters = event.getParameters()
                result = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client()
                send_event = Event("error", parameters = [result.get_status_code(),result.get_status_message()])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_populating_frame(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame][0] == self.Root_root_main_behaviour_creating_buttons_running_populating_frame_loop:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame][0] == self.Root_root_main_behaviour_creating_buttons_running_populating_frame_creating:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(self, event) :
        catched = False
        enableds = []
        if self.curr_children :
            enableds.append(1)
        
        if not self.curr_children :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_populating_frame_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
                text = self.curr_children.pop()[0]
                self.curr_name = text
                ctor_parameters = {"parent": self.f, "text": text}
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "labels","Label",ctor_parameters]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame()
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_populating_frame_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating()
                self.name_to_assoc[self.curr_name] = association_name
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_running(self, event) :
        catched = False
        enableds = []
        if event.name == "label_pressed" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] == 'up_level' and self.history :
                enableds.append(2)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] == 'select_type_model' :
                enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                text = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_running()
                self.curr_text = text
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'labels' , send_event]))
                send_event = Event("highlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.name_to_assoc[StringValue(text)] , send_event]))
                self.append_history = True
                self.selected_location = self.name_to_loc[StringValue(text)]
                self.enter_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
            elif enabled == 2 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_running()
                self.append_history = False
                self.selected_location = self.history.pop()
                self.enter_Root_root_main_behaviour_creating_buttons_running_getting_children()
            elif enabled == 3 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_running()
                self.enter_Root_root_main_behaviour_creating_buttons_running_get_type_model()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_waiting_for_second(self, event) :
        catched = False
        enableds = []
        if event.name == "label_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            text = parameters[0]
            if self.curr_text == text :
                enableds.append(1)
        
        if event.name == "label_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            text = parameters[0]
            if self.curr_text != text :
                enableds.append(2)
        
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_waiting_for_second. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                text = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
                self.enter_Root_root_main_behaviour_creating_buttons_running_getting_children()
            elif enabled == 2 :
                parameters = event.getParameters()
                text = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
                self.curr_text = text
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'labels' , send_event]))
                send_event = Event("highlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.name_to_assoc[StringValue(text)] , send_event]))
                self.append_history = True
                self.selected_location = self.name_to_loc[StringValue(text)]
                self.enter_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
            elif enabled == 3 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_get_type_model(self, event) :
        catched = False
        enableds = []
        enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_get_type_model. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_get_type_model()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': self.selected_location}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            result = parameters[0]
            if result.is_success() and isinstance(result[StringValue('item')], client_object.Model) and result[StringValue('item')].potency > IntegerValue(0) :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            if result.is_success() and not (isinstance(result[StringValue('item')], client_object.Model) and result[StringValue('item')].potency > IntegerValue(0)) :
                enableds.append(2)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            result = parameters[0]
            if not result.is_success() :
                enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                result = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model()
                send_event = Event("type_model_selected", parameters = [result[StringValue('item')],self.selected_location])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enterDefault_Root_root_main_behaviour_creating_buttons_running_populating_frame()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model()
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            elif enabled == 3 :
                parameters = event.getParameters()
                result = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client_type_model()
                send_event = Event("error", parameters = [result.get_status_code(),result.get_status_message()])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_packing_widgets][0] == self.Root_root_main_behaviour_packing_widgets_packing:
                catched = self.transition_Root_root_main_behaviour_packing_widgets_packing(event)
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets_packing(self, event) :
        catched = False
        enableds = []
        if event.name == "button_created" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "label_created" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_packing_widgets_packing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                widget = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                if self.curr_b == 0:
                    widget.pack(side=tk.TOP, fill=tk.Y)
                    self.f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                else:
                    widget.pack(side=tk.TOP, fill=tk.Y)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            elif enabled == 2 :
                parameters = event.getParameters()
                widget = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                widget.pack(side=tk.TOP, fill=tk.X)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening_client][0] == self.Root_root_main_behaviour_listening_client_listening_client:
                catched = self.transition_Root_root_main_behaviour_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_main_behaviour_listening_client_listening_client()
                send_event = Event("client_request", parameters = [self.association_name + '/' + association_name,data])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_client_listening_client()
            catched = True
        
        return catched
    
    def transition_Root_root_deleting(self, event) :
        catched = False
        enableds = []
        if event.name == "_1after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_deleting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_deleting()
                send_event = Event("delete_window", parameters = [self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_stopped()
            catched = True
        
        return catched
    
    def transition_Root_root_stopped(self, event) :
        catched = False
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
    

class ModelBrowser(Window, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_main_behaviour = 2
    Root_root_main_behaviour_creating_buttons = 3
    Root_root_main_behaviour_creating_buttons_running = 4
    Root_root_main_behaviour_creating_buttons_running_populating_frame = 5
    Root_root_main_behaviour_packing_widgets = 6
    Root_root_main_behaviour_listening_client = 7
    Root_root_initializing = 8
    Root_root_main_behaviour_creating_buttons_loop = 9
    Root_root_main_behaviour_creating_buttons_creating = 10
    Root_root_main_behaviour_creating_buttons_running_getting_children = 11
    Root_root_main_behaviour_creating_buttons_running_waiting_client = 12
    Root_root_main_behaviour_creating_buttons_running_populating_frame_loop = 13
    Root_root_main_behaviour_creating_buttons_running_populating_frame_creating = 14
    Root_root_main_behaviour_creating_buttons_running_running = 15
    Root_root_main_behaviour_creating_buttons_running_waiting_for_second = 16
    Root_root_main_behaviour_creating_buttons_running_get_model = 17
    Root_root_main_behaviour_creating_buttons_running_waiting_client_model = 18
    Root_root_main_behaviour_packing_widgets_packing = 19
    Root_root_main_behaviour_listening_client_listening_client = 20
    Root_root_deleting = 21
    Root_root_stopped = 22
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_main_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] = []
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def start(self):
        super(ModelBrowser, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        Window.__init__(self, self.controller)
        self.minsize(width=256, height=256)
        self.title('Browse Models')
        self.curr_location = LocationValue('.')
        
        self.buttons = [{"class_name": "Button", "parent": self, "visual": ImageVisual('icons/back-icon.png'), "tooltip_text": 'Go Up One Level', "event_parameters": {"event_name": "up_level"}},
                        {"class_name": "Button", "parent": self, "visual": TextVisual('SELECT'), "tooltip_text": 'Select Model', "event_parameters": {"event_name": "select_model"}}]
        
        self.f = tk.Frame(self, pady=30, bg="white")
        self.curr_location = LocationValue("")
        self.selected_location = LocationValue("")
        self.history = []
        self.append_history = True
        self.curr_children = []
        self.name_to_loc = {}
        self.name_to_assoc = {}
        self.curr_name = ""
        self.curr_b = 0
        self.instance_to_assoc = {}
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        if self.Root_root_deleting in self.current_state[self.Root_root] :
            self.exit_Root_root_deleting()
        if self.Root_root_stopped in self.current_state[self.Root_root] :
            self.exit_Root_root_stopped()
        self.current_state[self.Root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.exit_Root_root_main_behaviour_creating_buttons()
        self.exit_Root_root_main_behaviour_packing_widgets()
        self.exit_Root_root_main_behaviour_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_buttons(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_creating_buttons)
    
    def exit_Root_root_main_behaviour_creating_buttons(self):
        if self.Root_root_main_behaviour_creating_buttons_loop in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_loop()
        if self.Root_root_main_behaviour_creating_buttons_creating in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_creating()
        if self.Root_root_main_behaviour_creating_buttons_running in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_running()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_running)
    
    def exit_Root_root_main_behaviour_creating_buttons_running(self):
        if self.Root_root_main_behaviour_creating_buttons_running_getting_children in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_getting_children()
        if self.Root_root_main_behaviour_creating_buttons_running_waiting_client in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client()
        if self.Root_root_main_behaviour_creating_buttons_running_populating_frame in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame()
        if self.Root_root_main_behaviour_creating_buttons_running_running in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_running()
        if self.Root_root_main_behaviour_creating_buttons_running_waiting_for_second in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
        if self.Root_root_main_behaviour_creating_buttons_running_get_model in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_get_model()
        if self.Root_root_main_behaviour_creating_buttons_running_waiting_client_model in self.current_state[self.Root_root_main_behaviour_creating_buttons_running] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client_model()
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_populating_frame(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_populating_frame)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_populating_frame(self):
        if self.Root_root_main_behaviour_creating_buttons_running_populating_frame_loop in self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
        if self.Root_root_main_behaviour_creating_buttons_running_populating_frame_creating in self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] :
            self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating()
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_packing_widgets(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_packing_widgets)
    
    def exit_Root_root_main_behaviour_packing_widgets(self):
        if self.Root_root_main_behaviour_packing_widgets_packing in self.current_state[self.Root_root_main_behaviour_packing_widgets] :
            self.exit_Root_root_main_behaviour_packing_widgets_packing()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_client(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client(self):
        if self.Root_root_main_behaviour_listening_client_listening_client in self.current_state[self.Root_root_main_behaviour_listening_client] :
            self.exit_Root_root_main_behaviour_listening_client_listening_client()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_loop)
    
    def exit_Root_root_main_behaviour_creating_buttons_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_creating)
    
    def exit_Root_root_main_behaviour_creating_buttons_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_getting_children(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_getting_children)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_getting_children(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_waiting_client)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame].append(self.Root_root_main_behaviour_creating_buttons_running_populating_frame_loop)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame].append(self.Root_root_main_behaviour_creating_buttons_running_populating_frame_creating)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_running)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_waiting_for_second(self):
        self.timers[0] = 0.3
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_waiting_for_second)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_waiting_for_second(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_get_model(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_get_model)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_get_model(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running_waiting_client_model(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running].append(self.Root_root_main_behaviour_creating_buttons_running_waiting_client_model)
    
    def exit_Root_root_main_behaviour_creating_buttons_running_waiting_client_model(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons_running] = []
    
    def enter_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets].append(self.Root_root_main_behaviour_packing_widgets_packing)
    
    def exit_Root_root_main_behaviour_packing_widgets_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_widgets] = []
    
    def enter_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client].append(self.Root_root_main_behaviour_listening_client_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def enter_Root_root_deleting(self):
        self.timers[1] = 0.05
        self.current_state[self.Root_root].append(self.Root_root_deleting)
    
    def exit_Root_root_deleting(self):
        self.timers.pop(1, None)
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_stopped(self):
        self.current_state[self.Root_root].append(self.Root_root_stopped)
    
    def exit_Root_root_stopped(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_main_behaviour(self):
        self.enter_Root_root_main_behaviour()
        self.enterDefault_Root_root_main_behaviour_creating_buttons()
        self.enterDefault_Root_root_main_behaviour_packing_widgets()
        self.enterDefault_Root_root_main_behaviour_listening_client()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons(self):
        self.enter_Root_root_main_behaviour_creating_buttons()
        self.enter_Root_root_main_behaviour_creating_buttons_loop()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons_running(self):
        self.enter_Root_root_main_behaviour_creating_buttons_running()
        self.enter_Root_root_main_behaviour_creating_buttons_running_getting_children()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons_running_populating_frame(self):
        self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame()
        self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
    
    def enterDefault_Root_root_main_behaviour_packing_widgets(self):
        self.enter_Root_root_main_behaviour_packing_widgets()
        self.enter_Root_root_main_behaviour_packing_widgets_packing()
    
    def enterDefault_Root_root_main_behaviour_listening_client(self):
        self.enter_Root_root_main_behaviour_listening_client()
        self.enter_Root_root_main_behaviour_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_deleting:
                catched = self.transition_Root_root_deleting(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_stopped:
                catched = self.transition_Root_root_stopped(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                self.grab_set()
                self.enterDefault_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
        enableds = []
        if event.name == "close" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "window-close" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'labels']))
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'buttons']))
                self.enter_Root_root_deleting()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'labels']))
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'buttons']))
                self.enter_Root_root_deleting()
            catched = True
        
        if not catched :
            catched = self.transition_Root_root_main_behaviour_creating_buttons(event) or catched
            catched = self.transition_Root_root_main_behaviour_packing_widgets(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening_client(event) or catched
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_loop:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_creating:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_creating(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_running:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_loop(self, event) :
        catched = False
        enableds = []
        if self.buttons :
            enableds.append(1)
        
        if not self.buttons :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_loop()
                ctor_parameters = self.buttons.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "buttons",ctor_parameters["class_name"],ctor_parameters]))
                self.enter_Root_root_main_behaviour_creating_buttons_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_loop()
                self.enterDefault_Root_root_main_behaviour_creating_buttons_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_getting_children:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_getting_children(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_waiting_client:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_waiting_client(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_populating_frame:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_populating_frame(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_running:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_running(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_waiting_for_second:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_waiting_for_second(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_get_model:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_get_model(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running][0] == self.Root_root_main_behaviour_creating_buttons_running_waiting_client_model:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_waiting_client_model(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_getting_children(self, event) :
        catched = False
        enableds = []
        enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_getting_children. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_getting_children()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': self.selected_location}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_waiting_client()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            result = parameters[0]
            if result.is_success() and hasattr(result[StringValue('item')], 'children') :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            if result.is_success() and not hasattr(result[StringValue('item')], 'children') :
                enableds.append(2)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            result = parameters[0]
            if not result.is_success() :
                enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                result = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client()
                if self.append_history:
                    self.history.append(self.curr_location)
                self.curr_location = self.selected_location
                self.curr_children = result[StringValue("item")].children
                self.curr_item = result[StringValue('item')]
                self.name_to_loc = {}
                self.name_to_assoc = {}
                for c in self.curr_children:
                    self.name_to_loc[c[0]] = c[1]
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'labels']))
                self.enterDefault_Root_root_main_behaviour_creating_buttons_running_populating_frame()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client()
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            elif enabled == 3 :
                parameters = event.getParameters()
                result = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client()
                send_event = Event("error", parameters = [result.get_status_code(),result.get_status_message()])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_populating_frame(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame][0] == self.Root_root_main_behaviour_creating_buttons_running_populating_frame_loop:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons_running_populating_frame][0] == self.Root_root_main_behaviour_creating_buttons_running_populating_frame_creating:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop(self, event) :
        catched = False
        enableds = []
        if self.curr_children :
            enableds.append(1)
        
        if not self.curr_children :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_populating_frame_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
                text = self.curr_children.pop()[0]
                self.curr_name = text
                ctor_parameters = {"parent": self.f, "text": text}
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "labels","Label",ctor_parameters]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame()
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_populating_frame_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_populating_frame_creating()
                self.name_to_assoc[self.curr_name] = association_name
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_populating_frame_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_running(self, event) :
        catched = False
        enableds = []
        if event.name == "label_pressed" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] == 'up_level' and self.history :
                enableds.append(2)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters['event_name'] == 'select_model' :
                enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                text = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_running()
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'labels' , send_event]))
                send_event = Event("highlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.name_to_assoc[StringValue(text)] , send_event]))
                self.append_history = True
                self.selected_location = self.name_to_loc[StringValue(text)]
                self.curr_text = text
                self.enter_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
            elif enabled == 2 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_running()
                self.append_history = False
                self.selected_location = self.history.pop()
                self.enter_Root_root_main_behaviour_creating_buttons_running_getting_children()
            elif enabled == 3 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_running()
                self.enter_Root_root_main_behaviour_creating_buttons_running_get_model()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_waiting_for_second(self, event) :
        catched = False
        enableds = []
        if event.name == "label_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            text = parameters[0]
            if self.curr_text == text :
                enableds.append(1)
        
        if event.name == "label_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            text = parameters[0]
            if self.curr_text != text :
                enableds.append(2)
        
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_waiting_for_second. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                text = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
                self.enter_Root_root_main_behaviour_creating_buttons_running_getting_children()
            elif enabled == 2 :
                parameters = event.getParameters()
                text = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'labels' , send_event]))
                send_event = Event("highlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.name_to_assoc[StringValue(text)] , send_event]))
                self.append_history = True
                self.selected_location = self.name_to_loc[StringValue(text)]
                self.curr_text = text
                self.enter_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
            elif enabled == 3 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_for_second()
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_get_model(self, event) :
        catched = False
        enableds = []
        enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_get_model. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_get_model()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': self.selected_location}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_waiting_client_model()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running_waiting_client_model(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            result = parameters[0]
            if result.is_success() and isinstance(result[StringValue('item')], client_object.Model) :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            if result.is_success() and not isinstance(result[StringValue('item')], client_object.Model) :
                enableds.append(2)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            result = parameters[0]
            if not result.is_success() :
                enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_running_waiting_client_model. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                result = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client_model()
                send_event = Event("model_selected", parameters = [result[StringValue('item')],self.selected_location])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.addEvent(Event("close", parameters = []))
                self.enterDefault_Root_root_main_behaviour_creating_buttons_running_populating_frame()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client_model()
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            elif enabled == 3 :
                parameters = event.getParameters()
                result = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_running_waiting_client_model()
                send_event = Event("error", parameters = [result.get_status_code(),result.get_status_message()])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_running_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_packing_widgets][0] == self.Root_root_main_behaviour_packing_widgets_packing:
                catched = self.transition_Root_root_main_behaviour_packing_widgets_packing(event)
        return catched
    
    def transition_Root_root_main_behaviour_packing_widgets_packing(self, event) :
        catched = False
        enableds = []
        if event.name == "button_created" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "label_created" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_packing_widgets_packing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                widget = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                if self.curr_b == 0:
                    widget.pack(side=tk.TOP, fill=tk.Y)
                    self.f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                else:
                    widget.pack(side=tk.TOP, fill=tk.Y)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            elif enabled == 2 :
                parameters = event.getParameters()
                widget = parameters[0]
                self.exit_Root_root_main_behaviour_packing_widgets_packing()
                widget.pack(side=tk.TOP, fill=tk.X)
                self.enter_Root_root_main_behaviour_packing_widgets_packing()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening_client][0] == self.Root_root_main_behaviour_listening_client_listening_client:
                catched = self.transition_Root_root_main_behaviour_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_main_behaviour_listening_client_listening_client()
                send_event = Event("client_request", parameters = [self.association_name + '/' + association_name,data])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_client_listening_client()
            catched = True
        
        return catched
    
    def transition_Root_root_deleting(self, event) :
        catched = False
        enableds = []
        if event.name == "_1after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_deleting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_deleting()
                send_event = Event("delete_window", parameters = [self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_stopped()
            catched = True
        
        return catched
    
    def transition_Root_root_stopped(self, event) :
        catched = False
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
    

class ModelEditor(Window, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_running = 2
    Root_root_running_main_behaviour = 3
    Root_root_running_main_behaviour_saving_modelverse = 4
    Root_root_running_main_behaviour_restoring_modelverse = 5
    Root_root_running_main_behaviour_loading_model = 6
    Root_root_running_main_behaviour_loading_type_model = 7
    Root_root_running_main_behaviour_editing_instance = 8
    Root_root_running_main_behaviour_creating_instance = 9
    Root_root_running_main_behaviour_creating_model = 10
    Root_root_running_error_behaviour = 11
    Root_root_running_log_behaviour = 12
    Root_root_running_log_message_pack_behaviour = 13
    Root_root_running_log_click_behaviour = 14
    Root_root_running_toolbar_behaviour = 15
    Root_root_running_window_behaviour = 16
    Root_root_running_mvk_listener = 17
    Root_root_running_instance_behaviour = 18
    Root_root_running_canvas_behaviour = 19
    Root_root_running_listening_client = 20
    Root_root_initializing = 21
    Root_root_running_main_behaviour_running = 22
    Root_root_running_main_behaviour_validating_model = 23
    Root_root_running_main_behaviour_saving_modelverse_waiting_input = 24
    Root_root_running_main_behaviour_saving_modelverse_waiting_client = 25
    Root_root_running_main_behaviour_restoring_modelverse_waiting = 26
    Root_root_running_main_behaviour_restoring_modelverse_getting_file_name = 27
    Root_root_running_main_behaviour_restoring_modelverse_waiting_client = 28
    Root_root_running_main_behaviour_loading_model_waiting = 29
    Root_root_running_main_behaviour_loading_model_creating_main_toolbar = 30
    Root_root_running_main_behaviour_loading_model_reading_type_model = 31
    Root_root_running_main_behaviour_loading_model_loop = 32
    Root_root_running_main_behaviour_loading_model_reading_element = 33
    Root_root_running_main_behaviour_loading_model_drawing_clabjects = 34
    Root_root_running_main_behaviour_loading_model_drawing_associations = 35
    Root_root_running_main_behaviour_loading_type_model_waiting = 36
    Root_root_running_main_behaviour_loading_type_model_waiting_close = 37
    Root_root_running_main_behaviour_editing_instance_waiting_client = 38
    Root_root_running_main_behaviour_editing_instance_entering_instance_details = 39
    Root_root_running_main_behaviour_editing_instance_waiting_client_update = 40
    Root_root_running_main_behaviour_editing_instance_waiting_client_read = 41
    Root_root_running_main_behaviour_creating_instance_entering_instance_details = 42
    Root_root_running_main_behaviour_creating_instance_waiting_client = 43
    Root_root_running_main_behaviour_creating_instance_creating_on_canvas = 44
    Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read = 45
    Root_root_running_main_behaviour_creating_model_waiting = 46
    Root_root_running_main_behaviour_creating_model_waiting_close = 47
    Root_root_running_main_behaviour_creating_model_entering_model_details = 48
    Root_root_running_main_behaviour_creating_model_waiting_client = 49
    Root_root_running_main_behaviour_creating_model_deleting_toolbars = 50
    Root_root_running_main_behaviour_creating_model_creating_main_toolbar = 51
    Root_root_running_main_behaviour_creating_model_creating_toolbar = 52
    Root_root_running_error_behaviour_waiting = 53
    Root_root_running_log_behaviour_waiting = 54
    Root_root_running_log_behaviour_creating = 55
    Root_root_running_log_message_pack_behaviour_waiting = 56
    Root_root_running_log_click_behaviour_waiting = 57
    Root_root_running_log_click_behaviour_waiting_for_second = 58
    Root_root_running_toolbar_behaviour_waiting = 59
    Root_root_running_toolbar_behaviour_creating = 60
    Root_root_running_window_behaviour_waiting = 61
    Root_root_running_window_behaviour_creating = 62
    Root_root_running_window_behaviour_starting = 63
    Root_root_running_mvk_listener_waiting = 64
    Root_root_running_instance_behaviour_waiting = 65
    Root_root_running_instance_behaviour_moving_from_associations = 66
    Root_root_running_instance_behaviour_moving_to_associations = 67
    Root_root_running_instance_behaviour_deleting_instance = 68
    Root_root_running_canvas_behaviour_waiting = 69
    Root_root_running_canvas_behaviour_creating = 70
    Root_root_running_listening_client_listening_client = 71
    Root_root_deleting = 72
    Root_root_stopped = 73
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_running] = []
        self.current_state[self.Root_root_running_main_behaviour] = []
        self.current_state[self.Root_root_running_main_behaviour_saving_modelverse] = []
        self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse] = []
        self.current_state[self.Root_root_running_main_behaviour_loading_model] = []
        self.current_state[self.Root_root_running_main_behaviour_loading_type_model] = []
        self.current_state[self.Root_root_running_main_behaviour_editing_instance] = []
        self.current_state[self.Root_root_running_main_behaviour_creating_instance] = []
        self.current_state[self.Root_root_running_main_behaviour_creating_model] = []
        self.current_state[self.Root_root_running_error_behaviour] = []
        self.current_state[self.Root_root_running_log_behaviour] = []
        self.current_state[self.Root_root_running_log_message_pack_behaviour] = []
        self.current_state[self.Root_root_running_log_click_behaviour] = []
        self.current_state[self.Root_root_running_toolbar_behaviour] = []
        self.current_state[self.Root_root_running_window_behaviour] = []
        self.current_state[self.Root_root_running_mvk_listener] = []
        self.current_state[self.Root_root_running_instance_behaviour] = []
        self.current_state[self.Root_root_running_canvas_behaviour] = []
        self.current_state[self.Root_root_running_listening_client] = []
    
    def start(self):
        super(ModelEditor, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        Window.__init__(self, controller)
        self.title('ModelEditor')
        
        self.minsize(self.winfo_screenwidth() / 2, self.winfo_screenheight() / 2)
        
        self.INTER_SPACING = 5
        
        self.toolbar_frame = HorizontalScrolledFrame(parent=self)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X, expand=0)
        
        self.log_frame = VerticalScrolledFrame(parent=self)
        self.log_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        tk.Label(self.log_frame.interior, text="LOG", bg="white", pady=10, width=30, relief=tk.GROOVE, wraplength=200).pack(side=tk.TOP, fill=tk.X, expand=1)
        
        CANVAS_SIZE_TUPLE = (0, 0, self.winfo_screenwidth() * 2, self.winfo_screenheight() * 2)
        self.c = tk.Canvas(self, relief=tk.RIDGE, scrollregion=CANVAS_SIZE_TUPLE)
        
        vbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vbar.config(command=self.c.yview)
        vbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 16))
        
        hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        hbar.config(command=self.c.xview)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.c.config(background='white', yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        self.c.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        
        MvKWidget.__init__(self, self.controller, self.c)
        
        self.curr_formalism = None
        self.curr_formalism_location = None
        self.type_to_create = None
        self.type_to_create_location = None
        self.model_loc = None
        self.selected_location = None
        self.loc_to_instance = {}
        self.instance_to_from_assocs = {}
        self.instance_to_to_assocs = {}
        self.curr_editing_location = None
        self.log_id_to_assoc = {}
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_running in self.current_state[self.Root_root] :
            self.exit_Root_root_running()
        if self.Root_root_deleting in self.current_state[self.Root_root] :
            self.exit_Root_root_deleting()
        if self.Root_root_stopped in self.current_state[self.Root_root] :
            self.exit_Root_root_stopped()
        self.current_state[self.Root] = []
    
    def enter_Root_root_running(self):
        self.current_state[self.Root_root].append(self.Root_root_running)
    
    def exit_Root_root_running(self):
        self.exit_Root_root_running_main_behaviour()
        self.exit_Root_root_running_error_behaviour()
        self.exit_Root_root_running_log_behaviour()
        self.exit_Root_root_running_log_message_pack_behaviour()
        self.exit_Root_root_running_log_click_behaviour()
        self.exit_Root_root_running_toolbar_behaviour()
        self.exit_Root_root_running_window_behaviour()
        self.exit_Root_root_running_mvk_listener()
        self.exit_Root_root_running_instance_behaviour()
        self.exit_Root_root_running_canvas_behaviour()
        self.exit_Root_root_running_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_running_main_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_main_behaviour)
    
    def exit_Root_root_running_main_behaviour(self):
        if self.Root_root_running_main_behaviour_running in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_running()
        if self.Root_root_running_main_behaviour_validating_model in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_validating_model()
        if self.Root_root_running_main_behaviour_saving_modelverse in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_saving_modelverse()
        if self.Root_root_running_main_behaviour_restoring_modelverse in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_restoring_modelverse()
        if self.Root_root_running_main_behaviour_loading_model in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_loading_model()
        if self.Root_root_running_main_behaviour_loading_type_model in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_loading_type_model()
        if self.Root_root_running_main_behaviour_editing_instance in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_editing_instance()
        if self.Root_root_running_main_behaviour_creating_instance in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_creating_instance()
        if self.Root_root_running_main_behaviour_creating_model in self.current_state[self.Root_root_running_main_behaviour] :
            self.exit_Root_root_running_main_behaviour_creating_model()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_main_behaviour_saving_modelverse(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_saving_modelverse)
    
    def exit_Root_root_running_main_behaviour_saving_modelverse(self):
        if self.Root_root_running_main_behaviour_saving_modelverse_waiting_input in self.current_state[self.Root_root_running_main_behaviour_saving_modelverse] :
            self.exit_Root_root_running_main_behaviour_saving_modelverse_waiting_input()
        if self.Root_root_running_main_behaviour_saving_modelverse_waiting_client in self.current_state[self.Root_root_running_main_behaviour_saving_modelverse] :
            self.exit_Root_root_running_main_behaviour_saving_modelverse_waiting_client()
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_restoring_modelverse(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_restoring_modelverse)
    
    def exit_Root_root_running_main_behaviour_restoring_modelverse(self):
        if self.Root_root_running_main_behaviour_restoring_modelverse_waiting in self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse] :
            self.exit_Root_root_running_main_behaviour_restoring_modelverse_waiting()
        if self.Root_root_running_main_behaviour_restoring_modelverse_getting_file_name in self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse] :
            self.exit_Root_root_running_main_behaviour_restoring_modelverse_getting_file_name()
        if self.Root_root_running_main_behaviour_restoring_modelverse_waiting_client in self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse] :
            self.exit_Root_root_running_main_behaviour_restoring_modelverse_waiting_client()
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_loading_model(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_loading_model)
    
    def exit_Root_root_running_main_behaviour_loading_model(self):
        if self.Root_root_running_main_behaviour_loading_model_waiting in self.current_state[self.Root_root_running_main_behaviour_loading_model] :
            self.exit_Root_root_running_main_behaviour_loading_model_waiting()
        if self.Root_root_running_main_behaviour_loading_model_creating_main_toolbar in self.current_state[self.Root_root_running_main_behaviour_loading_model] :
            self.exit_Root_root_running_main_behaviour_loading_model_creating_main_toolbar()
        if self.Root_root_running_main_behaviour_loading_model_reading_type_model in self.current_state[self.Root_root_running_main_behaviour_loading_model] :
            self.exit_Root_root_running_main_behaviour_loading_model_reading_type_model()
        if self.Root_root_running_main_behaviour_loading_model_loop in self.current_state[self.Root_root_running_main_behaviour_loading_model] :
            self.exit_Root_root_running_main_behaviour_loading_model_loop()
        if self.Root_root_running_main_behaviour_loading_model_reading_element in self.current_state[self.Root_root_running_main_behaviour_loading_model] :
            self.exit_Root_root_running_main_behaviour_loading_model_reading_element()
        if self.Root_root_running_main_behaviour_loading_model_drawing_clabjects in self.current_state[self.Root_root_running_main_behaviour_loading_model] :
            self.exit_Root_root_running_main_behaviour_loading_model_drawing_clabjects()
        if self.Root_root_running_main_behaviour_loading_model_drawing_associations in self.current_state[self.Root_root_running_main_behaviour_loading_model] :
            self.exit_Root_root_running_main_behaviour_loading_model_drawing_associations()
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_loading_type_model(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_loading_type_model)
    
    def exit_Root_root_running_main_behaviour_loading_type_model(self):
        if self.Root_root_running_main_behaviour_loading_type_model_waiting in self.current_state[self.Root_root_running_main_behaviour_loading_type_model] :
            self.exit_Root_root_running_main_behaviour_loading_type_model_waiting()
        if self.Root_root_running_main_behaviour_loading_type_model_waiting_close in self.current_state[self.Root_root_running_main_behaviour_loading_type_model] :
            self.exit_Root_root_running_main_behaviour_loading_type_model_waiting_close()
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_editing_instance(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_editing_instance)
    
    def exit_Root_root_running_main_behaviour_editing_instance(self):
        if self.Root_root_running_main_behaviour_editing_instance_waiting_client in self.current_state[self.Root_root_running_main_behaviour_editing_instance] :
            self.exit_Root_root_running_main_behaviour_editing_instance_waiting_client()
        if self.Root_root_running_main_behaviour_editing_instance_entering_instance_details in self.current_state[self.Root_root_running_main_behaviour_editing_instance] :
            self.exit_Root_root_running_main_behaviour_editing_instance_entering_instance_details()
        if self.Root_root_running_main_behaviour_editing_instance_waiting_client_update in self.current_state[self.Root_root_running_main_behaviour_editing_instance] :
            self.exit_Root_root_running_main_behaviour_editing_instance_waiting_client_update()
        if self.Root_root_running_main_behaviour_editing_instance_waiting_client_read in self.current_state[self.Root_root_running_main_behaviour_editing_instance] :
            self.exit_Root_root_running_main_behaviour_editing_instance_waiting_client_read()
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_creating_instance(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_creating_instance)
    
    def exit_Root_root_running_main_behaviour_creating_instance(self):
        if self.Root_root_running_main_behaviour_creating_instance_entering_instance_details in self.current_state[self.Root_root_running_main_behaviour_creating_instance] :
            self.exit_Root_root_running_main_behaviour_creating_instance_entering_instance_details()
        if self.Root_root_running_main_behaviour_creating_instance_waiting_client in self.current_state[self.Root_root_running_main_behaviour_creating_instance] :
            self.exit_Root_root_running_main_behaviour_creating_instance_waiting_client()
        if self.Root_root_running_main_behaviour_creating_instance_creating_on_canvas in self.current_state[self.Root_root_running_main_behaviour_creating_instance] :
            self.exit_Root_root_running_main_behaviour_creating_instance_creating_on_canvas()
        if self.Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read in self.current_state[self.Root_root_running_main_behaviour_creating_instance] :
            self.exit_Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read()
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_creating_model(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_creating_model)
    
    def exit_Root_root_running_main_behaviour_creating_model(self):
        if self.Root_root_running_main_behaviour_creating_model_waiting in self.current_state[self.Root_root_running_main_behaviour_creating_model] :
            self.exit_Root_root_running_main_behaviour_creating_model_waiting()
        if self.Root_root_running_main_behaviour_creating_model_waiting_close in self.current_state[self.Root_root_running_main_behaviour_creating_model] :
            self.exit_Root_root_running_main_behaviour_creating_model_waiting_close()
        if self.Root_root_running_main_behaviour_creating_model_entering_model_details in self.current_state[self.Root_root_running_main_behaviour_creating_model] :
            self.exit_Root_root_running_main_behaviour_creating_model_entering_model_details()
        if self.Root_root_running_main_behaviour_creating_model_waiting_client in self.current_state[self.Root_root_running_main_behaviour_creating_model] :
            self.exit_Root_root_running_main_behaviour_creating_model_waiting_client()
        if self.Root_root_running_main_behaviour_creating_model_deleting_toolbars in self.current_state[self.Root_root_running_main_behaviour_creating_model] :
            self.exit_Root_root_running_main_behaviour_creating_model_deleting_toolbars()
        if self.Root_root_running_main_behaviour_creating_model_creating_main_toolbar in self.current_state[self.Root_root_running_main_behaviour_creating_model] :
            self.exit_Root_root_running_main_behaviour_creating_model_creating_main_toolbar()
        if self.Root_root_running_main_behaviour_creating_model_creating_toolbar in self.current_state[self.Root_root_running_main_behaviour_creating_model] :
            self.exit_Root_root_running_main_behaviour_creating_model_creating_toolbar()
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_error_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_error_behaviour)
    
    def exit_Root_root_running_error_behaviour(self):
        if self.Root_root_running_error_behaviour_waiting in self.current_state[self.Root_root_running_error_behaviour] :
            self.exit_Root_root_running_error_behaviour_waiting()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_log_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_log_behaviour)
    
    def exit_Root_root_running_log_behaviour(self):
        if self.Root_root_running_log_behaviour_waiting in self.current_state[self.Root_root_running_log_behaviour] :
            self.exit_Root_root_running_log_behaviour_waiting()
        if self.Root_root_running_log_behaviour_creating in self.current_state[self.Root_root_running_log_behaviour] :
            self.exit_Root_root_running_log_behaviour_creating()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_log_message_pack_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_log_message_pack_behaviour)
    
    def exit_Root_root_running_log_message_pack_behaviour(self):
        if self.Root_root_running_log_message_pack_behaviour_waiting in self.current_state[self.Root_root_running_log_message_pack_behaviour] :
            self.exit_Root_root_running_log_message_pack_behaviour_waiting()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_log_click_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_log_click_behaviour)
    
    def exit_Root_root_running_log_click_behaviour(self):
        if self.Root_root_running_log_click_behaviour_waiting in self.current_state[self.Root_root_running_log_click_behaviour] :
            self.exit_Root_root_running_log_click_behaviour_waiting()
        if self.Root_root_running_log_click_behaviour_waiting_for_second in self.current_state[self.Root_root_running_log_click_behaviour] :
            self.exit_Root_root_running_log_click_behaviour_waiting_for_second()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_toolbar_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_toolbar_behaviour)
    
    def exit_Root_root_running_toolbar_behaviour(self):
        if self.Root_root_running_toolbar_behaviour_waiting in self.current_state[self.Root_root_running_toolbar_behaviour] :
            self.exit_Root_root_running_toolbar_behaviour_waiting()
        if self.Root_root_running_toolbar_behaviour_creating in self.current_state[self.Root_root_running_toolbar_behaviour] :
            self.exit_Root_root_running_toolbar_behaviour_creating()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_window_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_window_behaviour)
    
    def exit_Root_root_running_window_behaviour(self):
        if self.Root_root_running_window_behaviour_waiting in self.current_state[self.Root_root_running_window_behaviour] :
            self.exit_Root_root_running_window_behaviour_waiting()
        if self.Root_root_running_window_behaviour_creating in self.current_state[self.Root_root_running_window_behaviour] :
            self.exit_Root_root_running_window_behaviour_creating()
        if self.Root_root_running_window_behaviour_starting in self.current_state[self.Root_root_running_window_behaviour] :
            self.exit_Root_root_running_window_behaviour_starting()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_mvk_listener(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_mvk_listener)
    
    def exit_Root_root_running_mvk_listener(self):
        if self.Root_root_running_mvk_listener_waiting in self.current_state[self.Root_root_running_mvk_listener] :
            self.exit_Root_root_running_mvk_listener_waiting()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_instance_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_instance_behaviour)
    
    def exit_Root_root_running_instance_behaviour(self):
        if self.Root_root_running_instance_behaviour_waiting in self.current_state[self.Root_root_running_instance_behaviour] :
            self.exit_Root_root_running_instance_behaviour_waiting()
        if self.Root_root_running_instance_behaviour_moving_from_associations in self.current_state[self.Root_root_running_instance_behaviour] :
            self.exit_Root_root_running_instance_behaviour_moving_from_associations()
        if self.Root_root_running_instance_behaviour_moving_to_associations in self.current_state[self.Root_root_running_instance_behaviour] :
            self.exit_Root_root_running_instance_behaviour_moving_to_associations()
        if self.Root_root_running_instance_behaviour_deleting_instance in self.current_state[self.Root_root_running_instance_behaviour] :
            self.exit_Root_root_running_instance_behaviour_deleting_instance()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_canvas_behaviour(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_canvas_behaviour)
    
    def exit_Root_root_running_canvas_behaviour(self):
        if self.Root_root_running_canvas_behaviour_waiting in self.current_state[self.Root_root_running_canvas_behaviour] :
            self.exit_Root_root_running_canvas_behaviour_waiting()
        if self.Root_root_running_canvas_behaviour_creating in self.current_state[self.Root_root_running_canvas_behaviour] :
            self.exit_Root_root_running_canvas_behaviour_creating()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_running_listening_client(self):
        self.current_state[self.Root_root_running].append(self.Root_root_running_listening_client)
    
    def exit_Root_root_running_listening_client(self):
        if self.Root_root_running_listening_client_listening_client in self.current_state[self.Root_root_running_listening_client] :
            self.exit_Root_root_running_listening_client_listening_client()
        self.current_state[self.Root_root_running] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_running_main_behaviour_running(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_running)
    
    def exit_Root_root_running_main_behaviour_running(self):
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_validating_model(self):
        self.current_state[self.Root_root_running_main_behaviour].append(self.Root_root_running_main_behaviour_validating_model)
    
    def exit_Root_root_running_main_behaviour_validating_model(self):
        self.current_state[self.Root_root_running_main_behaviour] = []
    
    def enter_Root_root_running_main_behaviour_saving_modelverse_waiting_input(self):
        self.current_state[self.Root_root_running_main_behaviour_saving_modelverse].append(self.Root_root_running_main_behaviour_saving_modelverse_waiting_input)
    
    def exit_Root_root_running_main_behaviour_saving_modelverse_waiting_input(self):
        self.current_state[self.Root_root_running_main_behaviour_saving_modelverse] = []
    
    def enter_Root_root_running_main_behaviour_saving_modelverse_waiting_client(self):
        self.current_state[self.Root_root_running_main_behaviour_saving_modelverse].append(self.Root_root_running_main_behaviour_saving_modelverse_waiting_client)
    
    def exit_Root_root_running_main_behaviour_saving_modelverse_waiting_client(self):
        self.current_state[self.Root_root_running_main_behaviour_saving_modelverse] = []
    
    def enter_Root_root_running_main_behaviour_restoring_modelverse_waiting(self):
        self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse].append(self.Root_root_running_main_behaviour_restoring_modelverse_waiting)
    
    def exit_Root_root_running_main_behaviour_restoring_modelverse_waiting(self):
        self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse] = []
    
    def enter_Root_root_running_main_behaviour_restoring_modelverse_getting_file_name(self):
        self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse].append(self.Root_root_running_main_behaviour_restoring_modelverse_getting_file_name)
    
    def exit_Root_root_running_main_behaviour_restoring_modelverse_getting_file_name(self):
        self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse] = []
    
    def enter_Root_root_running_main_behaviour_restoring_modelverse_waiting_client(self):
        self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse].append(self.Root_root_running_main_behaviour_restoring_modelverse_waiting_client)
    
    def exit_Root_root_running_main_behaviour_restoring_modelverse_waiting_client(self):
        self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse] = []
    
    def enter_Root_root_running_main_behaviour_loading_model_waiting(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_model].append(self.Root_root_running_main_behaviour_loading_model_waiting)
    
    def exit_Root_root_running_main_behaviour_loading_model_waiting(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_model] = []
    
    def enter_Root_root_running_main_behaviour_loading_model_creating_main_toolbar(self):
        self.timers[0] = 0.05
        self.current_state[self.Root_root_running_main_behaviour_loading_model].append(self.Root_root_running_main_behaviour_loading_model_creating_main_toolbar)
    
    def exit_Root_root_running_main_behaviour_loading_model_creating_main_toolbar(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root_running_main_behaviour_loading_model] = []
    
    def enter_Root_root_running_main_behaviour_loading_model_reading_type_model(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_model].append(self.Root_root_running_main_behaviour_loading_model_reading_type_model)
    
    def exit_Root_root_running_main_behaviour_loading_model_reading_type_model(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_model] = []
    
    def enter_Root_root_running_main_behaviour_loading_model_loop(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_model].append(self.Root_root_running_main_behaviour_loading_model_loop)
    
    def exit_Root_root_running_main_behaviour_loading_model_loop(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_model] = []
    
    def enter_Root_root_running_main_behaviour_loading_model_reading_element(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_model].append(self.Root_root_running_main_behaviour_loading_model_reading_element)
    
    def exit_Root_root_running_main_behaviour_loading_model_reading_element(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_model] = []
    
    def enter_Root_root_running_main_behaviour_loading_model_drawing_clabjects(self):
        self.timers[1] = 0.1
        self.current_state[self.Root_root_running_main_behaviour_loading_model].append(self.Root_root_running_main_behaviour_loading_model_drawing_clabjects)
    
    def exit_Root_root_running_main_behaviour_loading_model_drawing_clabjects(self):
        self.timers.pop(1, None)
        self.current_state[self.Root_root_running_main_behaviour_loading_model] = []
    
    def enter_Root_root_running_main_behaviour_loading_model_drawing_associations(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_model].append(self.Root_root_running_main_behaviour_loading_model_drawing_associations)
    
    def exit_Root_root_running_main_behaviour_loading_model_drawing_associations(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_model] = []
    
    def enter_Root_root_running_main_behaviour_loading_type_model_waiting(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_type_model].append(self.Root_root_running_main_behaviour_loading_type_model_waiting)
    
    def exit_Root_root_running_main_behaviour_loading_type_model_waiting(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_type_model] = []
    
    def enter_Root_root_running_main_behaviour_loading_type_model_waiting_close(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_type_model].append(self.Root_root_running_main_behaviour_loading_type_model_waiting_close)
    
    def exit_Root_root_running_main_behaviour_loading_type_model_waiting_close(self):
        self.current_state[self.Root_root_running_main_behaviour_loading_type_model] = []
    
    def enter_Root_root_running_main_behaviour_editing_instance_waiting_client(self):
        self.current_state[self.Root_root_running_main_behaviour_editing_instance].append(self.Root_root_running_main_behaviour_editing_instance_waiting_client)
    
    def exit_Root_root_running_main_behaviour_editing_instance_waiting_client(self):
        self.current_state[self.Root_root_running_main_behaviour_editing_instance] = []
    
    def enter_Root_root_running_main_behaviour_editing_instance_entering_instance_details(self):
        self.current_state[self.Root_root_running_main_behaviour_editing_instance].append(self.Root_root_running_main_behaviour_editing_instance_entering_instance_details)
    
    def exit_Root_root_running_main_behaviour_editing_instance_entering_instance_details(self):
        self.current_state[self.Root_root_running_main_behaviour_editing_instance] = []
    
    def enter_Root_root_running_main_behaviour_editing_instance_waiting_client_update(self):
        self.current_state[self.Root_root_running_main_behaviour_editing_instance].append(self.Root_root_running_main_behaviour_editing_instance_waiting_client_update)
    
    def exit_Root_root_running_main_behaviour_editing_instance_waiting_client_update(self):
        self.current_state[self.Root_root_running_main_behaviour_editing_instance] = []
    
    def enter_Root_root_running_main_behaviour_editing_instance_waiting_client_read(self):
        self.current_state[self.Root_root_running_main_behaviour_editing_instance].append(self.Root_root_running_main_behaviour_editing_instance_waiting_client_read)
    
    def exit_Root_root_running_main_behaviour_editing_instance_waiting_client_read(self):
        self.current_state[self.Root_root_running_main_behaviour_editing_instance] = []
    
    def enter_Root_root_running_main_behaviour_creating_instance_entering_instance_details(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_instance].append(self.Root_root_running_main_behaviour_creating_instance_entering_instance_details)
    
    def exit_Root_root_running_main_behaviour_creating_instance_entering_instance_details(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_instance] = []
    
    def enter_Root_root_running_main_behaviour_creating_instance_waiting_client(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_instance].append(self.Root_root_running_main_behaviour_creating_instance_waiting_client)
    
    def exit_Root_root_running_main_behaviour_creating_instance_waiting_client(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_instance] = []
    
    def enter_Root_root_running_main_behaviour_creating_instance_creating_on_canvas(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_instance].append(self.Root_root_running_main_behaviour_creating_instance_creating_on_canvas)
    
    def exit_Root_root_running_main_behaviour_creating_instance_creating_on_canvas(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_instance] = []
    
    def enter_Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_instance].append(self.Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read)
    
    def exit_Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_instance] = []
    
    def enter_Root_root_running_main_behaviour_creating_model_waiting(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_model].append(self.Root_root_running_main_behaviour_creating_model_waiting)
    
    def exit_Root_root_running_main_behaviour_creating_model_waiting(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_model] = []
    
    def enter_Root_root_running_main_behaviour_creating_model_waiting_close(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_model].append(self.Root_root_running_main_behaviour_creating_model_waiting_close)
    
    def exit_Root_root_running_main_behaviour_creating_model_waiting_close(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_model] = []
    
    def enter_Root_root_running_main_behaviour_creating_model_entering_model_details(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_model].append(self.Root_root_running_main_behaviour_creating_model_entering_model_details)
    
    def exit_Root_root_running_main_behaviour_creating_model_entering_model_details(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_model] = []
    
    def enter_Root_root_running_main_behaviour_creating_model_waiting_client(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_model].append(self.Root_root_running_main_behaviour_creating_model_waiting_client)
    
    def exit_Root_root_running_main_behaviour_creating_model_waiting_client(self):
        self.current_state[self.Root_root_running_main_behaviour_creating_model] = []
    
    def enter_Root_root_running_main_behaviour_creating_model_deleting_toolbars(self):
        self.timers[2] = 0.5
        self.current_state[self.Root_root_running_main_behaviour_creating_model].append(self.Root_root_running_main_behaviour_creating_model_deleting_toolbars)
    
    def exit_Root_root_running_main_behaviour_creating_model_deleting_toolbars(self):
        self.timers.pop(2, None)
        self.current_state[self.Root_root_running_main_behaviour_creating_model] = []
    
    def enter_Root_root_running_main_behaviour_creating_model_creating_main_toolbar(self):
        self.timers[3] = 0.1
        self.current_state[self.Root_root_running_main_behaviour_creating_model].append(self.Root_root_running_main_behaviour_creating_model_creating_main_toolbar)
    
    def exit_Root_root_running_main_behaviour_creating_model_creating_main_toolbar(self):
        self.timers.pop(3, None)
        self.current_state[self.Root_root_running_main_behaviour_creating_model] = []
    
    def enter_Root_root_running_main_behaviour_creating_model_creating_toolbar(self):
        self.timers[4] = 0.1
        self.current_state[self.Root_root_running_main_behaviour_creating_model].append(self.Root_root_running_main_behaviour_creating_model_creating_toolbar)
    
    def exit_Root_root_running_main_behaviour_creating_model_creating_toolbar(self):
        self.timers.pop(4, None)
        self.current_state[self.Root_root_running_main_behaviour_creating_model] = []
    
    def enter_Root_root_running_error_behaviour_waiting(self):
        self.current_state[self.Root_root_running_error_behaviour].append(self.Root_root_running_error_behaviour_waiting)
    
    def exit_Root_root_running_error_behaviour_waiting(self):
        self.current_state[self.Root_root_running_error_behaviour] = []
    
    def enter_Root_root_running_log_behaviour_waiting(self):
        self.current_state[self.Root_root_running_log_behaviour].append(self.Root_root_running_log_behaviour_waiting)
    
    def exit_Root_root_running_log_behaviour_waiting(self):
        self.current_state[self.Root_root_running_log_behaviour] = []
    
    def enter_Root_root_running_log_behaviour_creating(self):
        self.current_state[self.Root_root_running_log_behaviour].append(self.Root_root_running_log_behaviour_creating)
    
    def exit_Root_root_running_log_behaviour_creating(self):
        self.current_state[self.Root_root_running_log_behaviour] = []
    
    def enter_Root_root_running_log_message_pack_behaviour_waiting(self):
        self.current_state[self.Root_root_running_log_message_pack_behaviour].append(self.Root_root_running_log_message_pack_behaviour_waiting)
    
    def exit_Root_root_running_log_message_pack_behaviour_waiting(self):
        self.current_state[self.Root_root_running_log_message_pack_behaviour] = []
    
    def enter_Root_root_running_log_click_behaviour_waiting(self):
        self.current_state[self.Root_root_running_log_click_behaviour].append(self.Root_root_running_log_click_behaviour_waiting)
    
    def exit_Root_root_running_log_click_behaviour_waiting(self):
        self.current_state[self.Root_root_running_log_click_behaviour] = []
    
    def enter_Root_root_running_log_click_behaviour_waiting_for_second(self):
        self.timers[5] = 0.3
        self.current_state[self.Root_root_running_log_click_behaviour].append(self.Root_root_running_log_click_behaviour_waiting_for_second)
    
    def exit_Root_root_running_log_click_behaviour_waiting_for_second(self):
        self.timers.pop(5, None)
        self.current_state[self.Root_root_running_log_click_behaviour] = []
    
    def enter_Root_root_running_toolbar_behaviour_waiting(self):
        self.current_state[self.Root_root_running_toolbar_behaviour].append(self.Root_root_running_toolbar_behaviour_waiting)
    
    def exit_Root_root_running_toolbar_behaviour_waiting(self):
        self.current_state[self.Root_root_running_toolbar_behaviour] = []
    
    def enter_Root_root_running_toolbar_behaviour_creating(self):
        self.current_state[self.Root_root_running_toolbar_behaviour].append(self.Root_root_running_toolbar_behaviour_creating)
    
    def exit_Root_root_running_toolbar_behaviour_creating(self):
        self.current_state[self.Root_root_running_toolbar_behaviour] = []
    
    def enter_Root_root_running_window_behaviour_waiting(self):
        self.current_state[self.Root_root_running_window_behaviour].append(self.Root_root_running_window_behaviour_waiting)
    
    def exit_Root_root_running_window_behaviour_waiting(self):
        self.current_state[self.Root_root_running_window_behaviour] = []
    
    def enter_Root_root_running_window_behaviour_creating(self):
        self.current_state[self.Root_root_running_window_behaviour].append(self.Root_root_running_window_behaviour_creating)
    
    def exit_Root_root_running_window_behaviour_creating(self):
        self.current_state[self.Root_root_running_window_behaviour] = []
    
    def enter_Root_root_running_window_behaviour_starting(self):
        self.current_state[self.Root_root_running_window_behaviour].append(self.Root_root_running_window_behaviour_starting)
    
    def exit_Root_root_running_window_behaviour_starting(self):
        self.current_state[self.Root_root_running_window_behaviour] = []
    
    def enter_Root_root_running_mvk_listener_waiting(self):
        self.current_state[self.Root_root_running_mvk_listener].append(self.Root_root_running_mvk_listener_waiting)
    
    def exit_Root_root_running_mvk_listener_waiting(self):
        self.current_state[self.Root_root_running_mvk_listener] = []
    
    def enter_Root_root_running_instance_behaviour_waiting(self):
        self.current_state[self.Root_root_running_instance_behaviour].append(self.Root_root_running_instance_behaviour_waiting)
    
    def exit_Root_root_running_instance_behaviour_waiting(self):
        self.current_state[self.Root_root_running_instance_behaviour] = []
    
    def enter_Root_root_running_instance_behaviour_moving_from_associations(self):
        self.current_state[self.Root_root_running_instance_behaviour].append(self.Root_root_running_instance_behaviour_moving_from_associations)
    
    def exit_Root_root_running_instance_behaviour_moving_from_associations(self):
        self.current_state[self.Root_root_running_instance_behaviour] = []
    
    def enter_Root_root_running_instance_behaviour_moving_to_associations(self):
        self.current_state[self.Root_root_running_instance_behaviour].append(self.Root_root_running_instance_behaviour_moving_to_associations)
    
    def exit_Root_root_running_instance_behaviour_moving_to_associations(self):
        self.current_state[self.Root_root_running_instance_behaviour] = []
    
    def enter_Root_root_running_instance_behaviour_deleting_instance(self):
        self.current_state[self.Root_root_running_instance_behaviour].append(self.Root_root_running_instance_behaviour_deleting_instance)
    
    def exit_Root_root_running_instance_behaviour_deleting_instance(self):
        self.current_state[self.Root_root_running_instance_behaviour] = []
    
    def enter_Root_root_running_canvas_behaviour_waiting(self):
        self.current_state[self.Root_root_running_canvas_behaviour].append(self.Root_root_running_canvas_behaviour_waiting)
    
    def exit_Root_root_running_canvas_behaviour_waiting(self):
        self.current_state[self.Root_root_running_canvas_behaviour] = []
    
    def enter_Root_root_running_canvas_behaviour_creating(self):
        self.current_state[self.Root_root_running_canvas_behaviour].append(self.Root_root_running_canvas_behaviour_creating)
    
    def exit_Root_root_running_canvas_behaviour_creating(self):
        self.current_state[self.Root_root_running_canvas_behaviour] = []
    
    def enter_Root_root_running_listening_client_listening_client(self):
        self.current_state[self.Root_root_running_listening_client].append(self.Root_root_running_listening_client_listening_client)
    
    def exit_Root_root_running_listening_client_listening_client(self):
        self.current_state[self.Root_root_running_listening_client] = []
    
    def enter_Root_root_deleting(self):
        self.timers[6] = 0.05
        self.current_state[self.Root_root].append(self.Root_root_deleting)
    
    def exit_Root_root_deleting(self):
        self.timers.pop(6, None)
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_stopped(self):
        self.current_state[self.Root_root].append(self.Root_root_stopped)
    
    def exit_Root_root_stopped(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_running(self):
        self.enter_Root_root_running()
        self.enterDefault_Root_root_running_main_behaviour()
        self.enterDefault_Root_root_running_error_behaviour()
        self.enterDefault_Root_root_running_log_behaviour()
        self.enterDefault_Root_root_running_log_message_pack_behaviour()
        self.enterDefault_Root_root_running_log_click_behaviour()
        self.enterDefault_Root_root_running_toolbar_behaviour()
        self.enterDefault_Root_root_running_window_behaviour()
        self.enterDefault_Root_root_running_mvk_listener()
        self.enterDefault_Root_root_running_instance_behaviour()
        self.enterDefault_Root_root_running_canvas_behaviour()
        self.enterDefault_Root_root_running_listening_client()
    
    def enterDefault_Root_root_running_main_behaviour(self):
        self.enter_Root_root_running_main_behaviour()
        self.enter_Root_root_running_main_behaviour_running()
    
    def enterDefault_Root_root_running_main_behaviour_saving_modelverse(self):
        self.enter_Root_root_running_main_behaviour_saving_modelverse()
        self.enter_Root_root_running_main_behaviour_saving_modelverse_waiting_input()
    
    def enterDefault_Root_root_running_main_behaviour_restoring_modelverse(self):
        self.enter_Root_root_running_main_behaviour_restoring_modelverse()
        self.enter_Root_root_running_main_behaviour_restoring_modelverse_waiting()
    
    def enterDefault_Root_root_running_main_behaviour_loading_model(self):
        self.enter_Root_root_running_main_behaviour_loading_model()
        self.enter_Root_root_running_main_behaviour_loading_model_waiting()
    
    def enterDefault_Root_root_running_main_behaviour_loading_type_model(self):
        self.enter_Root_root_running_main_behaviour_loading_type_model()
        self.enter_Root_root_running_main_behaviour_loading_type_model_waiting()
    
    def enterDefault_Root_root_running_main_behaviour_editing_instance(self):
        self.enter_Root_root_running_main_behaviour_editing_instance()
        self.enter_Root_root_running_main_behaviour_editing_instance_waiting_client()
    
    def enterDefault_Root_root_running_main_behaviour_creating_instance(self):
        self.enter_Root_root_running_main_behaviour_creating_instance()
        self.enter_Root_root_running_main_behaviour_creating_instance_entering_instance_details()
    
    def enterDefault_Root_root_running_main_behaviour_creating_model(self):
        self.enter_Root_root_running_main_behaviour_creating_model()
        self.enter_Root_root_running_main_behaviour_creating_model_waiting()
    
    def enterDefault_Root_root_running_error_behaviour(self):
        self.enter_Root_root_running_error_behaviour()
        self.enter_Root_root_running_error_behaviour_waiting()
    
    def enterDefault_Root_root_running_log_behaviour(self):
        self.enter_Root_root_running_log_behaviour()
        self.enter_Root_root_running_log_behaviour_waiting()
    
    def enterDefault_Root_root_running_log_message_pack_behaviour(self):
        self.enter_Root_root_running_log_message_pack_behaviour()
        self.enter_Root_root_running_log_message_pack_behaviour_waiting()
    
    def enterDefault_Root_root_running_log_click_behaviour(self):
        self.enter_Root_root_running_log_click_behaviour()
        self.enter_Root_root_running_log_click_behaviour_waiting()
    
    def enterDefault_Root_root_running_toolbar_behaviour(self):
        self.enter_Root_root_running_toolbar_behaviour()
        self.enter_Root_root_running_toolbar_behaviour_waiting()
    
    def enterDefault_Root_root_running_window_behaviour(self):
        self.enter_Root_root_running_window_behaviour()
        self.enter_Root_root_running_window_behaviour_waiting()
    
    def enterDefault_Root_root_running_mvk_listener(self):
        self.enter_Root_root_running_mvk_listener()
        self.enter_Root_root_running_mvk_listener_waiting()
    
    def enterDefault_Root_root_running_instance_behaviour(self):
        self.enter_Root_root_running_instance_behaviour()
        self.enter_Root_root_running_instance_behaviour_waiting()
    
    def enterDefault_Root_root_running_canvas_behaviour(self):
        self.enter_Root_root_running_canvas_behaviour()
        self.enter_Root_root_running_canvas_behaviour_waiting()
    
    def enterDefault_Root_root_running_listening_client(self):
        self.enter_Root_root_running_listening_client()
        self.enter_Root_root_running_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_running:
                catched = self.transition_Root_root_running(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_deleting:
                catched = self.transition_Root_root_deleting(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_stopped:
                catched = self.transition_Root_root_stopped(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                self.addEvent(Event("create_toolbar", parameters = [{'class_name': 'MainToolbar', 'constructor_parameters': {}}]))
                self.enterDefault_Root_root_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running(self, event) :
        catched = False
        enableds = []
        if event.name == "window-close" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_running()
                send_event = Event("delete_self", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'toolbars' , send_event]))
                self.enter_Root_root_deleting()
            catched = True
        
        if not catched :
            catched = self.transition_Root_root_running_main_behaviour(event) or catched
            catched = self.transition_Root_root_running_error_behaviour(event) or catched
            catched = self.transition_Root_root_running_log_behaviour(event) or catched
            catched = self.transition_Root_root_running_log_message_pack_behaviour(event) or catched
            catched = self.transition_Root_root_running_log_click_behaviour(event) or catched
            catched = self.transition_Root_root_running_toolbar_behaviour(event) or catched
            catched = self.transition_Root_root_running_window_behaviour(event) or catched
            catched = self.transition_Root_root_running_mvk_listener(event) or catched
            catched = self.transition_Root_root_running_instance_behaviour(event) or catched
            catched = self.transition_Root_root_running_canvas_behaviour(event) or catched
            catched = self.transition_Root_root_running_listening_client(event) or catched
        return catched
    
    def transition_Root_root_running_main_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_running:
                catched = self.transition_Root_root_running_main_behaviour_running(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_validating_model:
                catched = self.transition_Root_root_running_main_behaviour_validating_model(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_saving_modelverse:
                catched = self.transition_Root_root_running_main_behaviour_saving_modelverse(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_restoring_modelverse:
                catched = self.transition_Root_root_running_main_behaviour_restoring_modelverse(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_loading_model:
                catched = self.transition_Root_root_running_main_behaviour_loading_model(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_loading_type_model:
                catched = self.transition_Root_root_running_main_behaviour_loading_type_model(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_editing_instance:
                catched = self.transition_Root_root_running_main_behaviour_editing_instance(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_creating_instance:
                catched = self.transition_Root_root_running_main_behaviour_creating_instance(event)
            elif self.current_state[self.Root_root_running_main_behaviour][0] == self.Root_root_running_main_behaviour_creating_model:
                catched = self.transition_Root_root_running_main_behaviour_creating_model(event)
        return catched
    
    def transition_Root_root_running_main_behaviour_running(self, event) :
        catched = False
        enableds = []
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters["event_name"] == "create_toolbar" :
                enableds.append(1)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters["event_name"] == "delete_toolbar" :
                enableds.append(2)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters["event_name"] == "select_type_to_create" :
                enableds.append(3)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters["event_name"] == "create_model" :
                enableds.append(4)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters["event_name"] == "load_model" :
                enableds.append(5)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters["event_name"] == "load_type_model" :
                enableds.append(6)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters["event_name"] == "save" :
                enableds.append(7)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters["event_name"] == "restore" :
                enableds.append(8)
        
        if event.name == "right-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) and self.type_to_create is not None :
                enableds.append(9)
        
        if event.name == "edit_instance" and event.getPort() == "" :
            enableds.append(10)
        
        if event.name == "button_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            event_parameters = parameters[0]
            if event_parameters["event_name"] == "validate" and self.model_loc and self.curr_formalism_location :
                enableds.append(11)
        
        if event.name == "escape" and event.getPort() == "input" :
            enableds.append(12)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                self.addEvent(Event("create_toolbar", parameters = [event_parameters]))
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 2 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                self.addEvent(Event("delete_toolbar", parameters = [event_parameters['association_name']]))
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 3 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                print 'selected type to create %s' % event_parameters["type_location"]
                self.type_to_create = event_parameters["type"]
                self.type_to_create_location = event_parameters["type_location"]
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 4 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                self.addEvent(Event("create_window", parameters = [{"class_name": "TypeModelBrowser", "constructor_parameters": {}}]))
                self.enterDefault_Root_root_running_main_behaviour_creating_model()
            elif enabled == 5 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                self.addEvent(Event("create_window", parameters = [{"class_name": "ModelBrowser", "constructor_parameters": {}}]))
                self.enterDefault_Root_root_running_main_behaviour_loading_model()
            elif enabled == 6 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                self.addEvent(Event("create_window", parameters = [{"class_name": "TypeModelBrowser", "constructor_parameters": {}}]))
                self.enterDefault_Root_root_running_main_behaviour_loading_type_model()
            elif enabled == 7 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                self.addEvent(Event("create_window", parameters = [{'class_name': 'InputWindow', 'constructor_parameters': {'option_names': ['File Name']}}]))
                self.enterDefault_Root_root_running_main_behaviour_saving_modelverse()
            elif enabled == 8 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'get_files'}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enterDefault_Root_root_running_main_behaviour_restoring_modelverse()
            elif enabled == 9 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                self.addEvent(Event("create_window", parameters = [{"class_name": "NewInstanceAttributeEditor", "constructor_parameters": {"type": self.type_to_create, "type_location": self.type_to_create_location, "location": self.model_loc}}]))
                self.enterDefault_Root_root_running_main_behaviour_creating_instance()
            elif enabled == 10 :
                parameters = event.getParameters()
                location = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                self.curr_editing_location = location
                send_event = Event("client_request", parameters = [self.association_name,{"event_name": "read", "request_parameters": location}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enterDefault_Root_root_running_main_behaviour_editing_instance()
            elif enabled == 11 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_main_behaviour_running()
                send_event = Event("client_request", parameters = [self.association_name,{"event_name": "validate", "request_parameters": {"model": self.model_loc, "type_model": self.curr_formalism_location}}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_main_behaviour_validating_model()
            elif enabled == 12 :
                self.exit_Root_root_running_main_behaviour_running()
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'canvas_elements' , send_event]))
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'log_messages' , send_event]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_validating_model(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_validating_model. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_validating_model()
                self.addEvent(Event("create_window", parameters = [{'class_name': 'PopupMessage', 'constructor_parameters': {'title': 'Info', 'message': '%s: %s' % (response.get_result(), response.get_status_message())}}]))
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_validating_model()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_saving_modelverse(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_main_behaviour_saving_modelverse][0] == self.Root_root_running_main_behaviour_saving_modelverse_waiting_input:
                catched = self.transition_Root_root_running_main_behaviour_saving_modelverse_waiting_input(event)
            elif self.current_state[self.Root_root_running_main_behaviour_saving_modelverse][0] == self.Root_root_running_main_behaviour_saving_modelverse_waiting_client:
                catched = self.transition_Root_root_running_main_behaviour_saving_modelverse_waiting_client(event)
        return catched
    
    def transition_Root_root_running_main_behaviour_saving_modelverse_waiting_input(self, event) :
        catched = False
        enableds = []
        if event.name == "input_given" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_saving_modelverse_waiting_input. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                given_input = parameters[0]
                self.exit_Root_root_running_main_behaviour_saving_modelverse_waiting_input()
                send_event = Event("client_request", parameters = [self.association_name,{"event_name": "backup", "request_parameters": {"file_name": given_input["File Name"]}}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_main_behaviour_saving_modelverse_waiting_client()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_saving_modelverse()
                print 'closed window!'
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 3 :
                self.exit_Root_root_running_main_behaviour_saving_modelverse()
                print 'error'
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_saving_modelverse_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_saving_modelverse_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_saving_modelverse()
                self.addEvent(Event("log", parameters = ['Successfully backed up Modelverse to %s' % response.get_result()]))
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_saving_modelverse()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_restoring_modelverse(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse][0] == self.Root_root_running_main_behaviour_restoring_modelverse_waiting:
                catched = self.transition_Root_root_running_main_behaviour_restoring_modelverse_waiting(event)
            elif self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse][0] == self.Root_root_running_main_behaviour_restoring_modelverse_getting_file_name:
                catched = self.transition_Root_root_running_main_behaviour_restoring_modelverse_getting_file_name(event)
            elif self.current_state[self.Root_root_running_main_behaviour_restoring_modelverse][0] == self.Root_root_running_main_behaviour_restoring_modelverse_waiting_client:
                catched = self.transition_Root_root_running_main_behaviour_restoring_modelverse_waiting_client(event)
        return catched
    
    def transition_Root_root_running_main_behaviour_restoring_modelverse_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_restoring_modelverse_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_restoring_modelverse_waiting()
                self.addEvent(Event("create_window", parameters = [{'class_name': 'SelectionWindow', 'constructor_parameters': {'selection_text': 'File', 'options': [i for i in response.get_result()]}}]))
                self.enter_Root_root_running_main_behaviour_restoring_modelverse_getting_file_name()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_restoring_modelverse()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_restoring_modelverse_getting_file_name(self, event) :
        catched = False
        enableds = []
        if event.name == "option_selected" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_restoring_modelverse_getting_file_name. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                selected_option = parameters[0]
                self.exit_Root_root_running_main_behaviour_restoring_modelverse_getting_file_name()
                print 'selected option %s' % selected_option
                send_event = Event("client_request", parameters = [self.association_name,{"event_name": "restore", "request_parameters": {"file_name": StringValue(selected_option)}}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_main_behaviour_restoring_modelverse_waiting_client()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_restoring_modelverse()
                print 'closed window!'
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 3 :
                self.exit_Root_root_running_main_behaviour_restoring_modelverse()
                print 'error'
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_restoring_modelverse_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_restoring_modelverse_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_restoring_modelverse()
                self.addEvent(Event("log", parameters = ['Successfully restored Modelverse from %s' % response.get_result()]))
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_restoring_modelverse()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_model(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_main_behaviour_loading_model][0] == self.Root_root_running_main_behaviour_loading_model_waiting:
                catched = self.transition_Root_root_running_main_behaviour_loading_model_waiting(event)
            elif self.current_state[self.Root_root_running_main_behaviour_loading_model][0] == self.Root_root_running_main_behaviour_loading_model_creating_main_toolbar:
                catched = self.transition_Root_root_running_main_behaviour_loading_model_creating_main_toolbar(event)
            elif self.current_state[self.Root_root_running_main_behaviour_loading_model][0] == self.Root_root_running_main_behaviour_loading_model_reading_type_model:
                catched = self.transition_Root_root_running_main_behaviour_loading_model_reading_type_model(event)
            elif self.current_state[self.Root_root_running_main_behaviour_loading_model][0] == self.Root_root_running_main_behaviour_loading_model_loop:
                catched = self.transition_Root_root_running_main_behaviour_loading_model_loop(event)
            elif self.current_state[self.Root_root_running_main_behaviour_loading_model][0] == self.Root_root_running_main_behaviour_loading_model_reading_element:
                catched = self.transition_Root_root_running_main_behaviour_loading_model_reading_element(event)
            elif self.current_state[self.Root_root_running_main_behaviour_loading_model][0] == self.Root_root_running_main_behaviour_loading_model_drawing_clabjects:
                catched = self.transition_Root_root_running_main_behaviour_loading_model_drawing_clabjects(event)
            elif self.current_state[self.Root_root_running_main_behaviour_loading_model][0] == self.Root_root_running_main_behaviour_loading_model_drawing_associations:
                catched = self.transition_Root_root_running_main_behaviour_loading_model_drawing_associations(event)
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_model_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "model_selected" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_loading_model_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                model = parameters[0]
                model_location = parameters[1]
                self.exit_Root_root_running_main_behaviour_loading_model_waiting()
                self.model_loc = model_location
                self.curr_formalism_location = model.linguistic_type
                self.curr_model = model
                self.curr_model_loc = model_location
                self.curr_element_idx = 0
                self.curr_clabjects = []
                self.curr_assocs = []
                self.curr_x = 50
                self.curr_y = 50
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'toolbars']))
                self.enter_Root_root_running_main_behaviour_loading_model_creating_main_toolbar()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_loading_model()
                print 'closed window!'
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 3 :
                self.exit_Root_root_running_main_behaviour_loading_model()
                print 'error'
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_model_creating_main_toolbar(self, event) :
        catched = False
        enableds = []
        if event.name == "_0after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_loading_model_creating_main_toolbar. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_loading_model_creating_main_toolbar()
                self.addEvent(Event("create_toolbar", parameters = [{'class_name': 'MainToolbar', 'constructor_parameters': {}}]))
                send_event = Event("client_request", parameters = [self.association_name,{"event_name": "read", "request_parameters": self.curr_model.linguistic_type}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_main_behaviour_loading_model_reading_type_model()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_model_reading_type_model(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_loading_model_reading_type_model. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_loading_model_reading_type_model()
                self.addEvent(Event("create_toolbar", parameters = [{'class_name': 'FormalismToolbar', 'constructor_parameters': {'formalism': response[StringValue('item')]}}]))
                self.c.delete("all")
                self.enter_Root_root_running_main_behaviour_loading_model_loop()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_loading_model()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_model_loop(self, event) :
        catched = False
        enableds = []
        if self.curr_element_idx < len(self.curr_model.elements) :
            enableds.append(1)
        
        if self.curr_element_idx == len(self.curr_model.elements) :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_loading_model_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_loading_model_loop()
                send_event = Event("client_request", parameters = [self.association_name,{"event_name": "read", "request_parameters": self.curr_model.elements[self.curr_element_idx][1]}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_main_behaviour_loading_model_reading_element()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_loading_model_loop()
                self.enter_Root_root_running_main_behaviour_loading_model_drawing_clabjects()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_model_reading_element(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_loading_model_reading_element. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_loading_model_reading_element()
                print 'read an item! %s' % response
                self.curr_element_idx += 1
                item = response[StringValue('item')]
                if isinstance(item, client_object.Association) and (not isinstance(item, client_object.Composition)) and item.potency == IntegerValue(0):
                    self.curr_assocs.append(item)
                elif isinstance(item, client_object.Clabject) and (not isinstance(item, client_object.Composition) or item.potency > IntegerValue(0)):
                    self.curr_clabjects.append(item)
                self.enter_Root_root_running_main_behaviour_loading_model_loop()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_loading_model()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_model_drawing_clabjects(self, event) :
        catched = False
        enableds = []
        if self.curr_clabjects :
            enableds.append(1)
        
        if event.name == "_1after" and event.getPort() == "" :
            if not self.curr_clabjects :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_loading_model_drawing_clabjects. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_loading_model_drawing_clabjects()
                item = self.curr_clabjects.pop(0)
                params = {'class_name': 'Instance', 'constructor_parameters': {'location': item.location, 'name': item.name, 'typename': item.linguistic_type.substring(start=item.linguistic_type.rfind(StringValue('.')) + IntegerValue(1)), 'x': self.curr_x, 'y': self.curr_y}}
                if isinstance(item, client_object.Association):
                    params['constructor_parameters']['from_loc'] = item.from_multiplicity.node
                    params['constructor_parameters']['to_loc'] = item.to_multiplicity.node
                print params
                print item
                self.addEvent(Event("create_instance_on_canvas", parameters = [params]))
                if self.curr_x >= self.winfo_width():
                    self.curr_x = 30
                    self.curr_y += 60
                else:
                    self.curr_x += 230
                print self.curr_x, self.curr_y
                self.enter_Root_root_running_main_behaviour_loading_model_drawing_clabjects()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_loading_model_drawing_clabjects()
                self.enter_Root_root_running_main_behaviour_loading_model_drawing_associations()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_model_drawing_associations(self, event) :
        catched = False
        enableds = []
        if self.curr_assocs :
            enableds.append(1)
        
        if not self.curr_assocs :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_loading_model_drawing_associations. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_loading_model_drawing_associations()
                item = self.curr_assocs.pop(0)
                data = {'class_name': 'ArrowInstance', 'constructor_parameters': {'location': item.location, 'name': item.name, 'typename': item.linguistic_type.substring(start=item.linguistic_type.rfind(StringValue('.')) + IntegerValue(1))}}
                data['constructor_parameters']['from_id'] = self.loc_to_instance[item.from_multiplicity.node].tagorid
                data['constructor_parameters']['to_id'] = self.loc_to_instance[item.to_multiplicity.node].tagorid
                data['constructor_parameters']['from_instance'] = item.from_multiplicity.node
                data['constructor_parameters']['to_instance'] = item.to_multiplicity.node
                self.addEvent(Event("create_instance_on_canvas", parameters = [data]))
                self.enter_Root_root_running_main_behaviour_loading_model_drawing_associations()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_loading_model()
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_type_model(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_main_behaviour_loading_type_model][0] == self.Root_root_running_main_behaviour_loading_type_model_waiting:
                catched = self.transition_Root_root_running_main_behaviour_loading_type_model_waiting(event)
            elif self.current_state[self.Root_root_running_main_behaviour_loading_type_model][0] == self.Root_root_running_main_behaviour_loading_type_model_waiting_close:
                catched = self.transition_Root_root_running_main_behaviour_loading_type_model_waiting_close(event)
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_type_model_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "type_model_selected" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_loading_type_model_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                formalism = parameters[0]
                formalism_location = parameters[1]
                self.exit_Root_root_running_main_behaviour_loading_type_model_waiting()
                self.addEvent(Event("create_toolbar", parameters = [{'class_name': 'FormalismToolbar', 'constructor_parameters': {'formalism': formalism}}]))
                self.addEvent(Event("log", parameters = ['Successfully loaded formalism %s.' % formalism_location]))
                self.enter_Root_root_running_main_behaviour_loading_type_model_waiting_close()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_loading_type_model()
                print 'closed window!'
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 3 :
                self.exit_Root_root_running_main_behaviour_loading_type_model()
                print 'error'
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_loading_type_model_waiting_close(self, event) :
        catched = False
        enableds = []
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_loading_type_model_waiting_close. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_loading_type_model()
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_editing_instance(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_main_behaviour_editing_instance][0] == self.Root_root_running_main_behaviour_editing_instance_waiting_client:
                catched = self.transition_Root_root_running_main_behaviour_editing_instance_waiting_client(event)
            elif self.current_state[self.Root_root_running_main_behaviour_editing_instance][0] == self.Root_root_running_main_behaviour_editing_instance_entering_instance_details:
                catched = self.transition_Root_root_running_main_behaviour_editing_instance_entering_instance_details(event)
            elif self.current_state[self.Root_root_running_main_behaviour_editing_instance][0] == self.Root_root_running_main_behaviour_editing_instance_waiting_client_update:
                catched = self.transition_Root_root_running_main_behaviour_editing_instance_waiting_client_update(event)
            elif self.current_state[self.Root_root_running_main_behaviour_editing_instance][0] == self.Root_root_running_main_behaviour_editing_instance_waiting_client_read:
                catched = self.transition_Root_root_running_main_behaviour_editing_instance_waiting_client_read(event)
        return catched
    
    def transition_Root_root_running_main_behaviour_editing_instance_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_editing_instance_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_editing_instance_waiting_client()
                self.addEvent(Event("create_window", parameters = [{"class_name": "InstanceAttributeEditor", "constructor_parameters": {"instance": response[StringValue("item")]}}]))
                self.enter_Root_root_running_main_behaviour_editing_instance_entering_instance_details()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_editing_instance()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_editing_instance_entering_instance_details(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_details_entered" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_editing_instance_entering_instance_details. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                data = parameters[0]
                self.exit_Root_root_running_main_behaviour_editing_instance_entering_instance_details()
                print 'Entered instance details! %s' % data
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'update', 'request_parameters': data}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_main_behaviour_editing_instance_waiting_client_update()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_editing_instance()
                print 'closed window!'
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 3 :
                self.exit_Root_root_running_main_behaviour_editing_instance()
                print 'error'
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_editing_instance_waiting_client_update(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_editing_instance_waiting_client_update. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_editing_instance_waiting_client_update()
                print response
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': response[StringValue('location')]}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_main_behaviour_editing_instance_waiting_client_read()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_editing_instance()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_editing_instance_waiting_client_read(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_editing_instance_waiting_client_read. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_editing_instance()
                print response
                item = response[StringValue("item")]
                if self.curr_editing_location != item.location:
                    self.loc_to_instance[self.curr_editing_location].set_text(item.name)
                    self.loc_to_instance[self.curr_editing_location].set_location(item.location)
                    self.loc_to_instance[item.location] = self.loc_to_instance[self.curr_editing_location]
                    del self.loc_to_instance[self.curr_editing_location]
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_editing_instance()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_instance(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_main_behaviour_creating_instance][0] == self.Root_root_running_main_behaviour_creating_instance_entering_instance_details:
                catched = self.transition_Root_root_running_main_behaviour_creating_instance_entering_instance_details(event)
            elif self.current_state[self.Root_root_running_main_behaviour_creating_instance][0] == self.Root_root_running_main_behaviour_creating_instance_waiting_client:
                catched = self.transition_Root_root_running_main_behaviour_creating_instance_waiting_client(event)
            elif self.current_state[self.Root_root_running_main_behaviour_creating_instance][0] == self.Root_root_running_main_behaviour_creating_instance_creating_on_canvas:
                catched = self.transition_Root_root_running_main_behaviour_creating_instance_creating_on_canvas(event)
            elif self.current_state[self.Root_root_running_main_behaviour_creating_instance][0] == self.Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read:
                catched = self.transition_Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read(event)
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_instance_entering_instance_details(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_details_entered" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_instance_entering_instance_details. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                data = parameters[0]
                self.exit_Root_root_running_main_behaviour_creating_instance_entering_instance_details()
                print 'Entered instance details! %s' % data
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'create', 'request_parameters': data}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_main_behaviour_creating_instance_waiting_client()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_creating_instance()
                print 'closed window!'
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 3 :
                self.exit_Root_root_running_main_behaviour_creating_instance()
                print 'error'
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_instance_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_instance_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_creating_instance_waiting_client()
                print response
                creation_loc = response.value[StringValue("location")]
                instance_loc = None
                instance_name = None
                if isinstance(response, mvk.interfaces.changelog.MvKCompositeLog):
                    found = False
                    for l in response.logs:
                        if found:
                            break
                        for a in l.value[StringValue("attributes")]:
                            print a
                            if a[StringValue('name')] == StringValue('name'):
                                instance_name = a[StringValue('value')]
                                instance_loc = creation_loc + StringValue('.') + instance_name
                            if a[StringValue('name')] == StringValue('class') and a[StringValue('value')] == self.type_to_create_location:
                                found = True
                else:
                    for a in response.value[StringValue("attributes")]:
                        print a
                        if a[StringValue('name')] == StringValue('name'):
                            instance_loc = creation_loc + StringValue('.') + a[StringValue('value')]
                self.data = {}
                if isinstance(self.type_to_create, client_object.Association) and self.type_to_create.potency == IntegerValue(1):
                    self.data['class_name'] = 'ArrowInstance'
                    self.data['constructor_parameters'] = {'location': instance_loc, 'name': instance_name, 'typename': self.type_to_create_location.substring(start=self.type_to_create_location.rfind(StringValue('.')) + IntegerValue(1))}
                else:
                    self.data['class_name'] = 'Instance'
                    self.data['constructor_parameters'] = {'location': instance_loc, 'name': instance_name, 'typename': self.type_to_create_location.substring(start=self.type_to_create_location.rfind(StringValue('.')) + IntegerValue(1)), 'x': self.last_x, 'y': self.last_y}
                self.addEvent(Event("log", parameters = ['(Create) %s ' % response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_creating_instance_creating_on_canvas()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_creating_instance()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_instance_creating_on_canvas(self, event) :
        catched = False
        enableds = []
        if (self.data['class_name'] == 'Instance' and (not isinstance(self.type_to_create, client_object.Association) or 'from_loc' in self.data['constructor_parameters'] and 'to_loc' in self.data['constructor_parameters'])) or ('from_id' in self.data['constructor_parameters'] and 'to_id' in self.data['constructor_parameters']) :
            enableds.append(1)
        
        if (self.data['class_name'] == 'ArrowInstance' or (self.data['class_name'] == 'Instance' and isinstance(self.type_to_create, client_object.Association))) and ('from_id' not in self.data['constructor_parameters'] or 'to_id' not in self.data['constructor_parameters']) :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_instance_creating_on_canvas. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_creating_instance()
                self.addEvent(Event("create_instance_on_canvas", parameters = [self.data]))
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_creating_instance_creating_on_canvas()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': self.data['constructor_parameters']['location']}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_creating_instance_waiting_client_assoc_read()
                item = response[StringValue("item")]
                if item.potency == IntegerValue(0):
                    self.data['constructor_parameters']['from_id'] = self.loc_to_instance[item.from_multiplicity.node].tagorid
                    self.data['constructor_parameters']['to_id'] = self.loc_to_instance[item.to_multiplicity.node].tagorid
                    self.data['constructor_parameters']['from_instance'] = item.from_multiplicity.node
                    self.data['constructor_parameters']['to_instance'] = item.to_multiplicity.node
                else:
                    self.data['constructor_parameters']['from_loc'] = item.from_multiplicity.node
                    self.data['constructor_parameters']['to_loc'] = item.to_multiplicity.node
                self.enter_Root_root_running_main_behaviour_creating_instance_creating_on_canvas()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_creating_instance()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_model(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_main_behaviour_creating_model][0] == self.Root_root_running_main_behaviour_creating_model_waiting:
                catched = self.transition_Root_root_running_main_behaviour_creating_model_waiting(event)
            elif self.current_state[self.Root_root_running_main_behaviour_creating_model][0] == self.Root_root_running_main_behaviour_creating_model_waiting_close:
                catched = self.transition_Root_root_running_main_behaviour_creating_model_waiting_close(event)
            elif self.current_state[self.Root_root_running_main_behaviour_creating_model][0] == self.Root_root_running_main_behaviour_creating_model_entering_model_details:
                catched = self.transition_Root_root_running_main_behaviour_creating_model_entering_model_details(event)
            elif self.current_state[self.Root_root_running_main_behaviour_creating_model][0] == self.Root_root_running_main_behaviour_creating_model_waiting_client:
                catched = self.transition_Root_root_running_main_behaviour_creating_model_waiting_client(event)
            elif self.current_state[self.Root_root_running_main_behaviour_creating_model][0] == self.Root_root_running_main_behaviour_creating_model_deleting_toolbars:
                catched = self.transition_Root_root_running_main_behaviour_creating_model_deleting_toolbars(event)
            elif self.current_state[self.Root_root_running_main_behaviour_creating_model][0] == self.Root_root_running_main_behaviour_creating_model_creating_main_toolbar:
                catched = self.transition_Root_root_running_main_behaviour_creating_model_creating_main_toolbar(event)
            elif self.current_state[self.Root_root_running_main_behaviour_creating_model][0] == self.Root_root_running_main_behaviour_creating_model_creating_toolbar:
                catched = self.transition_Root_root_running_main_behaviour_creating_model_creating_toolbar(event)
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_model_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "type_model_selected" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_model_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                formalism = parameters[0]
                formalism_location = parameters[1]
                self.exit_Root_root_running_main_behaviour_creating_model_waiting()
                self.addEvent(Event("create_window", parameters = [{"class_name": "NewInstanceAttributeEditor", "constructor_parameters": {"type": formalism, "type_location": formalism_location}}]))
                self.curr_formalism = formalism
                self.curr_formalism_location = formalism_location
                self.enter_Root_root_running_main_behaviour_creating_model_waiting_close()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_creating_model()
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_model_waiting_close(self, event) :
        catched = False
        enableds = []
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_model_waiting_close. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_creating_model_waiting_close()
                self.enter_Root_root_running_main_behaviour_creating_model_entering_model_details()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_model_entering_model_details(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_details_entered" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "error" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_model_entering_model_details. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                data = parameters[0]
                self.exit_Root_root_running_main_behaviour_creating_model_entering_model_details()
                print 'Entered model details! %s' % data
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'create', 'request_parameters': data}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_main_behaviour_creating_model_waiting_client()
            elif enabled == 2 :
                self.exit_Root_root_running_main_behaviour_creating_model()
                print 'closed window!'
                self.enter_Root_root_running_main_behaviour_running()
            elif enabled == 3 :
                self.exit_Root_root_running_main_behaviour_creating_model()
                print 'error'
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_model_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_model_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_creating_model_waiting_client()
                print response
                creation_loc = response.value[StringValue("location")]
                if isinstance(response, mvk.interfaces.changelog.MvKCompositeLog):
                    found = False
                    for l in response.logs:
                        if found:
                            break
                        for a in l.value[StringValue("attributes")]:
                            print a
                            if a[StringValue('name')] == StringValue('name'):
                                self.model_loc = creation_loc + StringValue('.') + a[StringValue('value')]
                            if a[StringValue('name')] == StringValue('type_model') and a[StringValue('value')] == self.curr_formalism_location:
                                found = True
                else:
                    for a in response.value[StringValue("attributes")]:
                            print a
                            if a[StringValue('name')] == StringValue('name'):
                                self.model_loc = creation_loc + StringValue('.') + a[StringValue('value')]
                self.addEvent(Event("log", parameters = ['(Create) %s ' % response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_creating_model_deleting_toolbars()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_main_behaviour_creating_model()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_model_deleting_toolbars(self, event) :
        catched = False
        enableds = []
        if event.name == "_2after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_model_deleting_toolbars. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_creating_model_deleting_toolbars()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, 'toolbars']))
                self.enter_Root_root_running_main_behaviour_creating_model_creating_main_toolbar()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_model_creating_main_toolbar(self, event) :
        catched = False
        enableds = []
        if event.name == "_3after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_model_creating_main_toolbar. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_creating_model_creating_main_toolbar()
                self.addEvent(Event("create_toolbar", parameters = [{'class_name': 'MainToolbar', 'constructor_parameters': {}}]))
                self.enter_Root_root_running_main_behaviour_creating_model_creating_toolbar()
            catched = True
        
        return catched
    
    def transition_Root_root_running_main_behaviour_creating_model_creating_toolbar(self, event) :
        catched = False
        enableds = []
        if event.name == "_4after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_main_behaviour_creating_model_creating_toolbar. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_main_behaviour_creating_model()
                self.addEvent(Event("create_toolbar", parameters = [{'class_name': 'FormalismToolbar', 'constructor_parameters': {'formalism': self.curr_formalism}}]))
                self.c.delete("all")
                self.enter_Root_root_running_main_behaviour_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running_error_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_error_behaviour][0] == self.Root_root_running_error_behaviour_waiting:
                catched = self.transition_Root_root_running_error_behaviour_waiting(event)
        return catched
    
    def transition_Root_root_running_error_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "error" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_error_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                error_code = parameters[0]
                error_message = parameters[1]
                self.exit_Root_root_running_error_behaviour_waiting()
                self.addEvent(Event("create_window", parameters = [{"class_name": "PopupMessage", "constructor_parameters": {"title": "ERROR", "message": "%s (%s)" % (error_message, error_code)}}]))
                self.addEvent(Event("log", parameters = ["%s (%s)" % (error_message, error_code)]))
                self.enter_Root_root_running_error_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_log_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_log_behaviour][0] == self.Root_root_running_log_behaviour_waiting:
                catched = self.transition_Root_root_running_log_behaviour_waiting(event)
            elif self.current_state[self.Root_root_running_log_behaviour][0] == self.Root_root_running_log_behaviour_creating:
                catched = self.transition_Root_root_running_log_behaviour_creating(event)
        return catched
    
    def transition_Root_root_running_log_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "log" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_log_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                log_message = parameters[0]
                self.exit_Root_root_running_log_behaviour_waiting()
                self.object_manager.addEvent(Event("create_instance", parameters = [self, 'log_messages','LogMessage',{'parent': self.log_frame.interior, 'log_message': log_message}]))
                self.enter_Root_root_running_log_behaviour_creating()
            catched = True
        
        return catched
    
    def transition_Root_root_running_log_behaviour_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_log_behaviour_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_log_behaviour_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_running_log_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_log_message_pack_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_log_message_pack_behaviour][0] == self.Root_root_running_log_message_pack_behaviour_waiting:
                catched = self.transition_Root_root_running_log_message_pack_behaviour_waiting(event)
        return catched
    
    def transition_Root_root_running_log_message_pack_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "log_message_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_log_message_pack_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                log_message = parameters[0]
                self.exit_Root_root_running_log_message_pack_behaviour_waiting()
                log_message.pack(side=tk.TOP, fill=tk.X, expand=True)
                self.log_id_to_assoc[id(log_message)] = log_message.association_name
                self.enter_Root_root_running_log_message_pack_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_log_click_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_log_click_behaviour][0] == self.Root_root_running_log_click_behaviour_waiting:
                catched = self.transition_Root_root_running_log_click_behaviour_waiting(event)
            elif self.current_state[self.Root_root_running_log_click_behaviour][0] == self.Root_root_running_log_click_behaviour_waiting_for_second:
                catched = self.transition_Root_root_running_log_click_behaviour_waiting_for_second(event)
        return catched
    
    def transition_Root_root_running_log_click_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "log_message_pressed" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_log_click_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                log_id = parameters[0]
                self.exit_Root_root_running_log_click_behaviour_waiting()
                self.curr_log_id = log_id
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'log_messages' , send_event]))
                send_event = Event("highlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.log_id_to_assoc[log_id] , send_event]))
                self.enter_Root_root_running_log_click_behaviour_waiting_for_second()
            catched = True
        
        return catched
    
    def transition_Root_root_running_log_click_behaviour_waiting_for_second(self, event) :
        catched = False
        enableds = []
        if event.name == "log_message_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            log_id = parameters[0]
            if self.curr_log_id == log_id :
                enableds.append(1)
        
        if event.name == "log_message_pressed" and event.getPort() == "" :
            parameters = event.getParameters()
            log_id = parameters[0]
            if self.curr_log_id != log_id :
                enableds.append(2)
        
        if event.name == "_5after" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_log_click_behaviour_waiting_for_second. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                log_id = parameters[0]
                self.exit_Root_root_running_log_click_behaviour_waiting_for_second()
                self.enter_Root_root_running_log_click_behaviour_waiting()
            elif enabled == 2 :
                parameters = event.getParameters()
                log_id = parameters[0]
                self.exit_Root_root_running_log_click_behaviour_waiting_for_second()
                self.curr_log_id = log_id
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'log_messages' , send_event]))
                send_event = Event("highlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.log_id_to_assoc[log_id] , send_event]))
                self.enter_Root_root_running_log_click_behaviour_waiting_for_second()
            elif enabled == 3 :
                self.exit_Root_root_running_log_click_behaviour_waiting_for_second()
                self.enter_Root_root_running_log_click_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_toolbar_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_toolbar_behaviour][0] == self.Root_root_running_toolbar_behaviour_waiting:
                catched = self.transition_Root_root_running_toolbar_behaviour_waiting(event)
            elif self.current_state[self.Root_root_running_toolbar_behaviour][0] == self.Root_root_running_toolbar_behaviour_creating:
                catched = self.transition_Root_root_running_toolbar_behaviour_creating(event)
        return catched
    
    def transition_Root_root_running_toolbar_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "create_toolbar" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_toolbar" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "toolbar_created" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_toolbar_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_toolbar_behaviour_waiting()
                print 'got a create_toolbar %s' % event_parameters
                event_parameters["constructor_parameters"]["parent"] = self.toolbar_frame.interior
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "toolbars",event_parameters["class_name"],event_parameters["constructor_parameters"]]))
                self.enter_Root_root_running_toolbar_behaviour_creating()
            elif enabled == 2 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_toolbar_behaviour_waiting()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, association_name]))
                self.enter_Root_root_running_toolbar_behaviour_waiting()
            elif enabled == 3 :
                parameters = event.getParameters()
                toolbar = parameters[0]
                self.exit_Root_root_running_toolbar_behaviour_waiting()
                toolbar.pack(side=tk.LEFT, fill=tk.Y, padx=self.INTER_SPACING, pady=self.INTER_SPACING)
                self.enter_Root_root_running_toolbar_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_toolbar_behaviour_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_toolbar_behaviour_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_toolbar_behaviour_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_running_toolbar_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_window_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_window_behaviour][0] == self.Root_root_running_window_behaviour_waiting:
                catched = self.transition_Root_root_running_window_behaviour_waiting(event)
            elif self.current_state[self.Root_root_running_window_behaviour][0] == self.Root_root_running_window_behaviour_creating:
                catched = self.transition_Root_root_running_window_behaviour_creating(event)
            elif self.current_state[self.Root_root_running_window_behaviour][0] == self.Root_root_running_window_behaviour_starting:
                catched = self.transition_Root_root_running_window_behaviour_starting(event)
        return catched
    
    def transition_Root_root_running_window_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "create_window" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "delete_window" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "grab_focus" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_window_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_window_behaviour_waiting()
                event_parameters["constructor_parameters"]["parent"] = self
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "windows",event_parameters["class_name"],event_parameters["constructor_parameters"]]))
                self.enter_Root_root_running_window_behaviour_creating()
            elif enabled == 2 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_window_behaviour_waiting()
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, association_name]))
                self.enter_Root_root_running_window_behaviour_waiting()
            elif enabled == 3 :
                self.exit_Root_root_running_window_behaviour_waiting()
                self.grab_set()
                self.enter_Root_root_running_window_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_window_behaviour_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_window_behaviour_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_window_behaviour_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                self.enter_Root_root_running_window_behaviour_starting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_window_behaviour_starting(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_started" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_window_behaviour_starting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_window_behaviour_starting()
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_running_window_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_mvk_listener(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_mvk_listener][0] == self.Root_root_running_mvk_listener_waiting:
                catched = self.transition_Root_root_running_mvk_listener_waiting(event)
        return catched
    
    def transition_Root_root_running_mvk_listener_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "mvk_instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_mvk_listener_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                instance = parameters[0]
                self.exit_Root_root_running_mvk_listener_waiting()
                print 'mvk_instance_created %s' % instance.location
                self.loc_to_instance[instance.location] = instance
                self.instance_to_from_assocs[instance.association_name] = []
                self.instance_to_to_assocs[instance.association_name] = []
                if isinstance(instance, ArrowInstance):
                    self.instance_to_from_assocs[self.loc_to_instance[instance.from_instance].association_name].append(instance.association_name)
                    self.instance_to_to_assocs[self.loc_to_instance[instance.to_instance].association_name].append(instance.association_name)
                self.enter_Root_root_running_mvk_listener_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_instance_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_instance_behaviour][0] == self.Root_root_running_instance_behaviour_waiting:
                catched = self.transition_Root_root_running_instance_behaviour_waiting(event)
            elif self.current_state[self.Root_root_running_instance_behaviour][0] == self.Root_root_running_instance_behaviour_moving_from_associations:
                catched = self.transition_Root_root_running_instance_behaviour_moving_from_associations(event)
            elif self.current_state[self.Root_root_running_instance_behaviour][0] == self.Root_root_running_instance_behaviour_moving_to_associations:
                catched = self.transition_Root_root_running_instance_behaviour_moving_to_associations(event)
            elif self.current_state[self.Root_root_running_instance_behaviour][0] == self.Root_root_running_instance_behaviour_deleting_instance:
                catched = self.transition_Root_root_running_instance_behaviour_deleting_instance(event)
        return catched
    
    def transition_Root_root_running_instance_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if event.name == "instance_pressed" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "instance_moved" and event.getPort() == "" :
            enableds.append(3)
        
        if event.name == "delete" and event.getPort() == "input" :
            enableds.append(4)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_instance_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_instance_behaviour_waiting()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_running_instance_behaviour_waiting()
            elif enabled == 2 :
                parameters = event.getParameters()
                location = parameters[0]
                association_name = parameters[1]
                self.exit_Root_root_running_instance_behaviour_waiting()
                send_event = Event("unhighlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'canvas_elements' , send_event]))
                send_event = Event("highlight", parameters = [])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.selected_location = location
                self.selected_association_name = association_name
                self.enter_Root_root_running_instance_behaviour_waiting()
            elif enabled == 3 :
                parameters = event.getParameters()
                association_name = parameters[0]
                dx = parameters[1]
                dy = parameters[2]
                self.exit_Root_root_running_instance_behaviour_waiting()
                self.curr_assoc_idx = 0
                self.curr_assoc_name = association_name
                self.dx = dx
                self.dy = dy
                self.enter_Root_root_running_instance_behaviour_moving_from_associations()
            elif enabled == 4 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_running_instance_behaviour_waiting()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'delete', 'request_parameters': self.selected_location}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.object_manager.addEvent(Event("delete_instance", parameters = [self, self.selected_association_name]))
                self.enter_Root_root_running_instance_behaviour_deleting_instance()
            catched = True
        
        return catched
    
    def transition_Root_root_running_instance_behaviour_moving_from_associations(self, event) :
        catched = False
        enableds = []
        if self.curr_assoc_idx < len(self.instance_to_from_assocs[self.curr_assoc_name]) :
            enableds.append(1)
        
        if self.curr_assoc_idx == len(self.instance_to_from_assocs[self.curr_assoc_name]) :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_instance_behaviour_moving_from_associations. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_instance_behaviour_moving_from_associations()
                send_event = Event("move", parameters = [self.dx,self.dy,'from'])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.instance_to_from_assocs[self.curr_assoc_name][self.curr_assoc_idx] , send_event]))
                self.curr_assoc_idx += 1
                self.enter_Root_root_running_instance_behaviour_moving_from_associations()
            elif enabled == 2 :
                self.exit_Root_root_running_instance_behaviour_moving_from_associations()
                self.curr_assoc_idx = 0
                self.enter_Root_root_running_instance_behaviour_moving_to_associations()
            catched = True
        
        return catched
    
    def transition_Root_root_running_instance_behaviour_moving_to_associations(self, event) :
        catched = False
        enableds = []
        if self.curr_assoc_idx < len(self.instance_to_to_assocs[self.curr_assoc_name]) :
            enableds.append(1)
        
        if self.curr_assoc_idx == len(self.instance_to_to_assocs[self.curr_assoc_name]) :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_instance_behaviour_moving_to_associations. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_running_instance_behaviour_moving_to_associations()
                send_event = Event("move", parameters = [self.dx,self.dy,'to'])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, self.instance_to_to_assocs[self.curr_assoc_name][self.curr_assoc_idx] , send_event]))
                self.curr_assoc_idx += 1
                self.enter_Root_root_running_instance_behaviour_moving_to_associations()
            elif enabled == 2 :
                self.exit_Root_root_running_instance_behaviour_moving_to_associations()
                self.curr_assoc_idx = 0
                self.enter_Root_root_running_instance_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_instance_behaviour_deleting_instance(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_instance_behaviour_deleting_instance. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_instance_behaviour_deleting_instance()
                self.enter_Root_root_running_instance_behaviour_waiting()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_running_instance_behaviour_deleting_instance()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_running_instance_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_canvas_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_canvas_behaviour][0] == self.Root_root_running_canvas_behaviour_waiting:
                catched = self.transition_Root_root_running_canvas_behaviour_waiting(event)
            elif self.current_state[self.Root_root_running_canvas_behaviour][0] == self.Root_root_running_canvas_behaviour_creating:
                catched = self.transition_Root_root_running_canvas_behaviour_creating(event)
        return catched
    
    def transition_Root_root_running_canvas_behaviour_waiting(self, event) :
        catched = False
        enableds = []
        if event.name == "create_instance_on_canvas" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_canvas_behaviour_waiting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_running_canvas_behaviour_waiting()
                print 'creating instance with params %s' % event_parameters["constructor_parameters"]
                event_parameters["constructor_parameters"]["parent"] = self.c
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "canvas_elements",event_parameters["class_name"],event_parameters["constructor_parameters"]]))
                self.enter_Root_root_running_canvas_behaviour_waiting()
            catched = True
        
        return catched
    
    def transition_Root_root_running_canvas_behaviour_creating(self, event) :
        catched = False
        return catched
    
    def transition_Root_root_running_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_running_listening_client][0] == self.Root_root_running_listening_client_listening_client:
                catched = self.transition_Root_root_running_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_running_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_running_listening_client_listening_client()
                send_event = Event("client_request", parameters = [self.association_name + '/' + association_name,data])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running_listening_client_listening_client()
            catched = True
        
        return catched
    
    def transition_Root_root_deleting(self, event) :
        catched = False
        enableds = []
        if event.name == "_6after" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_deleting. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_deleting()
                send_event = Event("delete_window", parameters = [self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_stopped()
            catched = True
        
        return catched
    
    def transition_Root_root_stopped(self, event) :
        catched = False
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
    

class Label(MvKWidget, tk.Label, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_running = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(Label, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        print constructor_parameters["text"]
        tk.Label.__init__(self, constructor_parameters["parent"], text=constructor_parameters["text"], bg="white")
        MvKWidget.__init__(self, controller)
    
    # User defined destructor
    def __del__(self):
        self.destroy()
        
    # User defined method
    def set_text(self, text):
        self.config(text=text)
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_running in self.current_state[self.Root_root] :
            self.exit_Root_root_running()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_running(self):
        self.current_state[self.Root_root].append(self.Root_root_running)
    
    def exit_Root_root_running(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_running:
                catched = self.transition_Root_root_running(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("label_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running(self, event) :
        catched = False
        enableds = []
        if event.name == "left-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(1)
        
        if event.name == "highlight" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "unhighlight" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_running()
                send_event = Event("label_pressed", parameters = [self.cget('text')])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running()
            elif enabled == 2 :
                self.exit_Root_root_running()
                self.config(bg="yellow")
                self.enter_Root_root_running()
            elif enabled == 3 :
                self.exit_Root_root_running()
                self.config(bg="white")
                self.enter_Root_root_running()
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
    

class LogMessage(MvKWidget, tk.Label, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_running = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(LogMessage, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        print constructor_parameters["log_message"]
        tk.Label.__init__(self, constructor_parameters["parent"], text=constructor_parameters["log_message"], pady=5, width=30, relief=tk.GROOVE, wraplength=200, bg="ivory2")
        MvKWidget.__init__(self, controller)
    
    # User defined destructor
    def __del__(self):
        self.destroy()
        
    # User defined method
    def set_text(self, text):
        self.config(text=text)
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_running in self.current_state[self.Root_root] :
            self.exit_Root_root_running()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_running(self):
        self.current_state[self.Root_root].append(self.Root_root_running)
    
    def exit_Root_root_running(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_running:
                catched = self.transition_Root_root_running(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("log_message_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running(self, event) :
        catched = False
        enableds = []
        if event.name == "left-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(1)
        
        if event.name == "highlight" and event.getPort() == "" :
            enableds.append(2)
        
        if event.name == "unhighlight" and event.getPort() == "" :
            enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_running()
                send_event = Event("log_message_pressed", parameters = [id(self)])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running()
            elif enabled == 2 :
                self.exit_Root_root_running()
                self.config(bg="yellow")
                self.enter_Root_root_running()
            elif enabled == 3 :
                self.exit_Root_root_running()
                self.config(bg="ivory2")
                self.enter_Root_root_running()
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
    

class Instance(MvKWidget, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_main_behaviour = 2
    Root_root_main_behaviour_editing_behaviour = 3
    Root_root_main_behaviour_moving_behaviour = 4
    Root_root_initializing = 5
    Root_root_main_behaviour_editing_behaviour_idle = 6
    Root_root_main_behaviour_editing_behaviour_holding_control = 7
    Root_root_main_behaviour_moving_behaviour_unselected = 8
    Root_root_main_behaviour_moving_behaviour_selected = 9
    Root_root_main_behaviour_moving_behaviour_moving = 10
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_main_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_editing_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_moving_behaviour] = []
    
    def start(self):
        super(Instance, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        self.c = constructor_parameters["parent"]
        x, y = constructor_parameters["x"], constructor_parameters["y"]
        self.typename = str(constructor_parameters["typename"])
        self.text = str(constructor_parameters["name"]) + ': ' + self.typename
        len_x = 200
        len_y = 30
        if 'from_loc' in constructor_parameters and 'to_loc' in constructor_parameters:
            self.text += '\n%s\n   --> %s' % (constructor_parameters['from_loc'], constructor_parameters['to_loc'])
            len_y += 30
        self.tagorid = self.c.create_rectangle(x, y, x + len_x, y + len_y, fill='ghost white')
        self.text_id = self.c.create_text(x + len_x / 2, y + len_y / 2, text=self.text)
        self.location = constructor_parameters["location"]
        MvKWidget.__init__(self, controller, self.c, [self.tagorid, self.text_id])
    
    # User defined destructor
    def __del__(self):
        self.c.delete(self.tagorid)
        self.c.delete(self.text_id)
        
    # User defined method
    def set_text(self, text):
        self.c.itemconfig(self.text_id, text=str(text) + ': ' + self.typename)
        
    # User defined method
    def set_location(self, location):
        self.location = location
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.exit_Root_root_main_behaviour_editing_behaviour()
        self.exit_Root_root_main_behaviour_moving_behaviour()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_editing_behaviour(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_editing_behaviour)
    
    def exit_Root_root_main_behaviour_editing_behaviour(self):
        if self.Root_root_main_behaviour_editing_behaviour_idle in self.current_state[self.Root_root_main_behaviour_editing_behaviour] :
            self.exit_Root_root_main_behaviour_editing_behaviour_idle()
        if self.Root_root_main_behaviour_editing_behaviour_holding_control in self.current_state[self.Root_root_main_behaviour_editing_behaviour] :
            self.exit_Root_root_main_behaviour_editing_behaviour_holding_control()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_moving_behaviour(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_moving_behaviour)
    
    def exit_Root_root_main_behaviour_moving_behaviour(self):
        if self.Root_root_main_behaviour_moving_behaviour_unselected in self.current_state[self.Root_root_main_behaviour_moving_behaviour] :
            self.exit_Root_root_main_behaviour_moving_behaviour_unselected()
        if self.Root_root_main_behaviour_moving_behaviour_selected in self.current_state[self.Root_root_main_behaviour_moving_behaviour] :
            self.exit_Root_root_main_behaviour_moving_behaviour_selected()
        if self.Root_root_main_behaviour_moving_behaviour_moving in self.current_state[self.Root_root_main_behaviour_moving_behaviour] :
            self.exit_Root_root_main_behaviour_moving_behaviour_moving()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_editing_behaviour_idle(self):
        self.current_state[self.Root_root_main_behaviour_editing_behaviour].append(self.Root_root_main_behaviour_editing_behaviour_idle)
    
    def exit_Root_root_main_behaviour_editing_behaviour_idle(self):
        self.current_state[self.Root_root_main_behaviour_editing_behaviour] = []
    
    def enter_Root_root_main_behaviour_editing_behaviour_holding_control(self):
        self.current_state[self.Root_root_main_behaviour_editing_behaviour].append(self.Root_root_main_behaviour_editing_behaviour_holding_control)
    
    def exit_Root_root_main_behaviour_editing_behaviour_holding_control(self):
        self.current_state[self.Root_root_main_behaviour_editing_behaviour] = []
    
    def enter_Root_root_main_behaviour_moving_behaviour_unselected(self):
        self.current_state[self.Root_root_main_behaviour_moving_behaviour].append(self.Root_root_main_behaviour_moving_behaviour_unselected)
    
    def exit_Root_root_main_behaviour_moving_behaviour_unselected(self):
        self.current_state[self.Root_root_main_behaviour_moving_behaviour] = []
    
    def enter_Root_root_main_behaviour_moving_behaviour_selected(self):
        self.current_state[self.Root_root_main_behaviour_moving_behaviour].append(self.Root_root_main_behaviour_moving_behaviour_selected)
    
    def exit_Root_root_main_behaviour_moving_behaviour_selected(self):
        self.current_state[self.Root_root_main_behaviour_moving_behaviour] = []
    
    def enter_Root_root_main_behaviour_moving_behaviour_moving(self):
        self.current_state[self.Root_root_main_behaviour_moving_behaviour].append(self.Root_root_main_behaviour_moving_behaviour_moving)
    
    def exit_Root_root_main_behaviour_moving_behaviour_moving(self):
        self.current_state[self.Root_root_main_behaviour_moving_behaviour] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_main_behaviour(self):
        self.enter_Root_root_main_behaviour()
        self.enterDefault_Root_root_main_behaviour_editing_behaviour()
        self.enterDefault_Root_root_main_behaviour_moving_behaviour()
    
    def enterDefault_Root_root_main_behaviour_editing_behaviour(self):
        self.enter_Root_root_main_behaviour_editing_behaviour()
        self.enter_Root_root_main_behaviour_editing_behaviour_idle()
    
    def enterDefault_Root_root_main_behaviour_moving_behaviour(self):
        self.enter_Root_root_main_behaviour_moving_behaviour()
        self.enter_Root_root_main_behaviour_moving_behaviour_unselected()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("mvk_instance_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enterDefault_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
        if not catched :
            catched = self.transition_Root_root_main_behaviour_editing_behaviour(event) or catched
            catched = self.transition_Root_root_main_behaviour_moving_behaviour(event) or catched
        return catched
    
    def transition_Root_root_main_behaviour_editing_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_editing_behaviour][0] == self.Root_root_main_behaviour_editing_behaviour_idle:
                catched = self.transition_Root_root_main_behaviour_editing_behaviour_idle(event)
            elif self.current_state[self.Root_root_main_behaviour_editing_behaviour][0] == self.Root_root_main_behaviour_editing_behaviour_holding_control:
                catched = self.transition_Root_root_main_behaviour_editing_behaviour_holding_control(event)
        return catched
    
    def transition_Root_root_main_behaviour_editing_behaviour_idle(self, event) :
        catched = False
        enableds = []
        if event.name == "middle-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(1)
        
        if event.name == "control" and event.getPort() == "input" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_editing_behaviour_idle. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour_editing_behaviour_idle()
                send_event = Event("edit_instance", parameters = [self.location])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_editing_behaviour_idle()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_editing_behaviour_idle()
                self.enter_Root_root_main_behaviour_editing_behaviour_holding_control()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_editing_behaviour_holding_control(self, event) :
        catched = False
        enableds = []
        if event.name == "control-release" and event.getPort() == "input" :
            enableds.append(1)
        
        if event.name == "left-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_editing_behaviour_holding_control. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_editing_behaviour_holding_control()
                self.enter_Root_root_main_behaviour_editing_behaviour_idle()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour_editing_behaviour_holding_control()
                send_event = Event("edit_instance", parameters = [self.location])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_editing_behaviour_idle()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_moving_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_moving_behaviour][0] == self.Root_root_main_behaviour_moving_behaviour_unselected:
                catched = self.transition_Root_root_main_behaviour_moving_behaviour_unselected(event)
            elif self.current_state[self.Root_root_main_behaviour_moving_behaviour][0] == self.Root_root_main_behaviour_moving_behaviour_selected:
                catched = self.transition_Root_root_main_behaviour_moving_behaviour_selected(event)
            elif self.current_state[self.Root_root_main_behaviour_moving_behaviour][0] == self.Root_root_main_behaviour_moving_behaviour_moving:
                catched = self.transition_Root_root_main_behaviour_moving_behaviour_moving(event)
        return catched
    
    def transition_Root_root_main_behaviour_moving_behaviour_unselected(self, event) :
        catched = False
        enableds = []
        if event.name == "left-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(1)
        
        if event.name == "highlight" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_moving_behaviour_unselected. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour_moving_behaviour_unselected()
                send_event = Event("instance_pressed", parameters = [self.location,self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_moving_behaviour_unselected()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_moving_behaviour_unselected()
                self.c.itemconfig(self.tagorid, fill="yellow")
                self.enter_Root_root_main_behaviour_moving_behaviour_selected()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_moving_behaviour_selected(self, event) :
        catched = False
        enableds = []
        if event.name == "left-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(1)
        
        if event.name == "unhighlight" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_moving_behaviour_selected. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour_moving_behaviour_selected()
                anchor = (self.c.canvasx(self.last_x), self.c.canvasy(self.last_y))
                coords = self.c.coords(self.tagorid)
                self.diff_w_anchor = (anchor[0] - self.c.canvasx(coords[0]), anchor[1] - self.c.canvasy(coords[1]))
                self.enter_Root_root_main_behaviour_moving_behaviour_moving()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_moving_behaviour_selected()
                self.c.itemconfig(self.tagorid, fill="ghost white")
                self.enter_Root_root_main_behaviour_moving_behaviour_unselected()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_moving_behaviour_moving(self, event) :
        catched = False
        enableds = []
        if event.name == "motion" and event.getPort() == "input" :
            enableds.append(1)
        
        if event.name == "left-release" and event.getPort() == "input" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_moving_behaviour_moving. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour_moving_behaviour_moving()
                coords = self.c.coords(self.tagorid)
                dx = self.c.canvasx(self.last_x) - self.c.canvasx(coords[0]) - self.diff_w_anchor[0]
                dy = self.c.canvasy(self.last_y) - self.c.canvasy(coords[1]) - self.diff_w_anchor[1]
                
                self.c.move(self.tagorid, dx, dy)
                self.c.move(self.text_id, dx, dy)
                send_event = Event("instance_moved", parameters = [self.association_name,dx,dy])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_moving_behaviour_moving()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_main_behaviour_moving_behaviour_moving()
                self.enter_Root_root_main_behaviour_moving_behaviour_selected()
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
    

class ArrowInstance(MvKWidget, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_main_behaviour = 1
    Root_main_behaviour_editing_behaviour = 2
    Root_main_behaviour_canvas_behaviour = 3
    Root_main_behaviour_move_behaviour = 4
    Root_initializing = 5
    Root_main_behaviour_editing_behaviour_idle = 6
    Root_main_behaviour_editing_behaviour_holding_control = 7
    Root_main_behaviour_canvas_behaviour_idle = 8
    Root_main_behaviour_canvas_behaviour_selected = 9
    Root_main_behaviour_move_behaviour_idle = 10
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_main_behaviour] = []
        self.current_state[self.Root_main_behaviour_editing_behaviour] = []
        self.current_state[self.Root_main_behaviour_canvas_behaviour] = []
        self.current_state[self.Root_main_behaviour_move_behaviour] = []
    
    def start(self):
        super(ArrowInstance, self).start()
        self.enter_Root_initializing()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        self.c = constructor_parameters["parent"]
        from_w = constructor_parameters["from_id"]
        to_w = constructor_parameters["to_id"]
        f_coords = self.c.coords(from_w)
        t_coords = self.c.coords(to_w)
        self.tagorid = self.c.create_line(f_coords[0] + 50, f_coords[1] + 30, t_coords[0] + 50, t_coords[1], arrow="last", fill="black")
        self.location = constructor_parameters["location"]
        self.from_instance = constructor_parameters["from_instance"]
        self.to_instance = constructor_parameters["to_instance"]
        MvKWidget.__init__(self, controller, self.c, self.tagorid)
    
    # User defined destructor
    def __del__(self):
        self.c.delete(self.tagorid)
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_main_behaviour(self):
        self.current_state[self.Root].append(self.Root_main_behaviour)
    
    def exit_Root_main_behaviour(self):
        self.exit_Root_main_behaviour_editing_behaviour()
        self.exit_Root_main_behaviour_canvas_behaviour()
        self.exit_Root_main_behaviour_move_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_main_behaviour_editing_behaviour(self):
        self.current_state[self.Root_main_behaviour].append(self.Root_main_behaviour_editing_behaviour)
    
    def exit_Root_main_behaviour_editing_behaviour(self):
        if self.Root_main_behaviour_editing_behaviour_idle in self.current_state[self.Root_main_behaviour_editing_behaviour] :
            self.exit_Root_main_behaviour_editing_behaviour_idle()
        if self.Root_main_behaviour_editing_behaviour_holding_control in self.current_state[self.Root_main_behaviour_editing_behaviour] :
            self.exit_Root_main_behaviour_editing_behaviour_holding_control()
        self.current_state[self.Root_main_behaviour] = []
    
    def enter_Root_main_behaviour_canvas_behaviour(self):
        self.current_state[self.Root_main_behaviour].append(self.Root_main_behaviour_canvas_behaviour)
    
    def exit_Root_main_behaviour_canvas_behaviour(self):
        if self.Root_main_behaviour_canvas_behaviour_idle in self.current_state[self.Root_main_behaviour_canvas_behaviour] :
            self.exit_Root_main_behaviour_canvas_behaviour_idle()
        if self.Root_main_behaviour_canvas_behaviour_selected in self.current_state[self.Root_main_behaviour_canvas_behaviour] :
            self.exit_Root_main_behaviour_canvas_behaviour_selected()
        self.current_state[self.Root_main_behaviour] = []
    
    def enter_Root_main_behaviour_move_behaviour(self):
        self.current_state[self.Root_main_behaviour].append(self.Root_main_behaviour_move_behaviour)
    
    def exit_Root_main_behaviour_move_behaviour(self):
        if self.Root_main_behaviour_move_behaviour_idle in self.current_state[self.Root_main_behaviour_move_behaviour] :
            self.exit_Root_main_behaviour_move_behaviour_idle()
        self.current_state[self.Root_main_behaviour] = []
    
    def enter_Root_initializing(self):
        self.current_state[self.Root].append(self.Root_initializing)
    
    def exit_Root_initializing(self):
        self.current_state[self.Root] = []
    
    def enter_Root_main_behaviour_editing_behaviour_idle(self):
        self.current_state[self.Root_main_behaviour_editing_behaviour].append(self.Root_main_behaviour_editing_behaviour_idle)
    
    def exit_Root_main_behaviour_editing_behaviour_idle(self):
        self.current_state[self.Root_main_behaviour_editing_behaviour] = []
    
    def enter_Root_main_behaviour_editing_behaviour_holding_control(self):
        self.current_state[self.Root_main_behaviour_editing_behaviour].append(self.Root_main_behaviour_editing_behaviour_holding_control)
    
    def exit_Root_main_behaviour_editing_behaviour_holding_control(self):
        self.current_state[self.Root_main_behaviour_editing_behaviour] = []
    
    def enter_Root_main_behaviour_canvas_behaviour_idle(self):
        self.current_state[self.Root_main_behaviour_canvas_behaviour].append(self.Root_main_behaviour_canvas_behaviour_idle)
    
    def exit_Root_main_behaviour_canvas_behaviour_idle(self):
        self.current_state[self.Root_main_behaviour_canvas_behaviour] = []
    
    def enter_Root_main_behaviour_canvas_behaviour_selected(self):
        self.current_state[self.Root_main_behaviour_canvas_behaviour].append(self.Root_main_behaviour_canvas_behaviour_selected)
    
    def exit_Root_main_behaviour_canvas_behaviour_selected(self):
        self.current_state[self.Root_main_behaviour_canvas_behaviour] = []
    
    def enter_Root_main_behaviour_move_behaviour_idle(self):
        self.current_state[self.Root_main_behaviour_move_behaviour].append(self.Root_main_behaviour_move_behaviour_idle)
    
    def exit_Root_main_behaviour_move_behaviour_idle(self):
        self.current_state[self.Root_main_behaviour_move_behaviour] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_main_behaviour(self):
        self.enter_Root_main_behaviour()
        self.enterDefault_Root_main_behaviour_editing_behaviour()
        self.enterDefault_Root_main_behaviour_canvas_behaviour()
        self.enterDefault_Root_main_behaviour_move_behaviour()
    
    def enterDefault_Root_main_behaviour_editing_behaviour(self):
        self.enter_Root_main_behaviour_editing_behaviour()
        self.enter_Root_main_behaviour_editing_behaviour_idle()
    
    def enterDefault_Root_main_behaviour_canvas_behaviour(self):
        self.enter_Root_main_behaviour_canvas_behaviour()
        self.enter_Root_main_behaviour_canvas_behaviour_idle()
    
    def enterDefault_Root_main_behaviour_move_behaviour(self):
        self.enter_Root_main_behaviour_move_behaviour()
        self.enter_Root_main_behaviour_move_behaviour_idle()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_initializing:
                catched = self.transition_Root_initializing(event)
            elif self.current_state[self.Root][0] == self.Root_main_behaviour:
                catched = self.transition_Root_main_behaviour(event)
        return catched
    
    def transition_Root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_initializing()
                self.association_name = association_name
                send_event = Event("mvk_instance_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enterDefault_Root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_main_behaviour(self, event) :
        catched = False
        if not catched :
            catched = self.transition_Root_main_behaviour_editing_behaviour(event) or catched
            catched = self.transition_Root_main_behaviour_canvas_behaviour(event) or catched
            catched = self.transition_Root_main_behaviour_move_behaviour(event) or catched
        return catched
    
    def transition_Root_main_behaviour_editing_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_main_behaviour_editing_behaviour][0] == self.Root_main_behaviour_editing_behaviour_idle:
                catched = self.transition_Root_main_behaviour_editing_behaviour_idle(event)
            elif self.current_state[self.Root_main_behaviour_editing_behaviour][0] == self.Root_main_behaviour_editing_behaviour_holding_control:
                catched = self.transition_Root_main_behaviour_editing_behaviour_holding_control(event)
        return catched
    
    def transition_Root_main_behaviour_editing_behaviour_idle(self, event) :
        catched = False
        enableds = []
        if event.name == "middle-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(1)
        
        if event.name == "control" and event.getPort() == "input" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_behaviour_editing_behaviour_idle. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_main_behaviour_editing_behaviour_idle()
                send_event = Event("edit_instance", parameters = [self.location])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_main_behaviour_editing_behaviour_idle()
            elif enabled == 2 :
                self.exit_Root_main_behaviour_editing_behaviour_idle()
                self.enter_Root_main_behaviour_editing_behaviour_holding_control()
            catched = True
        
        return catched
    
    def transition_Root_main_behaviour_editing_behaviour_holding_control(self, event) :
        catched = False
        enableds = []
        if event.name == "control-release" and event.getPort() == "input" :
            enableds.append(1)
        
        if event.name == "left-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_behaviour_editing_behaviour_holding_control. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_main_behaviour_editing_behaviour_holding_control()
                self.enter_Root_main_behaviour_editing_behaviour_idle()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_main_behaviour_editing_behaviour_holding_control()
                send_event = Event("edit_instance", parameters = [self.location])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_main_behaviour_editing_behaviour_idle()
            catched = True
        
        return catched
    
    def transition_Root_main_behaviour_canvas_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_main_behaviour_canvas_behaviour][0] == self.Root_main_behaviour_canvas_behaviour_idle:
                catched = self.transition_Root_main_behaviour_canvas_behaviour_idle(event)
            elif self.current_state[self.Root_main_behaviour_canvas_behaviour][0] == self.Root_main_behaviour_canvas_behaviour_selected:
                catched = self.transition_Root_main_behaviour_canvas_behaviour_selected(event)
        return catched
    
    def transition_Root_main_behaviour_canvas_behaviour_idle(self, event) :
        catched = False
        enableds = []
        if event.name == "left-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(1)
        
        if event.name == "highlight" and event.getPort() == "" :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_behaviour_canvas_behaviour_idle. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_main_behaviour_canvas_behaviour_idle()
                send_event = Event("instance_pressed", parameters = [self.location,self.association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_main_behaviour_canvas_behaviour_idle()
            elif enabled == 2 :
                self.exit_Root_main_behaviour_canvas_behaviour_idle()
                self.c.itemconfig(self.tagorid, fill="yellow")
                self.enter_Root_main_behaviour_canvas_behaviour_selected()
            catched = True
        
        return catched
    
    def transition_Root_main_behaviour_canvas_behaviour_selected(self, event) :
        catched = False
        enableds = []
        if event.name == "unhighlight" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_behaviour_canvas_behaviour_selected. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_main_behaviour_canvas_behaviour_selected()
                self.c.itemconfig(self.tagorid, fill="black")
                self.enter_Root_main_behaviour_canvas_behaviour_idle()
            catched = True
        
        return catched
    
    def transition_Root_main_behaviour_move_behaviour(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_main_behaviour_move_behaviour][0] == self.Root_main_behaviour_move_behaviour_idle:
                catched = self.transition_Root_main_behaviour_move_behaviour_idle(event)
        return catched
    
    def transition_Root_main_behaviour_move_behaviour_idle(self, event) :
        catched = False
        enableds = []
        if event.name == "move" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_main_behaviour_move_behaviour_idle. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                deltax = parameters[0]
                deltay = parameters[1]
                type = parameters[2]
                self.exit_Root_main_behaviour_move_behaviour_idle()
                coords = self.c.coords(self.tagorid)
                if type == 'from':
                    coords[0] += deltax
                    coords[1] += deltay
                if type == 'to':
                    coords[2] += deltax
                    coords[3] += deltay
                self.c.coords(self.tagorid, *coords)
                self.enter_Root_main_behaviour_move_behaviour_idle()
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
    

class Toolbar(tk.Frame, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_idle = 1
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
    
    def start(self):
        super(Toolbar, self).start()
        self.enter_Root_idle()
    
    #The actual constructor
    def __init__(self, controller, parent, name):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        tk.Frame.__init__(self, parent)
        
        self.config(relief=tk.RAISED, bd=1)
        
        tk.Label(self, text=name).pack(side=tk.TOP, pady=5)
    
    # User defined destructor
    def __del__(self):
        self.destroy()
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_idle(self):
        self.current_state[self.Root].append(self.Root_idle)
    
    def exit_Root_idle(self):
        self.current_state[self.Root] = []
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_idle:
                catched = self.transition_Root_idle(event)
        return catched
    
    def transition_Root_idle(self, event) :
        catched = False
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
    

class MainToolbar(Toolbar, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_main_behaviour = 2
    Root_root_main_behaviour_creating_buttons = 3
    Root_root_main_behaviour_packing_buttons = 4
    Root_root_main_behaviour_listening = 5
    Root_root_main_behaviour_listening_client = 6
    Root_root_initializing = 7
    Root_root_main_behaviour_creating_buttons_loop = 8
    Root_root_main_behaviour_creating_buttons_creating = 9
    Root_root_main_behaviour_creating_buttons_running = 10
    Root_root_main_behaviour_packing_buttons_packing = 11
    Root_root_main_behaviour_listening_listening = 12
    Root_root_main_behaviour_listening_client_listening_client = 13
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_main_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
        self.current_state[self.Root_root_main_behaviour_packing_buttons] = []
        self.current_state[self.Root_root_main_behaviour_listening] = []
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def start(self):
        super(MainToolbar, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        Toolbar.__init__(self, self.controller, constructor_parameters["parent"], 'Main')
        self.PADDING = 2
        self.buttons = [{"parent": self, "visual": ImageVisual('icons/new-icon.png'), "tooltip_text": 'Create New Model', "event_parameters": {"event_name": "create_model"}},
                        {"parent": self, "visual": ImageVisual('icons/load-type-model-icon.png'), "tooltip_text": 'Load a Type Model', "event_parameters": {"event_name": "load_type_model"}},
                        {"parent": self, "visual": ImageVisual('icons/open-icon.png'), "tooltip_text": 'Open a Model', "event_parameters": {"event_name": "load_model"}},
                        {"parent": self, "visual": ImageVisual('icons/save-icon.png'), "tooltip_text": 'Save Modelverse', "event_parameters": {"event_name": "save"}},
                        {"parent": self, "visual": ImageVisual('icons/restore-icon.png'), "tooltip_text": 'Restore Modelverse', "event_parameters": {"event_name": "restore"}},
                        {"parent": self, "visual": ImageVisual('icons/undo-icon.png'), "tooltip_text": 'Undo', "event_parameters": {"event_name": "undo"}},
                        {"parent": self, "visual": ImageVisual('icons/redo-icon.png'), "tooltip_text": 'Redo', "event_parameters": {"event_name": "redo"}},
                        {"parent": self, "visual": ImageVisual('icons/validate-icon.png'), "tooltip_text": 'Validate Model', "event_parameters": {"event_name": "validate"}}]
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.exit_Root_root_main_behaviour_creating_buttons()
        self.exit_Root_root_main_behaviour_packing_buttons()
        self.exit_Root_root_main_behaviour_listening()
        self.exit_Root_root_main_behaviour_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_buttons(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_creating_buttons)
    
    def exit_Root_root_main_behaviour_creating_buttons(self):
        if self.Root_root_main_behaviour_creating_buttons_loop in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_loop()
        if self.Root_root_main_behaviour_creating_buttons_creating in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_creating()
        if self.Root_root_main_behaviour_creating_buttons_running in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_running()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_packing_buttons(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_packing_buttons)
    
    def exit_Root_root_main_behaviour_packing_buttons(self):
        if self.Root_root_main_behaviour_packing_buttons_packing in self.current_state[self.Root_root_main_behaviour_packing_buttons] :
            self.exit_Root_root_main_behaviour_packing_buttons_packing()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening)
    
    def exit_Root_root_main_behaviour_listening(self):
        if self.Root_root_main_behaviour_listening_listening in self.current_state[self.Root_root_main_behaviour_listening] :
            self.exit_Root_root_main_behaviour_listening_listening()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_client(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client(self):
        if self.Root_root_main_behaviour_listening_client_listening_client in self.current_state[self.Root_root_main_behaviour_listening_client] :
            self.exit_Root_root_main_behaviour_listening_client_listening_client()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_loop)
    
    def exit_Root_root_main_behaviour_creating_buttons_loop(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_creating)
    
    def exit_Root_root_main_behaviour_creating_buttons_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_running)
    
    def exit_Root_root_main_behaviour_creating_buttons_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_packing_buttons_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_buttons].append(self.Root_root_main_behaviour_packing_buttons_packing)
    
    def exit_Root_root_main_behaviour_packing_buttons_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_buttons] = []
    
    def enter_Root_root_main_behaviour_listening_listening(self):
        self.current_state[self.Root_root_main_behaviour_listening].append(self.Root_root_main_behaviour_listening_listening)
    
    def exit_Root_root_main_behaviour_listening_listening(self):
        self.current_state[self.Root_root_main_behaviour_listening] = []
    
    def enter_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client].append(self.Root_root_main_behaviour_listening_client_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_main_behaviour(self):
        self.enter_Root_root_main_behaviour()
        self.enterDefault_Root_root_main_behaviour_creating_buttons()
        self.enterDefault_Root_root_main_behaviour_packing_buttons()
        self.enterDefault_Root_root_main_behaviour_listening()
        self.enterDefault_Root_root_main_behaviour_listening_client()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons(self):
        self.enter_Root_root_main_behaviour_creating_buttons()
        self.enter_Root_root_main_behaviour_creating_buttons_loop()
    
    def enterDefault_Root_root_main_behaviour_packing_buttons(self):
        self.enter_Root_root_main_behaviour_packing_buttons()
        self.enter_Root_root_main_behaviour_packing_buttons_packing()
    
    def enterDefault_Root_root_main_behaviour_listening(self):
        self.enter_Root_root_main_behaviour_listening()
        self.enter_Root_root_main_behaviour_listening_listening()
    
    def enterDefault_Root_root_main_behaviour_listening_client(self):
        self.enter_Root_root_main_behaviour_listening_client()
        self.enter_Root_root_main_behaviour_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("toolbar_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enterDefault_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
        if not catched :
            catched = self.transition_Root_root_main_behaviour_creating_buttons(event) or catched
            catched = self.transition_Root_root_main_behaviour_packing_buttons(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening_client(event) or catched
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_loop:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_creating:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_creating(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_running:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_loop(self, event) :
        catched = False
        enableds = []
        if self.buttons :
            enableds.append(1)
        
        if not self.buttons :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_loop()
                ctor_parameters = self.buttons.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "buttons","Button",ctor_parameters]))
                self.enter_Root_root_main_behaviour_creating_buttons_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_loop()
                self.enter_Root_root_main_behaviour_creating_buttons_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running(self, event) :
        catched = False
        return catched
    
    def transition_Root_root_main_behaviour_packing_buttons(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_packing_buttons][0] == self.Root_root_main_behaviour_packing_buttons_packing:
                catched = self.transition_Root_root_main_behaviour_packing_buttons_packing(event)
        return catched
    
    def transition_Root_root_main_behaviour_packing_buttons_packing(self, event) :
        catched = False
        enableds = []
        if event.name == "button_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_packing_buttons_packing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                button = parameters[0]
                self.exit_Root_root_main_behaviour_packing_buttons_packing()
                button.pack(side=tk.LEFT, fill=tk.Y, padx=self.PADDING)
                self.enter_Root_root_main_behaviour_packing_buttons_packing()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening][0] == self.Root_root_main_behaviour_listening_listening:
                catched = self.transition_Root_root_main_behaviour_listening_listening(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_listening(self, event) :
        catched = False
        enableds = []
        if event.name == "button_pressed" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_listening. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_listening_listening()
                send_event = Event("button_pressed", parameters = [event_parameters])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_listening()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening_client][0] == self.Root_root_main_behaviour_listening_client_listening_client:
                catched = self.transition_Root_root_main_behaviour_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_main_behaviour_listening_client_listening_client()
                send_event = Event("client_request", parameters = [self.association_name + '/' + association_name,data])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_client_listening_client()
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
    

class FormalismToolbar(Toolbar, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_main_behaviour = 2
    Root_root_main_behaviour_creating_buttons = 3
    Root_root_main_behaviour_packing_buttons = 4
    Root_root_main_behaviour_listening = 5
    Root_root_main_behaviour_listening_client = 6
    Root_root_initializing = 7
    Root_root_main_behaviour_creating_buttons_reading_formalism = 8
    Root_root_main_behaviour_creating_buttons_waiting_client = 9
    Root_root_main_behaviour_creating_buttons_loop = 10
    Root_root_main_behaviour_creating_buttons_creating = 11
    Root_root_main_behaviour_creating_buttons_running = 12
    Root_root_main_behaviour_packing_buttons_packing = 13
    Root_root_main_behaviour_listening_listening = 14
    Root_root_main_behaviour_listening_client_listening_client = 15
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        self.timers = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
        self.current_state[self.Root_root_main_behaviour] = []
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
        self.current_state[self.Root_root_main_behaviour_packing_buttons] = []
        self.current_state[self.Root_root_main_behaviour_listening] = []
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    def start(self):
        super(FormalismToolbar, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        self.formalism = constructor_parameters["formalism"]
        Toolbar.__init__(self, self.controller, constructor_parameters["parent"], self.formalism.name)
        self.label = tk.Label(self, text="Loading...")
        self.label.pack()
        self.i = 0
        self.buttons = []
        self.PADDING = 2
        self.created_buttons = []
    
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_main_behaviour in self.current_state[self.Root_root] :
            self.exit_Root_root_main_behaviour()
        self.current_state[self.Root] = []
    
    def enter_Root_root_main_behaviour(self):
        self.current_state[self.Root_root].append(self.Root_root_main_behaviour)
    
    def exit_Root_root_main_behaviour(self):
        self.exit_Root_root_main_behaviour_creating_buttons()
        self.exit_Root_root_main_behaviour_packing_buttons()
        self.exit_Root_root_main_behaviour_listening()
        self.exit_Root_root_main_behaviour_listening_client()
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_buttons(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_creating_buttons)
    
    def exit_Root_root_main_behaviour_creating_buttons(self):
        if self.Root_root_main_behaviour_creating_buttons_reading_formalism in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_reading_formalism()
        if self.Root_root_main_behaviour_creating_buttons_waiting_client in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_waiting_client()
        if self.Root_root_main_behaviour_creating_buttons_loop in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_loop()
        if self.Root_root_main_behaviour_creating_buttons_creating in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_creating()
        if self.Root_root_main_behaviour_creating_buttons_running in self.current_state[self.Root_root_main_behaviour_creating_buttons] :
            self.exit_Root_root_main_behaviour_creating_buttons_running()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_packing_buttons(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_packing_buttons)
    
    def exit_Root_root_main_behaviour_packing_buttons(self):
        if self.Root_root_main_behaviour_packing_buttons_packing in self.current_state[self.Root_root_main_behaviour_packing_buttons] :
            self.exit_Root_root_main_behaviour_packing_buttons_packing()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening)
    
    def exit_Root_root_main_behaviour_listening(self):
        if self.Root_root_main_behaviour_listening_listening in self.current_state[self.Root_root_main_behaviour_listening] :
            self.exit_Root_root_main_behaviour_listening_listening()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_main_behaviour_listening_client(self):
        self.current_state[self.Root_root_main_behaviour].append(self.Root_root_main_behaviour_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client(self):
        if self.Root_root_main_behaviour_listening_client_listening_client in self.current_state[self.Root_root_main_behaviour_listening_client] :
            self.exit_Root_root_main_behaviour_listening_client_listening_client()
        self.current_state[self.Root_root_main_behaviour] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_reading_formalism(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_reading_formalism)
    
    def exit_Root_root_main_behaviour_creating_buttons_reading_formalism(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_waiting_client)
    
    def exit_Root_root_main_behaviour_creating_buttons_waiting_client(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_loop(self):
        self.timers[0] = 0.05
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_loop)
    
    def exit_Root_root_main_behaviour_creating_buttons_loop(self):
        self.timers.pop(0, None)
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_creating)
    
    def exit_Root_root_main_behaviour_creating_buttons_creating(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_creating_buttons_running(self):
        self.label.pack_forget()
        for b in self.created_buttons:
            b.pack(side=tk.LEFT, fill=tk.Y, padx=self.PADDING)
        self.current_state[self.Root_root_main_behaviour_creating_buttons].append(self.Root_root_main_behaviour_creating_buttons_running)
    
    def exit_Root_root_main_behaviour_creating_buttons_running(self):
        self.current_state[self.Root_root_main_behaviour_creating_buttons] = []
    
    def enter_Root_root_main_behaviour_packing_buttons_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_buttons].append(self.Root_root_main_behaviour_packing_buttons_packing)
    
    def exit_Root_root_main_behaviour_packing_buttons_packing(self):
        self.current_state[self.Root_root_main_behaviour_packing_buttons] = []
    
    def enter_Root_root_main_behaviour_listening_listening(self):
        self.current_state[self.Root_root_main_behaviour_listening].append(self.Root_root_main_behaviour_listening_listening)
    
    def exit_Root_root_main_behaviour_listening_listening(self):
        self.current_state[self.Root_root_main_behaviour_listening] = []
    
    def enter_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client].append(self.Root_root_main_behaviour_listening_client_listening_client)
    
    def exit_Root_root_main_behaviour_listening_client_listening_client(self):
        self.current_state[self.Root_root_main_behaviour_listening_client] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    def enterDefault_Root_root_main_behaviour(self):
        self.enter_Root_root_main_behaviour()
        self.enterDefault_Root_root_main_behaviour_creating_buttons()
        self.enterDefault_Root_root_main_behaviour_packing_buttons()
        self.enterDefault_Root_root_main_behaviour_listening()
        self.enterDefault_Root_root_main_behaviour_listening_client()
    
    def enterDefault_Root_root_main_behaviour_creating_buttons(self):
        self.enter_Root_root_main_behaviour_creating_buttons()
        self.enter_Root_root_main_behaviour_creating_buttons_reading_formalism()
    
    def enterDefault_Root_root_main_behaviour_packing_buttons(self):
        self.enter_Root_root_main_behaviour_packing_buttons()
        self.enter_Root_root_main_behaviour_packing_buttons_packing()
    
    def enterDefault_Root_root_main_behaviour_listening(self):
        self.enter_Root_root_main_behaviour_listening()
        self.enter_Root_root_main_behaviour_listening_listening()
    
    def enterDefault_Root_root_main_behaviour_listening_client(self):
        self.enter_Root_root_main_behaviour_listening_client()
        self.enter_Root_root_main_behaviour_listening_client_listening_client()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_main_behaviour:
                catched = self.transition_Root_root_main_behaviour(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("toolbar_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enterDefault_Root_root_main_behaviour()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour(self, event) :
        catched = False
        if not catched :
            catched = self.transition_Root_root_main_behaviour_creating_buttons(event) or catched
            catched = self.transition_Root_root_main_behaviour_packing_buttons(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening(event) or catched
            catched = self.transition_Root_root_main_behaviour_listening_client(event) or catched
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_reading_formalism:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_reading_formalism(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_waiting_client:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_waiting_client(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_loop:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_loop(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_creating:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_creating(event)
            elif self.current_state[self.Root_root_main_behaviour_creating_buttons][0] == self.Root_root_main_behaviour_creating_buttons_running:
                catched = self.transition_Root_root_main_behaviour_creating_buttons_running(event)
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_reading_formalism(self, event) :
        catched = False
        enableds = []
        if self.i < len(self.formalism.elements) :
            enableds.append(1)
        
        if self.i == len(self.formalism.elements) :
            enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_reading_formalism. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_reading_formalism()
                send_event = Event("client_request", parameters = [self.association_name,{'event_name': 'read', 'request_parameters': self.formalism.elements[self.i][1]}])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.i += 1
                self.enter_Root_root_main_behaviour_creating_buttons_waiting_client()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_reading_formalism()
                self.enter_Root_root_main_behaviour_creating_buttons_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_waiting_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if response.is_success() :
                enableds.append(1)
        
        if event.name == "client_response" and event.getPort() == "" :
            parameters = event.getParameters()
            response = parameters[0]
            if not response.is_success() :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_waiting_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_waiting_client()
                item = response[StringValue("item")]
                if isinstance(item, client_object.Clabject) and item.potency > IntegerValue(0) and not isinstance(item, client_object.Composition) and not item.abstract:
                    self.buttons.append({"parent": self, "visual": TextVisual(item.name), "tooltip_text": 'Create New %s' % item.name, "event_parameters": {"event_name": "select_type_to_create", "type": item, "type_location": self.formalism.elements[self.i - 1][1]}})
                self.enter_Root_root_main_behaviour_creating_buttons_reading_formalism()
            elif enabled == 2 :
                parameters = event.getParameters()
                response = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_waiting_client()
                self.addEvent(Event("error", parameters = [response.get_status_code(),response.get_status_message()]))
                self.enter_Root_root_main_behaviour_creating_buttons_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_loop(self, event) :
        catched = False
        enableds = []
        if self.buttons :
            enableds.append(1)
        
        if event.name == "_0after" and event.getPort() == "" :
            if not self.buttons :
                enableds.append(2)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_loop. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                self.exit_Root_root_main_behaviour_creating_buttons_loop()
                ctor_parameters = self.buttons.pop(0)
                self.object_manager.addEvent(Event("create_instance", parameters = [self, "buttons","Button",ctor_parameters]))
                self.enter_Root_root_main_behaviour_creating_buttons_creating()
            elif enabled == 2 :
                self.exit_Root_root_main_behaviour_creating_buttons_loop()
                self.enter_Root_root_main_behaviour_creating_buttons_running()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_creating(self, event) :
        catched = False
        enableds = []
        if event.name == "instance_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_creating_buttons_creating. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_main_behaviour_creating_buttons_creating()
                self.object_manager.addEvent(Event("start_instance", parameters = [self, association_name]))
                send_event = Event("set_association_name", parameters = [association_name])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, association_name , send_event]))
                self.enter_Root_root_main_behaviour_creating_buttons_loop()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_creating_buttons_running(self, event) :
        catched = False
        return catched
    
    def transition_Root_root_main_behaviour_packing_buttons(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_packing_buttons][0] == self.Root_root_main_behaviour_packing_buttons_packing:
                catched = self.transition_Root_root_main_behaviour_packing_buttons_packing(event)
        return catched
    
    def transition_Root_root_main_behaviour_packing_buttons_packing(self, event) :
        catched = False
        enableds = []
        if event.name == "button_created" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_packing_buttons_packing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                button = parameters[0]
                self.exit_Root_root_main_behaviour_packing_buttons_packing()
                self.created_buttons.append(button)
                self.enter_Root_root_main_behaviour_packing_buttons_packing()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening][0] == self.Root_root_main_behaviour_listening_listening:
                catched = self.transition_Root_root_main_behaviour_listening_listening(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_listening(self, event) :
        catched = False
        enableds = []
        if event.name == "button_pressed" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_listening. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                event_parameters = parameters[0]
                self.exit_Root_root_main_behaviour_listening_listening()
                send_event = Event("button_pressed", parameters = [event_parameters])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_listening()
            catched = True
        
        return catched
    
    def transition_Root_root_main_behaviour_listening_client(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root_main_behaviour_listening_client][0] == self.Root_root_main_behaviour_listening_client_listening_client:
                catched = self.transition_Root_root_main_behaviour_listening_client_listening_client(event)
        return catched
    
    def transition_Root_root_main_behaviour_listening_client_listening_client(self, event) :
        catched = False
        enableds = []
        if event.name == "client_request" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_main_behaviour_listening_client_listening_client. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                data = parameters[1]
                self.exit_Root_root_main_behaviour_listening_client_listening_client()
                send_event = Event("client_request", parameters = [self.association_name + '/' + association_name,data])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_main_behaviour_listening_client_listening_client()
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
    

class Button(MvKWidget, tk.Button, RuntimeClassBase):
    
    # Unique IDs for all statechart nodes
    Root = 0
    Root_root = 1
    Root_root_initializing = 2
    Root_root_running = 3
    
    def commonConstructor(self, controller = None):
        """Constructor part that is common for all constructors."""
        RuntimeClassBase.__init__(self)
        
        # User defined input ports
        self.inports = {}
        self.controller = controller
        self.object_manager = controller.getObjectManager()
        self.current_state = {}
        self.history_state = {}
        
        #Initialize statechart :
        
        self.current_state[self.Root] = []
        self.current_state[self.Root_root] = []
    
    def start(self):
        super(Button, self).start()
        self.enterDefault_Root_root()
    
    #The actual constructor
    def __init__(self, controller, constructor_parameters = {}):
        self.commonConstructor(controller)
        
        #constructor body (user-defined)
        tk.Button.__init__(self, constructor_parameters["parent"], **(constructor_parameters["visual"].get_params()))
        MvKWidget.__init__(self, self.controller)
        self.event_parameters = constructor_parameters["event_parameters"]
        self.tooltip = ToolTip(self, constructor_parameters["tooltip_text"])
        self.visual = constructor_parameters["visual"]
    
    # User defined destructor
    def __del__(self):
        self.destroy()
        
    # Statechart enter/exit action method(s) :
    
    def enter_Root_root(self):
        self.current_state[self.Root].append(self.Root_root)
    
    def exit_Root_root(self):
        if self.Root_root_initializing in self.current_state[self.Root_root] :
            self.exit_Root_root_initializing()
        if self.Root_root_running in self.current_state[self.Root_root] :
            self.exit_Root_root_running()
        self.current_state[self.Root] = []
    
    def enter_Root_root_initializing(self):
        self.current_state[self.Root_root].append(self.Root_root_initializing)
    
    def exit_Root_root_initializing(self):
        self.current_state[self.Root_root] = []
    
    def enter_Root_root_running(self):
        self.current_state[self.Root_root].append(self.Root_root_running)
    
    def exit_Root_root_running(self):
        self.current_state[self.Root_root] = []
    
    #Statechart enter/exit default method(s) :
    
    def enterDefault_Root_root(self):
        self.enter_Root_root()
        self.enter_Root_root_initializing()
    
    #Statechart transitions :
    
    def transition_Root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root][0] == self.Root_root:
                catched = self.transition_Root_root(event)
        return catched
    
    def transition_Root_root(self, event) :
        catched = False
        if not catched :
            if self.current_state[self.Root_root][0] == self.Root_root_initializing:
                catched = self.transition_Root_root_initializing(event)
            elif self.current_state[self.Root_root][0] == self.Root_root_running:
                catched = self.transition_Root_root_running(event)
        return catched
    
    def transition_Root_root_initializing(self, event) :
        catched = False
        enableds = []
        if event.name == "set_association_name" and event.getPort() == "" :
            enableds.append(1)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_initializing. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                association_name = parameters[0]
                self.exit_Root_root_initializing()
                self.association_name = association_name
                send_event = Event("button_created", parameters = [self])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running()
            catched = True
        
        return catched
    
    def transition_Root_root_running(self, event) :
        catched = False
        enableds = []
        if event.name == "left-click" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(1)
        
        if event.name == "enter" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(2)
        
        if event.name == "leave" and event.getPort() == "input" :
            parameters = event.getParameters()
            tagorid = parameters[0]
            if tagorid == id(self) :
                enableds.append(3)
        
        if len(enableds) > 1 :
            print "Runtime warning : indeterminism detected in a transition from node Root_root_running. Only the first in document order enabled transition is executed."
        
        if len(enableds) > 0 :
            enabled = enableds[0]
            if enabled == 1 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_running()
                send_event = Event("button_pressed", parameters = [self.event_parameters])
                self.object_manager.addEvent(Event("narrow_cast", parameters = [self, 'parent' , send_event]))
                self.enter_Root_root_running()
            elif enabled == 2 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_running()
                self.tooltip.showtip()
                self.enter_Root_root_running()
            elif enabled == 3 :
                parameters = event.getParameters()
                tagorid = parameters[0]
                self.exit_Root_root_running()
                self.tooltip.hidetip()
                self.enter_Root_root_running()
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
        if class_name == "MvKFrontend" :
            instance =  MvKFrontend(self.controller, *construct_params)
            associations.append(Association("windows", "Window", 0, -1))
            associations.append(Association("client", "MvKClient", 1, 1))
        elif class_name == "MvKClient" :
            instance =  MvKClient(self.controller, *construct_params)
            associations.append(Association("parent", "MainApp", 1, 1))
        elif class_name == "Window" :
            instance =  Window(self.controller, *construct_params)
        elif class_name == "NewInstanceAttributeEditor" :
            instance =  NewInstanceAttributeEditor(self.controller, *construct_params)
            associations.append(Association("widgets", "MvKWidget", 0, -1))
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "InstanceAttributeEditor" :
            instance =  InstanceAttributeEditor(self.controller, *construct_params)
            associations.append(Association("widgets", "MvKWidgets", 0, -1))
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "InputWindow" :
            instance =  InputWindow(self.controller, *construct_params)
            associations.append(Association("widgets", "MvKWidgets", 0, -1))
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "Editor" :
            instance =  Editor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "EntryEditor" :
            instance =  EntryEditor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "AnyEditor" :
            instance =  AnyEditor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "BooleanEditor" :
            instance =  BooleanEditor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "EnumEditor" :
            instance =  EnumEditor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "FloatEditor" :
            instance =  FloatEditor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "IntInfEditor" :
            instance =  IntInfEditor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "IntegerEditor" :
            instance =  IntegerEditor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "LocationEditor" :
            instance =  LocationEditor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "StringEditor" :
            instance =  StringEditor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "TypeEditor" :
            instance =  TypeEditor(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "CompositionEditor" :
            instance =  CompositionEditor(self.controller, *construct_params)
            associations.append(Association("buttons", "Button", 0, -1))
            associations.append(Association("labels", "Label", 0, -1))
            associations.append(Association("windows", "Window", 0, -1))
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "SelectionWindow" :
            instance =  SelectionWindow(self.controller, *construct_params)
            associations.append(Association("buttons", "Button", 0, -1))
            associations.append(Association("labels", "Label", 0, -1))
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "PopupMessage" :
            instance =  PopupMessage(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "TypeModelBrowser" :
            instance =  TypeModelBrowser(self.controller, *construct_params)
            associations.append(Association("buttons", "Button", 0, -1))
            associations.append(Association("labels", "Label", 0, -1))
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "ModelBrowser" :
            instance =  ModelBrowser(self.controller, *construct_params)
            associations.append(Association("buttons", "Button", 0, -1))
            associations.append(Association("labels", "Label", 0, -1))
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "ModelEditor" :
            instance =  ModelEditor(self.controller, *construct_params)
            associations.append(Association("toolbars", "Toolbar", 0, -1))
            associations.append(Association("log_messages", "LogMessage", 0, -1))
            associations.append(Association("windows", "Window", 0, -1))
            associations.append(Association("canvas_elements", "MvKWidget", 0, -1))
            associations.append(Association("parent", "MvKFrontEnd", 1, 1))
        elif class_name == "Label" :
            instance =  Label(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "LogMessage" :
            instance =  LogMessage(self.controller, *construct_params)
            associations.append(Association("widgets", "MvKWidget", 0, -1))
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "Instance" :
            instance =  Instance(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "ArrowInstance" :
            instance =  ArrowInstance(self.controller, *construct_params)
            associations.append(Association("parent", "Window", 1, 1))
        elif class_name == "Toolbar" :
            instance =  Toolbar(self.controller, *construct_params)
            associations.append(Association("buttons", "Button", 0, -1))
        elif class_name == "MainToolbar" :
            instance =  MainToolbar(self.controller, *construct_params)
            associations.append(Association("buttons", "Button", 0, -1))
            associations.append(Association("parent", "Window", 0, -1))
        elif class_name == "FormalismToolbar" :
            instance =  FormalismToolbar(self.controller, *construct_params)
            associations.append(Association("buttons", "Button", 0, -1))
            associations.append(Association("parent", "Window", 0, -1))
        elif class_name == "Button" :
            instance =  Button(self.controller, *construct_params)
            associations.append(Association("parent", "Toolbar", 1, 1))
        if instance:
            return InstanceWrapper(instance, associations)
        else :
            return None

from python_runtime.statecharts_core import GameLoopControllerBase
class Controller(GameLoopControllerBase):
    def __init__(self, keep_running = True):
        super(Controller, self).__init__(ObjectManager(self), keep_running)
        self.addInputPort("input")
        self.object_manager.createInstance("MvKFrontend", [])
        
def main():
    controller = Controller()
    controller.start()

if __name__ == "__main__":
    main()
