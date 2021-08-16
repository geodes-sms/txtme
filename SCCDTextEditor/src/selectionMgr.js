/**
@class SelectionManager
@description handles the selection of text
@param selectionNode the DOM node that will serve as the parent for the highlighting
@param lineMgr an instance of the LineManager class
*/

function SelectionManager(selectionNode, lineMgr){
	var from = {row : -1 , col : -1}; //the beginning of the selection
	var to =  {row : -1 , col : -1}; //the end of the selection
	//var cursorPos  =  {row : -1 , col : -1};
	//var EMPTY_LINE_WIDTH = 4; //the constant value we use as width for a selection when the line is empty 
	
	var adjusted = false; //did we need to switch from and to get the in the right order
 	
	//makes sure 'from' is a position before 'to'
	//returns true if we needed to change , returns false if we didn't
	function adjustPostion(){
		var temp;
		var last = lineMgr.getLineCount()-1;
		var ret = false;
		
		if ( (from.row > to.row) || ((from.row == to.row) && (from.col > to.col)) ) {
			temp = from;
			from = to;
			to = temp;
			ret = true
		}
		
		//from cannot start after an LB it is always before the LB (unless it is the last character)
		if ((from.col == lineMgr.getLine(from.row).getTextLength()) && (from.row != last) && lineMgr.getLine(from.row).endsWithLineBreak()){
			from.col -= 1;
		}
		
		//we aren't allowed to select the last character
		if (to.row == last) {
			var len = lineMgr.getLine(to.row).getTextLength() 
			if (len == to.col){
				if (len > 1){
					to.col -= 1;
				}else if(to.row != 0){
					to.row -= 1;
					to.col = lineMgr.getLine(to.row).getTextLength();
				}
				else{
					to =  {row : 0 , col : 0}; 
				}
			}
		}
			
		//after those changes from might be after to again
		//in this case there is no selection and we change from to the samve value as to
		if ( (from.row > to.row) || ((from.row == to.row) && (from.col > to.col)) ) {
			from.row = to.row;
			from.col = to.col;
		}	
		
		//console.log("from = " , from);
		//console.log("to = " , to);
		return ret;			
	}
	
	
	//this will create a rectangle that will serve as highlight
	function createRect(x, y, width, height){
		 var rect = document.createElementNS(svgNS,"rect");
		 rect.setAttributeNS(null,"x",x);
		 rect.setAttributeNS(null,"y", y );
		 rect.setAttributeNS(null,"width", width);
		 rect.setAttributeNS(null,"height", height);
		 selectionNode.insertBefore(rect, null);
	}
	
	/** returns true if the start and end coordinates had to be switched*/
	this.isAdjusted = function(){
		return adjusted;
	}
	
	/** draws the selection over the given indices
	@param fromInd a map { row, col}
	@param toInd a map { row, col}
	@return true if something was selected, false if nothing was selected (the move was to small to select at least 1 character);
	*/
	this.drawSelectionIndices = function(fromInd ,toInd){
		from = fromInd;
		to = toInd;
		
		//we make sure they are in the right order
		adjusted = adjustPostion();
	
		//find the corresponding exact coordinates (exact as opposed to the one received from drawSelection who are mouse click and are just coordinates around the place)
		var fromY = lineMgr.getTotalDyUntil(from.row);
		var fromX = lineMgr.getLine(from.row).calculateX(from.col);
		var toY = lineMgr.getTotalDyUntil(to.row); 
		var toX = lineMgr.getLine(to.row).calculateX(to.col);
		
		//if there was a previous selection clear it
		deselectHelper()
		
		//now select
		var width
		var height;
		if (from.row == to.row){
			width = toX-fromX;
			if (from.col != to.col){
				var line = lineMgr.getLine(to.row)
				if (line.endsWithLineBreak() && (line.getTextLength() == to.col) ){
					width = line.getRightMargin() - fromX;
				}
				createRect(fromX, fromY.toString() + "pt", width, lineMgr.getLine(from.row).getDy().toString() + "pt");
			}
			else{
				return false;
			}
		}
		else{ 
			var x, y;
			var line;
			//Create the first rect
			width = lineMgr.getLine(from.row).getRightMargin()-fromX
			createRect(fromX, fromY.toString()+"pt", width, lineMgr.getLine(from.row).getDy().toString() +"pt")
			
			//draw the selection in between
			for( var i = from.row+1; i <= to.row-1 ; i++){
				line = lineMgr.getLine(i); 
				x = line.getLeftMargin(); //we can't assume is 0 we must get the left margin
				y = lineMgr.getTotalDyUntil(i);
				width = line.getRightMargin() - x;
				createRect(x, y.toString() + "pt", width, line.getDy().toString() +"pt")
			}
			
			//draw the last one
			line = lineMgr.getLine(to.row)
			if ( to.col == line.getTextLength()){
				width = line.getRightMargin() - line.getLeftMargin();
			}
			else{
				width = toX - line.getLeftMargin();
			}
			createRect(line.getLeftMargin(), toY.toString() + "pt", width, line.getDy().toString() + "pt");
		}
		return true;
	}
	
	/** draws a selection over the given screen coordinates. 
	@return true if something was selected, false if nothing was selected (the move was to small to select at least 1 character);
	*/
	this.drawSelection = function(startX, startY, endX, endY){
		//first we set from and to
		from.row = lineMgr.getLineFromY(startY);
		from.col = lineMgr.getLine(from.row).getColFromX(startX);
		to.row = lineMgr.getLineFromY(endY);
		to.col = lineMgr.getLine(to.row).getColFromX(endX);
					
		return this.drawSelectionIndices(from , to);
	}
	
	//remove all the drawn rects
	function deselectHelper(){
		while(selectionNode.childNodes.length){
			selectionNode.removeChild(selectionNode.childNodes[0]);
		}
	}
	
	/** Selects everything except the irremovable line break
	 @return true if something was selected
	 */
	this.selectAll = function(){
		var start = {row : 0, col : 0};
		var end = { row: -1, col: -1};
		// this is the absolute last position of the line but drawSelection will make sure the selection doesn't include the last character 
		end.row = lineMgr.getLineCount() -1 ;
		end.col = lineMgr.getLine(end.row).getTextLength();
		return this.drawSelectionIndices (start, end);
	}
	
	/** removes the highlights that were drawn*/
	this.deselect = function(){
		deselectHelper();
		from = {row : -1 , col : -1};
		to =  {row : -1 , col : -1};
	}
			
	/** returns a map {row, col} with the start coordinates*/
	this.getSelectionStart = function(){
		return from;
	}

	/** returns a map {row, col} with the end coordinates*/
	this.getSelectionEnd = function(){
		return to;
	}
		
	/** returns a map {row, col} where the user started the selection */
	this.getSelectionStartClickPos = function(){
		var ret = from;
		if (adjusted){
			ret = to;
		}
		return ret;	
	}
	
	/** returns a map {row, col} where the user ended the selection  */
	this.getSelectionEndClickPos = function(){
		var ret = to;
		if (adjusted){
			ret = from;
		}
		return ret;	
	}	

}