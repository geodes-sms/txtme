/**
@class Serializer
@description serializes the content of the line manager to a specific format
*/
function Serializer(){	
}

/** serialize to txt format 
@param lineMgr an instance of the LineManager class from which we read the text
*/
Serializer.serializeToTXT = function(lineMgr){
	var totLines  = lineMgr.getLineCount();
	var txt = "";
	var lineContent;
	var line;
	
	for (i = 0; i < totLines; i++){
		line = lineMgr.getLine(i);
		lineContent = line.getTextContent();
		//we make sure to print "\n", not \r or pilcrow
		if (line.endsWithLineBreak()){
			var l = lineContent.length;
			lineContent = lineContent.substring(0, l-1) + "\n";
		}
		txt += lineContent;
	}
	return txt;
}

/** serialize to txt format 
@param lineMgr an instance of the LineManager class from which we read the text
*/
Serializer.serializeToRTF = function(lineMgr){
	
	var fontTable = [];
	var colorTable = [];
	
	var curFont;
	var curFontSize;
	var curColor;
	
	var curItalic;
	var curUnder;
	var curBold;
	
	function toRtfRGBformat(color){
		var text = "\\red" + color.R.toString() + "\\green" + color.G.toString() + "\\blue" + color.B.toString();
		return text;
	}
	
	function  toRtfFont(str){
		//str can be a whole family we take the first one
		var regEx = /\'(.*?)\'/
		var s = regEx.exec(str)[0];
		//due to the can't look back in javascript regex we keep the ' '  
		//those are now removed
		return s.substring(1,s.length-1);
	}
	
	function fontTableToStr(){
		var ret = "{\\fonttbl"
		for (var i = 0; i < fontTable.length; i++){
			var font = "{\\f" + i.toString() + " " +fontTable[i] + ";}"
			ret += font;
		}
		ret += "}";
		return ret;
	}
	
	function colorTableToStr(){
		var ret = "{\\colortbl"
		for (var i = 0; i < colorTable.length; i++){
			var col = colorTable[i] + ";"
			ret += col;
		}
		ret += "}";
		return ret;
	}
	
	function initStyle(style){
		curFont = toRtfFont(style.getFontFamily());
		fontTable.push(curFont);
		curColor = toRtfRGBformat(style.getColorRGB());
		colorTable.push(curColor);
		curFontSize = style.getFontSizePt()*2;
		
		curBold = style.getBold();
		curItalic = style.getItalic();
		curUnder = style.getUnderline();
		
		
		tag = "\\f0\\cf0\\fs" + curFontSize.toString();
		if (curBold) {
			tag += "\\b";
		}
		if (curItalic) {
			tag += "\\i";
		}
		if (curUnder) {
			tag += "\\ul";
		}
		return tag;
	}
	
	function newStyle(style){
		var tag = "";
		
		var tBold = style.getBold();
		var tItalic = style.getItalic();
		var tUnder = style.getUnderline();
		
		if (tBold != curBold){
			//if the text was previously bold we close the bold property off else we now turn it on
			var b = (curBold == true)? "\\b0" : "\\b";
			curBold = tBold;
			tag += b;
		}
		if (tItalic != curItalic){
			var b = (curItalic == true)? "\\i0" : "\\i";
			curItalic = tItalic;
			tag += b;
		}
		if (tUnder!= curUnder){
			var b = (curUnder == true)? "\\ul0" : "\\ul";
			curUnder = tUnder;
			tag += b;
		}
		
		
		tFont = toRtfFont(style.getFontFamily());
		if (tFont != curFont){
			curFont = tFont;
			var index =  fontTable.indexOf(curFont);
			//if the font isn't in the table we add it
			if (index == -1){
				fontTable.push(curFont);
				index = fontTable.indexOf(curFont);
			}
			//we give the text current font by referencing to it using its position in the font table
			tag +="\\f" + index.toString();	
			
		}
		tColor = toRtfRGBformat(style.getColorRGB());
		if (tColor != curColor){
			curColor = tColor;
			var index =  colorTable.indexOf(curColor);
			if (index == -1){
				colorTable.push(curColor);
				index = colorTable.indexOf(curColor);
			}
			tag +="\\cf" + index.toString();	
			
		}
		tFontSize = style.getFontSizePt()*2;
		if (tFontSize != curFontSize){
			curFontSize = tFontSize;
			tag +="\\fs" + + curFontSize.toString();
		}
		return tag;
	}
		
	var linesTot  = lineMgr.getLineCount();
	var text= initStyle(lineMgr.getLine(0).getTspan(0).getStyle()) + " ";

	for (var i = 0; i < linesTot; i++){
		var line = lineMgr.getLine(i);
		var tspanTot = line.getTspansCount();
		var lineText = "";
		var tspan;
		
		for (var j = 0; j < tspanTot; j++){
			tspan = line.getTspan(j);
			content = tspan.getTextContent();
			
			var tag = newStyle(tspan.getStyle());
			tag = (tag == "")? "": tag + " "; //add space between tag and text
			lineText += tag;
			
			var c;
			for (var k = 0; k < content.length; k++) {
				c = content[k];
				code = c.charCodeAt(0);
				if (isLineBreak(c)){
					lineText += "\\par ";
				}
				//escape "\", "{", "}" or any char above 127
				else if ( (code == 92) || (code == 123) || (code == 125) || (code >  127) )
					lineText += "\\u"+code+"?";
				else{
					lineText += c;
				}
			} //for chars in a tspan
		}//for tspans in a line
		text += lineText;
	}//for lines in the line mgr
	
	var rtf = "{\\rtf1\\ansi\n" + fontTableToStr() +"\n" +colorTableToStr() + "\n" + text + "}";
	return rtf;
}

