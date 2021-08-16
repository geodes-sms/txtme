/**
@class Tspan 
@description 
A wrapper around an SVG tspan<br/> 
In the editor this is the most basic element of the text. all letters in a tspan have the same style

@param style the style used in the Tspan ; default the default value of the style
@param initialText, the text that is put inside the tspan default ""
@param x the x attribute of the tspan (the absolute x position) if none is provide we assume a dx (relative position) of 0 and no x value (this means this will be placed directly next to a previous tspan)
@param dy the relative y position. This is basically the height the tspan will have in the document; should only have a non 0 value when its the first Tspan of the line otherwise it will be placed relatively to the one that comes before. 
*/
function Tspan(style, initialText, x, dy){
	var tspan;
	var style;

	//the constructor;
	init = function(){
		tspan = document.createElementNS(svgNS,"tspan");
		
		style = (typeof(style) == "undefined")? new Style() : style;

		tspan.setAttributeNS(null,"style", style.toString());
		//for some strange reason the css color property doesn't always seems to work; to be sure we use the color in fill
		tspan.setAttributeNS(null,"fill", style.getCurrentAttribute("color"));
		
		tspan.textContent = (typeof(initialText) == "undefined")?  "": initialText;	
		
		if(typeof(dy) == "undefined"){
			tspan.setAttributeNS(null,"dy",0);
		}
		else{
			tspan.setAttributeNS(null,"dy", dy);
		}
		
		if(typeof(x) == "undefined"){ 
			tspan.setAttributeNS(null,"dx",0);
		}
		else{
			tspan.setAttributeNS(null,"x",x);
		}
	}
	
	init();//call init
	
	/** returns the tspan DOM element*/
	this.getDOM = function(){
		return tspan;
	}
	
	/** returns the style of the Tspan*/
	this.getStyle = function(){
		return style;
	}
		
	/** returns a deep copy of the style and content of the tspan. not the coordinates */
	this.copyDeep = function(){
		var text = tspan.textContent;
		var st = style.copyDeep();
		var ret = new Tspan(st, text);
		return ret;
	}
	
	/** write a string c at pos
	 @param str the string to write
	 @param pos 0 means before the first and n for n > 1 means after the nth character
	 */
	this.writeStringAt = function(str, pos){
		//whatever the name says nothing prohibits us from writing an entire string instead of just a char
		//note that this is a bit idiotic, we could also simply rename writeCharAt to writeString at 
		//but i think that keeping writeChar as separate is better since we also have overwrite char
		this.writeCharAt(str, pos)
	}
		
	/** write a character 'c' at position 'pos'
	 @param c the character to write
	 @param pos 0 means before the first and n for n > 1 means after the nth character
	 */
	this.writeCharAt= function(c, pos){
		var text = tspan.textContent;
		var len = text.length
		tspan.textContent = text.substring(0, pos) + c + text.substring(pos, len);
	}
	
	/** overwrite a character 'c' at position 'pos'
	 @param c the character to write
	 @param pos the position of the character, the first character having index 0
	 */
	this.overWriteCharAt= function(c, pos){
		var text = tspan.textContent;
		var len = text.length
		tspan.textContent = text.substring(0, pos) + c + text.substring(pos+1, len)
	}
	
	/** removes the character at the given position
	@param pos the position of the character , the first character having index 0
	@return the removed character or the empty string
	*/
	this.removeCharAt = function(pos){
		var ret = "";
		if (tspan.textContent.length != 0){
			var text = "";
			ret = tspan.textContent[pos];	
			text = tspan.textContent.substring(0,pos) + tspan.textContent.substring(pos+1)
			tspan.textContent = text;
		}
		return ret
	}
	
	/** returns a Tspan with the content of the asked for selection 
	and removes the content from the current Tspan
	@param from start index of the selection (included)
	@param to optional. end index of the selection (not included); default value =  getTextLength()
	*/
	this.cutSelection = function(from, to){
		var posTo =  (typeof(to) == "undefined") ? tspan.textContent.length : to
		var text = tspan.textContent;
		
		var curTspanContent = text.substring(0,from) + text.substring(posTo);
		var newTspanContent = text.substring(from, posTo);
		
		tspan.textContent = curTspanContent;
	
		var newTspan = new Tspan(style.copyDeep(), newTspanContent);
		return newTspan;
	}
	
	/** returns a Tspan with the content of the asked for selection 
	@param from start index of the selection (included)
	@param to end index of the selection (not included); default value textContent.length
	*/
	this.copySelection = function(from, to){
		var posTo =  (typeof(to) == "undefined") ? tspan.textContent.length : to
		var text = tspan.textContent;
		
		var newTspanContent = text.substring(from, posTo);
		
		var newTspan = new Tspan(style.copyDeep(), newTspanContent);		
		return newTspan
	}
	
	/** sets an absolute position x; when x is set dx is removed.*/
	this.setX = function(newX){ 
		tspan.removeAttribute("dx"); 
		tspan.setAttributeNS(null,"x",newX);
	} 
	
	/** sets the dy attribute; basically the height of the line*/
	this.setDy= function(newDy){ 
		tspan.setAttributeNS(null,"dy",newDy);
	}
	/** set the dx attribute, the relative x position of a tspan to another; when dx is set x is removed*/
	this.setDx= function(newDx){
		tspan.removeAttribute("x"); 
		tspan.setAttributeNS(null,"dx",newDx); 
	}
	/** changes the style of the tspan*/
	this.setStyle = function(st){
		style = st;
		tspan.setAttributeNS(null,"style", style.toString());
		//for some strange reason the css color property doesn't always seems to work; to be sure we use the color in fill
		var temp = style.getCurrentAttribute("color")
		tspan.setAttributeNS(null,"fill", style.getCurrentAttribute("color"));
	} 

	/** returns the dy of the tspan */
	this.getDy = function(){
		return tspan.dy.baseVal.getItem(0).value;
	}
	
	/** returns the height of the tspan*/
	this.getHeight = function(){
		//it would seem that the height is always the same per font and size
		//no matter what character is used therefore we only check the first
		var len = tspan.textContent.length
		var height = (len > 0)? tspan.getExtentOfChar(0).height : 0;
		return height;
	} 
	
	/** returns the total the width of the tspan */
	this.getTotalWidth = function(){ 
		return this.getSelectionWidth(0);
	}
	
	/** returns a the width of the chosen interval
	@param from start index of the selection interval(included)
	@param to optional. end index of the selection interval (not included); default value getTextLength()
	*/
	this.getSelectionWidth = function(from, to){
		var f = ((typeof(from) == "undefined") || (from < 0)) ? 0 : from;
		var len = tspan.textContent.length
		var t = ((typeof(to) == "undefined") || (to > len)) ? len : to;
		
		var sum = 0;
		for (var i = f ;i < t; i++){
			sum += tspan.getExtentOfChar(i).width;
		}
		return sum;
	} 
	
	/** returns the length of the text*/
	this.getTextLength = function(){
		return tspan.textContent.length;
	}
	
	/** returns the text contained in the Tspan*/
	this.getTextContent = function(){
		return tspan.textContent;
	}
	
		
	/** returns true if the last character is a line break */
	this.endsWithLineBreak = function (){
		var len = tspan.textContent.length;
		var ch = tspan.textContent[len-1];
		return isLineBreak(ch);
	}
	
	/** returns if the Tspan is empty*/
	this.isEmpty = function(){
		return (tspan.textContent.length == 0);
	}
}