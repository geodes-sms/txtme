/**
 @class keywordList
 @description a very small data structure to save keywords list.
*/
function KeywordList(){
    var keywords = {};
    
    /** adds a keyword list
    @param name the name of the list. if a list already exists with that name it will be overwritten
    @param list the list of keywords to added
    @param style the highlight style associated with this list 
    */
    this.add = function(name, list, style){
		keywords[name] = { keywordslist: list , style: style.copyDeep()};
    }
    
    this.remove =function(name){
		delete keywords[name];
    }
    
    this.getList = function(name){     
		var ret = null;
        if (keywords[name] != "undefined")
			ret =  keywords[name].keywordsList;
		return ret;
    }
    
    
    this.getStyle = function(name){     
		var ret = null;
			if (keywords[name] != "undefined")
				ret =  keywords[name].style;
		return ret;
    }
    
    /**
     returns whether or not a keyword is in the list.
     @return  if found: a Style object. this is the style the keyword is highlighted in because in most use case this is what we want to do if found
              if not found: null
     */
    this.isInList= function(word){
	  var ret = null;
	  for (var key in keywords){
	      var list = keywords[key].keywordslist;
	      if (list.indexOf(word) > -1){
			ret = keywords[key].style;
			break;
	      }
	  }
	  return ret;
    }
}


/**
 @class HighlightMgr
 @description
 a class responsible for highlighting text.
 it will highlight keywords that appear in keywordlist in their respective styles.
 note that it is best that a keyword only appears in one list.
 @param theEditor the instance of the editor the highlightManager is responsible for 
 @param defaultSyle Optional The style that is considered default (not highlighted). if not provided the default style is the default style of the editor
 @param defaultHighlightSyle optional. the default style used to highlight keywords. if  not provided the default highlight style is bold blue
 */
