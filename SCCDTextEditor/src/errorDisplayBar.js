var ERROR_IMG_SOURCE = "error_img.svg" 

/**
 * A node that displays an image where the user can hover over to see the error
 * @param size A number or a string. The size of the image displayed (size=width=height).
 * A string will be kept as such, if size is given a s number it will be treated as the size in pixels
 * @param y A number or a string. The y value of where the image is shown. same note as size.
 */
function ErrorNode(size, y){
  
  var node;
  var parentNode = null;

  
  function init(){
    //<image x="0" y="32px" width="15px" height="15px" xlink:href="error_img.svg"/>
    
    sizeStr = valToStr(size)
    yStr = valToStr(y)
    
    //Both svgNS and xlinkNS are defined in editor.html
    //but are svgNS = "http://www.w3.org/2000/svg"; and xlinkNS = "http://www.w3.org/1999/xlink"; in case this needs tobe used outisde the editor
    node = document.createElementNS(svgNS,"image");
    node.setAttributeNS(xlinkNS,"href", ERROR_IMG_SOURCE);
    node.setAttributeNS(null, "height", sizeStr);
    node.setAttributeNS(null, "width", sizeStr);
    node.setAttributeNS(null, "x", "0");
    node.setAttributeNS(null, "y", yStr);
  }
  
  function valToStr(val){
    var ret = "" 
    if (typeof val == 'string'){
      ret = val;
    } else if (typeof y == 'number'){
      ret = String(val) + 'px'
    }
    return ret;
  }
  
  init();
  
  this.addToDOM = function(parent){
    parentNode = parent;
    parentNode.appendChild(node)
  }
  
  this.removeFromDOM = function(){
    parentNode.removeChild(node)
  }
  
  this.addErrorMessage = function(msg){
    err= ""
    if (node.hasAttribute("title")){
	err = node.getAttribute("title") +"\n"
    }
    err += msg
    node.setAttribute("title", err);  
  }
  
  this.clearErrorMessage = function(){
    node.removeAttribute("title");
  }
  
  /** set the size(=width=height)  of the node
   @param size : A String or a number. A number will be interpreted as being in pixels, a sting will be left a such
  */
  this.setSize = function(size){
    val = valToStr(size)
    node.setAttributeNS(null, "height", val);
    node.setAttributeNS(null, "width", val);
  }
  
  /** set the Y value of the node
   @param y : A String or a number. A number will be interpreted as being in pixels, a sting will be left a such
   */
  this.setY = function(y){
    val = valToStr(y)
    node.setAttributeNS(null, "y", val);
  }
  
}


/**
 * @class ErrorDisplayBar A bar to display the errors
 */
function ErrorDisplayBar(parentDOMNode, lineManager){
  
  var parentNode = parentDOMNode;
  var errors = new Dictionary();
  var lineMgr = lineManager;
  var size = parentDOMNode.getElementsByTagName("rect")[0].width.baseVal.value;//we get the width of the 
  
  /** Adds the error to the line*/
  this.addLineError = function(lineNum, errorStr){
    if (errors.hasKey(lineNum)){
      errors.get(lineNum).addErrorMessage(errorStr);
    }else{
      var y = calcYforLine(lineNum)
      var node = new ErrorNode(size,y)
      node.addErrorMessage(errorStr)
      node.addToDOM(parentNode)
      errors.set(lineNum, node)
    }
  }
  
  function calcYforLine(lineNum){
    ret = lineMgr.getTotalHeightUntil(lineNum)
    return ret
  }
  
  this.replaceLineError = function(lineNmbr, errorStr){
    if (errors.hasKey(lineNum)){
      var n = errors.get(lineNum)
      n.clearErrorMessage();
      n.addErrorMessage(errorStr);
    }
  }
  
  this.clearErrors = function(){
    var keys = errors.keys()
	var lineNum;
	var node;
    //first we need to remove the current nodes from DOM
    //var it = errors.iterator();
    for (var i in keys){
		lineNum = keys[i];
		node = errors.get(lineNum)
		node.removeFromDOM();
	}
    //once the nodes are remove from DOM we simply reset the dictionary
    errors = new Dictionary();
  }
  
}

