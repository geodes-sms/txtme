/**
The style used by the SVG Rich Text Editor and the GUI
@author Daniel Riegelhaupt
@date july, august 2011
Version 2: december 2014
*/
//the CSS color list , contains the rgb values of color names; will be initialized once and used by ll styles
var CSS_COLOR_LIST = new CSSColorList(); //only init this once 

/**
@class Style
@description 
a small class to serialize/deserialize a simple css string
NOTE color attribute: accepts, hex, rgb, hsl and offical cc3 color names. NOT rgba and hsla (opacity in font is not supported in rtf so we cant save that)
this only matters for regular attributes.
NOTE Not a 100% sure but even the whole color stuff is only needed to save to rtf. if rtf is removed (after refactoring), we can remove all thos methods 
to tramsfrom color including the whole CSS list simply add it as a regular attribute (after buffer etc have been reafctored)
*/
function Style(normalStyleStr , errorStyleStr){
  	
	var EM_PT_SIZE = 12;   //1 em = 12 points
	var PX_PT_SIZE = 0.75  //16 px = 12 pt => 1px = 0.75pt 
	var PC_PT_SIZE = 0.12  //100 % = 12 pt 

	var dict = new Dictionary;
	var errDict = new Dictionary;
	var errorBool = false
	
	normalStyleStr = (typeof(normalStyleStr) == "undefined") ? "font-family:\'Nimbus Mono L\';font-size:12pt;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration:none" : normalStyleStr;
	errorStyleStr = (typeof(errorStyleStr) == "undefined") ?"text-decoration:underline;text-decoration-style:wavy;text-decoration-color:red;-moz-text-decoration-style:wavy;-moz-text-decoration-color:red": errorStyleStr;
	
	/*Those two lines cant be placed here becaue the mehtods arent defined yet so they are placed before the depractaed methods
	they are kept here for clarification
	this is bascially the constructor*/
	//this.fromNormalString(normalStyleStr);
	//this.fromErrorString(errorStyleStr);
			
	/** serialize this style to a string*/ 
	this.toString = function(){
	    var str = "";
	    if (errorBool == false){
	      str = this.normalStatusStr()
	    } else {
	      str = this.errorStatusStr()
	    }	  
	    return str;
	}
	
	/** regardless of current error status returns the css string as if error status were false
	 */
	this.normalStatusStr = function(){
	    return dicToStr(dict);
	}
	
	//returns the string of the key value pair in css style 
	function dicToStr(dic){
	    var str = ""
	    var keys = dic.keys()
	    var key = null
	    var l = keys.length -1 
	    for (var i in keys) {
	      key = keys[i]
	      str += key + ":" + dic.get(key) 
	      if (i < l)
		str += ";"
	    }
	    return str
	}
	
	/** regardless of current error status returns the css string for this style as if errorStatus were true
	    this means return the regular attributes with their value replaced by those of the error style if 
	    there is an overlap as well as the error only attributes
	 */
	this.errorStatusStr = function(){
	    var str = ""
	    var keys = dict.keys();
	    var key = null
	    var l = keys.length -1 
	    //first the regular attributes
	    for (var i in keys) {
	      key = keys[i]
	      str += key + ":"  
	      if (errDict.hasKey(key)) //if an attribute is defined in both we take the error one
		str += errDict.get(key);
	      else
		str += dict.get(key); 
	      
	      //if (i < l) always add the ;
		str += ";"
	    }
	    
	    //followed by the attributes that are specifically for the error
	    var errKeys = errDict.keys()
	    var eKey = null
	    for (var j in errKeys){
	      eKey = errKeys[j];
	      if (dict.hasKey(eKey) == false){ //it hasnt been added yet so add it now
		str += eKey + ":" + errDict.get(eKey) + ";"
	      }
	    }
	    
	    return str
	}
	
	/** returns only the error attributes string*/
	this.getErrorStr = function(){
	  return dicToStr(errDict);
	}
	
	/** returns only the normal attributes string
	 Note the resulted string is the same one as returned by getNormalStatusStr(). this method is only here because getErrorStr is here
	 */
	this.getNormalStr = function(){
	  return this.normalStatusStr();
	}
	
	/** set whether or not the style should be displayed as error style 
	 @param bool a boolean, when true the style must display with error attributes (if they have been set)
	 */
	this.setErrorStatus = function(bool){
	    errorBool = bool;
	}
	
	/** returns true if the style is in error status*/
	this.getErrorStatus = function(){
	    return errorBool;
	}
	
	/**fills/replaces the Style with the key value pairs from the string.
	 * IMPORTANT: this does not erease key value pairs that were already specified but arent specified here
	 * If this needs to be done create a new Style with styleStr in the constructor (1ste argument)
	 @param styleStr a css string
	 */
	this.fromNormalString = function(styleStr){	  
	    fromStr(styleStr, dict)
	}
	
	/**fill the Error Style with the key value pairs from the string.
	 * IMPORTANT: this does not erease key value pairs that were already specified but arent specified here
	 * If this needs to be done create a new Style with styleStr in the constructor (2nd argument)
	 @param styleStr a css string
	 */
	this.fromErrorString = function(styleStr){
	    fromStr(styleStr, errDict)
	}
	
	//helper function for from(Error)String
	function fromStr(styleStr, dic){
	  var arr = styleStr.split(";")
	  var pair, value, key;
	    for (var i in arr){
		if (arr[i] != ""){
		    pair = arr[i].split(":");
		    key = pair[0];
		    value = pair[1];
		    setAttr(key, value, dic);
		}  
	    }
	}
	
	/** set a css attribute and its value*/
	function setAttribute(attr,value) {
	  setAttr(attr, value, dict)
	} 
	
	/** set a css attribute and its value to the error style*/
	function setErrorAttribute(attr,value){
	  setAttr(attr, value, errDict)
	}
	
	
	function setAttr(attr,value, dic){
	    //console.log("set Attr called: ", attr, value)
	    var a = attr.trim();
	    var v = value.trim();
	    
	    if (a == "color")
	      setAttrColor(v,dic)
	    else if (a == "font-size")
	      setAttrSize(v,dic)
	    else
	      dic.set(a, v) 
	}
	
	function setAttrColor (colorStr, dic){
	    var rgb = {R:0, G :0, B:0};
	    var rgbReg = /rgb\(((.|\s)*?)(?:\))/
	    var hslReg = /hsl\(((.|\s)*?)(?:\))/
	    var hex3Reg = /#([0-9A-Fa-f]{3})/
	    var hex6Reg = /#([0-9A-Fa-f]{6})/
	    
	    if (rgbReg.test(colorStr)){
		var colAr = rgbReg.exec(colorStr)[1].split(",");
		rgb.R = parseInt(colAr[0]);
		rgb.G = parseInt(colAr[1]);
		rgb.B = parseInt(colAr[2]);
	      
	    } else if (hslReg.test(colorStr)) {
		var colAr = hsl.exec(colorStr)[1].split(",");
		var h = parseInt(colAr[0].split("%")[0]);
		var s = parseInt(colAr[1].split("%")[0]);
		var l = parseInt(colAr[2].split("%")[0]); 
		
		var rgbAr = hslToRgb(h,s,l);
		rgb.R = rgbAr[0];
		rgb.G = rgbAr[1];
		rgb.B = rgbAr[2];
	    } else if(hex3Reg.test(colorStr)) { //#rgb becomes #rrggbb
		rgb.R = parseInt(colorStr[1] + colorStr[1],16 );
		rgb.G = parseInt(colorStr[2] + colorStr[2],16);
		rgb.B = parseInt(colorStr[3] + colorStr[3],16);
	      
	    } else if(hex6Reg.test(colorStr)) {
		rgb.R = parseInt(colorStr.slice(1,3),16);
		rgb.G = parseInt(colorStr.slice(3,5),16);
		rgb.B = parseInt(colorStr.slice(5,7),16);
	      
	    } else if (CSS_COLOR_LIST.hasColor(colorStr)){
		colAr = CSS_COLOR_LIST.getColor(colorStr)
		rgb.R = colAr[0];
		rgb.G = colAr[1];
		rgb.B = colAr[2];
	    } 
	    
	    color = String("rgb(" + rgb.R + "," + rgb.G + "," + rgb.B + ")")
	    dic.set("color", color);
	}
	
	function hslToRgb(h,s,l){ 
	    //adapted from http://www.w3.org/TR/css3-color/
	    // h,s,l = Hue , Saturation, Lightness  
	    
	    //from percent to normalized
	    h /= 100.0; 
	    s /= 100.0;
	    l /= 100.0;
	    
	    var m2 = (l <= 0.5) ? l * (1 + s) : l + s - l*s;
	    var m1 = l*2 - m2
	     
	    var r = hueToRgb(m1, m2, h + 1/3) 
	    var g = hueToRgb(m1, m2, h    ) 
	    var b = hueToRgb(m1, m2, h - 1/3) 
	    
	    //values are 0 -1 we want 0- 255
	    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
	}
	   
	function hueToRgb(m1, m2, h){
	    //adapted from http://www.w3.org/TR/css3-color/
	    if (h < 0) { h += 1} 
	    else if (h > 1) { h-= 1}
	    
	    var ret = m1
	    
	    if ((h*6)< 1)
	      ret = m1+(m2-m1)*h*6;
	    else if ((h*2)<1)
	      ret = m2;
	    else if ((h*3)<2)
	      ret = m1+(m2 - m1)*(2/3 - h)*6;
	    
	    return ret;
	}
	
	
	function setAttrSize(size, dic){
	    var sizeReg = /([0-9]+([\.][0-9])?)/
	    var unitReg = /pt|em|%|px/
	    
	    var s = parseFloat(sizeReg.exec(size)[0])
	    var u = unitReg.exec(size)[0]
	   
	    var scale = 1.0
	    if (u == "px")
	      scale = PX_PT_SIZE
	    else if (u == "em")
	      scale = EM_PT_SIZE
	    else if (u == "%")
	      scale = PC_PT_SIZE
	  
	    fontSize = s* scale
	    sizeStr = String(fontSize) + "pt"
	    dic.set("font-size", sizeStr)
	}
	
	this.getAttribute = function(attr){
	    if (this.hasAttribute(attr))  
		return dict.get(attr);
	    else
	      return "";
	}
	
	this.getErrorAttribute = function(attr){
	    if (this.hasErrorAttribute(attr))
		return errDict.get(attr);
	    else
		return "";
	}
	
	this.getCurrentAttribute = function(attr){
	  if (errorBool && this.hasErrorAttribute(attr))
	    return this.getErrorAttribute (attr); //even if we display the error style, dont emidatyl return "" if not present we first must check if it is in the regular attributes
	  else //if it is not present(or we are not in displaying the error style) we check the the normal attributes (and return "" ifnot present)
	    return this.getAttribute(attr);
	    
	}
	
	this.hasAttribute = function(attr){
	     return dict.hasKey(attr)
	}
	
	this.hasErrorAttribute = function(attr){
	     return errDict.hasKey(attr)
	}
	
	/** returns a deep copy of the style*/
	this.copyDeep = function(){
	      var norm = this.getNormalStr();
	      var err = this.getErrorStr();
	      var st = new Style(norm,err)
	      st.setErrorStatus(this.getErrorStatus());
	      return st;
	}
	
	
	this.fromNormalString(normalStyleStr);
	this.fromErrorString(errorStyleStr);
	
	/****************** 
	 * Getters and setters kept for backwards compatibility while refactoring,but will be mostly useless after that.
	 *******************/
	
	/** set the font family, 
	@param fontStr a string: a font family consisting of more then one word must be inside single quote, multiple fonts are divided by a ','. no ';' at the end !
	*/
	this.setFontFamily = function(fontStr){
		dict.set("font-family", fontStr);
	}
			
	/** set the font color in rgb (red green blue) values : integers between 0 and 255 (both included)*/	
	this.setColorRGB = function(R,G,B){
		var rgb = {R:0, G :0, B:0};
		rgb.R = ((0<=R) && (R<=255))? R : 0;
		rgb.G = ((0<=G) && (G<=255))? G : 0;
		rgb.B = ((0<=B) && (B<=255))? B : 0; 
		str = "rgb(" + rgb.R.toString() + "," + rgb.G.toString() + "," + rgb.B.toString() + ", )";
		dict.set("color", str);
	}
	
	/** set the font color in a string should be "rgb(r,g,b)" , "hsl(h,s,)", a hex "#rgb" or "#rrggbb" without whitespaces */	
	this.setColorString = function(colorStr){
		setAttrColor(colorStr.trim())	 
	}
	
	/** set the fontsize in points*/
	this.setFontSizePt = function(pt){
	  fontSizePt = pt; 
	  dict.set("font-size", pt.toString() + " pt");
	}
	/** set whether the text is bold or not*/
	this.setBold = function(bool){ dict.set("font-weight", "bold")}
	/** set whether the text is italic or not*/
	this.setItalic = function(bool){ dict.set("font-style", "italic")}
	/** set whether the text is underlined or not*/
	this.setUnderline = function(bool){ dict.set("font-decoration", "underline")}
	
	/** returns the font-family string*/
	this.getFontFamily = function(){ return dict.get("font-family");}
	/** returns a map {R, G, B} with the red blue green values of the current font color*/
	this.getColorRGB = function(){ return rgb;}
	/** returns the color as a string "rgb(r,G,B)"*/
	this.getColorString = function() { return dict.get("color");}
	/** returns the font size in points*/
	this.getFontSizePt = function(){ return parseFloat(dict.get("font-size").slice(0,-2));} //slice -2 to remove pt
	/** returns whether the text is bold or not*/
	this.getBold = function(){ return (dict.hasKey("font-weight") && dict.get("font-weight") == "bold")}
	/** returns whether the text is italic or not*/
	this.getItalic = function(){return (dict.hasKey("font-style") && dict.get("font-style") == "italic")}
	/** returns whether the text is underlined or not*/
	this.getUnderline = function(){return (dict.hasKey("font-decoration") && dict.get("font-decoration") == "underline")}
}


