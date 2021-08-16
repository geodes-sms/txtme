/****
Daniel Riegelhaupt

A helper  class for use with the statechart
****/


/**
returns the controller from the behaviour
Used create a controller with or without parameters and with or without event loop if you are using the newer version of SCCD
@param initParam: one param, use a dictionary as the param if you need more and refer to them by key name inside the statechart
@param eventLoop: keep this empty if you use the SCCD version originally supplied with this editor. if you use the newer version simply write new JsEventLoop() here
*/
function createController(behaviour, initParam, eventLoop){
	var controller = null
	if (initParam != null && typeof(initParam) !== 'undefined'){
		if (typeof(eventLoop) !== 'undefined'){
			controller = new behaviour.Controller(initParam, eventLoop);
		}else{
			controller = new behaviour.Controller(initParam);
		}
	}else{
		if (typeof(eventLoop) !== 'undefined'){
			controller = new behaviour.Controller(eventLoop);
		}else{
			controller = new behaviour.Controller();
		}
	}
	return controller;
}

/**
a little wrapper around the SCCD controller 
so that we don't have to change the gen function where it appears
also nice for when switching SCCD version, when using the newer version simply change addEvent to addInput  here
and things should (normally) still work 
@param controllerInstance: and instance of the behaviour controller
@param defPort: the default port this wrapper uses if no port is supplied in the gen method. optional. if not provided the default port is 'in'
*/
function StateChartWrapper(controllerInstance, defPort, isNew){
	var controller = controllerInstance;
	var DEF_PORT = typeof(defPort) != 'undefined' ? defPort : 'in';
	var useInput = (typeof(isNew) != 'undefined')? isNew : false; 
	
	this.start = function(){
		controller.start() 
	}
	
	/** Generate as an event to the statechart */
	this.gen = function(eventName, eventData, port, timeOffset) {
		var dataArray = [];
		var curPort = typeof(port) != 'undefined' ? port : DEF_PORT;
		var tOffset = typeof(timeOffset) != 'undefined' ? timeOffset : 0.0;
		if (eventData != null && typeof(eventData) != "undefined")
			dataArray.push(eventData) //we keep the data in a dictionary and just put that in the array
			//the statechart can access is as usual using data.<dictionary_key> (assuming we name the parameter data)
		
		if (!useInput){
			controller.addEvent(new Event(eventName, curPort , dataArray), tOffset);
		}else{
			controller.addInput(new Event(eventName, curPort , dataArray), tOffset); //new sccd version uses this instead of addEvent
		}
		//this.printCurrentState();
	}
	
	//helps a bit with debugging
	/*this.printCurrentState = function(){
		console.log(controller.object_manager.instances[0]);
		console.log(controller.object_manager.instances[0].current_state);
	}*/
}