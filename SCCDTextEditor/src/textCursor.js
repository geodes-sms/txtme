/**
@class TextCursor
@description the text cursor of the editor
@param cursorNode the cursor SVG DOM element
@param lineMgr an instance of the LineManager class
@param displayMgr an instance of the DisplayManager class 
@param startRow the row where the cursor will be
@param startCol the position on the row where the cursor will be
*/
function TextCursor(cursorNode, lineMgr, displayMgr, startRow, startCol){
	var colNum, rowNum; //the relative coordinate
	var screenX, screenY; //the screen (absolute ) coordinates

	function init(){
		colNum = (typeof(startCol) == "undefined") ? 0 : startCol;
		rowNum = (typeof(startRow) == "undefined") ? 0 : startRow;
		
		updateCoords();
	}	
	init();
	
	//NOTE remove this and give the line manager directly  to the editor
	/** return the LineManager instance the text cursor is associated with*/
	this.getLineManager = function(){
		return lineMgr;
	}
	
	/** return the current cursor coordinates in a map {row , col}*/
	this.getCoords = function(){
		var ret = {row : rowNum , col : colNum};
		return ret;
	}
	
	/** return the current cursor screen coordinates in a map {x , y}
	the coordinates are relative to the SVG root node and in pixel units
	*/
	this.getXYCoords = function(){
		var ret = { x : screenX , y : Math.ceil((screenY*16)/12)};
		return ret;
	}
		
	//returns the y value on screen of the given relative row position
	function getY(){
		var y =  lineMgr.getTotalDyUntil(rowNum); 
		//the cursor is placed relative to the top of the line we need to correct it to be to the bottom
		var delta = lineMgr.getLine(rowNum).getDy() - lineMgr.getLine(rowNum).getStyleAt(colNum).getFontSizePt();

		return y + delta;
	}
	
	//returns the x value on screen of the given relative col position
	function getX(col){
		return lineMgr.getLine(rowNum).calculateX(colNum);
	}
	
	//returns the relative x position (column) for a given screen x 
	function getColFromX(x){
		return lineMgr.getLine(rowNum).getColFromX(x);
	}
	
	//returns the relative y position (line number) for a give screen y
	function getRowFromY(y){
		return lineMgr.getLineFromY(y);
	}
	
	//sets the cursorNode at the given position on the screen
	function setCursorPos(x,y){
		cursorNode.setAttributeNS(null,"x",x);
		cursorNode.setAttributeNS(null,"y",y);
	}
	
	//update the coordinates
	function updateCoords(){
		screenY = getY();
		screenX = getX();
		//setCursorPos(screenX, screenY);
		setCursorPos(screenX, screenY.toString()+"pt");
	}
	
	//we are not allowed to place the cursor directly after a LB on click
	//nor are we allowd to put the cursor in a negative collumn or row
	function applyConstraints(){
		if (colNum < 0){
			colNum = 0;
		}
		
		if (rowNum < 0){
			rowNum = 0;
		}
	  
		var line = lineMgr.getLine(rowNum)
		if ((line.getTextLength() == colNum) && line.endsWithLineBreak()){
			colNum -= 1;
		}
	}
	
	/** move the cursor to the correct position in the text given the screen coordinates
	@param x the x coordinate on the screen 
	@param y the y coordinate on the screen 
	*/
	this.moveToScreenCoords = function(x,y){
		rowNum = getRowFromY(y);
		colNum = getColFromX(x);
		applyConstraints();
		updateCoords();
	}
	
	/** move the cursor to given row and column */
	this.moveToRowCol = function(row , col){
		rowNum = row;
		colNum = col;
		applyConstraints();
		updateCoords();
	}
	
	/** move the cursor one position up*/
	this.moveUp = function(){
		if (rowNum > 0){
			rowNum -= 1; 
			colNum = getColFromX(screenX);
			applyConstraints();
		}
		updateCoords();
	}
	
	/** move the cursor one position down*/
	this.moveDown = function(){
		if (rowNum < lineMgr.getLineCount()-1){
			rowNum += 1; 
			colNum = getColFromX(screenX);
			applyConstraints();
		}
		updateCoords();
	}
	
	/** move the cursor one position to the left*/
	this.moveLeft = function(){
		if (colNum != 0) { 
			colNum -= 1;
		}
		else if(rowNum != 0){ //if it is 0 but this isn't the first line go to the end of previous line
			rowNum -= 1;
			var line = lineMgr.getLine(rowNum);
			var len = line.getTextLength();
			colNum = (line.endsWithLineBreak())? len-1: len;

		}
		updateCoords();
	}
	
	/** move the cursor one position to the right */
	this.moveRight = function(){
		var line = lineMgr.getLine(rowNum);
		var len = line.getTextLength();
		len = (line.endsWithLineBreak())? len-1: len;
		if (colNum < len){
			colNum += 1;
		}
		else if(rowNum+1 < lineMgr.getLineCount()){
			rowNum +=1;
			colNum = 0;
		}
		updateCoords();
	}
	
	/** hide the cursor*/
	this.hide = function(){cursorNode.setAttributeNS(null,"visibility","hidden");}
	/** show the cursor*/
	this.show = function(){cursorNode.removeAttributeNS(null,"visibility");}
	
	//FIXME make this dynamical for the current char because if the font is not monospace the extent.width 
	//of the character used in the displayManager to get that width might be to big/small
	/** turns the text cursor into a rectangle with the width of a character */
	this.makeFat = function(){
		cursorNode.width.baseVal.value = displayMgr.getCharWidth();
		cursorNode.setAttributeNS(null, "opacity", "0.7");
	} 
	
	/** turns the test cursor into a vertical line */
	this.makeThin = function(){
		cursorNode.width.baseVal.value = 1;	
		cursorNode.setAttributeNS(null, "opacity", "1");
	}
	
	/** changes the size of the cursor to be of the same size as the current style*/
	this.changeSize = function(){
		//cursorNode.height.baseVal.value  gets input in pixels 12 pt = 16 px so instead we use setAttribute
		//var size = String(displayMgr.getStyle().getFontSizePt()) + "pt";
		var size = this.getStyle().getFontSizePt() + "pt";
		cursorNode.setAttributeNS(null,"height",size)
	}
	
	/** returns the style at the current position. sometimes a position is between two styles.
	 * the default behavior is to return the style to the left of the position. can be changed by setting the optional parameter to true
	 @param pickRight a boolean: (optional) default false. pick the style to right of the position if true.
	 */
	this.getStyle = function(pickRight){
		var rightBool = (typeof(pickRight) == "undefined")? false : pickRight;
		return lineMgr.getLine(rowNum).getStyleAt(colNum, pickRight);
	} 
	
	/** returns the margins of the current line*/
	//this.getMargins = function(){} TODO if we add margins per line
}