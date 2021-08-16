/**
 * Statechart compiler by Glenn De Jonghe
 * Javascript generator by Joeri Exelmans
 * 
 * Date:   Sun Mar  1 19:53:12 2015
 * 
 * Model author: Daniel Riegelhaupt
 * Model name:   editor_behaviour
 * Model description:
    Describes the behaviour of a SVG text editor. 
		This particular version concentrates on editing concrete syntax based on a given grammar and metamodel.
		Please note that as this was originally written for SCXML alone this might not use the SCCD formalisme in the best or most optimal way and instead just 
		translates from one to the other with minimal changes.
 */

// put everything in an object (serves as "namespace")
editor_behaviour = {};

// closure scope
(function() {

// The actual constructor
var Main = function(controller) {
    // Unique IDs for all statechart nodes
    this.Root = 0;
    this.Root_root = 1;
    this.Root_root_main = 2;
    this.Root_root_deletion = 3;
    this.Root_root_main_running = 4;
    this.Root_root_main_waiting = 5;
    this.Root_root_deletion_default = 6;
    
    this.commonConstructor(controller);
    
    // constructor body (user-defined)
    this.editorList = []
};


Main.prototype = new RuntimeClassBase();

// Statechart enter/exit action method(s) :

Main.prototype.enter_Root_root = function() {
    this.current_state[this.Root].push(this.Root_root);
};

Main.prototype.exit_Root_root = function() {
    this.exit_Root_root_main();
    this.exit_Root_root_deletion();
    this.current_state[this.Root] = new Array();
};

Main.prototype.enter_Root_root_main = function() {
    this.current_state[this.Root_root].push(this.Root_root_main);
};

Main.prototype.exit_Root_root_main = function() {
    if (this.current_state[this.Root_root_main].indexOf(this.Root_root_main_running) !== -1) {
        this.exit_Root_root_main_running();
    }
    if (this.current_state[this.Root_root_main].indexOf(this.Root_root_main_waiting) !== -1) {
        this.exit_Root_root_main_waiting();
    }
    this.current_state[this.Root_root] = new Array();
};

Main.prototype.enter_Root_root_deletion = function() {
    this.current_state[this.Root_root].push(this.Root_root_deletion);
};

Main.prototype.exit_Root_root_deletion = function() {
    if (this.current_state[this.Root_root_deletion].indexOf(this.Root_root_deletion_default) !== -1) {
        this.exit_Root_root_deletion_default();
    }
    this.current_state[this.Root_root] = new Array();
};

Main.prototype.enter_Root_root_main_running = function() {
    this.current_state[this.Root_root_main].push(this.Root_root_main_running);
};

Main.prototype.exit_Root_root_main_running = function() {
    this.current_state[this.Root_root_main] = new Array();
};

Main.prototype.enter_Root_root_main_waiting = function() {
    this.current_state[this.Root_root_main].push(this.Root_root_main_waiting);
};

Main.prototype.exit_Root_root_main_waiting = function() {
    this.current_state[this.Root_root_main] = new Array();
};

Main.prototype.enter_Root_root_deletion_default = function() {
    this.current_state[this.Root_root_deletion].push(this.Root_root_deletion_default);
};

Main.prototype.exit_Root_root_deletion_default = function() {
    this.current_state[this.Root_root_deletion] = new Array();
};

// Statechart enter/exit default method(s) :

Main.prototype.enterDefault_Root_root = function() {
    this.enter_Root_root();
    this.enterDefault_Root_root_main();
    this.enterDefault_Root_root_deletion();
};

Main.prototype.enterDefault_Root_root_main = function() {
    this.enter_Root_root_main();
    this.enter_Root_root_main_running();
};

Main.prototype.enterDefault_Root_root_deletion = function() {
    this.enter_Root_root_deletion();
    this.enter_Root_root_deletion_default();
};

// Statechart transitions :

Main.prototype.transition_Root = function(event) {
    var catched = false;
    if (!catched) {
        if (this.current_state[this.Root][0] === this.Root_root) {
            catched = this.transition_Root_root(event);
        }
    }
    return catched;
};

Main.prototype.transition_Root_root = function(event) {
    var catched = false;
    if (!catched) {
        catched = this.transition_Root_root_main(event) || catched
        catched = this.transition_Root_root_deletion(event) || catched
    }
    return catched;
};

Main.prototype.transition_Root_root_main = function(event) {
    var catched = false;
    if (!catched) {
        if (this.current_state[this.Root_root_main][0] === this.Root_root_main_running) {
            catched = this.transition_Root_root_main_running(event);
        }
        else if (this.current_state[this.Root_root_main][0] === this.Root_root_main_waiting) {
            catched = this.transition_Root_root_main_waiting(event);
        }
    }
    return catched;
};

Main.prototype.transition_Root_root_main_running = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "create_editors_from_list") {
        enableds.push(1);
    }
    
    if (event.name === "try_creating") {
        if (this.editorList.length > 0) {
            enableds.push(2);
        }
    }
    
    if (event.name === "create_editor") {
        enableds.push(3);
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_root_main_running. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var list = parameters[0];
            this.exit_Root_root_main_running();
            this.editorList = list;
            console.log("got list:", this.editorList)
            this.addEvent(new Event("try_creating", null, []));
            this.enter_Root_root_main_running();
        }
        else if (enabled === 2) {
            this.exit_Root_root_main_running();
            var curData = this.editorList.shift();
            console.log("will create editor:", curData.editor.getId());
            this.addEvent(new Event("create_editor", null, [curData]));
            this.enter_Root_root_main_running();
        }
        else if (enabled === 3) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_root_main_running();
            this.object_manager.addEvent(new Event("create_instance", null, [this, "EditorAssoc",data]));
            this.enter_Root_root_main_waiting();
        }
        catched = true;
    }
    
    return catched;
};

Main.prototype.transition_Root_root_main_waiting = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "instance_created") {
        enableds.push(1);
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_root_main_waiting. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var association_name = parameters[0];
            this.exit_Root_root_main_waiting();
            this.object_manager.addEvent(new Event("start_instance", null, [this, association_name]));
            var send_event = new Event("set_association_name", null, [association_name]);
            this.object_manager.addEvent(new Event("narrow_cast", null, [this, association_name , send_event]));
            this.addEvent(new Event("try_creating", null, []));
            this.enter_Root_root_main_running();
        }
        catched = true;
    }
    
    return catched;
};

Main.prototype.transition_Root_root_deletion = function(event) {
    var catched = false;
    if (!catched) {
        if (this.current_state[this.Root_root_deletion][0] === this.Root_root_deletion_default) {
            catched = this.transition_Root_root_deletion_default(event);
        }
    }
    return catched;
};

Main.prototype.transition_Root_root_deletion_default = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "close_editor") {
        enableds.push(1);
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_root_deletion_default. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var association_name = parameters[0];
            this.exit_Root_root_deletion_default();
            this.object_manager.addEvent(new Event("delete_instance", null, [this, association_name]));
            this.enter_Root_root_deletion_default();
        }
        catched = true;
    }
    
    return catched;
};

