/**
a basic client (for the server <-> client communication)
to be used by the editor to communicate with the server
@author: Daniel Riegelhaupt
*/

/**
@class Client
a small client class that can save and load a file
@param statechart the statechart instance used
@param editorId optional. id of the editro , default is empty.
@param server optional , the adrres of the server , default is "http://localhost:PORT/" where PORT is the currently used port
@param timeout optional the time a request will wait before timing out in ms default is 300000 ms = 5 min
*/
function Client(statechart, editorId, server, timeout){
	var port = window.location.port;
	
	var eId = typeof(editorId) != 'undefined' ? editorId : "";
	var SERVER = typeof(server) != 'undefined' ? server : "http://localhost:" + port + "/"; // if there is no server use this as default parameter
	var scInstance = statechart;
	var time = typeof(timeout) != 'undefined' ? timeout : 300000; //timeout in ms 
	
	$.ajaxSetup({
	  url: SERVER,
	  type: "POST",
	  timeout: time,
	  beforeSend: function( xhr ) {
	    xhr.overrideMimeType( "text/plain; charset=utf-8" ); //this needs to be here otherwise there is a not well formed error
	  }
	});
	
	/** save the given content to 'fileName' 
	@return the jqHRX object
	*/
	this.save = function(fileName, fileContent){
		
	    var data = {command : "save", editor_id: eId, file_name : fileName, content : fileContent};
	    var jsonData = JSON.stringify(data);
	    
	    var jqHRX = $.ajax({ data : jsonData
			}).done(function(data){
			  resp = JSON.parse(data)
			  if (resp.response_status == "OK"){
			    u = resp.save_path.slice(2); //remove the ./ of the current directory
			    console.log("addres= ", SERVER+u)
			    window.location = SERVER + u;
			    scInstance.gen("save_succes", null);
			  }else if (resp.response_status == "ERROR"){
				var err = "Failed to save file:\n" + resp.message
				var data = {error : err}
				scInstance.gen("save_fail", data);
			   }
			});
		
	    return jqHRX; 

	}
	
	
	/** save the given content to 'fileName' 
	@return the jqHRX object
	*/
	this.loadFile = function(fileName){
		
	    var data = {command : "load", editor_id: eId, file_name : fileName};
	    var jsonData = JSON.stringify(data);
	    
	    var jqHRX = $.ajax({ data : jsonData
			}).done(function(data){
			  //console.log("data:", data)
			   resp = JSON.parse(data)
			   if (resp.response_status == "OK"){
				var data = {file_name : resp.file_name, file_content : resp.file_content}
				scInstance.gen("load_file_succes", data);
			     
			   }else if (resp.response_status == "ERROR"){
				var err = "Failed to load file:\n" + resp.message
				var data = {error : err}
				scInstance.gen("load_file_fail", data);
			   }
				
			}).fail(function(jqxhr, textStatus, errorThrown){
			  console.log(jqxhr, textStatus, errorThrown)
				var err = "Failed to load file:\n" +textStatus+ ": " + errorThrown;
				var data = {error : err}
				scInstance.gen("load_file_fail", data);
			}) ;
		
		
	    return jqHRX; 

	}
		
	/** tells the server we will close the application */
	this.close = function(){
		
		var data = {command : "close", editor_id: eId}
		
		var jsonData = JSON.stringify(data);
	    
		//the first close request puts a boolean to true in the server but it will only be checked when it receives a next request so we send two close request
	    var jqHRX = $.ajax({ data : jsonData
			}).done(function(data){
				var secondReq = $.ajax({ data : jsonData })
				scInstance.gen("quit_succes", null);	
			});
		
	    return jqHRX; 
		
	}
	
	
	/** loads a grammar to the editor*/
	this.loadGrammar = function(gramFile, metaFile, stDefFile, stMapFile){
	    
	  var data = {grammar_command: "load_grammar", editor_id: eId, grammar : gramFile , metamap: metaFile, styledef : stDefFile, stylemap : stMapFile}
	  var jsonData = JSON.stringify(data);
	  var jqHRX = $.ajax({ data : jsonData
			}).done(function(data){
			  //console.log("data:", data)
			   resp = JSON.parse(data)
			   if (resp.response_status == "OK"){
				var data = {keywords : resp.keywords, defaultStyleStr : resp.default_style, errorStyleStr : resp.error_style}
				scInstance.gen("load_grammar_succes", data);
			     
			   }else if (resp.response_status == "ERROR"){
				var err = "Failed to load grammar:\n" + resp.message
				var data = {error : err}
				scInstance.gen("load_grammar_fail", data);
			   }
				
			}).fail(function(jqxhr, textStatus, errorThrown){
			  console.log(jqxhr, textStatus, errorThrown)
				var err = "Failed to load grammar:\n" +textStatus+ ": " + errorThrown;
				var data = {error : err}
				scInstance.gen("load_grammar_fail", data);
			}) ;
		
	    return jqHRX; 
	}
	
	/** check the text for style and errors*/
	this.checkText = function(text) {
	      var data = { grammar_command: "check_text", editor_id: eId, input : text}
	      var jsonData = JSON.stringify(data);
		  
	      var jqHRX = $.ajax({ data : jsonData
			}).done(function(data){
			   //console.log("data:", data)
			   resp = JSON.parse(data)
			   if (resp.response_status == "OK"){
				var data = {styles : resp.styles, errors : resp.error_log}
				scInstance.gen("check_text_succes", data);
			     
			   }else if (resp.response_status == "ERROR"){
				var err = "Failed to check the text:\n" + resp.message
				var data = {error : err}
				scInstance.gen("check_text_fail", data);
			   }
				
			}).fail(function(jqxhr, textStatus, errorThrown){
			  console.log(jqxhr, textStatus, errorThrown)
				var err = "Failed to check text:\n" +textStatus+ ": " + errorThrown;
				var data = {error : err}
				scInstance.gen("check_text_fail", data);
			}) ;
		  return jqHRX; 
	}
	
	/** check the text for style and errors*
	 @param text the input of the editor
	 @param pos {line, column}
	 */
	this.autoComplete = function(text, pos){
	      pos.line += 1; //the server indices start with 1 the editors with 0
	      pos.column += 1;
	      var data = { grammar_command: "auto_complete", editor_id: eId, input : text, position : pos}
	      var jsonData = JSON.stringify(data);
	      var jqHRX = $.ajax({ data : jsonData
			}).done(function(data){
			   //console.log("data:", data)
			   resp = JSON.parse(data)
			   if (resp.response_status == "OK"){
				if ("autocomplete_list" in resp){
				    var data = { suggestions: resp.autocomplete_list}
				    scInstance.gen("auto_complete_succes", data);
				}
				else{ //a syntax error was received
				    var data = { styles : resp.styles, errors : resp.error_log}
				    scInstance.gen("auto_complete_syntax_error", data);
				}
			     
			   }else if (resp.response_status == "ERROR"){
				var err = "Auto complete failure:\n" + resp.message
				var data = {error : err}
				scInstance.gen("auto_complete_fail", data);
			   }
				
			}).fail(function(jqxhr, textStatus, errorThrown){
			  console.log(jqxhr, textStatus, errorThrown)
				var err = "Auto complete failure:\n" +textStatus+ ": " + errorThrown;
				var data = {error : err}
				scInstance.gen("auto_complete_fail", data);
			}) ;
		  return jqHRX; 
	  
	}
} 
