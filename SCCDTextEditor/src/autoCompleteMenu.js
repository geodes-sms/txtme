function AutoCompleteMenu(rootNode){
  
  this.root = rootNode;
  this.input = this.root.firstElementChild;
  this.JQInput = $(this.input) 
  this.list = $(this.root.lastElementChild);
  this.scInstance = null
  var me = this
  
  this.setStateChart = function(scInstance){
      this.scInstance = scInstance;
	  this.addListeners();
	  
	  //the nodes have been created dynamically and will have no visible width and height the first time
	  //they are called. the seond time evryhting show op fine
	  //in order for the user not to have to call the menu twice the first time we call it here first and remove it directly after
	  this.createMenu([['foobar',true]], {x:0,y:0}, '')
	  this.removeMenu()
  }
  
  this.removeListners =function(){
	//this.input.off();  
  }
  
  this.addListeners = function(){
		//var origListner = this.input.onkeyup
		//console.log(this.input.onkeyup)
		var input = this.input
		//those two need to be here to stop the event from propagatin to the documetn so that the defulat behaviour will be kept
		input.addEventListener("keypress", function (event) {
			//console.log("input keypress:", event.which);
			event.stopPropagation();
		}, true);
		input.addEventListener("keydown", function (event) {
			//console.log("input keydown:", event.which);
			event.stopPropagation();
		}, true);
		
		input.addEventListener("keyup", function (event) {
			//console.log("input keyup:", event.which)
			if (event.which == 13){ //Enter
				event.preventDefault();
				var inputVal = input.value ;
				if ((inputVal != null) && (inputVal != ""))
					me.scInstance.gen("auto_complete_exit_value", { value: inputVal});
				console.log("Enter pressed, value = ", inputVal);
				
			}
			else if (event.which == 27){ //escape
				event.preventDefault();
				me.scInstance.gen("auto_complete_exit_empty", null);
				//console.log("ESCAPE");
				//me.removeMenu();
			}
      }, true);
  }
  
  
  /**
   @param suggestionList a list of suggestion. a susggestion is tuple string, boolean (where boolean is true is the string is selectable and false if it is only a hint)
   @param xyPos: a dictionary { x, y }: the coordinates where to show the menu
   @param startText: A string oprtional: the text that should be in the input
   */
  this.createMenu = function(suggestionList, xyPos, startText){
      if (suggestionList.length > 0){
		maxLen = 3;
		//this.input.append("<option value=\"\">   </option>")//an empy disabled input option
		for (index in suggestionList){
			suggestion = suggestionList[index]
			l = suggestion[0].length;
			if (l > maxLen)
			maxLen = l;
			
			if (suggestion[1] == true)
				this.list.append("<option value=\"" + suggestion[0] +"\">" + suggestion[0] + "</option>")
			else
				this.list.append("<option value=\"\" label=\"hint: "+ suggestion[0] + "\"></option>")
		}
		
		this.root.setAttribute("x", xyPos.x);
		this.root.setAttribute("y", xyPos.y);
		this.root.setAttribute("z", 9999);
		this.root.setAttribute("height", this.JQInput.outerHeight()+2);
		//this.root.setAttribute("width", (maxLen).toString() + "em"); //Width is set twice. first a too big number, too make sure the input is visible 
		this.root.setAttribute("width", this.JQInput.outerWidth()+2); 
		//than the correct input width.Note that this must be done this way. if we directly try the slect width it will give a wrong number (too small)
		this.input.focus();
		var text = (typeof(startText) == "undefined") ? "" : startText;
			this.input.value = text
		
		//forces the list to be show each time it is created
		//list[0] means getting the DOM object from the jquery element
		this.list[0].setAttribute("style", "display:none;"); //this force it to be shown every time if this line is not here it will only be shown on first use
		this.list[0].setAttribute("style", "");
      }
  } 
  
  
  this.removeMenu = function(){
	  //this.removeListners();
      this.input.value = "";
	  this.input.blur(); //make it lose focus
	  this.list.empty();
      this.root.setAttribute("x", 0);
      this.root.setAttribute("y", 0);
      this.root.setAttribute("z", 0);
      this.root.setAttribute("width", 0);
      this.root.setAttribute("height", 0);
  }
}