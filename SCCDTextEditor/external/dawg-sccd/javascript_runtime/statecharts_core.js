// Exception
function RuntimeException(msg) {
	this.msg = msg;
}

// InputException
function InputException(msg) {
	RuntimeException.call(this, msg);
}

InputException.prototype = new RuntimeException();

// AssociationException
function AssociationException(msg) {
	RuntimeException.call(this, msg);
}

AssociationException.prototype = new RuntimeException();

// AssociationReferenceException
function AssociationReferenceException(msg) {
	RuntimeException.call(this, msg);
}

AssociationReferenceException.prototype = new RuntimeException();

// ParameterException
function ParameterException(msg) {
	RuntimeException.call(this, msg);
}

ParameterException.prototype = new RuntimeException();

// InputException
function InputException(msg) {
	RuntimeException.call(this, msg);
}

InputException.prototype = new RuntimeException();

// EventQueueEntry
function EventQueueEntry(event, time_offset) {
	this.event = event;
	this.time_offset = time_offset;
}

EventQueueEntry.prototype.decreaseTime = function(offset) {
	this.time_offset -= offset;
};

// EventQueue
function EventQueue() {
	this.event_list = new Array();
}

EventQueue.prototype.add = function(event, time_offset) {
	var entry = new EventQueueEntry(event, time_offset);
	var insert_index = 0;
	var index = this.event_list.length - 1;
	while (index >= 0) {
		if (this.event_list[index].time_offset <= time_offset) {
			insert_index = index + 1;
			break;
		}
		index -= 1;
	}
	this.event_list.splice(insert_index, 0, entry);
};

EventQueue.prototype.decreaseTime = function(offset) {
	for (var event in this.event_list) {
		if (!this.event_list.hasOwnProperty(event)) continue;
		this.event_list[event].decreaseTime(offset);
	}
};

EventQueue.prototype.isEmpty = function() {
	return this.event_list.length === 0;
};

EventQueue.prototype.getEarliestTime = function() {
	if (this.isEmpty()) {
		return Infinity;
	} else {
		return this.event_list[0].time_offset;
	}
};

EventQueue.prototype.popDueEvents = function() {
	if (this.isEmpty() || this.event_list[0].time_offset > 0.0) {
		return new Array();
	}
	var index = 0;
	while (index < this.event_list.length &&
			this.event_list[index].time_offset <= 0.0)
	{
		index++;
	}
	return this.event_list.splice(0, index);
};

// Association
function Association(to_class, min_card, max_card) {
	this.to_class = to_class;
	this.min_card = min_card;
	this.max_card = max_card;
	this.instances = new Array();
}

Association.prototype.allowedToAdd = function() {
	return (this.max_card === -1 || this.instances.length < this.max_card);
};

Association.prototype.addInstance = function(instance) {
	if (this.allowedToAdd()) {
		this.instances.push(instance);
		return this.instances.length-1;
	} else {
		throw new AssociationException("Not allowed to add the instance to the association.");
	}
};

Association.prototype.getInstance = function(index) {
	if (index >= this.instances.length) {
		throw new AssociationException("Invalid index for fetching instance(s) from association.");
	}
	return this.instances[index];
};

// ObjectManagerBase
function ObjectManagerBase(controller) {
	this.controller = controller;
	this.events = new EventQueue();
	this.instances = new Array();
}

ObjectManagerBase.prototype.addEvent = function(event, time_offset) {
	if (!time_offset) time_offset = 0.0;
	this.events.add(event, time_offset);
};

ObjectManagerBase.prototype.broadcast = function(new_event) {
	for (var i in this.instances) {
		if (!this.instances.hasOwnProperty(i)) continue;
		this.instances[i].addEvent(new_event);
	}
};

ObjectManagerBase.prototype.getWaitTime = function() {
	var smallest_time = this.events.getEarliestTime();
	for (var i in this.instances) {
		if (!this.instances.hasOwnProperty(i)) continue;
		smallest_time = Math.min(smallest_time, this.instances[i].getEarliestEventTime());
	}
	return smallest_time;
};

ObjectManagerBase.prototype.stepAll = function(delta) {
	this.step(delta);
	for (var i in this.instances) {
		if (!this.instances.hasOwnProperty(i)) continue;
		this.instances[i].step(delta);
	}
};

ObjectManagerBase.prototype.step = function(delta) {
	this.events.decreaseTime(delta);
	var due = this.events.popDueEvents();
	for (var e in due) {
		this.handleEvent(due[e].event);
	}
};

ObjectManagerBase.prototype.start = function() {
	for (var i in this.instances) {
		if (!this.instances.hasOwnProperty(i)) continue;
		this.instances[i].start();
	}
};

