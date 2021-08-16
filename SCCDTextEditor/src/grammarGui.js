function GrammarGUI() {

    var scInstance, editorInstance;
    var grammarSelect, styleSelect, loadGrammar, openFile, saveFile, saveAsOptions, checkText;
    
    var menuData = null;
    
     /**set the statechart instance*/
    this.setStateChart = function(sc){
		scInstance = sc;
    }
    
    function focusParent(){
		//unfortunatly you can't use one line for all browsers
		/*if (navigator.userAgent.indexOf('Chrome/') > 0) { //for chrome
			parent.focus();
		}
		else{ //for firefox and others
			parent.document.documentElement.focus();
		}*/
		
		var rootDiv = window.frameElement ? window.frameElement.parentNode : parent;
		var svgParent = rootDiv.getElementsByTagName("svg")[0].parentNode 
		//this is a roundabout way of getting the node, .but one that is sure to work
		//first i get the svg root of which i know there will only be one
		//then i get its parent which it the elemt who will get focus
		//i could also directly get the div instead since for the moment there is only one child div. 
		//but that could change 
		
		svgParent.focus();
    }
    
    this.setDOMNodes = function(grammarSelectNode, styleSelectNode, loadGrammarNode, openFileNode, saveFileNode, checkTextNode){
      grammarSelect = grammarSelectNode;
      styleSelect = styleSelectNode;
      loadGrammar = loadGrammarNode;
      openFile = openFileNode;
      saveFile = saveFileNode;
      checkText = checkTextNode;
      
      this.initDOMNodes();
    }
    
    this.initDOMNodes = function(){
		loadGrammar.button();
		openFile.button();
		saveFile.button();
		checkText.button();
		var me = this
      
		//grammarSelect.selectmenu();
		//styleSelect.selectmenu();
      
		grammarSelect.change(function(){
			me.fillGrammarStyle();
		});
      
		loadGrammar.click(function(){
			if (menuData != null){
				var gr = grammarSelect.val()
				var st = styleSelect.val()
				var gramFile = menuData[gr]["concretesyntax"];
				var metaFile = menuData[gr]["metamap"];
				var stDefFile = menuData[gr]["styles"][st]["styledef"];
				var stMapFile = menuData[gr]["styles"][st]["stylemap"];
				
				
				var data = { grammar : gramFile , metamap : metaFile, styledef : stDefFile, stylemap : stMapFile}
				//console.log("Will send the following data to the server:\n", data);
				scInstance.gen("load_grammar_request_event", data)	
				
				focusParent()
			}
		});
      
		openFile.click(function(){
			data = { name : "ctrl_o_keypress"};
			scInstance.gen("keypress_event", data);
		});
      
		saveFile.click(function(){
			SVG_SAVE= "ctrl_s_keypress"
			TXT_SAVE= "ctrl_t_keypress"
			RTF_SAVE= "ctrl_m_keypress"
			//TODO REMOVE THOSE AND ADD XML SAVE
			
			data = { name : TXT_SAVE}
			scInstance.gen("keypress_event", data)	
		});
      
		checkText.click(function(){
			data = { name : "ctrl_e_keypress"}
			scInstance.gen("keypress_event", data)	
		});
      
    }
    
    /** fills the menu with the grammar data in the forn of a json string*/
    this.fillMenus = function(jString){
		menuData = JSON.parse(jString)
		txt = ""
		for (var grammar in menuData){
			grammarSelect.append("<option value=\"" + grammar +"\">" + grammar + "</option>")
		}
		//grammarSelect.selectmenu("refresh");
		
		this.fillGrammarStyle();
	}
		
	this.fillGrammarStyle = function(){
		if (menuData != null){
			var val = grammarSelect.val()
			styleSelect.empty()
			var styles = menuData[val]['styles']
			for (var style in styles){
				styleSelect.append("<option value=\"" + style +"\">" + style + "</option>")
			}
			//styleSelect.selectmenu("refresh");
		}
    }
  
    
}