function CSSColorList(){
/**
 This is the official CSS3 list of color, taken from
 http://www.w3.org/TR/css3-color/
*/  
    
    var obj = new Object()
	
    //basic color words
    obj.black 	 = [0,0,0]
    obj.silver 	 = [192,192,192]
    obj.gray 	 = [128,128,128]
    obj.white 	 = [255,255,255]
    obj.maroon 	 = [128,0,0]
    obj.red 	 = [255,0,0]
    obj.purple 	 = [128,0,128]
    obj.fuchsia  = [255,0,255]
    obj.green 	 = [0,128,0]
    obj.lime 	 = [0,255,0]
    obj.olive 	 = [128,128,0]
    obj.yellow 	 = [255,255,0]
    obj.navy 	 = [0,0,128]
    obj.blue 	 = [0,0,255]
    obj.teal 	 = [0,128,128]
    obj.aqua 	 = [0,255,255] 
    //Extended color keywords
    obj.aliceblue 	 = [240,248,255]
    obj.antiquewhite 	 = [250,235,215]
    obj.aqua 		 = [0,255,255]
    obj.aquamarine 	 = [127,255,212]
    obj.azure 		 = [240,255,255]
    obj.beige 		 = [245,245,220]
    obj.bisque 		 = [255,228,196]
    obj.black 		 = [0,0,0]
    obj.blanchedalmond 	 = [255,235,205]
    obj.blue 		 = [0,0,255]
    obj.blueviolet 	 = [138,43,226]
    obj.brown 		 = [165,42,42]
    obj.burlywood 	 = [222,184,135]
    obj.cadetblue 	 = [95,158,160]
    obj.chartreuse 	 = [127,255,0]
    obj.chocolate 	 = [210,105,30]
    obj.coral 		 = [255,127,80]
    obj.cornflowerblue 	 = [100,149,237]
    obj.cornsilk 	 = [255,248,220]
    obj.crimson 	 = [220,20,60]
    obj.cyan 		 = [0,255,255]
    obj.darkblue 	 = [0,0,139]
    obj.darkcyan 	 = [0,139,139]
    obj.darkgoldenrod 	 = [184,134,11]
    obj.darkgray 	 = [169,169,169]
    obj.darkgreen 	 = [0,100,0]
    obj.darkgrey 	 = [169,169,169]
    obj.darkkhaki 	 = [189,183,107]
    obj.darkmagenta 	 = [139,0,139]
    obj.darkolivegreen 	 = [85,107,47]
    obj.darkorange 	 = [255,140,0]
    obj.darkorchid 	 = [153,50,204]
    obj.darkred 	 = [139,0,0]
    obj.darksalmon 	 = [233,150,122]
    obj.darkseagreen 	 = [143,188,143]
    obj.darkslateblue 	 = [72,61,139]
    obj.darkslategray 	 = [47,79,79]
    obj.darkslategrey 	 = [47,79,79]
    obj.darkturquoise 	 = [0,206,209]
    obj.darkviolet 	 = [148,0,211]
    obj.deeppink 	 = [255,20,147]
    obj.deepskyblue 	 = [0,191,255]
    obj.dimgray 	 = [105,105,105]
    obj.dimgrey 	 = [105,105,105]
    obj.dodgerblue 	 = [30,144,255]
    obj.firebrick 	 = [178,34,34]
    obj.floralwhite 	 = [255,250,240]
    obj.forestgreen 	 = [34,139,34]
    obj.fuchsia 	 = [255,0,255]
    obj.gainsboro 	 = [220,220,220]
    obj.ghostwhite 	 = [248,248,255]
    obj.gold 		 = [255,215,0]
    obj.goldenrod 	 = [218,165,32]
    obj.gray 		 = [128,128,128]
    obj.green 		 = [0,128,0]
    obj.greenyellow 	 = [173,255,47]
    obj.grey 		 = [128,128,128]
    obj.honeydew 	 = [240,255,240]
    obj.hotpink 	 = [255,105,180]
    obj.indianred 	 = [205,92,92]
    obj.indigo 		 = [75,0,130]
    obj.ivory 		 = [255,255,240]
    obj.khaki 		 = [240,230,140]
    obj.lavender 	 = [230,230,250]
    obj.lavenderblush 	 = [255,240,245]
    obj.lawngreen 	 = [124,252,0]
    obj.lemonchiffon 	 = [255,250,205]
    obj.lightblue 	 = [173,216,230]
    obj.lightcoral 	 = [240,128,128]
    obj.lightcyan 	 = [224,255,255]
    obj.lightgoldenrodyellow 	 = [250,250,210]
    obj.lightgray 	 = [211,211,211]
    obj.lightgreen 	 = [144,238,144]
    obj.lightgrey 	 = [211,211,211]
    obj.lightpink 	 = [255,182,193]
    obj.lightsalmon 	 = [255,160,122]
    obj.lightseagreen 	 = [32,178,170]
    obj.lightskyblue 	 = [135,206,250]
    obj.lightslategray 	 = [119,136,153]
    obj.lightslategrey 	 = [119,136,153]
    obj.lightsteelblue 	 = [176,196,222]
    obj.lightyellow 	 = [255,255,224]
    obj.lime 		 = [0,255,0]
    obj.limegreen 	 = [50,205,50]
    obj.linen 		 = [250,240,230]
    obj.magenta 	 = [255,0,255]
    obj.maroon 		 = [128,0,0]
    obj.mediumaquamarine = [102,205,170]
    obj.mediumblue 	 = [0,0,205]
    obj.mediumorchid 	 = [186,85,211]
    obj.mediumpurple 	 = [147,112,219]
    obj.mediumseagreen 	 = [60,179,113]
    obj.mediumslateblue 	 = [123,104,238]
    obj.mediumspringgreen 	 = [0,250,154]
    obj.mediumturquoise 	 = [72,209,204]
    obj.mediumvioletred 	 = [199,21,133]
    obj.midnightblue 	 = [25,25,112]
    obj.mintcream 	 = [245,255,250]
    obj.mistyrose 	 = [255,228,225]
    obj.moccasin 	 = [255,228,181]
    obj.navajowhite 	 = [255,222,173]
    obj.navy 		 = [0,0,128]
    obj.oldlace 	 = [253,245,230]
    obj.olive 		 = [128,128,0]
    obj.olivedrab 	 = [107,142,35]
    obj.orange 		 = [255,165,0]
    obj.orangered 	 = [255,69,0]
    obj.orchid 		 = [218,112,214]
    obj.palegoldenrod 	 = [238,232,170]
    obj.palegreen 	 = [152,251,152]
    obj.paleturquoise 	 = [175,238,238]
    obj.palevioletred 	 = [219,112,147]
    obj.papayawhip 	 = [255,239,213]
    obj.peachpuff 	 = [255,218,185]
    obj.peru 	 	 = [205,133,63]
    obj.pink 	 	 = [255,192,203]
    obj.plum 	 	 = [221,160,221]
    obj.powderblue 	 = [176,224,230]
    obj.purple 	         = [128,0,128]
    obj.red 	 	 = [255,0,0]
    obj.rosybrown 	 = [188,143,143]
    obj.royalblue 	 = [65,105,225]
    obj.saddlebrown 	 = [139,69,19]
    obj.salmon 	 	 = [250,128,114]
    obj.sandybrown 	 = [244,164,96]
    obj.seagreen 	 = [46,139,87]
    obj.seashell 	 = [255,245,238]
    obj.sienna 	 	 = [160,82,45]
    obj.silver 	 	 = [192,192,192]
    obj.skyblue 	 = [135,206,235]
    obj.slateblue 	 = [106,90,205]
    obj.slategray 	 = [112,128,144]
    obj.slategrey 	 = [112,128,144]
    obj.snow 	 	 = [255,250,250]
    obj.springgreen 	 = [0,255,127]
    obj.steelblue 	 = [70,130,180]
    obj.tan 	 	 = [210,180,140]
    obj.teal 	 	 = [0,128,128]
    obj.thistle 	 = [216,191,216]
    obj.tomato 	 	 = [255,99,71]
    obj.turquoise 	 = [64,224,208]
    obj.violet 	 	 = [238,130,238]
    obj.wheat 	 	 = [245,222,179]
    obj.white 	 	 = [255,255,255]
    obj.whitesmoke 	 = [245,245,245]
    obj.yellow 	 	 = [255,255,0]
    obj.yellowgreen 	 = [154,205,50] 
    
    this.hasColor = function(color){
      return (typeof obj[color] !== 'undefined');
    }
    
    this.getColor = function(color){
      return obj[color]
    }
}