// Execute transitions
Main.prototype.transition = function(event) {
    if (!event) event = new Event();
    this.state_changed = this.transition_Root(event);
};

// inState method for statechart
Main.prototype.inState = function(nodes) {
    for (var c in this.current_state) {
        if (!this.current_state.hasOwnProperty(c)) continue;
        var new_nodes = new Array();
        for (var n in nodes) {
            if (!nodes.hasOwnProperty(n)) continue;
            if (this.current_state[c].indexOf(nodes[n]) === -1) {
                new_nodes.push(nodes[n]);
            }
        }
        nodes = new_nodes;
        if (nodes.length === 0) {
            return true;
        }
    }
    return false;
};

Main.prototype.commonConstructor = function(controller) {
    if (!controller) controller = null;
    // Constructor part that is common for all constructors.
    RuntimeClassBase.call(this);
    this.controller = controller;
    this.object_manager = controller.object_manager;
    this.current_state = new Object();
    this.history_state = new Object();
    
    // Initialize statechart
    this.current_state[this.Root] = new Array();
    this.current_state[this.Root_root] = new Array();
    this.current_state[this.Root_root_main] = new Array();
    this.current_state[this.Root_root_deletion] = new Array();
};

Main.prototype.start = function() {
    RuntimeClassBase.prototype.start.call(this);
    this.enterDefault_Root_root();
};

// put class in global diagram object
editor_behaviour.Main = Main;

// The actual constructor
var Editor = function(controller, data) {
    // Unique IDs for all statechart nodes
    this.Root = 0;
    this.Root_client = 1;
    this.Root_editor_main = 2;
    this.Root_editor_main_typing_mode_state = 3;
    this.Root_editor_main_editor_modes_parent = 4;
    this.Root_initial_default = 5;
    this.Root_wait = 6;
    this.Root_client_default = 7;
    this.Root_client_load_grammar = 8;
    this.Root_client_check_text = 9;
    this.Root_client_auto_complete = 10;
    this.Root_client_client_save = 11;
    this.Root_client_client_quit = 12;
    this.Root_editor_main_typing_mode_state_insert_mode = 13;
    this.Root_editor_main_typing_mode_state_overtype_mode = 14;
    this.Root_editor_main_editor_modes_parent_editor_mode = 15;
    this.Root_editor_main_editor_modes_parent_mouse = 16;
    this.Root_editor_main_editor_modes_parent_selection = 17;
    this.Root_editor_main_editor_modes_parent_auto_complete = 18;
    this.Root_exit_state = 19;
    
    this.commonConstructor(controller);
    
    // constructor body (user-defined)
    console.log("creating instance for: ", data.editor.getId());
    this.editor = data.editor;
    this.ID = this.editor.getId();
    this.styleToolbar = data.styleToolbar;
    this.grammarToolbar = data.grammarToolbar;
    this.cursor = this.editor.getCursor();
    this.display = this.editor.getDisplayManager();
    this.loader = data.loader;
    this.errorBar = data.errorBar;
    this.autoCompleteMenu = data.autoComplete;
    
    this.moved = false; 
    this.mouseDownCursorPos = null;
    this.ajaxRequest = null;
    this.highlight = null;
    
    //create a scInstace wrapper for this specific Editor instace
    
    this.controller.addInputPort(this.ID) //needed to make sure that there will not be a crahs because the port has not been defined				
    this.scInstance = new StateChartWrapper(this.controller, this.ID);
    
    this.editor.setStateChart(this.scInstance);
    this.autoCompleteMenu.setStateChart(this.scInstance);
    this.loader.setStateChart(this.scInstance);
    
    //set the state chart in every aspect!
    if (this.styleToolbar != null){
    	this.styleToolbar.setStateChart(this.scInstance);
    }
    if (this.grammarToolbar != null){
    	this.grammarToolbar.setStateChart(this.scInstance);
    }
    
    this.client = new Client(this.scInstance, this.ID);
    this.editor.init()
    console.log("editor:", this.ID , "has been created");
    this.repeat = 0
};


Editor.prototype = new RuntimeClassBase();

// Statechart enter/exit action method(s) :

Editor.prototype.enter_Root_client = function() {
    this.timers[0] = 300000;
    this.current_state[this.Root].push(this.Root_client);
};

Editor.prototype.exit_Root_client = function() {
    if (this.current_state[this.Root_client].indexOf(this.Root_client_default) !== -1) {
        this.exit_Root_client_default();
    }
    if (this.current_state[this.Root_client].indexOf(this.Root_client_load_grammar) !== -1) {
        this.exit_Root_client_load_grammar();
    }
    if (this.current_state[this.Root_client].indexOf(this.Root_client_check_text) !== -1) {
        this.exit_Root_client_check_text();
    }
    if (this.current_state[this.Root_client].indexOf(this.Root_client_auto_complete) !== -1) {
        this.exit_Root_client_auto_complete();
    }
    if (this.current_state[this.Root_client].indexOf(this.Root_client_client_save) !== -1) {
        this.exit_Root_client_client_save();
    }
    if (this.current_state[this.Root_client].indexOf(this.Root_client_client_quit) !== -1) {
        this.exit_Root_client_client_quit();
    }
    delete this.timers[0];
    this.current_state[this.Root] = new Array();
};

Editor.prototype.enter_Root_editor_main = function() {
    this.current_state[this.Root].push(this.Root_editor_main);
};

Editor.prototype.exit_Root_editor_main = function() {
    this.exit_Root_editor_main_typing_mode_state();
    this.exit_Root_editor_main_editor_modes_parent();
    this.current_state[this.Root] = new Array();
};

Editor.prototype.enter_Root_editor_main_typing_mode_state = function() {
    this.current_state[this.Root_editor_main].push(this.Root_editor_main_typing_mode_state);
};

Editor.prototype.exit_Root_editor_main_typing_mode_state = function() {
    if (this.current_state[this.Root_editor_main_typing_mode_state].indexOf(this.Root_editor_main_typing_mode_state_insert_mode) !== -1) {
        this.exit_Root_editor_main_typing_mode_state_insert_mode();
    }
    if (this.current_state[this.Root_editor_main_typing_mode_state].indexOf(this.Root_editor_main_typing_mode_state_overtype_mode) !== -1) {
        this.exit_Root_editor_main_typing_mode_state_overtype_mode();
    }
    this.current_state[this.Root_editor_main] = new Array();
};

Editor.prototype.enter_Root_editor_main_editor_modes_parent = function() {
    this.current_state[this.Root_editor_main].push(this.Root_editor_main_editor_modes_parent);
};