//TODO rethink this whole thing there is much to much similarity in the code and the use case dont differ that much except for maybe one or two indices
function HighlightMgr(theEditor, defaultStyle, defaultHighlightStyle){
	
	var editor;
	var cursor;
	var lineMgr;
	var defHighStyle
	var defStyle;
	var keywordList;
	var errorBar;
	
	function init(){
		editor = theEditor;
		cursor = editor.getCursor();
		lineMgr = cursor.getLineManager();
		
		defStyle = (typeof(defaultStyle) != "undefined")? defaultStyle : new Style();
		
		blueStyle = defStyle.copyDeep();
		blueStyle.setColorRGB(0,0,238);
		blueStyle.setBold(true)
		
		defHighStyle = (typeof(defaultHighlightStyle) != "undefined")? defaultHighlightStyle : blueStyle;
		
		keywordList = new KeywordList();
		errorBar = null;
	}
	init();
	
	this.getDefaultStyle = function(){
		return defStyle;
	}
	
	this.getDefaultHighlightStyle = function(){
		return defHighStyle;
	}
	
	/** adds a keyword list
	 @param name the name of the list. if a list already exists with that name it will be overwritten
	 @param keywords the list of keywords to added (a list of strings)
	 @param highlightStyle optional. the style this particular list of keywords is highlighted in. if not provided the default hightlightsyle is used 
	 */
	this.addKeywordList = function(name, keywords, highlightStyle){
		var st = (typeof(highlightStyle) != "undefined")? highlightStyle : defHighStyle;
		keywordList.add(name, keywords, st);
	}
	/**Sets the error bar on which errors are going to be displayed*/
	this.setErrorBar = function(bar){
		errorBar = bar;
	}
	/** removes the given list*/
	this.removeKeywordList = function(name){
		keywordList.remove(name);
	}
	
	function withinBorders(row, col){
		return ( (row >= 0) && (row < lineMgr.getLineCount()) && 
			 (col >= 0) && (col <= lineMgr.getLine(row).getTextLength()) );
	}
	  
	function checkWord(rowI, colI){
		
		//console.log("keywords: ", keywordList.toString());
		if ( withinBorders(rowI,colI) ){
			//console.log("Whitin borders");
			var c = { row: rowI, col: colI};
			wordInfo = editor.getWordInformationAtCoord(c);
		    
			if (wordInfo.word != null){ //check that it is a word not a space/lb/tab
				var wordText = wordInfo.word.getTextContent();
				//console.log("check highlight typing: word NOT null: ", wordText);
				var styles = wordInfo.word.getContentStyles();
				var keyStyle = keywordList.isInList(wordText);
				
				if (keyStyle != null){ //if the word is 
				    //console.log("check highlight typing: word in list");
				    if ((styles.length > 1) || (styles[0].toString() != keyStyle)){
					editor.changeRangeStyle(wordInfo.start, wordInfo.end, keyStyle);
				    }
				}
				else{
				    //console.log("check highlight typing: word NOT in list");
				    if ((styles.length > 1) || (styles[0].toString() != defStyle)){
					editor.changeRangeStyle(wordInfo.start, wordInfo.end, defStyle);
				    }
				} // end if word in list
			} //end if word != null
		}
		
	} //end checkword
	
	
	this.checkKeywordsOnType = function(c, position){
		var coord = (typeof position === "undefined" ? cursor.getCoords() : position);
	    var ch = (typeof c === "number" ? String.fromCharCode(c) : c);
	    //console.log(keywordList);	

	    if (ch != " " && ch != "\t"){
			//var coord = cursor.getCoords();
			//the cursor is behind the newly added char we want to check the word the char belongs to
			//so first we check to the left of the cursor
			//note that checkWord performs range checks so nothing will happend if coord.col-1 = -1
			checkWord(coord.row, coord.col-1);
	    }
	    else{
			this.checkKeywordsOnSpace(coord);
	    } 
	}
	
	/** when removing characters*/
	this.checkKeywordsOnRemove = function(position){
					  
		var coord = (typeof position === "undefined" ? cursor.getCoords() : position);
		
		checkWord(coord.row, coord.col-1); // normal backspace + delete if we are a end of line  
		checkWord(coord.row, coord.col);//normal delete + backspace if we are at 0
		
		
		if ( coord.col == lineMgr.getLine(coord.row).getTextLength() ){
		  checkNextLine(coord.row);
		}
		
		if ( (coord.col == 1) || (coord.col == 0)){
		  checkPrevLine(coord.row);  
		}	
	} 
	
	//check the previous line
	function checkPrevLine(row){
		if (row > 0 && row-1 < lineMgr.getLineCount()){
			var line = lineMgr.getLine(row-1);
			var len = line.getTextLength();
			
			checkWord(row-1, len-1);
			checkWord(row-1, len-2); 
			/*due to wordwrap  the cursor might be in next line but newly added space in previous line
			or when checking after line breaks len- will be the lb while len-
			we need to check -2 to make sure will be the word*/
		}
	}
	
	function checkNextLine(row){
		if (row >= 0 && row+1 < lineMgr.getLineCount()){
			checkWord(row+1,0);
			checkWord(row+1,1);
		} 
	}
	
	/** the use case when adding a space*/
	this.checkKeywordsOnSpace = function(position){  	
		var coord = (typeof position === "undefined" ? cursor.getCoords() : position);
		//regular case check the word before and after the space
		checkWord(coord.row, coord.col-2);//before -2 because -1 is the position of the space itselef -2 of the character before it
		checkWord(coord.row, coord.col);// after
		
		//in the context of insert we also need to check the word on the right because 
		//in the context of ' dord' changing to ' word' in insert mode the word to check is the right one
		//TODO maybe create an extra parameter insert mode and call it with parameter for insert mode


		/*when typing visible characters or removing them the cursor is generally inside the word
		 or to the left or right of it at the very least
		 when adding space there is a possibility that it caused a split of words and even a change in lines
		 due to line rearrangement and wordwrap
		 */
		
		//if the cursor is not at the end of a line adding a whitespace might have caused a keyword to be at the beginning of next line
		if ( coord.col == lineMgr.getLine(coord.row).getTextLength() ){
		  checkNextLine(coord.row);
		}
		
		//we check the previous line 
		if ( (coord.col == 1) || (coord.col == 0)){
		  checkPrevLine(coord.row);  
		}
	} 
	
	/** the use case when adding a line break/new line*/
	this.checkKeywordsOnLB = function(){  	
		var coord = cursor.getCoords();
		checkPrevLine(coord.row); //before the new line
		checkWord(coord.row, coord.col);//after
	}  
	
	function adjustEndCoords(from, to){
		var end = null;
		if ((typeof to === "undefined") || (to == null)){
			end = { row: from.row, col : lineMgr.getLine(from.row).getTextLength()};
			if (end.row == lineMgr.getLineCount()-1){
				end.col -= 1; //we must never select the last character of the last line
			}
		} else {
			end = to;
		}
		//an end coordinate of row x col 0 means that is is the previous line
		//note that in that case we do not need to tocehck for last character since it has a previous line
		//of course we assume valid coordinateswere given in te first place
		if (end.col == 0){
			end.row -= 1;
			end.col = lineMgr.getLine(end.row).getTextLength();
		}
		return end
		  
	}
	
	
	function adjustStartCoords(coord){
		/*we are not allowed to start a selection with the last character of the text (that is the ireemoavalbe linebreak inserted to make sure the text is never empty)*/ 
		if ((coord.row == lineMgr.getLineCount() -1) && ( coord.col >= lineMgr.getLine(coord.row).getTextLength() -1 ) ){
			if (coord.col == 0){
				coord.row -= 1; //start becomes the last char of the previous line
				coord.col =  lineMgr.getLine(coord.row).getTextLength() -1 
			}
			else{
				coord.col -=1 // we simply take the before last character
			}
		}
		return coord
	}
	
	/** apply the following style to the given range
	 @param styleString a String, the style to apply aboce the current one
	 @param fromPos { col, row } the beginning of the range
	 @param toPos Optional. {col, row} the end position - not inlcuded - of the range, if not present it is the end of the fromPos.row
	 */
	this.applyStyle = function(styleStr, fromPos, toPos){
		var start = adjustStartCoords(fromPos);  
		var end = adjustEndCoords(start, toPos);
		editor.changeRangeStyle(start, end, styleStr);
	}
	
	/** apply the following style to the given range
	 @param errorMsg a String the error message to display for that range
	 @param fromPos Optional.{ col, row } the beginning of the range. if not provided the error is attached to line 1
	 @param toPos Optional. {col, row} the end position - not inlcuded - of the range, if not present it is the end of the fromPos.row
	 */
	this.applyError = function(errorMsg, fromPos, toPos){
		var listSymbol =String.fromCharCode(0x25a0) //0x25a0 = black square
		var msg = listSymbol + " " + errorMsg;
		var start = adjustStartCoords(fromPos);  
		var end = adjustEndCoords(start, toPos);
		editor.addRangeError(start, end);
		if (errorBar != null){
		  errorBar.addLineError(fromPos.row, msg);
		}
		else{
		  console.log("Error: ", errorMsg);
		} 
	}
	
	this.resetHighlights = function(){
		lineMgr.resetStyle(defStyle);
		if (errorBar != null){
		  errorBar.clearErrors();
		}
	}
	

}