//
/** serialize to stand alone svg format 
@param lineMgr an instance of the LineManager class from which we read the text
*/
Serializer.serializeToSVG = function(lineMgr){
	var txt = "<?xml version=\"1.0\"?>\n"
	txt += "<svg  xmlns=\"http://www.w3.org/2000/svg\">\n"
	txt += "<text xml:space=\"preserve\" stroke=\"none\" y=\"0\" x=\"0\">\n";
	txt += lineMgr.getTextDOMRoot().innerHTML
	txt += "\n</text>\n</svg>"
	return txt;
}

/**
 @class Deserializer
 @description reads a laoded file and inputs it in the linemanager 
 */
function Deserializer(){
}

Deserializer.setHighlighter = function(high){
	highlighter = high;
	if (high == null || typeof(high) == 'undefined'){
		//define an empty object so that we don't break the code and do not need to check != null
		highlighter = function(){};
		highlighter.checkKeywordsOnType = function(){};
	}
}

/** deserialize from txt format 
@param lineMgr an instance of the LineManager class where we load the text to 
@param file the file content we read. A string
*/
Deserializer.fromTXT = function(lineMgr, file){
	//console.log("fromTXT start", (new Date()).getTime().toString());

	//console.log("load start", (new Date()).getTime().toString());
	var text = file;
	//if the text ends with an LB we don't add it because there is already a last LB
	var len = (isLineBreak(text[text.length-1]))? text.length - 2 : text.length - 1;
	//var line = lineMgr.getLine(0);
	var c;
	var pos = 0;
	var lineIndex = 0;
	var line = lineMgr.getLine(0);
	for (var i = 0; i <= len; i++){
		c= text[i];
		//line.writeCharAt(c, 0);
		if (isLineBreak(c) == false){
			line.writeCharAt(c, pos);
			pos++;
			highlighter.checkKeywordsOnType(c, {row: lineIndex, col: pos}); 
			//only need to check on char not for LB.
			//the word just before it we just check with this and there is nothing after yet
		}
		else{
			//create a new line after line index
			//a line already ends with a lb so we add the new  one at the beginning of the next one
			lineMgr.createNewLine(lineIndex, LINEBREAK_CHAR);
			
			lineIndex++;
			pos = 0;
			line = lineMgr.getLine(lineIndex);
		}
	}
	//console.log("load end", (new Date()).getTime().toString());
	//console.log("done loading");
  
}

/** deserialize from svg format 
@param lineMgr an instance of the LineManager class where we load the text to 
@param file the file content we read. A string
*/
Deserializer.fromSVG = function(lineMgr, file){
	//console.log("fromSVG start", (new Date()).getTime().toString());

	//console.log("load start", (new Date()).getTime().toString());
	var svgStr = file;
	
	var parser = new DOMParser();
	//var svgDoc = parser.parseFromString(svgStr, "image/svg+xml");
	var svgDoc = parser.parseFromString(svgStr, "text/xml");
	// returns a SVGDocument, which also is a Document.
	var tspans = svgDoc.getElementsByTagName("tspan");
	
	var len = tspans.length; 
	var t, text, styleStr;
	var c, tLen;
	
	var pos = 0;
	var lineIndex = 0;
	var line = lineMgr.getLine(0);
	
	for (var i = 0; i < len; i++){
		t = tspans[i]
		text = t.textContent;
		var style = new Style(); //this has to be declared new again because otherwise the other styles refer to the same object with new values
		style.fromString(t.getAttribute("style"));
		
		//if the text ends with an LB we don't add it because there is already a last LB
		tLen = ( (i==len-1) && isLineBreak(text[text.length-1]))? text.length - 2 : text.length - 1;
		//var line = lineMgr.getLine(0);
		for (var j = 0; j <= tLen; j++){
			c= text[j];
			if (isLineBreak(c) == false){
				line.writeCharAt(c, pos, style);
				pos++;
			}
			else{
				//lineMgr.createNewLine(lineIndex, LINEBREAK_CHAR); this will ignore style so we dont use this
				line.removeCharAt(pos);
				line.writeCharAt(LINEBREAK_CHAR, pos,style); //we overwirte the linebreak that is already there to be of the same style
				lineMgr.createNewLine(lineIndex, LINEBREAK_CHAR); //we create a newline with a lb in default style (if any text comes before it it will be change then)
				
				//lineMgr.createNewLine()
									
				lineIndex++;
				pos = 0;
				line = lineMgr.getLine(lineIndex);
				//line.writeCharAt(LINEBREAK_CHAR, 0, new Style()); 
				
			}
		}
	}

	//console.log("load end", (new Date()).getTime().toString());
	//console.log("done loading"); 
}