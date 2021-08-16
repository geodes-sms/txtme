/**
small logger class and utilities</br> 
this is a small prototype and will be change to accomodate clicks.
@author: Daniel Riegelhaupt
*/

/** 
@class LogEntry
@description a class to store the log: date & char 
*/
function LogEntry(time, character){
	this.time = time //time a string
	this.character = character //the character typed
	
	/** returns the timestamp stored*/
	this.getTimeStamp = function() {
		return this.time;
	}
	
	/** returns the character stored stored*/
	this.getCharacter = function(){
		return this.character;
	}
	
	/** returns the entry as a string*/
	this.toString = function(){
		entry = time + " : " + character;
		return entry;
	}
}

/**
@class
@description a simple log book class
*/
function Logger(){
	var logBook = new Array();
	var scInstance;
	
	/**set the statechart will be needed to save*/
	this.setStateChart = function(sc){
		scInstance = sc;
	}
	
	/** adds the given character/string to the logbook
	param str the character or string to add
	param fromCharCodeBool default false ; if true we got a charcode instead of a character and it nees to be converted
	*/
	this.addEntry = function(character, fromCharCodeBool){	
		now = new Date();
		mili = now.getMilliseconds();
		sec = now.getSeconds();
		mins = now.getMinutes();
		hour = now.getHours();
		timeStamp = hour.toString() + ":" + mins.toString() + ":" + sec.toString() + ":" + mili.toString();
		
		convert = (typeof(fromCharCodeBool) == "undefined") ? false :  fromCharCodeBool;
		ch = convert? String.fromCharCode(character) : character;
		entry = new LogEntry(timeStamp, ch);
		logBook.push(entry);	
	}
	
	/** prints the log book to the firebug console*/
	this.printLog = function(){
		l = logBook.length;
		if(l == 0 ){
			console.log("The log book is empty");
		}
		else{			
			logText = "";
			/*for (i = 0; i < l ; i++){
				logText += logBook[i].getEntryString();	
				logText +="</br>";
			}
			document.write(logText);*/
			//firebugg logger
			//TODO change this when it can be printed to something else then the firebug console
			for (i = 0; i < l ; i++){
				if (logBook[i].getCharacter() != "ENTER"){
					console.log( "%s - %s", logBook[i].getTimeStamp(), logBook[i].getCharacter() ); 
				}
				else{
					console.log( "%s - ENTER", logBook[i].getTimeStamp() ); 
				}
			}
		} 
	}
	
	/** returns the eniter logbook as a string*/
	this.toString = function(){
		l = logBook.length;
		logText = "";
		if(l == 0 ){
			logText = "The log book is empty";
		}
		else{		
			for (i = 0; i < l ; i++){
				logText += logBook[i].getTimeStamp() + " - " + logBook[i].getCharacter();	
				logText +="\n";
			}
		}
		return logText; 
	}
	
	/** saves the log book*/
	this.saveLog = function(){
		fname = "Log_" + (new Date()).getTime().toString();
		scInstance.GEN("save_event", { fileName: fname, fileContent: this.toString()});
	}
		
}
	