Editor.prototype.exit_Root_editor_main_editor_modes_parent = function() {
    if (this.current_state[this.Root_editor_main_editor_modes_parent].indexOf(this.Root_editor_main_editor_modes_parent_editor_mode) !== -1) {
        this.exit_Root_editor_main_editor_modes_parent_editor_mode();
    }
    if (this.current_state[this.Root_editor_main_editor_modes_parent].indexOf(this.Root_editor_main_editor_modes_parent_mouse) !== -1) {
        this.exit_Root_editor_main_editor_modes_parent_mouse();
    }
    if (this.current_state[this.Root_editor_main_editor_modes_parent].indexOf(this.Root_editor_main_editor_modes_parent_selection) !== -1) {
        this.exit_Root_editor_main_editor_modes_parent_selection();
    }
    if (this.current_state[this.Root_editor_main_editor_modes_parent].indexOf(this.Root_editor_main_editor_modes_parent_auto_complete) !== -1) {
        this.exit_Root_editor_main_editor_modes_parent_auto_complete();
    }
    this.current_state[this.Root_editor_main] = new Array();
};

Editor.prototype.enter_Root_initial_default = function() {
    this.current_state[this.Root].push(this.Root_initial_default);
};

Editor.prototype.exit_Root_initial_default = function() {
    this.current_state[this.Root] = new Array();
};

Editor.prototype.enter_Root_wait = function() {
    console.log(this.ID, "is in wait state")
    this.current_state[this.Root].push(this.Root_wait);
};

Editor.prototype.exit_Root_wait = function() {
    this.current_state[this.Root] = new Array();
};

Editor.prototype.enter_Root_client_default = function() {
    this.current_state[this.Root_client].push(this.Root_client_default);
};

Editor.prototype.exit_Root_client_default = function() {
    this.current_state[this.Root_client] = new Array();
};

Editor.prototype.enter_Root_client_load_grammar = function() {
    this.current_state[this.Root_client].push(this.Root_client_load_grammar);
};

Editor.prototype.exit_Root_client_load_grammar = function() {
    this.current_state[this.Root_client] = new Array();
};

Editor.prototype.enter_Root_client_check_text = function() {
    this.current_state[this.Root_client].push(this.Root_client_check_text);
};

Editor.prototype.exit_Root_client_check_text = function() {
    this.current_state[this.Root_client] = new Array();
};

Editor.prototype.enter_Root_client_auto_complete = function() {
    this.current_state[this.Root_client].push(this.Root_client_auto_complete);
};

Editor.prototype.exit_Root_client_auto_complete = function() {
    this.current_state[this.Root_client] = new Array();
};

Editor.prototype.enter_Root_client_client_save = function() {
    this.current_state[this.Root_client].push(this.Root_client_client_save);
};

Editor.prototype.exit_Root_client_client_save = function() {
    this.current_state[this.Root_client] = new Array();
};

Editor.prototype.enter_Root_client_client_quit = function() {
    this.current_state[this.Root_client].push(this.Root_client_client_quit);
};

Editor.prototype.exit_Root_client_client_quit = function() {
    this.current_state[this.Root_client] = new Array();
};

Editor.prototype.enter_Root_editor_main_typing_mode_state_insert_mode = function() {
    this.current_state[this.Root_editor_main_typing_mode_state].push(this.Root_editor_main_typing_mode_state_insert_mode);
};

Editor.prototype.exit_Root_editor_main_typing_mode_state_insert_mode = function() {
    this.current_state[this.Root_editor_main_typing_mode_state] = new Array();
};

Editor.prototype.enter_Root_editor_main_typing_mode_state_overtype_mode = function() {
    this.current_state[this.Root_editor_main_typing_mode_state].push(this.Root_editor_main_typing_mode_state_overtype_mode);
};

Editor.prototype.exit_Root_editor_main_typing_mode_state_overtype_mode = function() {
    this.current_state[this.Root_editor_main_typing_mode_state] = new Array();
};

Editor.prototype.enter_Root_editor_main_editor_modes_parent_editor_mode = function() {
    this.current_state[this.Root_editor_main_editor_modes_parent].push(this.Root_editor_main_editor_modes_parent_editor_mode);
};

Editor.prototype.exit_Root_editor_main_editor_modes_parent_editor_mode = function() {
    this.current_state[this.Root_editor_main_editor_modes_parent] = new Array();
};

Editor.prototype.enter_Root_editor_main_editor_modes_parent_mouse = function() {
    this.current_state[this.Root_editor_main_editor_modes_parent].push(this.Root_editor_main_editor_modes_parent_mouse);
};

Editor.prototype.exit_Root_editor_main_editor_modes_parent_mouse = function() {
    this.moved = false;
    this.current_state[this.Root_editor_main_editor_modes_parent] = new Array();
};

Editor.prototype.enter_Root_editor_main_editor_modes_parent_selection = function() {
    this.current_state[this.Root_editor_main_editor_modes_parent].push(this.Root_editor_main_editor_modes_parent_selection);
};

Editor.prototype.exit_Root_editor_main_editor_modes_parent_selection = function() {
    this.current_state[this.Root_editor_main_editor_modes_parent] = new Array();
};

Editor.prototype.enter_Root_editor_main_editor_modes_parent_auto_complete = function() {
    this.current_state[this.Root_editor_main_editor_modes_parent].push(this.Root_editor_main_editor_modes_parent_auto_complete);
};

Editor.prototype.exit_Root_editor_main_editor_modes_parent_auto_complete = function() {
    this.current_state[this.Root_editor_main_editor_modes_parent] = new Array();
};

Editor.prototype.enter_Root_exit_state = function() {
    console.log("closing editor");
    //todo clear editor, remove from DOM if possible ad remove association
    //window.close(); //mutiple editors we do not want to close the current tab anymore (besides firefox never allowed it)
    this.current_state[this.Root].push(this.Root_exit_state);
};

Editor.prototype.exit_Root_exit_state = function() {
    this.current_state[this.Root] = new Array();
};

// Statechart enter/exit default method(s) :

Editor.prototype.enterDefault_Root_client = function() {
    this.enter_Root_client();
    this.enter_Root_client_default();
};

Editor.prototype.enterDefault_Root_editor_main = function() {
    this.enter_Root_editor_main();
    this.enterDefault_Root_editor_main_typing_mode_state();
    this.enterDefault_Root_editor_main_editor_modes_parent();
};

Editor.prototype.enterDefault_Root_editor_main_typing_mode_state = function() {
    this.enter_Root_editor_main_typing_mode_state();
    this.enter_Root_editor_main_typing_mode_state_insert_mode();
};

Editor.prototype.enterDefault_Root_editor_main_editor_modes_parent = function() {
    this.enter_Root_editor_main_editor_modes_parent();
    this.enter_Root_editor_main_editor_modes_parent_editor_mode();
};

// Statechart transitions :

Editor.prototype.transition_Root = function(event) {
    var catched = false;
    if (!catched) {
        if (this.current_state[this.Root][0] === this.Root_initial_default) {
            catched = this.transition_Root_initial_default(event);
        }
        else if (this.current_state[this.Root][0] === this.Root_wait) {
            catched = this.transition_Root_wait(event);
        }
        else if (this.current_state[this.Root][0] === this.Root_client) {
            catched = this.transition_Root_client(event);
        }
        else if (this.current_state[this.Root][0] === this.Root_editor_main) {
            catched = this.transition_Root_editor_main(event);
        }
        else if (this.current_state[this.Root][0] === this.Root_exit_state) {
            catched = this.transition_Root_exit_state(event);
        }
    }
    return catched;
};

