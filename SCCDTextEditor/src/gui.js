/**
@class GUI
the GUI interface, it communicates between the DOM buttons and the editor using the Style class
@param style an instance of the style to give start values
*/
function GUI(style) {

    var currentStyle;
    var scInstance;

    //the nodes that correspond to the gui in the DOM
    var setNode, boldNode, italicNode, underlineNode, fontTypeNode, fontSizeNode, fontColorNode;

    //init the the GUI with the style
    function init(){
        currentStyle = (typeof(style) == "undefined")? (new Style()) : style;
        scInstance = null;
    }
    init();

    /** set the DOM nodes of the gui so that this class can edit them or get information from them*/
    this.setDomNodes = function(setDNode, boldDNode, italicDNode, underlineDNode,fontTypeDNode, fontSizeDNode, fontColorDNode){
        setNode = setDNode;
        boldNode = boldDNode;
        italicNode = italicDNode;
        underlineNode = underlineDNode;
        
        fontTypeNode = fontTypeDNode;
        fontSizeNode = fontSizeDNode;
        fontColorNode = fontColorDNode;
        
        initDOMNodes();
        update(currentStyle);
    }

    //inits some of the DOM nodes
    function initDOMNodes(){
        //display every font in the font picker in its own font
        var options = fontTypeNode.children();	
        options.each(function(){
            var me = $(this);
            me.css("font-family", me.val() ); //doesn't work in chromium for some reason, color does
        });
        
        var options2 = fontColorNode.children();	
        options2.each(function(){
            var me = $(this);
            me.css({"color" : me.val(), "background-color" : me.val()});
        });
    }

    //update the GUI with the current value of the style
    function update(nStyle){
        currentStyle = nStyle;
        boldNode.prop('checked', nStyle.getBold());
        italicNode.prop('checked', nStyle.getItalic());
        underlineNode.prop('checked', nStyle.getUnderline());	

        fontTypeNode.val(nStyle.getFontFamily());
        fontTypeN.css("font-family", fontTypeN.val());
        
        fontSizeNode.val(nStyle.getFontSizePt());	
        
        fontColorNode.val(nStyle.getColorString());		
        fontColorNode.css({"color" : fontColorNode.val(), "background-color" : fontColorNode.val()});
        
        setNode.buttonset("refresh");
    }

    /** update the GUI to show the given style*/
    this.updateGUI = function(nStyle){
        if (currentStyle.toString() != nStyle.toString()){
            update(nStyle);
        }	
    }

    /** returns an instance of the Style class with the style indicated by the GUI*/
    this.createStyle = function(){
        var ret = new Style();
        
        ret.setBold(boldNode.prop('checked'));
        ret.setItalic(italicNode.prop('checked'));
        ret.setUnderline(underlineNode.prop('checked'));
        
        ret.setFontFamily(fontTypeNode.val());
        ret.setFontSizePt(fontSizeNode.val());
        ret.setColorString(fontColorN.val());
        
        currentStyle = ret;
        return ret;
    }

    /**set the statechart instance*/
    this.setStateChart = function(sc){
		scInstance = sc;
    }

    /** alert the statechart of a change 
    @param styleAttr the name of the css attribute which has been change for example "text-decoration" for bold
    */
    this.alertStateChart  = function(styleAttr){
        //send an event to the state chart with the new style as data
        scInstance.gen("gui_style_change",{style: this.createStyle() , attr : styleAttr});        
    }
}
