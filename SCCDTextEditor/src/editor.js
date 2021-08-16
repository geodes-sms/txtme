/**
An SVG rich text editor prototype
@author Daniel Riegelhaupt
@date may 2014
*/
SVGEditorFactory = {
	
	/** 
	@function createNewSVGEditorInstance 
	@description a factory for the svg editor
	@param editorId the id (name) of the editor. only usefull in cases of multiple instances
	@param scInstance the instance of the statechart
	@param loadNode the DOM input node that needed to load files
	@param rootNode the DOM root of the SVG editor
	@param textNode the DOM element where the text will be placed
	@param textCursorNode the DOM element that will serve as text cursor
	@param selectionNode the DOM element that will serve as parent for the selection highlighting
	@param autoCompleteMenuRootNode the DOM parent where the auto complete menu will be displayed
	@param leftBarNode the DOM element for the bar at the left of the text (that will display errors)
	@param styleT the interface between the DOM buttons and the editor for editing style (may be null)
	@param grammarT the interface between the DOM buttons and the editor for loading grammars  (may be null)

	@param leftMargin the minimum allowed x position of the text
	@param rightMargin the maximum allowed x position of the text
	@param height the height of a page on screen  

	@return an instance of the SVGEditor class
	*/
	createNewSVGEditorInstance : function( editorId, scInstance, loadNode, rootNode, textNode, textCursorNode, selectionNode ,leftMargin, rightMargin, height,
					       leftBarNode, autoCompleteMenuRootNode ,styleT, grammarT){
		
		//create everything the editor will need
		//var displayMgr = new DisplayManager(rootNode,leftMargin, rightMargin, height);
		var displayMgr = new DisplayManagerScrollBars(rootNode,leftMargin, rightMargin, height);		
		var lineMgr = new LineManager(textNode, displayMgr, LINEBREAK_CHAR);
		
		var textCursor = new TextCursor(textCursorNode, lineMgr, displayMgr);
		var selectionMgr = new SelectionManager(selectionNode, lineMgr)
		
		var loaderInstance = new Loader(loadNode)
		//different aspects
		var leftBar = new ErrorDisplayBar(leftBarNode, lineMgr);
		var styleToolbarInst = (typeof(gui) != "undefined")? gui : null;
		var grammarToolbarInst = (typeof(grammarT) != "undefined")? grammarT : null;
		var autoCompleteMenu = new AutoCompleteMenu(autoCompleteMenuRootNode);
		
		//create the editor
		var editor = new SVGEditor(editorId, rootNode, textCursor, displayMgr, selectionMgr);
		
		var dt = {editor: editor, styleToolbar: styleToolbarInst, grammarToolbar: grammarToolbarInst, loader : loaderInstance , errorBar: leftBar, autoComplete: autoCompleteMenu};		
		
		return dt;
	}
}

/**
a wrapper around an input DOM node with type file
*/
function Loader(loadDOM){

	this.setStateChart =function(sc){ //note that sc is not scInstance given here, it is another one with its own default port
		loadDOM.onchange = function(event){
			var file = event.target.files[0]
			var name = file.name

			//we read the text and alert the statechart when done
			var reader = new FileReader(); 
			reader.onload = function(){
				var content = reader.result;
				data = { file_name: name , file_content: content }
				sc.gen("load_text_event", data); 
			}; 
			reader.readAsText(file); 
		}
	}

	this.click = function(){
		loadDOM.click();
	}
}

