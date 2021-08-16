/**
@class DisplayManager
@description a class that manages the display: current text style, page height, and margins (currently one and min max value allowed) 
@FIXME if we also want movable up and down margins height should be replaced and an analogous system to left right should be implemented 
*/
function DisplayManager(svgRootNode, leftMargin, rightMargin, height, style){
	
	var displayStyle;
	var minLeftMargin; //the minimum value for the left margin
	var maxRightMargin //the maximum value for the right margin
	
	var curLeftMargin; //the current value; here for if we want movable margins like for example Word or LibreOffice
	var curRightMargin;
	
	var pageHeight;
	
	var charHeight, charWidth; //the extent.height of a character in the current style
	
	function init(){
		displayStyle = (typeof(style) == "undefined") ? new Style() : style;
				
		minLeftMargin = (leftMargin <= rightMargin) ? leftMargin : rightMargin; //make sure left is smaller then right
		maxRightMargin = (leftMargin <= rightMargin) ? rightMargin : leftMargin;
		
		curLeftMargin  = minLeftMargin;
		curRightMargin = maxRightMargin;
		
		pageHeight = height;
		setCharExtent();
	}
	init(); //call init
	
	function setCharExtent(){
			//to get the extent we add the a character in the current style to DOM
			var tmptxt = document.createElementNS(svgNS,"text"); //create element
			tmptxt.setAttributeNS(null,"style", displayStyle.toString()); //set its style to the current style
			tmptxt.textContent="q"; //add a content
			svgRootNode.appendChild(tmptxt); //add the elem to DOM
			charHeight = tmptxt.getExtentOfChar(0).height; //set the extent height and width
			charWidth = tmptxt.getExtentOfChar(0).width;
			svgRootNode.removeChild(tmptxt); //remove the element from DOM			
	}
	
	/** sets the style*/
	this.setStyle = function(style){
		displayStyle= style
		setCharExtent();
	}
	
	/** set the current left margin if it falls between the mini left margin and current right margin else it keeps it current value */
	this.setCurLMargin = function(lMargin){
		curLeftMargin = ((lMargin >= minLeftMargin)&&(lMargin < curRightMargin)) ? lMargin : curLeftMargin;
	}
	
	/** set the current right margin if it falls between the maximum allowed right margin and the current left margin else keep the current value */
	this.setCurRMargin = function(rMargin){
		curRightMargin = ((rMargin <= maxRightMargin)&&(rMargin > curLeftMargin)) ? rMargin : curRightMargin;
	}
	
	/** returns the current style*/
	this.getStyle = function(){return displayStyle.copyDeep();}
	/** returns the current value of the left margin*/
	this.getCurLMargin =function(){return curLeftMargin;}
	/** returns the current value of the right margin*/
	this.getCurRMargin = function(){return curRightMargin;}
	/** returns the minimum value the current left margin can have*/
	this.getMinLMargin = function(){return minLeftMargin;}
	/** returns the maximum value the current right margin can have */
	this.getMaxRMargin = function(){return maxRightMargin;}
	/** returns the maximum line width possible on display*/
	this.getWidth = function(){return maxRightMargin-minLeftMargin;}
	/** returns the current width displayed*/
	this.getCurWidth = function(){return curRightMargin-curLeftMargin;}
	/** returns the height of the page*/
	this.getPageHeight = function(){ return pageHeight;}
	/** returns the height of a char in the current style*/
	this.getCharHeight = function(){ return charHeight;}
	/** returns the width of a char in the current style*/
	this.getCharWidth = function(){ return charWidth;}
}

/** class added for scrollbar control. this functionality might be removed from here
i'm not sure this really is a subclass of the display manager (or maybe it should be renamed)
*/
function DisplayManagerScrollBars(svgRootNode, leftMargin, rightMargin, height, style){
	var base = new DisplayManager(svgRootNode, leftMargin, rightMargin, height, style);
	
	//var self;
	var container = svgRootNode.parentNode;
	var textNode = svgRootNode.getElementsByTagName("text")[0];
	var curWindowHeight = base.getPageHeight();
	var curWindowWidth = base.getWidth();
	
	var pageH = base.getPageHeight();
	var pageW = base.getWidth();
	
	
	function getTextNodeHeight(){
		return Math.ceil(textNode.getBBox().height);
	}
	
	function getTextNodeWidth(){
		return Math.ceil(textNode.getBBox().width);
	}
	
	/** updates the height of the svg inside the container, due to the css being set to overflow this will cause scrollbars to appear if needed*/
	base.updateHeight = function(){
		var h = getTextNodeHeight();		
		if (h > curWindowHeight){
			curWindowHeight = h;
			svgRoot.setAttributeNS(null,"height",h);
		}
		else if( (h <= pageH) && (curWindowHeight > pageH)){
			curWindowHeight = pageH;
			svgRoot.setAttributeNS(null,"height",pageH); 
		}
	}
	
	/** updates the height of the svg inside the container, due to the css being set to overflow this will cause scrollbars to appear if needed*/
	base.updateWidth = function(){
		var w = getTextNodeWidth();		
		if (w > curWindowWidth){
			console.log("IF: W(", w , ") > savedW(",curWindowWidth, ")\nsetting width to W: " ,w);
			curWindowWidth = w;
			svgRoot.setAttributeNS(null,"width",w);
		}
		else if( (w <= pageW) && (curWindowWidth > pageW)){
			console.log("ELSE: W(", w , ") <= pageW(",pageW, ") &&\n" , 
						"savedW(",curWindowWidth, ") > pageW(",pageW, ")\n",
						"setting width to pageW: ", pageW	);
			curWindowWidth = pageW;
			svgRoot.setAttributeNS(null,"width",pageW); 
		}
	}
	
	base.updateWidthAndHeight = function(){
		base.updateHeight();
		base.updateWidth();
	}
	
	base.updateViewPort = function(cursor){
		
		var coords = cursor.getXYCoords();
		var style = cursor.getStyle();
		pt = cursor.getStyle().getFontSizePt();
		
		var cursorH = Math.ceil((pt*16)/12);
		
		var cursorTop = coords.y;
		var cursorBottom = cursorTop + cursorH;

		var pageTop = container.scrollTop;
		var pageBottom = pageTop + pageH;
		
		if ((cursorBottom >= pageTop) && (cursorTop <= pageBottom)
			&& (cursorBottom <= pageBottom) &&  (cursorTop >= pageTop) ){
			/*console.log("cursor:  top= ", cursorTop, " bottom = ", cursorBottom);
			console.log("page:  top= ", pageTop, " bottom = ", pageBottom);
			console.log("scroll top before: " , container.scrollTop);
			
			console.log("scroll top after: " , container.scrollTop);*/
		}
		else{
			console.log("new top: ", cursorBottom)
			container.scrollTop = cursorBottom;
		}
		
	}
	
	return base;
}