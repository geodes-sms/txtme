/**
 @class Buffer
 @descition a class wrapping a group of tspans. primarily used to add to and iterate over 
 TODO some refactoring it has a lot in common with line maybe give line and this the same bases class as long as private var can be accessed
 or simply add extra methods from buffer to line and remove this class
 */
function Buffer(){
	var tspanAr = [];
	
	/** clears the buffer*/
	this.clear = function(){ 
		tspanAr = [];
	}
	
	/** Appends the content of a buffer to this one*/
	this.appendBuffer = function(buf){
		var len = buf.getTspanCount()
		for (var i = 0; i < len; i++){
			tspanAr.push(buf.getTspan(i));
		}
	}
	
	/** appends a tspan at the end of the buffer*/
	this.append = function(tspan){
		tspanAr.push(tspan)
	}
	
	/** inserts a tspan at the begining of the buffer*/
	this.addAsFirst = function(tspan){
		var temp = [tpsan];
		tspanAr = temp.concat(tspanAr);
	}
	
	/** returns how many tspans are in the buffer*/
	this.getTspanCount = function(){
		return tspanAr.length;
	}
	
	/** return true if there are no tspans in the line or only one empty tspan	*/
	this.isEmpty = function(){
		return( (tspanAr.length == 0) || ( (tspanAr.length == 1) && tspanAr[0].isEmpty()) )
	}
	
	/** returns the text content of the buffer*/
	this.getTextContent = function(){
		var len = tspanAr.length
		var txt ="";
		for (var i =0; i < len ; i++){
			txt += tspanAr[i].getTextContent();
		}
		return txt;
		
	}
	
	/** returns the tspan position i or null if out of bound*/
	this.getTspan = function(i){
		var  ret = ((i >= 0) && (i < tspanAr.length))?  tspanAr[i] : null;
		return ret;
	}
	
	/** returns the length of the text in the buffer*/
	this.getTextLength = function(){
		var len = tspanAr.length
		var ret  = 0;
		for ( var i =0; i < len ; i++){
			ret += tspanAr[i].getTextLength();
		}
		return ret;
	}
	
	/** returns the character at position i or the last character if i is over bound*/
	this.getChar = function(i){
		var coord = getIndicesContainingPos(i);
		return tspanAr[coord.tsIndex].getTextContent()[coord.charIndex];
	}
	
	/** returns the style at position i or the style of the last character if i is over bound*/
	this.getStyle = function(i){
		var coord = getIndicesContainingPos(i);
		return tspanAr[coord.tsIndex].getStyle();
	}
	
	/** returns a list of all the styles the buffer contains*/
	this.getContentStyles = function(){
		var len = tspanAr.length
		var ret  = [];
		for ( var i =0; i < len ; i++){
		  ret.push(tspanAr[i].getStyle());
		}
		return ret;
	}
	
	/** change the complete style of the buffer
	 @see {changeStyleAttribute}*/
	this.changeContentStyles = function(nStyle){
		var len = tspanAr.length;
		//NOTE maybe we could apply the style only to the first tspan and then merge them
		//now thst they all have the same style.
		//on the otherhand merging will happen when pastin the content to the editor anyway
		for (var i = 0 ; i < len; i++){
			tspanAr[i].setStyle(nStyle.copyDeep());
		}
	}
	
	/** adds the style str to the style of the buffer; will overwrite the given attributes but keep the others the same
	 @see {changeStyleAttribute}*/
	this.changeContentStylesFromString = function(styleStr){
		var len = tspanAr.length;
		var st = null
		for (var i = 0 ; i < len; i++){
			st = tspanAr[i].getStyle().copyDeep();
			st.fromNormalString(styleStr)
			tspanAr[i].setStyle(st);
		}
	}
	
	this.setContentStyleToError = function(){
		var len = tspanAr.length;
		var st = null;
		var msg ="";
		var t = null;
		for (var i = 0 ; i < len; i++){
			t = tspanAr[i]
			st = t.getStyle();
			st.setErrorStatus(true);
			t.setStyle(st.copyDeep());
		}
	}
	
	/** returns the style and char at the given position in map {char, style}. slightly more efficient than calling them both separately and in most use cases we need them both
	 @return a dictionary/map : {char, style}
	 */
	this.getCharAndStyle = function(i){
		var coord = getIndicesContainingPos(i);
		var c = tspanAr[coord.tsIndex].getTextContent()[coord.charIndex];
		var s = tspanAr[coord.tsIndex].getStyle();
		return {char: c, style: s};
	}
	
	/*
	returns a map {tsIndex, charIndex} where tsIndex is the index of the tspan where the character is
	@param pos  the position of the character on the line. if pos is bigger than the line it will return the last character of the line 
	NOTE same as the method from line except that the only behavior here is pick right.
	in the context of a buffer we always want the first character of a next tspan instead of the last position of a previous one
	*/
	function getIndicesContainingPos(pos){ 
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
				//if there is a next tspan we want position 0 of the next tspan 
				if (i < len){
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
			ret.charIndex = tspanAr[len].getTextLength()-1;//note that in line we return getTextLength because we can write after the last character here we return the last character
		} 
		
		return ret;
	}
	
	/**
	 * NOTE SEEMS COMPLETELY USELESS can't calculate width through get extent if not in DOM  
	 * 
	 * return the width of the buffer
	 @param ignoreLineBreak optional, default false. if true  returns the width of the buffer minus the line break
	 */
	/*this.getWidth = function(ignoreLineBreak){
		var bool = (typeof(ignoreLineBreak) == "undefined")? false : ignoreLineBreak;
		var len = (bool && tspanAr[tspanAr.length-1].endsWithLineBreak()) ? tspanAr.length-1 : tspanAr.length;
		var ret  = 0;
		for (var i =0; i < len ; ++i){
			ret += tspanAr[i].getTotalWidth();
		}
		if (bool){
			var pos = tspanAr[len].getTextLength() -1;
			ret += tspanAr[len].getSelectionWidth(0,pos);	
		}
		return ret;
	}*/
	
	/** return true if the buffer ends with a line break*/
	this.endsWithLineBreak = function (){
		var arLen = tspanAr.length-1;
		return (tspanAr[arLen].endsWithLineBreak());
	}
	
	/** change the given style attribute of every tspan in the buffer to the value of that attribute in the new style
	@param nStyle the style whose attributevalue we want
	@param attr a string denoting a css attribute, the specific attribute whose value we want
	 */
	this.changeStyleAttribute = function(nStyle, attr){
		var len = tspanAr.length;
		for (var i = 0 ; i < len; i++){
			var s = copyStyleAttr(tspanAr[i].getStyle(),nStyle, attr);
			tspanAr[i].setStyle(s);
		}
	}
	
	/*
	returns a new (deep copy) style with one attribute changed to be the same value as the other style
	@param oStyle the orginal style (the one whose attribute we want to change)
	@param nStyle the style whose attribute we want to copy
	@param attr a string denoting a css attribute
	*/
	function copyStyleAttr(oStyle,nStyle, attr){
		var ret = oStyle.copyDeep();
		/*var attributes = {
			"font-family": function() { ret.setFontFamily(nStyle.getFontFamily()) },
			"font-size": function() { ret.setFontSizePt(nStyle.getFontSizePt()) },
			"color": function() { ret.setColorString(nStyle.getColorString()) },
			"font-weight" : function() { ret.setBold(nStyle.getBold()) },
			"font-style" : function() { ret.setItalic(nStyle.getItalic()) },
			"text-decoration" : function() { ret.setUnderline(nStyle.getUnderline()) }
			
		};
		if(attributes[attr]) {
			attributes[attr]();
		}*/
		if (nStyle.hasAttribute(attr))
		  ret.setAttribute(attr, nStyle.getAttribute(attr))
		return ret;
	}
}