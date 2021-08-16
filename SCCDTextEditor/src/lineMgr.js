/**
@class LineManger
@description a class that handles the lines in the document. rearrangement after typing is done at this level
@param textNode the DOM element where the text is placed
@param displayMgr an instance of the DisplayManager class
@param initialText The text that will be set when we initialize or clear the LineManager
*/
function LineManager(textNode, displayMgr, initialText){
	var lines = [];
	var initText = (typeof(initialText) == "undefined")? "" : initialText;

		
	//returns the tspan a new line should be inserted before
	function toInsertBefore(line){
		var index = lines.indexOf(line);
		var ret = null;
		if ( (index != -1) && ((index+1) < lines.length) ){
			ret = lines[index+1].getTspan(0).getDOM();
		}
		return ret;
	}
	
	/** returns the DOM root of the text*/
	this.getTextDOMRoot = function(){
		return textNode;
	}
	
	/** clears the line manager */
	this.clear = function(){
		for (var i = 0; i < lines.length; i++){
			lines[i].removeFromDOM();
		}
		lines = [];
		this.createNewLine(0, initText);
	}
	
	/** returns the line at given position*/
	this.getLine = function(pos){
		return lines[pos];
	}
	
	/** returns the number of lines*/
	this.getLineCount = function(){
		return lines.length;
	}
	
	
	/** adds a Line after the given position and returns it
	@param afterPosition optional. the position after which we add the new Line, default at the end.
	@param initialText optional. the text the line is initialized with
	*/
	this.createNewLine = function(afterPos, initialText){
		pos = ( (typeof(afterPos) != "undefined") && (afterPos < lines.length)) ?  afterPos : lines.length-1;
				var text = ( typeof(initialText) == "undefined") ?  "" : initialText;
		var nLine = new Line(textNode, displayMgr, toInsertBefore,text);
		if (pos == lines.length-1){
			lines.push(nLine);
		}
		else{
			var first = lines.slice(0, pos+1);
			first.push(nLine);
			var end = lines.slice(pos+1);
			lines = first.concat(end);
		}
		
		index = lines.indexOf(nLine);
		lines[index].addToDOM(); //calls toInsertBefore and adds it to DOM  this MUST be called AFTER having added it to the array
		
		return lines[index];	
	}
	
	/** removes the line at pos*/
	this.removeLine = function(pos){
		lines[pos].removeFromDOM();
		var first = lines.slice(0, pos);
		var last = lines.slice(pos+1);
		lines = first.concat(last);
		
		//the line manager can never be empty, if need be create a line 0
		if (lines.length == 0){
			this.createNewLine(0, initText);
		}
	}
				
	this.init = function(){
		//create the first line
		this.createNewLine(0, initText);
	}
	
	this.init(); //call init
	
	/** returns the total height in pixels until the given line (the given line's height is not included)
	@param pos optional. The given line. if it is not given the total height of all lines is returned
	*/
	this.getTotalHeightUntil = function(pos){
		var r = this.getTotalDyUntil(pos);
		return ptToPixel(r);
	}
	
	/** returns the total height in pt (in function of of the max DY value of the line) until the given line (the given line's height is not included)
	@param pos optional. The given line. if it is not given the total height of all lines is returned
	*/
	this.getTotalDyUntil = function(pos){
		var y = ((typeof(pos) != "undefined") && (pos <= lines.length) ) ? pos :  lines.length;
		var sum = 0;
		for (var i = 0; i < y ;++i){
			sum += lines[i].getDy();
		}
		return sum;
	}
	
	/** return the width of the widest line  
	 @param ignoreLineBreak optional, default false. if true  returns the width of the line minus the line break
	 */
	this.getMaxLinesWidth = function(ignoreLineBreak){
		var bool = (typeof(ignoreLineBreak) == "undefined")? false : ignoreLineBreak;
		var max = lines[0].getLineWidth(bool);
		var w = 0;
		for (var i = 1 ; i < lines,length; i++){
			w = lines[i].getLineWidth(bool);
			if (w > max){
				max = v; 
			}
		}
		return max;
	}
	
	//converts pt to pixel
	function ptToPixel(pt){
		return Math.ceil((pt*16)/12);
	}
	
	/** returns the line at the given screen y position*/
	this.getLineFromY = function(y){
		var len = lines.length-1;
		var stop = false;
		var i = 0 
		var sum = 0; //TODO if we ever work with horizontal margins in the future this need to be adapted to the top Margin instead of 0 
		var pos = 0;
		var prevT, prevC;
		
		
				
		//if y is bigger then then the total height return the last line
		var total = ptToPixel(this.getTotalDyUntil());
		if ( total <= y){
			pos = len;
		}
		//if y is above the first line return the first line 
		//TODO if we ever work with horizontal margins in the future this need to be adapted to the top Margin instead of 0 
		else if (y <= 0){
			pos = 0;
		}
		//else search for it
		else{
			while ((i <= len) && !stop){
				prevL = ptToPixel(lines[i].getDy());
				sum+= prevL
				if (sum >= y){
					stop = true;
				}
				else{
					++i;
				}
			}
		
			/*the y value is the top of the cursor.
			  if it is equal to the height it means the user pressed in the line below it
			  if it is bigger it means the cursor was in the line we pressed in */
			pos = (sum == y)? i+1 :i ;
		}
		return pos;		
	}
	
	/** returns an Buffer with the content of the asked for selection 
	@param from start index {row, col} of the selection (included)
	@param to end index {row, col} of the selection ( col position not included)
	 */
	this.copySelection = function(from, to){
		var ret = new Buffer();
		if (from.row == to.row){
			ret = lines[from.row].copySelection(from.col, to.col);
		}
		else{
			//first line select starting from col until end of line
			var first = lines[from.row].copySelection(from.col);
			ret.appendBuffer(first);
			
			//between firrst and last line select everything
			for (var i = from.row+1; i < to.row; i++){
				var buf = lines[i].copySelection(0);
				ret.appendBuffer(buf);
			}
			
			//last line select from beginning until but not including  to.col
			var last = lines[to.row].copySelection(0,to.col);
			ret.appendBuffer(last);
		}
		return ret;
	}
	
	/** returns a map {row , col} with the postion at a distance offset from right to left	*/
	this.getPositionLeftOffset = function(rowPos, colPos, offset){
		var stop = false;
		var ret = {row: rowPos, col: colPos}
		
		var len = lines.length
		
		if (colPos < offset){
			offset -= colPos;
			ret.row -= 1
			//while the offset is bigger then the line go to the previous line and substract the length of the line from the offset
			while((ret.row >= 0)&&( stop == false)){
				if (lines[ret.row].getTextLength() < offset){
					offset -= lines[ret.row].getTextLength();
					ret.row -= 1;
				}
				else{
					//when the offset is no longer bigger then the line the offset = length - offset
					stop = true;
					ret.col = lines[ret.row].getTextLength()-offset;
				}
			}
			
			//if we stopped because we ran out of lines we simply return the first position of the first line
			if (!stop){
				ret.row = 0;
				ret.col =  0;
			}
		}
		else{
			//if the offset fits in the same line
			ret.col -= offset;
		}
		
		return ret;
	}
	
	/** rearrange the text after having added a line break	
	@param lineIndex the index of the line where we added the linebreak
	@pos the position in the line where the line break was added
	*/
	this.rearangeOnAddLB = function(lineIndex, pos){
		//this version contains no word wrap. each new line means it is preceded by a LB. therefore we do not need to do recursice checking and such
		//adding a line means cutting anything that comes after the enter and putting it in that new line. 
		
		var move = lines[lineIndex].cutSelection(pos+1);//cut everything after the line break
		if (!(move.isEmpty())){
			//creates a new line after the current one
			this.createNewLine(lineIndex);
			var line = lines[lineIndex+1];
			var len = move.getTspanCount();
			var pos = 0;
			for (var i = 0; i < len; i++){
				var t = move.getTspan(i)
				//wheter we add one character or a string it doesn't matter
				//the regular use case is just one char while typing but we can still use this method
				line.writeCharAt(t.getTextContent(), pos, t.getStyle())
				pos += t.getTextLength();
			}
		}
	}
	
	/** rearrange the text after having removed a line break
	@param lineIndex the line wher the lb war removed from
	*/
	this.rearangeOnRemoveLB = function(lineIndex){
		if (lineIndex < lines.length - 1){
			var move = lines[lineIndex+1].cutSelection(0);//cut the whole next line
			if (!(move.isEmpty())){
				var line = lines[lineIndex];
				var len = move.getTspanCount();
				var pos = line.getTextLength();
				for (var i = 0; i < len; i++){
					var t = move.getTspan(i)
					//whether we add one character or a string it doesn't matter
					//the regular use case is just one char while typing but we can still use this method
					line.writeCharAt(t.getTextContent(), pos, t.getStyle())
					pos += t.getTextLength();
				}
				this.removeLine(lineIndex+1); //now that all the text of the next line has been cut to this one we remove the line
			}
			
		}
	}
		
	/****************************************************************************/
	// Added for highlighting
	/****************************************************************************/
		
	/** returns a dictionary contacting relevant information about a word at the current position
	 *basically given a cursor position give the word the cursor is in and the information needed to check and select it.  
	 @param lineIndex: the line we are looking at
	 @param pos: the position of the cursor in the line
	 @return a dictionary {word, start, end}: where <br> 
	 word: is a copy of the word in a Buffer or null if pos doesn't contain a word<br>
	 start: is an integer the start position of the word<br>
	 end: is the end position of the word (not included)<br>
	 */
	 this.getWordInformationAtPos = function(lineIndex, pos){
		var line = lines[lineIndex];
		var text = line.getTextContent();
		var len = text.length;
		var ret = { word: null, start: -1, end: -1}
	    
		function getStartIndex(){
			var i = pos;
			var stop = false;
			var ret = -1;
			while((i >= 0) && !(stop)){
				var c = text[i];
				if (isLineBreak(c) || c == ' ' || c == '\t')
					stop = true;
				else
					i--;
			}
			
			if (stop == true){
				//if the current position is a space/tab/lb return -1
				//if (i != pos){
				    ret= i+1; //i is the position of the first non visible char encountered we want the last char of our loop
				//}
			}
			else{
				ret = 0;
			}
			return ret;
		}
		
		function getEndIndex(){
			var i = pos;
			i = (i > 0)? i : 0; //if len is 0 we dont want len-1 because that would start the while loop and give an exception
			var stop = false;
			var ret = -1;
			while((i < len) && !(stop)){
				var c = text[i];
				if (isLineBreak(c) || c == ' ' || c == '\t')
					stop = true;
				else
					i++;
			}
			
			if (stop == true){
				//if the current position is a space/tab/lb return -1
				//if (i != pos){
				    ret= i; //the end index should be the first non visible character because it isnt included in the selection anyway
				//}
			}
			else{
				ret = len;
			}
			return ret;
		}
		
		var startIndex = getStartIndex();
		var endIndex = getEndIndex();
				
		if (startIndex < endIndex) { //startIndex >= endIndex means that the given position is a space/tab/lb
			ret.start = startIndex;
			ret.end = endIndex;
			ret.word = line.copySelection(startIndex, endIndex);
		}
		return ret;
	}
	
	/** Sets the style of all the lines in the linemanager to the given style*/
	this.resetStyle = function(style){
		for (var i in lines){
			lines[i].resetLineStyle(style.copyDeep());
		}
	  
	}
}	