ObjectManagerBase.prototype.handleEvent = function(e) {
	if (e.name === "narrow_cast") {
		this.handleNarrowCastEvent(e.parameters);
	} else if (e.name === "broad_cast") {
		this.handleBroadcastEvent(e.parameters);
	} else if (e.name === "create_instance") {
		this.handleCreateEvent(e.parameters);
	} else if (e.name === "associate_instance") {
		this.handleAssociateEvent(e.parameters);
	} else if (e.name === "start_instance") {
		this.handleStartInstanceEvent(e.parameters);
	} else if (e.name === "delete_instance") {
		this.handleDeleteInstanceEvent(e.parameters);
	}
};

ObjectManagerBase.prototype.processAssociationReference = function(input_string) {
	//if (input_string === "") {
		//throw new AssociationReferenceException("Empty association reference.");
	//}
	var regex = /^([a-zA-Z_]\w*)(?:\[(\d+)\])?$/;
	var path_string = input_string.split('/');
	var result = new Array();
	if (input_string !== "") {
		for (var p in path_string) {
			if (!path_string.hasOwnProperty(p)) continue;
			var m = regex.exec(path_string[p]);
			if (m) {
				var name = m[1];
				var index = m[2];
				if (!index) {
					index = -1;
				}
				result.push({name:name,index:index});
			} else {
				throw new AssociationReferenceException("Invalid entry in association reference.");
			}
		}
	}
	return result;
};

ObjectManagerBase.prototype.handleStartInstanceEvent = function(parameters) {
	if (parameters.length !== 2) {
		throw new ParameterException("The start instance event needs 2 parameters.");
	}
	var source = parameters[0];
	var traversal_list = this.processAssociationReference(parameters[1]);
	var instances = this.getInstances(source, traversal_list);
	for (var i in instances) {
		if (!instances.hasOwnProperty(i)) continue;
		instances[i].start();
	}
};

ObjectManagerBase.prototype.handleDeleteInstanceEvent = function(parameters) {
	if (parameters.length !== 2) {
		throw new ParameterException("The delete instance event needs 2 parameters.");
	}
	var source = parameters[0];
	var traversal_list = this.processAssociationReference(parameters[1]);
	var instances = this.getInstances(source, traversal_list);
	for (var i in instances) {
		if (!instances.hasOwnProperty(i)) continue;
		var index = this.instances.indexOf(instances[i]);
		instances[i].stop();
		if (instances[i].destructor)
			instances[i].destructor();
		this.instances.splice(index,1);
	}
};

ObjectManagerBase.prototype.handleBroadcastEvent = function(parameters) {
	if (parameters.length !== 1) {
		throw new ParameterException("The broadcast event needs 1 parameter.");
	}
	this.broadcast(parameters[0]);
};

ObjectManagerBase.prototype.handleCreateEvent = function(parameters) {
	if (parameters.length < 2) {
		throw new ParameterException("The create event needs at least 2 parameters.");
	}
	var source = parameters[0];
	var association_name = parameters[1];
	var association = source.associations[association_name];
	if (!association) {
		throw new ParameterException("No such association: " + association_name);
	}
	if (association.allowedToAdd()) {
		var new_instance_wrapper = this.createInstance(association.to_class, parameters.slice(2));
		var index = association.addInstance(new_instance_wrapper);
		// TODO: maybe change order of Event constructor parameters such that we don't have to
		//       explicitly set the port to 'undefined'?
		source.addEvent(new Event("instance_created", undefined, [association_name+"["+index+"]"]));
	} else {
		source.addEvent(new Event("instance_creation_error", undefined, [association_name]));
	}
};

ObjectManagerBase.prototype.handleAssociateEvent = function(parameters) {
	if (parameters.length !== 3) {
		throw new ParameterException("The associate_instance event needs 3 parameters.");
	}
	var source = parameters[0];
	var to_copy_list = this.getInstances(source, this.processAssociationReference(parameters[1]));
	if (to_copy_list.length !== 1) {
		throw new AssociationReferenceException("Invalid source association reference.");
	}
	var wrapped_to_copy_instance = to_copy_list[0];
	var dest_list = this.processAssociationReference(parameters[2]);
	if (dest_list.length === 0) {
		throw new AssociationReferenceException("Invalid destination association reference.");
	}
	var last = dest_list.pop();
	if (last[1] !== -1) {
		throw new AssociationReferenceException("Last association name in association reference could not be accompanied by an index.");
	}
	var instances = this.getInstances(source, dest_list)
	for (var i in instances) {
		if (!instances.hasOwnProperty(i)) continue;
		instances[i].getAssociation(last[0]).addInstance(wrapped_to_copy_instance);
	}
};