Editor.prototype.transition_Root_initial_default = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "set_association_name") {
        enableds.push(1);
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_initial_default. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var association_name = parameters[0];
            this.exit_Root_initial_default();
            this.association_name = association_name;						
            this.enter_Root_wait();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_wait = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "load_grammar_request_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(1);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_wait. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_wait();
            //console.log("Editor", this.ID, "reacting to load grammar event")
            this.ajaxRequest =  this.client.loadGrammar(data.grammar, data.metamap ,data.styledef, data.stylemap);
            this.enter_Root_client();
            this.enter_Root_client_load_grammar();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_client = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "_0after") {
        enableds.push(1);
    }
    
    if (event.name === "abort_ajax_request_event") {
        if (event.port == this.ID) {
            enableds.push(2);
        }
    }
    
    if (event.name === "time_out_event") {
        if (event.port == this.ID) {
            enableds.push(3);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'ctrl_q_keypress' && this.inState([this.Root_client_client_quit]) == false) {
            enableds.push(4);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_client. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            this.exit_Root_client();
            //this.scInstance.gen("time_out_event", [], this.ID);
            this.addEvent(new Event("time_out_event", this.ID,[]));
            this.enterDefault_Root_client();
        }
        else if (enabled === 2) {
            this.exit_Root_client();
            console.log('aborting due to user event');
            if (this.ajaxRequest != null){
            	this.ajaxRequest.abort();
            }
            this.ajaxRequest = null;
            console.log("The current request has been aborted by the user");
            this.enterDefault_Root_editor_main();
        }
        else if (enabled === 3) {
            this.exit_Root_client();
            console.log('aborting due to timout');	
            if (this.ajaxRequest != null){
            	this.ajaxRequest.abort();
            }
            this.ajaxRequest = null;
            console.warning("the current request timed out");
            this.enterDefault_Root_editor_main();
        }
        else if (enabled === 4) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_client();
            this.editor.close()
            this.enter_Root_client();
            this.enter_Root_client_client_quit();
        }
        catched = true;
    }
    
    if (!catched) {
        if (this.current_state[this.Root_client][0] === this.Root_client_default) {
            catched = this.transition_Root_client_default(event);
        }
        else if (this.current_state[this.Root_client][0] === this.Root_client_load_grammar) {
            catched = this.transition_Root_client_load_grammar(event);
        }
        else if (this.current_state[this.Root_client][0] === this.Root_client_check_text) {
            catched = this.transition_Root_client_check_text(event);
        }
        else if (this.current_state[this.Root_client][0] === this.Root_client_auto_complete) {
            catched = this.transition_Root_client_auto_complete(event);
        }
        else if (this.current_state[this.Root_client][0] === this.Root_client_client_save) {
            catched = this.transition_Root_client_client_save(event);
        }
        else if (this.current_state[this.Root_client][0] === this.Root_client_client_quit) {
            catched = this.transition_Root_client_client_quit(event);
        }
    }
    return catched;
};

Editor.prototype.transition_Root_client_default = function(event) {
    var catched = false;
    return catched;
};

