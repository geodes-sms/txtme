/**
@class Line
@description a line in the document<br/>
as long as it appears on one line in the document it belongs here, it doesn't matter whether there is a line break at the end or not.<br/>
@param textNode the DOM element where the text is placed
@param displayMgr an instance of the DisplayManager class
@param toInsertBefore a function that returns a DOM node or null that tells where to insert the tspan before
it needs to be a function and not a variable , because the text keeps getting edited and that tspan will change over time
@param initialText the text to fill the line with
*/
function Line(textNode, displayMgr,toInsertBefore, initialText){

	var self = this;
	
	var tspanAr = []; //an array of Tspan
	var maxDy; //the biggest font size; used to set as the dy value of the first tspan
	
	var lMargin;
	var rMargin;
	 
	function init(){
		lMargin = displayMgr.getCurLMargin();
		rMargin = displayMgr.getCurRMargin();
		maxDy = displayMgr.getStyle().getFontSizePt();
		maxHeight = displayMgr.getCharHeight();
		
		//get the initial text if it is given
		var text = (typeof(initialText) == "undefined") ? "" : initialText;
		//create a new Tspan
		var curTspan = new Tspan(displayMgr.getStyle(), text , lMargin, maxDy.toString() +"pt");
		//add it to the array
		tspanAr.push(curTspan);		
	}
	init(); //call init
	
	/** adds the line to the DOM, MUST be called AFTER adding the line where we want to add it (like the line manager)*/
	this.addToDOM = function(){
		textNode.insertBefore(tspanAr[0].getDOM(), toInsertBefore(self));
	}
	/** removes each tspan from DOM*/
	this.removeFromDOM = function(){
		tspanAr.forEach(function(tspanCl){
			textNode.removeChild(tspanCl.getDOM());
		});
	}
		
	/** return true if the line ends with a line break*/
	this.endsWithLineBreak = function (){
		var arLen = tspanAr.length-1;
		return (tspanAr[arLen].endsWithLineBreak());
	}
	
	/** return true if the line ends with a space or tab character*/
	this.endsWithSpace = function (){
		var arLen = tspanAr.length-1;
		var text = tspanAr[arLen].getTextContent()
		var c = text[text.length-1];
		return (c == " " || c == "\t");
	}
	
	/** return true if the line begins with a space or tab character*/
	this.beginsWithSpace = function (){
		var text = tspanAr[0].getTextContent()
		var c = text[0];
		return (c == " " || c == "\t");
	}
	
	/** return true if there are no tspans in the line or only one empty tspan	*/
	this.isEmpty = function(){
		return( (tspanAr.length == 0) || ( (tspanAr.length == 1) && tspanAr[0].isEmpty()) )
	}
	
	/** returns the number of Tspan in the line*/
	this.getTspansCount = function(){
		return tspanAr.length;
	}
	
	/** returns the Tspan at the given position */
	this.getTspan = function(pos){
		return tspanAr[pos];
	}
	
	
	/** returns the right margin of the line*/
	this.getRightMargin = function(){
		return rMargin;
	}
	
	/** returns the right margin of the line*/
	this.getLeftMargin = function(){
		return lMargin;
	}
	
	
	/** writes the given character 'c' to position 'pos' on the line
	 @param c the character to write;
	 @param pos the position on the line
	 @param style optional. the style of the char. default value = get the style from the display manager
	 */
	this.writeCharAt = function(c, pos, style){
		var indices = getIndicesContainingPos(pos);
		var charStyle = (typeof(style) == "undefined")? displayMgr.getStyle() : style;
		curTspan = tspanAr[indices.tsIndex];
	
		//if the style of the tspan we want to add is the same as the current one simply add the text
		if (curTspan.getStyle().toString() == charStyle.toString()){
			curTspan.writeCharAt(c, indices.charIndex);
		}
		else{
			
			//if the current Tspan is empty
			if (curTspan.isEmpty()){
				curTspan.setStyle(charStyle);
				curTspan.writeCharAt(c ,0);
			}
			//if we are at the beginning of a Tspan
			else if (indices.charIndex == 0){
				addCharBefore(indices.tsIndex, c, charStyle);
			}
			//if we are at the end of a Tspan
			else if (indices.charIndex == curTspan.getTextLength()){
				addCharAfter(indices.tsIndex, c, charStyle);
			}
			//we are in the middle of a Tspan
			else{
				insertCharAt(indices , c, charStyle);
			}
			
			//despite our best effort the there can be cases where tspans with the same stlye are next to each other, merge them
			//mergeTspans();
			//we adjust the attributes again
			//updateHeight();
		}
		updateHeight();
	}
	
	/** adds the Tspan 't' to position 'pos' on the line
	 @param t the Tspan to add;
	 @param pos the position on the line
	 @param style optional. the style of the char. default value = get the style from the display manager
	 */
	this.addTspanAt = function(t, pos){
		//This method is analgous to writeharAt but needed for pasting purposes, because it uses a whole
	        //tspan 
		var indices = getIndicesContainingPos(pos);
		curTspan = tspanAr[indices.tsIndex];
	
		//if the style of the tspan we want to add is the same as the current one simply add the text
		if (curTspan.getStyle().toString() == t.getStyle().toString()){
			curTspan.writeStringAt(t.getTextContent(), indices.charIndex);
		}
		else{
			//if the current Tspan is empty
			if (curTspan.isEmpty()){
				curTspan.setStyle(t.getStyle()); 
				curTspan.writeStringAt(t.getTextContent() ,0);
			}
			//if we are at the beginning of a Tspan
			else if (indices.charIndex == 0){
				addTspanBefore(indices.tsIndex, t);
			}
			//if we are at the end of a Tspan
			else if (indices.charIndex == curTspan.getTextLength()){
				addTspanAfter(indices.tsIndex, t);
			}
			//we are in the middle of a Tspan
			else{
				insertTspanAt(indices , t);
			}
			
		}
		updateHeight();
	}
	
	/** removes the character at the given position 
	 @param pos the given position
	 @return the removed character or the empty string
	 */
	this.removeCharAt = function(pos){
		//true means we give priority to index 0 of right tspan rather than last index of previous tspan
		var indices = getIndicesContainingPos(pos, true);
		var ret = tspanAr[indices.tsIndex].removeCharAt(indices.charIndex);
		
		if (tspanAr[indices.tsIndex].isEmpty() && (tspanAr.length > 1)){
			//first remove from DOM
			textNode.removeChild(tspanAr[indices.tsIndex].getDOM());
			//then we remove it from the array
			var first = tspanAr.slice(0, indices.tsIndex);
			var last =  tspanAr.slice(indices.tsIndex+1);
			tspanAr = first.concat(last);
			
			if (tspanAr.length == 0){ //there has to be at least one tspan in the line
				init();
				tspanAr[0].getDOM().textContent == ""; //in case there was an inital text we dont want it as content
				this.addToDOM();//we can call this now because the index hasn't changed
			}
			
			//check to see if tspans can't be merged now that we have removed a tspan
			mergeTspans();	
			//if we have removed a Tspan there is a chance we have removed the Tspan with the biggest height in the line we therefore make sure to set the position of the line correctly
			updateHeight();
		}
		return ret;
	}
	
	/** returns the text style at the given position. If a position is between two styles it will return the left one by default.
	 * this behaviour can be changed by setting the optional parameter to true
	 @param pickRight a boolean: (optional) default false. pick the style to right of the position if true.
	 */
	this.getStyleAt = function(pos, pickRight){
		var rightBool = (typeof(pickRight) == "undefined")? false : pickRight;
		var indices = getIndicesContainingPos(pos, rightBool);
		return tspanAr[indices.tsIndex].getStyle();
	}
	
	/** gets the dy value of the line*/
	this.getDy = function(){
		return maxDy/1.0; //return divide by 1.0 to make sure its returned as a numeral instead of string
	}
	
	/** return the width of the line 
	 @param ignoreLineBreak optional, default false. if true  returns the width of the line minus the line break
	 */
	this.getLineWidth = function(ignoreLineBreak){
		var bool = (typeof(ignoreLineBreak) == "undefined")? false : ignoreLineBreak;
		var condition = (bool && this.endsWithLineBreak())
		var len = (condition)? tspanAr.length-1 : tspanAr.length;
		
		ret = 0;
		for (var i =0; i < len ; ++i){
			ret += tspanAr[i].getTotalWidth();
		}
		if (condition){
			var pos = tspanAr[len].getTextLength() -1;
			ret += tspanAr[len].getSelectionWidth(0,pos);	
		}
		return ret;
	}
	
	/** returns a Buffer with the content of the asked for selection and removes the content from the Line
	@param from start index of the selection (included)
	@param to end index of the selection (not included); default value end of the line 
	*/
	this.cutSelection = function(from, to){
		var length = this.getTextLength();
		var f = ((typeof(from) == "undefined") || (f < 0)) ? 0 : from;
		var t = ((typeof(to) == "undefined") || (t > length)) ? length : to;
		
		var start = getIndicesContainingPos(f, true);
		var end = getIndicesContainingPos(t);
		
		//we return the cut selection
		return cutHelper(start, end);
	}
		
	//a helper function for cut Selection
	function cutHelper (start, end){
		var ret= new Buffer();
		
		//we check to see if the end and start Tspans are the same
		if (start.tsIndex == end.tsIndex){
			ret.append(tspanAr[start.tsIndex].cutSelection(start.charIndex , end.charIndex));
			
			//if after the selection the tspan is now empty remove it from dom and from the array
			if (tspanAr[start.tsIndex].isEmpty()){
				textNode.removeChild(tspanAr[start.tsIndex].getDOM()); 
				var first = tspanAr.slice(0,start.tsIndex);
				var last = tspanAr.slice(start.tsIndex+1);
				tspanAr = first.concat(last);
			}
		}
		else{
			var removeStart = false;
			var removeEnd = false;
			
			//for the start Tspan get the selection from the start
			ret.append(tspanAr[start.tsIndex].cutSelection(start.charIndex));
			if (tspanAr[start.tsIndex].isEmpty()){ //if it is now empty remove it from DOM and remember to remove it with te rest from the array later
				textNode.removeChild(tspanAr[start.tsIndex].getDOM());
				removeStart = true; 
			}			
			
			//for the Tspans between the start and the end just copy the whole thing, and remove them from DOM
			for( var i = start.tsIndex + 1 ; i <= end.tsIndex -1 ; i++ ){
				ret.append(tspanAr[i]);
				textNode.removeChild(tspanAr[i].getDOM());
			}
			
			//for the last Tspan take the selection from 0 to the given charIndex
			ret.append(tspanAr[end.tsIndex].cutSelection(0,end.charIndex));
			if (tspanAr[end.tsIndex].isEmpty()){ //if it is now empty remove it from DOM and remember to remove it with te rest from the array later
				textNode.removeChild(tspanAr[end.tsIndex].getDOM());
				removeEnd = true; 
			}
			
			//we now remove the Tspans from the Tspan array
			var firstInd = removeStart? start.tsIndex : start.tsIndex+1;
			var lastInd = removeEnd? end.tsIndex +1 : end.tsIndex;
			
			var first = tspanAr.slice(0,firstInd);
			var last = tspanAr.slice(lastInd);
			tspanAr = first.concat(last);
			
			//check to see if tspans can't be merged now that we have removed tspan(s)
			mergeTspans();	
		}
		
		//there has to be at least one tspan in the line
		if (tspanAr.length == 0){ 
			init();
			tspanAr[0].getDOM().textContent == ""; //in case there was an initial text we don't want it as content
			//we can call this now because the index hasn't changed
			//can't call addToDOM because public so we call the inside of the method
			textNode.insertBefore(tspanAr[0].getDOM(), toInsertBefore(self));
		}
		
		//if we have removed a Tspan there is a chance we have removed the Tspan with the biggest height or the first in the line we therefore make sure to set the position of the line correctly
		updateHeight();
		return ret;
	}
	
	/** returns a Buffer with the content of the asked for selection 
	@param from start index of the selection (included)
	@param to end index of the selection (not included); default value end of the line 
	*/
	this.copySelection = function(from, to){
		var length = this.getTextLength();
		var f = ((typeof(from) == "undefined") || (f < 0)) ? 0 : from;
		var t = ((typeof(to) == "undefined") || (t > length)) ? length : to;
		
		var start = getIndicesContainingPos(f, true);
		var end = getIndicesContainingPos(t);
				
		return  copyHelper(start, end);; 
	}
	
	//does the actual copying for indices
	function copyHelper(start, end){
		var ret= new Buffer();
		
		//we check to see if the en and start Tspans are the same
		if (start.tsIndex == end.tsIndex){
			ret.append(tspanAr[start.tsIndex].copySelection(start.charIndex , end.charIndex));
		}
		else{
			ret.append(tspanAr[start.tsIndex].copySelection(start.charIndex));
			//for the Tspans between the start and the end just copy the whole thing, and remove them from DOM
			for( var i = start.tsIndex + 1 ; i <= end.tsIndex -1 ; i++ ){
				ret.append(tspanAr[i].copyDeep());
				//ret.append(tspanAr[i])
			}
			//for the last Tspan take the selection from 0 to the given charIndex
			ret.append(tspanAr[end.tsIndex].copySelection(0,end.charIndex));
		}
		return ret;
	}
		
	/** returns a the width of the chosen interval
	@param from start index of the selection interval(included)
	@param to optional. end index of the selection interval (not included); default value getTextLength()
	*/
	this.getSelectionWidth = function(from, to){
		var ret = 0;
		var length = this.getTextLength();
		var f = ((typeof(from) == "undefined") || (from < 0)) ? 0 : from;
		var t = ((typeof(to) == "undefined") || (to > length)) ? length : to;
		
		if ( (f == 0) && (t >= this.getTextLength() ) ){
			ret = this.getLineWidth();
		}
		else{
			//for the start of a selection we want position 0 of the next tspan instead of the last position of a previous tspan 
			var start = getIndicesContainingPos(f, true);
			var end = getIndicesContainingPos(t);
			
			
			//if they are in the same tspan
			if (start.tsIndex == end.tsIndex){
				ret = tspanAr[start.tsIndex].getSelectionWidth(start.charIndex, end.charIndex);
			}
			else{
				//get the width of the start index
				ret = tspanAr[start.tsIndex].getSelectionWidth(start.charIndex);
				//get the width of the whole tspans between start and end
				for (var j = start.tsIndex+1 ; j <= end.tsIndex-1 ; j++){
					ret += tspanAr[j].getTotalWidth(); 
				}
				//get the width of the end index
				ret += tspanAr[end.tsIndex].getSelectionWidth(0,end.charIndex);
			} 		
		}
		return ret;
	}
	
	/** returns true of if at least one character except the line break is over the current right margin
	 @param offset optional default 0. an extra width to take into account. 
	 used to calculate if the current line width + the offset will be over the right margin.
	 */
	this.isOverRightMargin = function(offset){
		var ofs = (typeof(offset) == "undefined") ? 0 : offset;
		var width = this.getLineWidth(true); //the line break is allowed over the margin.
		var expression = ((lMargin + width) + ofs > rMargin);
		return expression;
	}
	
	/*
	returns a map {tsIndex, charIndex} where tsIndex is the index of the tspan where the character is
	@param pos  the position of the character on the line. if pos is bigger than the line it will return the last position of the last tspan 
	@param pickRight optional boolean. default false. When a position falls between two Tspans A an B. we can either return the last position in A (left  from the position) or 0 in B
	(right from the position) the default behavior is left. by setting this to true we pick right.
	*/
	function getIndicesContainingPos(pos, pickRight){ 
		var rightBool = (typeof(pickRight) == "undefined")? false : pickRight;
		var ret = {tsIndex : -1 , charIndex: -1}
		var len = tspanAr.length-1
		var stop = false
		var i = 0;
		var sum = 0;
		var temp;
		
		while ((i <= len) && !stop){
			sum+= tspanAr[i].getTextLength();
			if (sum >= pos){
				stop = true;
				ret.tsIndex = i;
			}
			else{
				++i;
			}
		}
		if (stop){

			//if the position == the total length it means the relative position we want is either the last character of the given tspan
			//or the first of the next is there is a next
			if (pos == sum){
				//if there is a next tspan and we give priority to the right of the position then we want position 0 of the next tspan 
				if (rightBool && (i < len)){
					ret.tsIndex += 1;
					ret.charIndex = 0;
				}
				else{ //the position is after the last character of that tspan
					ret.charIndex = tspanAr[i].getTextLength();
				}
			}
			//if it is in the first tspan the position in the line is the same as in the tspan
			//note that we only check this after we checked pos == sum because checking this first
			//would return the wrong tspan if the position was the last character of the first tspan
			//and the behavior was set to right
			else if (i == 0){
				ret.charIndex = pos;
			}
			else{
				//the relative position = the absolute position - the total length of all tspans until, but not including, the length of the tspan the character is in)
				temp = tspanAr[i].getTextLength();
				ret.charIndex = pos - ( sum - temp); 
			}
		}
		else{
			ret.tsIndex =len;
			ret.charIndex = tspanAr[len].getTextLength();
		} 
		
		return ret;
	}
	
	/** returns the plain text content of the entire line*/
	this.getTextContent = function(){
		var len = tspanAr.length
		var txt ="";
		for (var i =0; i < len ; i++){
			txt += tspanAr[i].getTextContent();
		}
		return txt;
	}
	
	/** returns the number of characters in the entire line */
	this.getTextLength = function(){
		var len = tspanAr.length
		var ret  = 0;
		for ( var i =0; i < len ; i++){
			ret += tspanAr[i].getTextLength();
		}
		return ret;
	}
	
	//returns true if the last tspan consist of a single lb char
	function lastTspanIsSingleLB(){
		var len = tspanAr.length -1;
		var tspan = tspanAr[len];
		return ( (tspan.getTextLength() == 1) && isLineBreak(tspan.getTextContent()[0]) )
	}
	
	//checks every Tspan and gets the maximum height */
	function updateHeight(){
		var len = tspanAr.length
		if ( 0 < len){
			var dy = 0;
			var height = 0;
			var singleLB = lastTspanIsSingleLB(); // set to true if the last tspan is a single LB
			for (var i = 0; i < len; i++){
				if (tspanAr[i].getStyle().getFontSizePt()/1 > dy){ //div by 1 to force numerical value TODO maybe 1.0 to force float ?
					//We want to avoid the situation where a linebreak character has its own style and is bigger than the rest(this can happen due to remove)
					//in that case  we want the newline to have the same hight as the maximum height
					//we do not need to do all those checks if there is only one tspan (the linebreak might even be the only character)
					//if ( (i == len-1) && (len  > 1 ) && (lastTspanIsSingleLB() == true)  { /* pass*/}
					
					// in the regular case or if lb is the only character we set dy to be the new maxheight
					if ( (i != len-1) || (len  <= 1 ) || (singleLB == false))  {
						dy = tspanAr[i].getStyle().getFontSizePt();
					}
				}
			}
			maxDy = dy;
			
			/*we set the lb at the end to be as high as the rest of the line 
			this is actually only needed if the LB is visible (the pilcrow sign)*/
			if (singleLB){ 
				var st = tspanAr[len-1].getStyle();
				st.setFontSizePt(maxDy);
				tspanAr[len-1].setStyle(st);
			}
			
			tspanAr[0].setX(displayMgr.getCurLMargin());
			tspanAr[0].setDy(maxDy.toString()+'pt');
		}
	}
	
	//check if there are tspans next to each other with the same style that can be merged into one
	function mergeTspans(){
		if ( tspanAr.length > 1){
			var i = 0;
			var len;
			var first = [];
			var end = [];
			while( (i+1) < tspanAr.length) {
				if (tspanAr[i].getStyle().toString() == tspanAr[i+1].getStyle().toString()){
					//merge the tspans
					len = tspanAr[i].getTextLength();
					tspanAr[i].writeStringAt(tspanAr[i+1].getTextContent() , len);
					
					//remove tspan i+1 from DOM and from the array
					textNode.removeChild(tspanAr[i+1].getDOM());
					first = tspanAr.slice(0, i+1);
					end = tspanAr.slice(i+2);
					tspanAr = first.concat(end);
				}
				else{
					i++;
				}
			}
		
		}
	}
	
	///////// Write Char Helpers //////////
	
	//adds the new character before the Tspan at index tsIndex  
	function addCharBefore(tsIndex , c, style){
		//first we check to see if there is a previous Tspan with the same style
		if ( ((tsIndex-1) >= 0) && (tspanAr[tsIndex-1].getStyle().toString() == style.toString()) ){
			//if that is the case add the text at the end of that tspan
			var len = tspanAr[tsIndex-1].getTextLength();
			tspanAr[tsIndex-1].writeCharAt(c, len); 
		}
		//else we need to insert the Tspan before the current one
		else{
			//if we are going to insert before 0 it is no longer the first tspan, set the attributes accordingly
			if (tsIndex == 0){
				tspanAr[0].setDy(0);
				tspanAr[0].setDx(0);
			}
			
			var bef = tspanAr[tsIndex].getDOM();
			var ts = new Tspan(style,c);
			textNode.insertBefore(ts.getDOM(), bef); //add it to DOM	
			
			//add it to the array
			var first = tspanAr.slice(0, tsIndex);
			first.push(ts);
			var end = tspanAr.slice(tsIndex);
			tspanAr = first.concat(end);	
		}
	}
	
	//adds the new character after the Tspan at index tsIndex  
	function addCharAfter(tsIndex , c, style){
		//first we check to see if there is a next Tspan with the same style
		if ( ((tsIndex+1) < tspanAr.length) && (tspanAr[tsIndex+1].getStyle().toString() == style.toString()) ){
			//if that is the case add the text at the beginning of that tspan
			tspanAr[tsIndex+1].writeCharAt(c, 0); 
		}
		//else we need to insert the text after the current one
		else{
			var bef = ((tsIndex+1) < tspanAr.length)? tspanAr[tsIndex+1].getDOM() : toInsertBefore(self);
			var ts = new Tspan(style, c);
			textNode.insertBefore(ts.getDOM(), bef); //add it to DOM	
			//add it to the array
			var first = tspanAr.slice(0, tsIndex+1);
			first.push(ts);
			var end = tspanAr.slice(tsIndex+1);
			tspanAr = first.concat(end);	
		}
	}
	
	
	//insert the character in the given tspan at the given position
	function insertCharAt(indices , c, style){
		var curTspan = tspanAr[indices.tsIndex];
		
		var splitTspan = curTspan.cutSelection(indices.charIndex);//we split the current tspan in curTspan + splitTspan 
		var bef = ((indices.tsIndex+1) < tspanAr.length)? tspanAr[indices.tsIndex+1].getDOM() : toInsertBefore(self); //if there is a next Tspan take it as the one to add before else we ask for the tspan we need to add before
		textNode.insertBefore(splitTspan.getDOM(), bef); //add the split to DOM
		var newTspan = new Tspan(style, c); //create a new Tspan with the char
		textNode.insertBefore(newTspan.getDOM(), splitTspan.getDOM()); //we add the new tspan to the DOM before the split tspan
		
		//we now update the Tspan array
		var first = tspanAr.slice(0,indices.tsIndex+1);
		first.push(newTspan);
		first.push(splitTspan);
		var end = tspanAr.slice(indices.tsIndex+1);	
		tspanAr = first.concat(end);
	}
	
	///////// Write Char Helpers END //////////
	
	///////// Write Tspan Helpers //////////
	
	//adds the given Tspan before the Tspan at index tsIndex  
	function addTspanBefore(tsIndex , t){
		//first we check to see if there is a previous Tspan with the same style
		if ( ((tsIndex-1) >= 0) && (tspanAr[tsIndex-1].getStyle().toString() == t.getStyle().toString()) ){
			//if that is the case add the text at the end of that tspan
			var len = tspanAr[tsIndex-1].getTextLength();
			tspanAr[tsIndex-1].writeStringAt(t.getTextContent(), len); 
		}
		//else we need to insert the Tspan before the current one
		else{
			//if we are going to insert before 0 it is no longer the first tspan, set the attributes accordingly
			if (tsIndex == 0){
				tspanAr[0].setDy(0);
				tspanAr[0].setDx(0);
			}
			
			var bef = tspanAr[tsIndex].getDOM();
			//var ts = t.copyDeep() 
			textNode.insertBefore(t.getDOM(), bef); //add it to DOM	
			
			//add it to the array
			var first = tspanAr.slice(0, tsIndex);
			first.push(t);
			var end = tspanAr.slice(tsIndex);
			tspanAr = first.concat(end);	
		}
	}
	
	//adds the given Tspan after the Tspan at index tsIndex  
	function addTspanAfter(tsIndex , t){
		//first we check to see if there is a next Tspan with the same style
		if ( ((tsIndex+1) < tspanAr.length) && (tspanAr[tsIndex+1].getStyle().toString() == t.getStyle().toString()) ){
			//if that is the case add the text at the beginning of that tspan
			tspanAr[tsIndex+1].writeStringAt(t.getTextContent(), 0); 
		}
		//else we need to insert the text after the current one
		else{
			var bef = ((tsIndex+1) < tspanAr.length)? tspanAr[tsIndex+1].getDOM() : toInsertBefore(self);
			//var ts = t.copyDeep()
			textNode.insertBefore(t.getDOM(), bef); //add it to DOM	
			//add it to the array
			var first = tspanAr.slice(0, tsIndex+1);
			first.push(t);
			var end = tspanAr.slice(tsIndex+1);
			tspanAr = first.concat(end);	
		}
	}
	
	//insert the given Tspan inside the Tspan at the given index at the given position
	function insertTspanAt(indices , t){
		var curTspan = tspanAr[indices.tsIndex];
		
		var splitTspan = curTspan.cutSelection(indices.charIndex);//we split the current tspan in curTspan + splitTspan 
		var bef = ((indices.tsIndex+1) < tspanAr.length)? tspanAr[indices.tsIndex+1].getDOM() : toInsertBefore(self); //if there is a next Tspan take it as the one to add before else we ask for the tspan we need to add before
		textNode.insertBefore(splitTspan.getDOM(), bef); //add the split to DOM
		//var newTspan = new Tspan(style, c); //create a new Tspan with the char
		//var ts = t.copyDeep() ?
		textNode.insertBefore(t.getDOM(), splitTspan.getDOM()); //we add the new tspan to the DOM before the split tspan
		
		//we now update the Tspan array
		var first = tspanAr.slice(0,indices.tsIndex+1);
		first.push(t);
		first.push(splitTspan);
		var end = tspanAr.slice(indices.tsIndex+1);	
		tspanAr = first.concat(end);
	}
	
	///////// Write Tspan Helpers END //////////
	
	/** returns the screen X value of the char at the given position*/
	this.calculateX = function(pos){
		var ret = lMargin; //we start at the left margin. for the moment it is 0 but this might change in the future
		var indices = getIndicesContainingPos(pos);
		if (indices.tsIndex == 0){
			ret += tspanAr[0].getSelectionWidth(0,pos); 
		}
		else{
			//for every full tspan take the sum of the widths
			for(var i = 0; i < indices.tsIndex; i++){
				ret += tspanAr[i].getTotalWidth();
			}
			//then add the width from the beginning of the tspan were the position is until that position
			ret += tspanAr[indices.tsIndex].getSelectionWidth(0,indices.charIndex);
		}
		return ret
	}
	
	/** returns the position of the character that falls on the given x value*/
	this.getColFromX = function(x){
	 	var len = tspanAr.length-1;
		var stop = false;
		var i = 0 
		var sum = lMargin; //we start at the left margin
		var linePos = 0;
		var pos = 0 ;
		var prevT, prevC;
				
		//if the the width starting from the left margin doesn't reach x, return the last position on the line
		if ((this.getLineWidth() + lMargin) < x){;
			pos = this.getTextLength();
		}
		//if the x is behind the left margin or equal to it return the first position on the line
		else if (x <= lMargin){
			pos = 0;
		}
		//if it reaches it search for it
		else{
			//first find out in wich Tspan we are
			while ((i <= len) && !stop){
				prevT = tspanAr[i].getTotalWidth();
				sum+= prevT
				if (sum >= x){
					stop = true;
				}
				else{
					++i;
				}
			}
			if (sum == x){
				for (var k = 0; k <= i; k++){
					pos += tspanAr[k].getTextLength();
				}	
			}
			//if it is bigger
			else{ 
				sum -= prevT //if the width is bigger remove the width of the previous tspan and now check character by character
				var lenTspan = tspanAr[i].getTextLength()-1;
				var j = 0;
				stop = false;
				while ((j <= lenTspan) && !stop){
					prevC = tspanAr[i].getDOM().getExtentOfChar(j).width; 
					sum+= prevC
					if (sum >= x){
						stop = true;
					}
					else{
						++j;
					}
				}
				
				for (var k = 0; k < i; k++){ //notice the smaller then i not smaller or equal
					pos += tspanAr[k].getTextLength();
				}	
				
				//the position is now chosen by closeness 			
				pos = ((sum-x) <= x-(sum-prevC)) ? pos+j+1 : pos+j;

			}
		}
		return pos;
	}
	
	/**METHOD ADDED FOR STYLE HIGHLIGHTING ETC*/
	
	/** sets the style of the entire line to one style*/
	this.resetLineStyle = function(style){
		if ( tspanAr.length >= 1){
			//set the style on the first tspan
			tspanAr[0].setStyle(style);
			
			//merge the other tspans by copying the text content to the first one and removing them from DOM
			if ( tspanAr.length > 1){
				var len = tspanAr[0].getTextLength();
				var first = [];
				var end = [];
				var i = 1
				while( i < tspanAr.length) {
				      //merge the tspans
				      tspanAr[0].writeStringAt(tspanAr[i].getTextContent() , len);
				      len += tspanAr[i].getTextLength();
				      //remove tspan i from DOM and from the array
				      textNode.removeChild(tspanAr[i].getDOM());
				      i++
				}
			
			}
			tspanAr = tspanAr.slice(0,1)
		}
	}
} 