/**
@class SVGEditor
@description an SVG rich text editor prototype
@param editorId the id (name) of the editor
@param rootNode the DOM root of the SVG editor
@param textCursor an instance of the TextCursor class
@param displayMgr an instance of the DisplayManager class , to handle styles and margins
@param selectionMgr an instance of the SelectionManager class, to handle selecting as well as copying , removing and cutting that selection	
*/
function SVGEditor(editorId, rootNode, textCursor, displayMgr, selectionMgr){

	var self = this; //for when a reference to this editor is needed from outside the editor (like for example the load helper	
	this.scInstance = null; //the statechart instance that describes the behavior, the editor won't work without it
	
	var id = editorId; // the id of the editor
	var lineMgr = textCursor.getLineManager();//the object that manages the actual text in the form of lines and words
	var clipboard = null; //place where copied or cut text is placed
	var highlightMgr = null; //the highlightmanager, needed by load
	
	var me = this
	
	/** set the state chart that describes the behavior of the editor*/
	this.setStateChart = function(sc){
		this.scInstance = sc;
	}
	
	/** return the statechart that describes the editor behavior */
	this.getStateChart = function(){
		return this.scInstance
	}
	
	this.getLineManager = function(){
		return lineMgr;
	}
	
	this.getId = function(){
		return id;
	}
	
	this.setHighlighter = function(highlight){
		highlightMgr = highlight;
	}
	
	/** return the text cursor associated with the editor*/
	this.getCursor = function(){
		return textCursor;
	};
	
	/** return the display manager associated with the editor*/
	this.getDisplayManager = function(){
		return displayMgr;
	};
	
	this.focus =function(){
		var divParent = rootNode.parentNode
		divParent.focus();
	}
	
	/** write the given character in the document*/
	this.writeChar = function(c){
		//console.log("editor:", id, "writting char", c)
		writeHelper(c, false);
	}
	
	/** write the given character over the current character in the document*/
	this.overWriteChar = function(c){
		writeHelper(c, true);
	}
	
	//over write and write have so much in common that everything has been put here to be called by simple parameter
	//overWrite if true we overwrite instead of write. default false
	function writeHelper(c, overWrite){
		var over = (typeof(overWrite) == "undefined")? false : overWrite;
		var ch = (typeof c === "number" ? String.fromCharCode(c) : c);
		
		var coord = textCursor.getCoords();
		var line = lineMgr.getLine(coord.row);	
		
		var len = line.getTextLength()
		len = (line.endsWithLineBreak())? len-1 : len;
		
		//can't overwrite a line break but if we are in overwrite mode and it isn't a linebreak	
		if (over &&  !(line.endsWithLineBreak() && (coord.col == len)) ){
			line.removeCharAt(coord.col);
		}
		line.writeCharAt(ch,coord.col);
	}
	
	
	/** adds a line break at the current position in the document*/
	this.writeLineBreak = function(){
		//console.log("Enter pressed but not yet implemented");
		var coord = textCursor.getCoords();
		var line = lineMgr.getLine(coord.row);
		
		line.writeCharAt(LINEBREAK_CHAR,coord.col);
		lineMgr.rearangeOnAddLB(coord.row, coord.col);
	}
	
	/**  removes the char at the current position and returns it*/
	this.removeChar = function(){
		var coord = textCursor.getCoords();
		var line = lineMgr.getLine(coord.row);
		var last = line.getTextLength();
		var ch = null; //the removed char
	
		if ((coord.col == (last-1)) && (coord.row == lineMgr.getLineCount()-1)){
			//don' to anything we aren't allowed to remove the last character of the last line
		}
		else if (coord.col != last){ 
			ch = line.removeCharAt(coord.col);	
		}
		//pretty sure this cant happen in this version but keep this in anyway
		else if(coord.row != lineMgr.getLineCount()-1){
			ch = lineMgr.getLine(coord.row+1).removeCharAt(0);
		}
		
		if ((ch != null) && isLineBreak(ch)){
			lineMgr.rearangeOnRemoveLB(coord.row);
		}
		return ch;
	}
		
	/** select the part of the text between the given screen coordinates
	 @return true if there was a selection (if the cursor moved enough to make a selection) false otherwise
	 */
	this.select = function(fromX, fromY, toX, toY){
		return selectionMgr.drawSelection(fromX, fromY, toX, toY);
	}
	
	/** select everything except for  irremovable line break
	 @return true if something was selected (in other words true if there is text)
	 */
	this.selectAll = function(){
		return selectionMgr.selectAll();
	}
	
	/** deselect the current selection */
	this.deselect = function(){
		selectionMgr.deselect();
	}
		
	/** returns the selection manager associated with the editor*/
	this.getSelectionMgr = function(){
		return selectionMgr;
	}
	
	/** copy the selected text to the editor's own clipboard*/
	this.copySelection = function(){
		var start = selectionMgr.getSelectionStart();
		var end = selectionMgr.getSelectionEnd();
		if (start.row != -1){ //if there is a selection
			clipboard = lineMgr.copySelection(start, end);
			//console.log("Copied some text:");
			//console.log(clipboard.getTextContent());
		}
	}
	
	/** cut the selected text to the editor's own clipboard*/
	this.cutSelection = function(){
		var temp = this.removeSelection();
		if (temp != null){
			clipboard = temp;
			//console.log("cut some text:");
			//console.log(clipboard.getTextContent());
		}
	}
	
	/** remove the selected text
	 @return the removed text
	 */
	this.removeSelection = function(){
		//NOTE this method will probably be very inefficient for big selections
		//we do it this way because it will keep the text rearranged correctly on remove
		//but for multiple line removed it might be better to simply remove the lines
		//the problem is we need to reorganize the text correctly after that.
		
		var ret = null;
		var start = selectionMgr.getSelectionStart();
		var end = selectionMgr.getSelectionEnd();
		if (start.row != -1){ //if there is a selection
			ret = lineMgr.copySelection(start, end);
			var len = ret.getTextLength()
			
			//we move the text textCursor to the start position
			//since we remove it doesn't matter if we were at the start or not we will end up on the same place
			textCursor.moveToRowCol(start.row, start.col);
			for (var i = 0; i < len; i++){
				this.removeChar();
			} 
		}
		return ret;
	}
	
	/** paste the content of the clipboard to the editor at the current cursor position*/
	this.paste = function(){
		if (clipboard != null){
			this.pasteHelper(clipboard);
		}
	}
	
	//paste the content of a buffer to the the current cursor position
	//TODO for the moment this private function is public to access the changeStyle function
	//this should change somehow  this needs to be private
	this.pasteHelper = function(buf){
		var len = buf.getTextLength();
		var c;
		
		var style = buf.getStyle(0);
		this.changeStyle(style);
		
		for (var i = 0; i < len ; i++){
			c = buf.getCharAndStyle(i);
			if (c.style.toString() != style.toString()){
				var style = c.style;
				this.changeStyle(style);
			}
			if (isLineBreak(c.char) == false){
				this.writeChar(c.char);
				textCursor.moveRight();
			}
			else{
				this.writeLineBreak();
				textCursor.moveRight();
			}
		}
	}
	
	//paste the content of a buffer to the the current cursor position
	//difference between this and the regular is that this uses tspan internally 
	//TODO after testing remove paseHelper and keep this one. it is more effcient to past one tspan at the time than one character at the time
	//TODO for the moment this private function is public to access the changeStyle function
	//this should change somehow  this needs to be private
	//@precondition an important assumption here is that newline characters can only appear at the end of tspans
	this.pasteHelperTspan = function(buf){
		var tspanArLen = buf.getTspanCount();
		var t;
		var line, coords;
		
		for (var i = 0; i < tspanArLen ; i++){
			t = buf.getTspan(i);
			len = t.getTextLength();
			coords = textCursor.getCoords();
			line = lineMgr.getLine( coords.row);

			if (t.endsWithLineBreak() == false){
				line.addTspanAt(t ,coords.col);	
				for (var j = 0; j < len; j++){
					textCursor.moveRight();
				}
			}
			else{
				t.cutSelection(len-1)//cut the last character
				line.addTspanAt(t ,coords.col);	
				for (var j = 0; j < len-1; j++){
					textCursor.moveRight();
				}
				this.changeStyle(t.getStyle());
				this.writeLineBreak();
				textCursor.moveRight();
			}
		}
		
		this.changeStyle(buf.getTspan(tspanArLen-1).getStyle());
	}
	
	/** changes one style attribute of the selection
	 to that of the value of that attribute in the new style
	 @param nStyle the new style whose attribute value we take
	 @param attr, a css string name of a style attribute
	 */
	this.changeSelectionStyle = function(nStyle, attr){
		var buf = this.removeSelection();
		buf.changeStyleAttribute(nStyle, attr);
		this.pasteHelper(buf);
		
		var end = textCursor.getCoords();
		var start = lineMgr.getPositionLeftOffset(end.row, end.col, buf.getTextLength());
		//console.log("old start=",selectionMgr.getSelectionStart());
		//console.log("new start=", start);
		
		//we redraw the selection and make sure to give start and end in the same order they were given originally
		//so the we can determine what the new style must be in another method
		var adjusted = selectionMgr.isAdjusted();
		if (adjusted){
			//console.log("adjusted")
			selectionMgr.drawSelectionIndices(end, start);
		}
		else{
			//console.log("not adjusted")
			selectionMgr.drawSelectionIndices(start, end);
		}
	}
	
	/** ADDED FOR HIGHLIGHTING CODE   **/
	
	/** change the style of the given range to the given style.
	 the difference between a range and a selection is that a selection is shown as such (there is a blue selection rectangle over the selection)
	 while a range isn't highlighted and is selected by code not by userinput.
	 @param start a map { row, col} the start coordinates of the range
	 @param end a map { row, col} the end coordinates of the range, not included
	 @param nStyle an instance of Style OR a string. if nStyle is an instance of style it will completely replace the current style
	 if it is a string the attributes will simply be added
	 @precondition the given coordinates must be valid.
	 @precondition The style change will not change the word wrap leaving the cursor postion the same
	 */
	this.changeRangeStyle = function(start, end, nStyle){
		
		var coord = textCursor.getCoords();
		
		//we copy the selection 
		var ret = lineMgr.copySelection(start, end);
		var len = ret.getTextLength();
		
		//we remove the range, to do this we first move the text cursor to the start position and then start deleting
		//since we remove it doesn't matter if we were at the start or not we will end up on the same place
		textCursor.moveToRowCol(start.row, start.col);
		//console.log("ret before delete:", ret.getTextContent());
		for (var i = 0; i < len; i++){
			this.removeChar();
		}
		
		//we change the style of the selection
		//console.log("ret now:",ret.getTextContent());
		if (typeof nStyle === 'string')
		      ret.changeContentStylesFromString(nStyle);
		else
		      ret.changeContentStyles(nStyle);
		//and finally we can paste it back with the new style
		this.pasteHelperTspan(ret);
		
		//IMPORTANT ASSUMPTION: the style change will not change the word wrap leaving the cursor postion the same
		textCursor.moveToRowCol(coord.row, coord.col);
	}
	
	/** Displays the range as an error 
	 @param start a map { row, col} the start coordinates of the range
	 @param end a map { row, col} the end coordinates of the range, not included
	 @precondition the given coordinates must be valid.
	 @precondition The style change will not change the word wrap leaving the cursor postion the same
	 */
	this.addRangeError = function(start, end){
		
		var coord = textCursor.getCoords();
		
		//we copy the selection 
		var ret = lineMgr.copySelection(start, end);
		var len = ret.getTextLength();
		
		//we remove the range, to do this we first move the text cursor to the start position and then start deleting
		//since we remove it doesn't matter if we were at the start or not we will end up on the same place
		textCursor.moveToRowCol(start.row, start.col);
		//console.log("ret before delete:", ret.getTextContent());
		for (var i = 0; i < len; i++){
			this.removeChar();
		}
		
		//we add the error message to the selection
		//console.log("ret now:",ret.getTextContent());
		ret.setContentStyleToError();
		this.pasteHelperTspan(ret);
		
		//IMPORTANT ASSUMPTION: the style change will not change the word wrap leaving the cursor postion the same
		textCursor.moveToRowCol(coord.row, coord.col);
	}
	
	/** get information about the word on the given
	@param coord a map {row, col}. optional default is current position
	@return a map { word: the word as a Buffer or null
			start:  a map {row, col}
			end: a map {row, col}
		      }
	 */
	this.getWordInformationAtCoord = function(coord){
		var c = (typeof(coord) == "undefined")? textCursor.getCoords() : coord;
		var dict =  lineMgr.getWordInformationAtPos(c.row, c.col);
		var ret = { word: dict.word ,
			    start: { row : c.row , col : dict.start},
			    end: { row : c.row , col : dict.end}
			  };
		return ret;
	}
	
	/** END ADDED FOR HIGHLIGHTING CODE   **/
	
	/** change the current font style if no style is given the new style becomes the one at the current text cursor position*/
	this.changeStyle = function(nStyle){
		var style = (typeof(nStyle) == "undefined") ? textCursor.getStyle() : nStyle;
		displayMgr.setStyle(style);
		textCursor.changeSize();
	}
	
	/** Returns a string conting the current text*/
	this.getCurrentText = function(){
		var content = Serializer.serializeToTXT(lineMgr);
		return content;
	}
	
	/** closes the editor and the server*/
	this.close = function(){
		var c = new Client(this.scInstance);
		return c.close();
	}
	
	/** Saves the current text in the editor to txt*/
	this.saveAsTXT = function(){
		var name = "Document_" + (new Date()).getTime().toString() + ".txt";
		var content = Serializer.serializeToTXT(lineMgr);
		
		//var blob = new Blob([content], {type: "text/plain;charset=utf-8"});
		//saveAs(blob, name);
			
		var c = new Client(this.scInstance);
		return c.save(name, content);
		//return null;
	}
	
	/** Saves the current text in the editor to rtf*/
	this.saveAsRTF = function(){
		var name = "Document_" + (new Date()).getTime().toString() + ".rtf";
		var content = Serializer.serializeToRTF(lineMgr);
		
		//var blob = new Blob([content], {type: "text/rtf"});
		//saveAs(blob, name);
		
		var c = new Client(this.scInstance);
		return c.save(name, content);
		//return null;
	}
	
		
	/** Saves the current text in the editor to stand alone SVG*/
	this.saveAsSVG = function(){
		var name = "Document_" + (new Date()).getTime().toString() + ".svg";		
		var content = Serializer.serializeToSVG(lineMgr);
		
		//var blob = new Blob([content], {type: "image/svg+xml"});
		//saveAs(blob, name);
		
		var c = new Client(this.scInstance);
		return c.save(name, content);
		//return null;
	}
	
	/** Loads a file to the editor
	 @param file a file that can be read by the HTML5 FileReader API 
	 @param highlightMgr the HighlightMgr to use. optional, default null
	 */
	this.load = function(fileName, fileContent){
		var txtReg = /.*\.(text|txt)$/i;
		var rtfReg = /.*\.rtf$/i;
		var svgReg = /.*\.svg$/i;
		
		var mimeReg = /^text\//
		
		Deserializer.setHighlighter(highlightMgr);
		
		var name = fileName;
		console.log("about to read: ", name);
		//lineMgr.hide()
		if( txtReg.test(name) ){
			Deserializer.fromTXT(lineMgr, fileContent);
		}
		/*else if( rtfReg.test(name) ){
			console.log("no support for loading rtf yet");
		} for the momemnt no support for rtf planned*/
		else if( svgReg.test(name) ){
			Deserializer.fromSVG(lineMgr, fileContent);
		}
		else{
			console.log("extension not recognized. file will be read as plain text");
			Deserializer.fromTXT(lineMgr, fileContent);
		}
		//lineMgr.show()
	}
			
	/** resets the content of the editor*/
	this.clear= function(){
		//history = new CommandHistory(); //clear the history
		clipboard = null; //clear the clipboard 
		selectionMgr.deselect();//if something was selected deselect it
		lineMgr.clear();
		textCursor.moveToRowCol(0,0);
	}
		
	/** initialize the editor the editor doesn't work whitout this*/
	this.init = function(){
		if (this.scInstance == null){
			alert("The state chart behavior must be set for the editor to work!")
			return;
		} 
		
		/* Maps keyboardEvent.keyCode to the correct event.*/
		var eventCodeMap = {
			8:  "backspace",
			13: "enter",
			37: "left",
			27: "escape",    
			38: "up",
			39: "right",
			40: "down",
			45: "insert",
			46 : "delete"
		}
		
		/* Maps keyboardEvent.key to the correct event
		 * Some key values depend on the browser : ArrowLeft an Left both mean the left Arrow   
		 * needs to be in a separate map from the keyCode map because pressing the number 8 key translate to backspace otherwise
		 */ 
		var eventKeyMap = {
			"Backspace": "backspace",
			"Enter": "enter",
			"Left": "left",
			"ArrowLeft": "left",
			"Up":"up",
			"ArrowUp":"up",
			"Right": "right",
			"ArrowRight": "right",
			"Down": "down",
			"ArrowDown": "down",
			"Insert": "insert",
			"Del": "delete",
			"Delete": "delete",
			"Esc": "escape",
			"Escape": "escape"
		}
		
		/* only needed for chrome. 
		 * basically any key we are going to capture along with a ctrl key 
		 */
		var shortcutEventMap = {
			"A": "a",
			"C" : "c",
			"E" : "e",
			"L" : "l",
			"M": "m",
			"O": "o",
			"Q" : "q",
			"S" : "s",
			"T" : "t",
			"V" : "v",
			"X": "x",
			" ": " "
		}
		
		/* EVENT LISTENERS: note: the SVG doesn't appear to be focusable  when embedded directly in html so use the html root instead to capture key event
		 we can capture mouse events on SVG so we will use that for selection
		 */
		
		//add event listener when typing
		var container = rootNode.parentNode //the div parent of the svg rootnode
		//an svg node cannot accept keystrokes it seems so the container has to catch them instead
		container.addEventListener("keypress",function(e){
		//document.documentElement.addEventListener("keypress",function(e){
			//e.preventDefault(); //TODO uncomment this and remove the one in the if loop when done developing this blocks ctrl+f5 which is very annoying
			var scEvent = null;
			//console.log("document keypress", e.key)
			if (e.key){
				scEvent = (e.key != "Spacebar")? e.key : " "; //some version of the implementation returns the char some the name. we want the char
				scEvent = (scEvent.length == 1)? scEvent : null; //if key returns a whole name instead of one character we aren't interested (except for space but that has been handled)
			}
			else if(e.charCode != 0){
				scEvent = String.fromCharCode(e.charCode) || null;
			}
			
			if(scEvent != null){
				e.preventDefault();
				//we used to pass the event and take the charCode but charCode is deprecated 
				//so to make sure we give a valid event we send this as data wheter charCode or key was used
				var data = { "char" : scEvent} ;
				
				//this only seems to work correctly in firefox
				if(e.ctrlKey){
					scEvent = "ctrl_" + scEvent;
					//console.log("inside keypress event ctrl");
				}
				//console.log("keypress scevent=", scEvent);

				scEvent += "_keypress";
				//console.log("Press: ", scEvent);
				//scInstance.gen(scEvent,data);
				
				data["name"] = scEvent;
				me.scInstance.gen("keypress_event",data);
			}
		},false)
		
		//add event listener when typing a char from event map
		container.addEventListener("keydown",function(e){
		//document.documentElement.addEventListener("keydown",function(e){
			//console.log("editor:", id,"document keydown", e.key)
			//in chrome we can only capture the ctrl key in down 
			var w = String.fromCharCode(e.which) || null;
			if(e.ctrlKey && shortcutEventMap[w]){
				var scEvent = "ctrl_" + shortcutEventMap[w] + "_keypress";
				e.preventDefault();
				var data = { "name" : scEvent} ;
				me.scInstance.gen("keypress_event",data);
			}
			
			else{	
				var scEvent = null;
				if (e.key){
					scEvent = eventKeyMap[e.key] || null;}
				else{
					scEvent = eventCodeMap[e.keyCode] || null; }
							
				if (scEvent != null){	
					e.preventDefault();
					scEvent += "_keypress";
					//console.log("Down: ", scEvent);
					//scInstance.gen(scEvent,e);
					var data = { "name" : scEvent} ;
					me.scInstance.gen("keypress_event",data);
				};
			}
		},false)
				
		//add event listeners for click and select
		
		//disable the context menu TODO uncomment this but for the moment needed to inspect elements and such
		//document.documentElement.addEventListener("contextmenu", function(e){e.preventDefault();}, true);
		
		var jQueryRoot = $(rootNode)//a jQuery object of the rootnode needed to calculate the offset
		//need to be a function because this might change depending on resize and all
		function getOffset(){
			var ret = { X :0 , Y : 0}
			var offset = jQueryRoot.offset(); 
			ret.X = Math.ceil(offset.left);
			ret.Y = Math.ceil(offset.top);
			return ret;
			
		}
		
		var mouseMoveListener = function(e){
			e.preventDefault();
			var o = getOffset();		
			var data  = { X : e.pageX - o.X, Y : e.pageY - o.Y};
			me.scInstance.gen("mouse_move",data);
		}
				
		rootNode.addEventListener("mousedown", function(e){
			//e.preventDefault(); don't prevent default , we won't be able to gain focus by click again , browser selection has been canceled trough use of CSS 
			if (e.button == 0){ // 0 WC3 for left button
				rootNode.addEventListener("mousemove" , mouseMoveListener , true);
				var o = getOffset();
				//clientX & Y will return the same value if the mouse stay where it is but the page scrolls down
				//var data  = { X : e.clientX - o.X, Y : e.clientY - o.Y}; 
				//we need page absolute coordinates
				var data  = { X : e.pageX - o.X, Y : e.pageY - o.Y}; 
				me.scInstance.gen("left_mouse_down", data);
			}
		}, false)
		
		rootNode.addEventListener("mouseup", function(e){
			e.preventDefault();
			if (e.button == 0){ // if left mouse button
				var o = getOffset()
				//clientX & Y will return the same value if the mouse stay where it is but the page scrolls down
				//var data  = { X : e.clientX - o.X, Y : e.clientY - o.Y}; 
				//we need page absolute coordinates
				var data  = { X : e.pageX - o.X, Y : e.pageY - o.Y}; 
				me.scInstance.gen("left_mouse_up",data);
	
				//console.log("remove listener");
				rootNode.removeEventListener("mousemove" , mouseMoveListener , true);
			}
		}, false)
		
	}
}