Editor.prototype.transition_Root_client_load_grammar = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "load_grammar_succes") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(1);
        }
    }
    
    if (event.name === "load_grammar_fail") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(2);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_client_load_grammar. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_client();
            console.log(this.ID, "grammar loaded")
            var defaultStyle = new Style(data.defaultStyleStr, data.errorStyleStr);
            this.editor.changeStyle(defaultStyle);	
            
            this.highlight= new HighlightMgr(this.editor, defaultStyle); 
            this.highlight.setErrorBar(this.errorBar);
            //this.editor.setHighlighter(this.highlight); //this is done to hightlight text on load. //not needed now that checkError is done after load
            //TODO send text to server instead: for the moment there are problems with concurency and stuff
            var name, st, list;
            for (var s in data.keywords){
            	name = s;
            	st = defaultStyle.copyDeep();//each highlight style starts from default 
            	st.fromNormalString(data.keywords[s].style);//and we change the difference
            	list = data.keywords[s].values;
            	//console.log("SET KEYWORDS: ", name, list, st);
            	this.highlight.addKeywordList(name, list, st);
            } 
            this.ajaxRequest = null;
            console.log("Finished loading grammar you may type now")
            this.enterDefault_Root_editor_main();
        }
        else if (enabled === 2) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_client();
            this.ajaxRequest = null;
            var error = data.error
            console.log(error)
            alert(error)
            this.enter_Root_wait();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_client_check_text = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "check_text_succes") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(1);
        }
    }
    
    if (event.name === "check_text_fail") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(2);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_client_check_text. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_client();
            //defintion of a function to adapt Coords from server coordintaes to editor coordinates
            function adaptCoord(line,column){
            	//server coorindates are human readable: as in first ine and char index starts with 1 not 0
            	//this method adjust it. this does not take into account any more editor specifc things
            	var coord = { row :- 1, col :- 1 }
            	coord.row = (line > 0)? line -1 : 0;
            	coord.col = (column > 0) ? column -1 : 0; 
            	if (column == 0){
            		coord.row = (coord.row > 0)? coord.row -1 : 0;// col 0 means last char of previous row
            		coord.col = this.cursor.getLineManager().getLine(coord.row).getTextLength()-1;//last char of prev line
            	} 
            	return coord;
            }
            
            this.highlight.resetHighlights()
            
            var styles = data.styles;
            if (styles.length > 0){
            	var st, fromPos, toPos;
            	for (var i in styles){
            		st = styles[i]
            		fromPos = adaptCoord(st.startpos.line, st.startpos.column)
            		toPos = adaptCoord(st.endpos.line, st.endpos.column)
            
            		this.highlight.applyStyle(st.style, fromPos, toPos);
            	}
            }
            
            var errors = data.errors
            if (errors.length > 0){
            	//error_position.startpos , error_position.endpos (optional)
            	var err, fromPos; 
            	var toPos = null;
            	for (var i in errors){
            		err = errors[i]
            		fromPos = adaptCoord(err.error_position.startpos.line, err.error_position.startpos.column)
            		if (err.error_position.endpos)
            		toPos = adaptCoord(err.error_position.endpos.line, err.error_position.endpos.column)
            
            		this.highlight.applyError(err.error, fromPos, toPos);
            	}
            }
            //after the changing of stylewe resetthe style to write to 
            var defStyle = this.highlight.getDefaultStyle();
            this.editor.changeStyle(defStyle);
            this.ajaxRequest = null;
            this.enterDefault_Root_editor_main();
        }
        else if (enabled === 2) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_client();
            this.ajaxRequest = null;
            var error = data.error
            console.log(error)
            alert(error)
            this.enterDefault_Root_editor_main();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_client_auto_complete = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.port == this.ID && this.ajaxRequest == null) {
        enableds.push(1);
    }
    
    if (event.name === "auto_complete_succes") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID && data.suggestions.length > 0) {
            enableds.push(2);
        }
    }
    
    if (event.name === "auto_complete_succes") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID && data.suggestions.length == 0) {
            enableds.push(3);
        }
    }
    
    if (event.name === "auto_complete_syntax_error") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(4);
        }
    }
    
    if (event.name === "auto_complete_fail") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(5);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_client_auto_complete. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            this.exit_Root_client();
            this.enterDefault_Root_editor_main();
        }
        else if (enabled === 2) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_client();
            xyPos = this.cursor.getXYCoords()
            
            //calculate current word at cursor position
            var coords1 = this.cursor.getCoords();
            var coords2 = this.cursor.getCoords();//move the cursur one pos to the left
            coords2.col -= 1;
            
            var word1Dic = this.editor.getWordInformationAtCoord(coords1); 
            //wil give the word to the right of the cursor or null if lb tab or ws
            var word2Dic = this.editor.getWordInformationAtCoord(coords2); 
            //will give the word to the right of cursor.col- 1 = to the left of current cursor
            //this is usefull if curosr is drectly after a word
            var startText = ""
            
            //TODO word is calculated using white sapce, tab or newline. we need to cut at 
            //symbols given to us by a grammar or mapping (such as a dot or a comma or an arrow symbol)
            if (word1Dic.word != null){ 
            	startText = word1Dic.word.getTextContent();
            }else if (word2Dic.word != null){
            	startText = word2Dic.word.getTextContent();
            }
            //if both of them arent null its is the same word (cursor is inside a word)
            
            
            this.autoCompleteMenu.createMenu(data.suggestions, xyPos, startText)
            this.ajaxRequest = null;
            
            //this.scInstance.gen("to_autocomplete_mode", [], this.ID);
            this.addEvent(new Event("to_autocomplete_mode", this.ID,[]));
            this.enterDefault_Root_editor_main();
        }
        else if (enabled === 3) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_client();
            this.ajaxRequest = null;
            this.enterDefault_Root_editor_main();
        }
        else if (enabled === 4) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_client();
            //defintion of a function to adapt Coords from server coordintaes to editor coordinates
            function adaptCoord(line,column){
            	//server coorindates are human readable: as in first ine and char index starts with 1 not 0
            	//this method adjust it. this does not take into account any more editor specifc things
            	var coord = { row :- 1, col :- 1 }
            	coord.row = (line > 0)? line -1 : 0;
            	coord.col = (column > 0) ? column -1 : 0; 
            	if (column == 0){
            		coord.row = (coord.row > 0)? coord.row -1 : 0;// col 0 means last char of previous row
            		coord.col = this.cursor.getLineManager().getLine(coord.row).getTextLength()-1;//last char of prev line
            	} 
            	return coord;
            }
            this.highlight.resetHighlights()
            
            //autocomplete doesnt return styles for the moment
            
            var errors = data.errors
            if (errors.length > 0){
            	//error_position.startpos , error_position.endpos (optional)
            	var err, fromPos; 
            	var toPos = null;
            	for (var i in errors){
            		err = errors[i]
            		fromPos = adaptCoord(err.error_position.startpos.line, err.error_position.startpos.column)
            		if (err.error_position.endpos)
            		toPos = adaptCoord(err.error_position.endpos.line, err.error_position.endpos.column)
            
            		this.highlight.applyError(err.error, fromPos, toPos);
            	}
            }
            //after the changing of style we reset the style to write to 
            var defStyle = this.highlight.getDefaultStyle();
            this.editor.changeStyle(defStyle);
            this.ajaxRequest = null;
            this.enterDefault_Root_editor_main();
        }
        else if (enabled === 5) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_client();
            this.ajaxRequest = null;
            var error = data.error
            console.log(error)
            alert(error)
            this.enterDefault_Root_editor_main();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_client_client_save = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "save_succes") {
        if (event.port == this.ID) {
            enableds.push(1);
        }
    }
    
    if (event.name === "save_fail") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(2);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_client_client_save. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            this.exit_Root_client();
            this.ajaxRequest = null;
            this.enterDefault_Root_editor_main();
        }
        else if (enabled === 2) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_client();
            this.ajaxRequest = null;
            var error = data.error
            console.log(error)
            alert(error)
            this.enterDefault_Root_editor_main();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_client_client_quit = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "quit_succes") {
        if (event.port == this.ID) {
            enableds.push(1);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_client_client_quit. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            this.exit_Root_client();
            this.ajaxRequest = null;
            this.enter_Root_exit_state();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_editor_main = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'ctrl_q_keypress') {
            enableds.push(1);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_editor_main. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main();
            this.editor.close()
            this.enter_Root_client();
            this.enter_Root_client_client_quit();
        }
        catched = true;
    }
    
    if (!catched) {
        catched = this.transition_Root_editor_main_typing_mode_state(event) || catched
        catched = this.transition_Root_editor_main_editor_modes_parent(event) || catched
    }
    return catched;
};

Editor.prototype.transition_Root_editor_main_typing_mode_state = function(event) {
    var catched = false;
    if (!catched) {
        if (this.current_state[this.Root_editor_main_typing_mode_state][0] === this.Root_editor_main_typing_mode_state_insert_mode) {
            catched = this.transition_Root_editor_main_typing_mode_state_insert_mode(event);
        }
        else if (this.current_state[this.Root_editor_main_typing_mode_state][0] === this.Root_editor_main_typing_mode_state_overtype_mode) {
            catched = this.transition_Root_editor_main_typing_mode_state_overtype_mode(event);
        }
    }
    return catched;
};