ObjectManagerBase.prototype.handleNarrowCastEvent = function(parameters) {
	if (parameters.length !== 3) {
		throw new ParameterException("The narrow_cast event needs 3 parameters.");
	}
	var source = parameters[0];
	var traversal_list = this.processAssociationReference(parameters[1]);
	var cast_event = parameters[2];
	var instances = this.getInstances(source, traversal_list);
	for (var i in instances) {
		if (!instances.hasOwnProperty(i)) continue;
		instances[i].addEvent(cast_event);
	}
};

ObjectManagerBase.prototype.getInstances = function(source, traversal_list) {
	var currents = [source];
	for (var t in traversal_list) {
		if (!traversal_list.hasOwnProperty(t)) continue;
		var name = traversal_list[t].name;
		var index = traversal_list[t].index;
		nexts = new Array();
		for (var c in currents) {
			if (!currents.hasOwnProperty(c)) continue;
			var association = currents[c].associations[name];
			if (index >= 0) {
				nexts.push(association.getInstance(index));
			} else if (index === -1) {
				nexts = nexts.concat(association.instances);
			} else {
				throw new AssociationReferenceException("Incorrect index in association reference.");
			}
		}
		currents = nexts;
	}
	return currents;
};

ObjectManagerBase.prototype.instantiate = function(to_class, construct_params) {
	// pure virtual
};

ObjectManagerBase.prototype.createInstance = function(to_class, construct_params) {
	var instance = this.instantiate(to_class, construct_params);
	this.instances.push(instance);
	return instance;
};

// Event
function Event(name, port, parameters) {
	this.name = name;
	this.port = port;
	this.parameters = parameters;
}

// ControllerBase
function ControllerBase(object_manager, keep_running, finished_callback) {
	this.object_manager = object_manager;
	this.keep_running = keep_running;
	this.finished_callback = finished_callback;
	this.input_ports = new Array();
	this.input_queue = new EventQueue();
	this.output_ports = new Array();
	this.output_listeners = new Array();
}

ControllerBase.prototype.addInputPort = function(port_name) {
	this.input_ports.push(port_name);
};

ControllerBase.prototype.addOutputPort = function(port_name) {
	this.output_ports.push(port_name);
};

ControllerBase.prototype.broadcast = function(new_event) {
	this.object_manager.broadcast(new_event);
};

ControllerBase.prototype.start = function() {
	this.object_manager.start();
};

ControllerBase.prototype.stop = function() {
};

ControllerBase.prototype.addEvent = function(input_event, time_offset) {
	if (input_event.name === "") {
		throw new InputException("Input event can't have an empty name.");
	}
	if (this.input_ports.indexOf(input_event.port) === -1) {
		throw new InputException("Input port mismatch.");
	}
	this.input_queue.add(input_event, time_offset);
};

ControllerBase.prototype.outputEvent = function(event) {
	for (var l in this.output_listeners) {
		if (!this.output_listeners.hasOwnProperty(l)) continue;
		this.output_listeners[l].add(event);
	}
};

ControllerBase.prototype.addOutputListener = function(ports) {
	var listener = new OutputListener(ports);
	this.output_listeners.push(listener);
	return listener;
};

ControllerBase.prototype.addEventList = function(event_list) {
	for (var e in event_list) {
		if (!event_list.hasOwnProperty(e)) continue;
		var entry = event_list[e];
		this.addEvent(entry.event, entry.time_offset);
	}
};

// GameLoopControllerBase
function GameLoopControllerBase(object_manager, keep_running, finished_callback) {
	ControllerBase.call(this, object_manager, keep_running, finished_callback);
}

GameLoopControllerBase.prototype = new ControllerBase();

GameLoopControllerBase.prototype.update = function(delta) {
	this.input_queue.decreaseTime(delta);
	var due = this.input_queue.popDueEvents();
	for (var e in due) {
		if (!due.hasOwnProperty(e)) continue;
		this.broadcast(due[e].event);
	}
	this.object_manager.stepAll(delta);
};

function TimeoutId(id, delay) {
	this.id = id;
	this.delay = delay;
}

// JsEventLoopControllerBase
function JsEventLoopControllerBase(object_manager, keep_running, finished_callback) {
	ControllerBase.call(this, object_manager, keep_running, finished_callback);
	this.running = false;
	this.next_timeout = null;
	this.last_simulation_time = null;
}

JsEventLoopControllerBase.prototype = new ControllerBase();

JsEventLoopControllerBase.prototype.handleInput = function(delta) {
	this.input_queue.decreaseTime(delta);
	var due = this.input_queue.popDueEvents();
	for (var e in due) {
		if (!due.hasOwnProperty(e)) continue;
		this.broadcast(due[e].event);
	}
};