Editor.prototype.transition_Root_editor_main_typing_mode_state_insert_mode = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && ((data != null)  && (data.char) && (data.name.search(/ctrl/) == -1)) && this.inState([this.Root_editor_main_editor_modes_parent_editor_mode])) {
            enableds.push(1);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'insert_keypress') {
            enableds.push(2);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_editor_main_typing_mode_state_insert_mode. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_typing_mode_state_insert_mode();
            //logger.addEntry(data.char, true);
            this.editor.writeChar(data.char);
            this.cursor.moveRight();
            this.cursor.changeSize();
            this.highlight.checkKeywordsOnType(data.char);
            
            //this.display.updateWidthAndHeight();
            //this.display.updateViewPort(this.cursor);
            this.enter_Root_editor_main_typing_mode_state_insert_mode();
        }
        else if (enabled === 2) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_typing_mode_state_insert_mode();
            //logger.addEntry("INSERT");
            this.cursor.makeFat();
            this.enter_Root_editor_main_typing_mode_state_overtype_mode();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_editor_main_typing_mode_state_overtype_mode = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && ((data != null)  && (data.char) && (data.name.search(/ctrl/) == -1)) && this.inState([this.Root_editor_main_editor_modes_parent_editor_mode])) {
            enableds.push(1);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'insert_keypress') {
            enableds.push(2);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_editor_main_typing_mode_state_overtype_mode. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_typing_mode_state_overtype_mode();
            //logger.addEntry(data.char , true) 
            this.editor.overWriteChar(data.char);
            this.cursor.moveRight();
            this.cursor.changeSize();
            this.highlight.checkKeywordsOnType(data.char);
            this.enter_Root_editor_main_typing_mode_state_overtype_mode();
        }
        else if (enabled === 2) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_typing_mode_state_overtype_mode();
            //logger.addEntry("INSERT");
            this.cursor.makeThin();
            this.enter_Root_editor_main_typing_mode_state_insert_mode();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_editor_main_editor_modes_parent = function(event) {
    var catched = false;
    if (!catched) {
        if (this.current_state[this.Root_editor_main_editor_modes_parent][0] === this.Root_editor_main_editor_modes_parent_editor_mode) {
            catched = this.transition_Root_editor_main_editor_modes_parent_editor_mode(event);
        }
        else if (this.current_state[this.Root_editor_main_editor_modes_parent][0] === this.Root_editor_main_editor_modes_parent_mouse) {
            catched = this.transition_Root_editor_main_editor_modes_parent_mouse(event);
        }
        else if (this.current_state[this.Root_editor_main_editor_modes_parent][0] === this.Root_editor_main_editor_modes_parent_selection) {
            catched = this.transition_Root_editor_main_editor_modes_parent_selection(event);
        }
        else if (this.current_state[this.Root_editor_main_editor_modes_parent][0] === this.Root_editor_main_editor_modes_parent_auto_complete) {
            catched = this.transition_Root_editor_main_editor_modes_parent_auto_complete(event);
        }
    }
    return catched;
};

Editor.prototype.transition_Root_editor_main_editor_modes_parent_editor_mode = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "to_autocomplete_mode") {
        if (event.port == this.ID) {
            enableds.push(1);
        }
    }
    
    if (event.name === "gui_style_change") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(2);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'ctrl_e_keypress') {
            enableds.push(3);
        }
    }
    
    if (event.name === "to_client_check_text") {
        var parameters = event.parameters;
        
        var text = parameters[0];
        if (event.port == this.ID) {
            enableds.push(4);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'ctrl_ _keypress') {
            enableds.push(5);
        }
    }
    
    if (event.name === "to_client_auto_complete") {
        var parameters = event.parameters;
        
        var text = parameters[0];
        if (event.port == this.ID) {
            enableds.push(6);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'right_keypress') {
            enableds.push(7);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'left_keypress') {
            enableds.push(8);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'up_keypress') {
            enableds.push(9);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'down_keypress') {
            enableds.push(10);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'enter_keypress') {
            enableds.push(11);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'backspace_keypress') {
            enableds.push(12);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'delete_keypress') {
            enableds.push(13);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'ctrl_m_keypress') {
            enableds.push(14);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'ctrl_s_keypress') {
            enableds.push(15);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'ctrl_t_keypress') {
            enableds.push(16);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'ctrl_o_keypress') {
            enableds.push(17);
        }
    }
    
    if (event.name === "load_text_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(18);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'ctrl_a_keypress' && this.editor.selectAll()) {
            enableds.push(19);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'ctrl_v_keypress') {
            enableds.push(20);
        }
    }
    
    if (event.name === "left_mouse_down") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(21);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_editor_main_editor_modes_parent_editor_mode. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            this.enter_Root_editor_main_editor_modes_parent_auto_complete();
        }
        else if (enabled === 2) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            //console.log("Change style event");
            //this.editor.changeStyle(data.style);
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 3) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            var text = this.editor.getCurrentText();
            text = text.slice(0,-1); 
            
            /*we do not parse the last default LB as it is not realy part of the text but only of the 
            editor, also if we do it will cause problems down the line because changing the style or adding an error means temporaly cutting the text. and cutting the last character is not allowed.*/
            if (text.length > 0){
            	this.addEvent(new Event("to_client_check_text", this.ID,[text]));
            	//this.editor.getStateChart().gen("to_client_check_text", text, this.ID); this will not work bizarly enough but the above will
            }else{
            	console.log("Text check request denied: Will not check an empty text")
            }
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 4) {
            var parameters = event.parameters;
            
            var text = parameters[0];
            this.exit_Root_editor_main();
            this.ajaxRequest =  this.client.checkText(text);
            this.enter_Root_client();
            this.enter_Root_client_check_text();
        }
        else if (enabled === 5) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            var text = this.editor.getCurrentText();
            text = text.slice(0,-1); 
            /*we do not parse the last default LB as it is not realy part of the text but only of the 
            editor, also if we do it will cause problems down the line because changing the style or adding an error means temporaly cutting the text. and cutting the last character is not allowed.*/
            
            if (text.length > 0){
            	this.addEvent(new Event("to_client_auto_complete", this.ID,[text]));
            	//this.scInstance.gen("to_client_auto_complete", text, this.ID); for some resaon this does not work you must you line above
            }else{
            	console.log("Autocomplete request denied: Will not check an empty text")
            }
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 6) {
            var parameters = event.parameters;
            
            var text = parameters[0];
            this.exit_Root_editor_main();
            var coords = this.cursor.getCoords();
            var pos = {line: coords.row, column: coords.col}
            this.ajaxRequest =  this.client.autoComplete(text, pos);
            this.enter_Root_client();
            this.enter_Root_client_auto_complete();
        }
        else if (enabled === 7) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            //logger.addEntry("RIGHT");
            this.cursor.moveRight();
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 8) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            //logger.addEntry("LEFT");
            this.cursor.moveLeft();
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 9) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            //logger.addEntry("UP");
            this.cursor.moveUp();
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            
            //this.display.updateWidthAndHeight();
            //this.display.updateViewPort(this.cursor);
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 10) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            //logger.addEntry("DOWN");
            this.cursor.moveDown();
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            
            //this.display.updateWidthAndHeight();
            //this.display.updateViewPort(this.cursor);
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 11) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            //logger.addEntry("ENTER");
            this.editor.writeLineBreak();
            this.cursor.moveRight();
            this.highlight.checkKeywordsOnLB();
            
            //this.display.updateWidthAndHeight();
            //this.display.updateViewPort(this.cursor);
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 12) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            //logger.addEntry("BACK SPACE");
            var coord = this.cursor.getCoords();
            if (coord.row != 0 || coord.col != 0){
            	this.cursor.moveLeft();
            	this.editor.removeChar();
            	//this.editor.changeStyle();
            	if (this.styleToolbar != null){
            		this.styleToolbar.updateGUI(this.cursor.getStyle());
            	}
            	this.highlight.checkKeywordsOnRemove();
            
            	//this.display.updateWidthAndHeight();
            	//this.display.updateViewPort(this.cursor);
            }
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 13) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            //logger.addEntry("DELETE");
            this.editor.removeChar();
            this.highlight.checkKeywordsOnRemove();
            
            //this.display.updateWidthAndHeight();
            //this.display.updateViewPort(this.cursor);
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 14) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main();
            //logger.addEntry("ctrl + m");
            this.ajaxRequest = this.editor.saveAsRTF();
            this.enter_Root_client();
            this.enter_Root_client_client_save();
        }
        else if (enabled === 15) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main();
            //logger.addEntry("ctrl + s");
            this.ajaxRequest = this.editor.saveAsSVG();
            this.enter_Root_client();
            this.enter_Root_client_client_save();
        }
        else if (enabled === 16) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main();
            //logger.addEntry("ctrl + t");
            this.ajaxRequest = this.editor.saveAsTXT();
            this.enter_Root_client();
            this.enter_Root_client_client_save();
        }
        else if (enabled === 17) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            this.loader.click();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 18) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            this.ajaxRequest = null;
            this.editor.clear();
            this.errorBar.clearErrors();
            this.editor.load(data.file_name, data.file_content);
            //this.scInstance.gen("keypress_event", {name:'ctrl_e_keypress'}, this.ID);
            this.addEvent(new Event("keypress_event", this.ID,[{name:'ctrl_e_keypress'}]));
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 19) {
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            this.cursor.hide();
            this.enter_Root_editor_main_editor_modes_parent_selection();
        }
        else if (enabled === 20) {
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            //logger.addEntry("ctrl + v");
            this.editor.paste();
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.cursor.show();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 21) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_editor_mode();
            this.cursor.hide();
            this.mouseDownCursorPos = data;
            //console.log(" LEFT MOUSE DOWN from EDITOR to MOUSE, pos =data")
            this.enter_Root_editor_main_editor_modes_parent_mouse();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_editor_main_editor_modes_parent_mouse = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "left_mouse_up") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && this.moved == false) {
            enableds.push(1);
        }
    }
    
    if (event.name === "mouse_move") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(2);
        }
    }
    
    if (event.name === "left_mouse_up") {
        if (event.port == this.ID  && this.moved == true) {
            enableds.push(3);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_editor_main_editor_modes_parent_mouse. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_mouse();
            //logger.addEntry(String("mouse up at x = " + data.X + "  y = " +  data.Y ));
            this.cursor.moveToScreenCoords(data.X , data.Y);
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.cursor.show();
            this.mouseDownCursorPos = null;
            //console.log(" LEFT MOUSE UP (MOVED FALSE) from MOUSE to EDITOR, pos =null")
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 2) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_mouse();
            this.moved = this.editor.select(this.mouseDownCursorPos.X, this.mouseDownCursorPos.Y, data.X, data.Y)
            //console.log(" MOUSE MOVE from MOUSE to MOUSE")
            this.enter_Root_editor_main_editor_modes_parent_mouse();
        }
        else if (enabled === 3) {
            this.exit_Root_editor_main_editor_modes_parent_mouse();
            this.mouseDownCursorPos = null;
            var select = this.editor.getSelectionMgr();
            var pos = select.getSelectionEndClickPos();
            var bool = (select.getSelectionStart() == pos);
            
            this.cursor.moveToRowCol(pos.row, pos.col);
            var style = this.cursor.getStyle(bool); //if pos == start we want to pick the style at the right side of the position
            //this.editor.changeStyle(style);
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(style);
            }
            //console.log(" LEFT MOUSE UP (MOVED TRUE)from MOUSE to SELECTION, pos =null")
            this.enter_Root_editor_main_editor_modes_parent_selection();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_editor_main_editor_modes_parent_selection = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'enter_keypress') {
            enableds.push(1);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'backspace_keypress') {
            enableds.push(2);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && data.name == 'delete_keypress') {
            enableds.push(3);
        }
    }
    
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && ((data != null)  && (data.char) && (data.name.search(/ctrl/) == -1))) {
            enableds.push(4);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'ctrl_c_keypress') {
            enableds.push(5);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'ctrl_x_keypress') {
            enableds.push(6);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'ctrl_v_keypress') {
            enableds.push(7);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'ctrl_a_keypress') {
            enableds.push(8);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'right_keypress') {
            enableds.push(9);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'left_keypress') {
            enableds.push(10);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'up_keypress') {
            enableds.push(11);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'down_keypress') {
            enableds.push(12);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'ctrl_m_keypress') {
            enableds.push(13);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'ctrl_s_keypress') {
            enableds.push(14);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'ctrl_t_keypress') {
            enableds.push(15);
        }
    }
    
    if (event.name === "keypress_event") {
        if (event.port == this.ID  && data.name == 'ctrl_o_keypress') {
            enableds.push(16);
        }
    }
    
    if (event.name === "load_text_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(17);
        }
    }
    
    if (event.name === "left_mouse_down") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(18);
        }
    }
    
    if (event.name === "gui_style_change") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(19);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_editor_main_editor_modes_parent_selection. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry("ENTER");
            this.editor.removeSelection();
            this.editor.writeLineBreak();
            
            this.editor.deselect();
            this.cursor.show();
            this.highlight.checkKeywordsOnLB();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 2) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry("BACK SPACE");
            this.editor.removeSelection();
            
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.editor.deselect();
            this.cursor.show();
            this.highlight.checkKeywordsOnRemove();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 3) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry("DELETE");
            this.editor.removeSelection();
            
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.editor.deselect();
            this.cursor.show();
            this.highlight.checkKeywordsOnRemove();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 4) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry(data.char, true);
            this.editor.removeSelection();
            this.editor.writeChar(data.char);
            
            this.editor.deselect();
            this.cursor.moveRight();
            this.cursor.show();
            
            this.highlight.checkKeywordsOnType(data.char);
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 5) {
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry("ctrl + c");
            this.editor.copySelection();
            this.enter_Root_editor_main_editor_modes_parent_selection();
        }
        else if (enabled === 6) {
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry("ctrl + x");
            this.editor.cutSelection();
            
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.editor.deselect();
            this.cursor.show();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 7) {
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry("ctrl + v");
            this.editor.removeSelection();
            this.editor.deselect();
            this.editor.paste();
            
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.cursor.show();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 8) {
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //we remove the selection that was already there
            this.editor.deselect();
            //and now select all
            this.editor.selectAll();
            
            this.cursor.moveToRowCol(0,0);
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.enter_Root_editor_main_editor_modes_parent_selection();
        }
        else if (enabled === 9) {
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry("RIGHT");
            this.cursor.moveRight();
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.editor.deselect();
            this.cursor.show();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 10) {
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry("LEFT");
            this.cursor.moveLeft();
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.editor.deselect();
            this.cursor.show();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 11) {
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry("UP");
            this.cursor.moveUp();
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.editor.deselect();
            this.cursor.show();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 12) {
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry("DOWN");
            this.cursor.moveDown();
            //this.editor.changeStyle();
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(this.cursor.getStyle());
            }
            this.editor.deselect();
            this.cursor.show();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 13) {
            this.exit_Root_editor_main();
            //logger.addEntry("ctrl + m");
            this.ajaxRequest = this.editor.saveAsRTF();
            this.enter_Root_client();
            this.enter_Root_client_client_save();
        }
        else if (enabled === 14) {
            this.exit_Root_editor_main();
            //logger.addEntry("ctrl + s");
            this.ajaxRequest = this.editor.saveAsSVG();
            this.enter_Root_client();
            this.enter_Root_client_client_save();
        }
        else if (enabled === 15) {
            this.exit_Root_editor_main();
            //logger.addEntry("ctrl + t");
            this.ajaxRequest = this.editor.saveAsTXT();
            this.enter_Root_client();
            this.enter_Root_client_client_save();
        }
        else if (enabled === 16) {
            this.exit_Root_editor_main_editor_modes_parent_selection();
            this.loader.click();
            this.enter_Root_editor_main_editor_modes_parent_selection();
        }
        else if (enabled === 17) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_selection();
            this.editor.clear();
            this.errorBar.clearErrors();
            this.editor.load(data.text);
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 18) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //logger.addEntry(String("mouse down at x = " + data.X + "	y = " +	 data.Y ));
            this.editor.deselect();
            this.mouseDownCursorPos = data;
            console.log(" LEFT MOUSE DOWN from SELECTION to MOUSE: pos = data")
            this.enter_Root_editor_main_editor_modes_parent_mouse();
        }
        else if (enabled === 19) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_selection();
            //console.log("got style change event");
            this.editor.changeSelectionStyle(data.style, data.attr);
            
            var select = this.editor.getSelectionMgr();
            var pos = select.getSelectionEndClickPos();
            var bool = (select.getSelectionStart() == pos);
            
            this.cursor.moveToRowCol(pos.row, pos.col);
            var style = this.cursor.getStyle(bool); //if pos == start we want to pick the style at the right side of the position
            //this.editor.changeStyle(style);
            if (this.styleToolbar != null){
            	this.styleToolbar.updateGUI(style);
            }
            //console.log(" GUI STYLE CHANGE from SELECTION to SELECTION")
            this.enter_Root_editor_main_editor_modes_parent_selection();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_editor_main_editor_modes_parent_auto_complete = function(event) {
    var catched = false;
    var enableds = new Array();
    if (event.name === "keypress_event") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID  && ((data != null)  && (data.name) && (data.name == 'escape_keypress'))) {
            enableds.push(1);
        }
    }
    
    if (event.name === "auto_complete_exit_empty") {
        if (event.port == this.ID) {
            enableds.push(2);
        }
    }
    
    if (event.name === "auto_complete_exit_value") {
        var parameters = event.parameters;
        
        var data = parameters[0];
        if (event.port == this.ID) {
            enableds.push(3);
        }
    }
    
    if (enableds.length > 1) {
        console.log("Runtime warning : indeterminism detected in a transition from node Root_editor_main_editor_modes_parent_auto_complete. Only the first in document order enabled transition is executed.")
    }
    
    if (enableds.length > 0) {
        var enabled = enableds[0];
        if (enabled === 1) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_auto_complete();
            this.addEvent(new Event("auto_complete_exit_empty", this.ID,[]));
            this.enter_Root_editor_main_editor_modes_parent_auto_complete();
        }
        else if (enabled === 2) {
            this.exit_Root_editor_main_editor_modes_parent_auto_complete();
            this.autoCompleteMenu.removeMenu();
            this.editor.focus();
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        else if (enabled === 3) {
            var parameters = event.parameters;
            
            var data = parameters[0];
            this.exit_Root_editor_main_editor_modes_parent_auto_complete();
            this.autoCompleteMenu.removeMenu();
            var text = data.value
            for (i in text){
            	this.editor.writeChar(text[i]);
            	this.cursor.moveRight();
            }
            
            
            this.cursor.changeSize();
            this.highlight.checkKeywordsOnType(text[text.length-1]);
            this.editor.focus();
            
            //this.display.updateWidthAndHeight();
            //this.display.updateViewPort(this.cursor);
            this.enter_Root_editor_main_editor_modes_parent_editor_mode();
        }
        catched = true;
    }
    
    return catched;
};