JsEventLoopControllerBase.prototype.addEvent = function(input_event, time_offset) {
	if (this.last_simulation_time && this.next_timeout) {
		var waited = (new Date).getTime() - this.last_simulation_time;
		var remaining = this.next_timeout.delay - waited;
	} else {
		var waited = 0.0;
		var remaining = 0.0;
	}
	var interleave = time_offset < remaining;
	if (this.next_timeout) {
		var additional_offset = waited;
	} else {
		var additional_offset = 0.0;
	}
	ControllerBase.prototype.addEvent.call(this, input_event, time_offset + additional_offset);
	if (this.running && (interleave || !this.next_timeout)) {
		this.run(); // adjust timeout
	}
};

JsEventLoopControllerBase.prototype.start = function() {
	ControllerBase.prototype.start.call(this);
	this.running = true;
	this.run();
};

JsEventLoopControllerBase.prototype.stop = function() {
	this.run(); // update timeouts
	if (this.next_timeout) {
		window.clearTimeout(this.next_timeout.id);
	}
	this.running = false;
	ControllerBase.prototype.stop.call(this);
};

JsEventLoopControllerBase.prototype.getWaitTime = function() {
	var wait_time = Math.min(this.object_manager.getWaitTime(), this.input_queue.getEarliestTime());
	return wait_time;
};

JsEventLoopControllerBase.prototype.run = function() {
		// clear previous timeout
		if (this.next_timeout) {
			window.clearTimeout(this.next_timeout.id);
			this.next_timeout = null;
		}
		// calculate last time since simulation
		if (this.last_simulation_time) {
			var simulation_duration = (new Date).getTime() - this.last_simulation_time;
		} else {
			var simulation_duration = 0.0;
		}
		// simulate
		this.handleInput(simulation_duration);
		this.object_manager.stepAll(simulation_duration);
		// keep time
		this.last_simulation_time = (new Date).getTime();
		// set next timeout
		var wait_time = this.getWaitTime();
		if (wait_time !== Infinity) {
			var actual_wait_time = wait_time - ((new Date).getTime() - this.last_simulation_time);
			if (actual_wait_time < 0.0)
				actual_wait_time = 0.0;
			// wait actual_wait_time
			//console.log("waiting " + actual_wait_time + " ms");
			this.next_timeout = new TimeoutId(window.setTimeout(this.run.bind(this), actual_wait_time), actual_wait_time);
		} else {
			// wait forever
			//console.log("waiting forever");
			this.last_simulation_time = null;
			if (this.finished_callback) {
				this.finished_callback();
			}
		}
};

// OutputListener
function OutputListener(port_names) {
	this.port_names = port_names;
	this.queue = new Array(); // TODO: optimize!
}

OutputListener.prototype.add = function(event) {
	if (this.port_names.length === 0
		|| this.port_names.indexOf(event.port) !== -1)
	{
		this.queue.push(event);
	}
};

OutputListener.prototype.fetch = function(timeout) {
	return this.queue.shift();
};

// RuntimeClassBase
function RuntimeClassBase() {
	this.active = false;
	this.state_changed = false;
	this.events = new EventQueue();
	this.timers = null;
}

RuntimeClassBase.prototype.addEvent = function(event, time_offset) {
	if (!time_offset) time_offset = 0.0;
	this.events.add(event, time_offset);
};

RuntimeClassBase.prototype.getEarliestEventTime = function() {
	if (this.timers) {
		var minimum = Infinity;
		for (var t in this.timers) {
			if (!this.timers.hasOwnProperty(t)) continue;
			minimum = Math.min(minimum, this.timers[t]);
		}
		return Math.min(this.events.getEarliestTime(), minimum);
	}
	return this.events.getEarliestTime();
};


RuntimeClassBase.prototype.step = function(delta) {
	if (!this.active) {
		return;
	}
	this.events.decreaseTime(delta);
	if (this.timers) {
		var next_timers = new Object();
		for (var t in this.timers) {
			if (!this.timers.hasOwnProperty(t)) continue;
			var time_left = this.timers[t] - delta;
			if (time_left <= 0.0) {
				this.addEvent(new Event("_" + t + "after"), time_left);
			} else {
				next_timers[t] = time_left;
			}
		}
		this.timers = next_timers;
	}

	this.microstep();
	while (this.state_changed) {
		this.microstep();
	}
};

RuntimeClassBase.prototype.microstep = function() {
	var due = this.events.popDueEvents();
	if (due.length === 0) {
		this.transition();
	} else {
		for (var e in due) {
			if (!due.hasOwnProperty(e)) continue;
			this.transition(due[e].event);
		}
	}
};

RuntimeClassBase.prototype.transition = function(event) {
	// pure virtual
};

RuntimeClassBase.prototype.start = function() {
	this.active = true;
};

RuntimeClassBase.prototype.stop = function() {
	this.active = false;
};