Editor.prototype.transition_Root_exit_state = function(event) {
    var catched = false;
    return catched;
};

// Execute transitions
Editor.prototype.transition = function(event) {
    if (!event) event = new Event();
    this.state_changed = this.transition_Root(event);
};

// inState method for statechart
Editor.prototype.inState = function(nodes) {
    for (var c in this.current_state) {
        if (!this.current_state.hasOwnProperty(c)) continue;
        var new_nodes = new Array();
        for (var n in nodes) {
            if (!nodes.hasOwnProperty(n)) continue;
            if (this.current_state[c].indexOf(nodes[n]) === -1) {
                new_nodes.push(nodes[n]);
            }
        }
        nodes = new_nodes;
        if (nodes.length === 0) {
            return true;
        }
    }
    return false;
};

Editor.prototype.commonConstructor = function(controller) {
    if (!controller) controller = null;
    // Constructor part that is common for all constructors.
    RuntimeClassBase.call(this);
    this.controller = controller;
    this.object_manager = controller.object_manager;
    this.current_state = new Object();
    this.history_state = new Object();
    this.timers = new Object();
    
    // Initialize statechart
    this.current_state[this.Root] = new Array();
    this.current_state[this.Root_client] = new Array();
    this.current_state[this.Root_editor_main] = new Array();
    this.current_state[this.Root_editor_main_typing_mode_state] = new Array();
    this.current_state[this.Root_editor_main_editor_modes_parent] = new Array();
};

Editor.prototype.start = function() {
    RuntimeClassBase.prototype.start.call(this);
    this.enter_Root_initial_default();
};

// put class in global diagram object
editor_behaviour.Editor = Editor;

var ObjectManager = function(controller) {
    ObjectManagerBase.call(this, controller);
};

ObjectManager.prototype = new ObjectManagerBase();

ObjectManager.prototype.instantiate = function(class_name, construct_params) {
    if (class_name === "Main") {
        var instance = new Main(this.controller);
        instance.associations = new Object();
        instance.associations["EditorAssoc"] = new Association("Editor", 0, -1);
    } else if (class_name === "Editor") {
        var instance = new Editor(this.controller, construct_params[0]);
        instance.associations = new Object();
    }
    return instance;
};

// put in global diagram object
editor_behaviour.ObjectManager = ObjectManager;

var Controller = function(keep_running, finished_callback) {
    if (keep_running === undefined) keep_running = true;
    JsEventLoopControllerBase.call(this, new ObjectManager(this), keep_running, finished_callback);
    this.addInputPort("in");
    this.object_manager.createInstance("Main", []);
};

Controller.prototype = new JsEventLoopControllerBase();

// put in global diagram object
editor_behaviour.Controller = Controller;

})();
