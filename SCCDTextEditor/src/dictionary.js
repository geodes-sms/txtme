/**
A simple dictionary class
@author Daniel Riegelhaupt
@date December, 2014
*/

function Dictionary(){
  var dict = new Object();
  
  /** will add key, value  pair to the dictionry if key is not yet in the dictionary and overwrite value if it already was*/
  this.set = function(key, value){
    dict[key] = value
  }
  
  /** will return the value assigned to key or undefined if no such key is in the dictionary*/
  this.get = function(key){
    return dict[key]
  } 
  
  /** returns the list of keys*/
  this.keys = function(){
    return Object.getOwnPropertyNames(dict)
  }
  
  /** returns true if the dictionry contains the key, false otherwise*/
  this.hasKey = function(key){
    return typeof dict[key] !== 'undefined'
  }
  
  /** will remove key if it is in the dictionary*/
  this.remove = function(key){
    delete dict[key]
  }
  
  /** will return true if the key value pair of both dictionary match, will return false otherwise*/
  this.compare = function(other){
    var ret = true;
    if (other instanceof Dictionary){
      otherKeys = other.keys()
      theseKeys = this.keys()
      if (otherKeys.length == theseKeys.length){
	for(var k in theseKeys){
	  key = theseKeys[k]
	  if (other.hasKey(key) && (this.get(key) == other.get(key))){
	    continue
	  } else{
	    ret = false;
	    break;
	  }
	}  
      } else{	
	ret = false;
      }
    } else{ 
      ret = false;
    }
    return ret;
  }
   
  /** returns a new object with the same key value pairs
  this will only be a true deep copy if value is a primitive (like int or string)
   */
  this.deepCopy =function(){
    var d = new Dictionary();
    var keys = this.keys()
    var key, value;
    for ( var i in  keys) {
      key = keys[i]
      d.set(key,dict[key])
    } 
    return d;
  }
  
  /** returns a Javascript Iterator that can be used to iterator over the dictionary content.
   itererator().next() will return an array [key,value]
   */
  this.iterator = function(){
     
	var is_chrome = navigator.userAgent.toLowerCase().indexOf('chrome') > -1;
	if (is_chrome == false){
		return Iterator(dict);
	}
	else{
		var l =  []
		var keys = this.keys()
		for ( var i in  keys) {
			key = keys[i]
			l.push([key,dict[key]])
			
		} 
		return l;
	}
	
	
	/*TODO CHECK IF CHROME:
	 and define Iterator as:
	 var Iterator = function(arr){ return {
		index : -1,
		hasNext : function(){ return this.index + 1< arr.length; },
		hasPrevious: function(){ return this.index > 0; },

		current: function(){ return arr[ this["index"] ]; },

		next : function(){
			if(this.hasNext()){
				this.index = this.index + 1;            
				return this.current();
			} 
			return false;
		},

		previous : function(){
			if(this.hasPrevious()){
				this.index = this.index - 1
				return this.current();
			}
			return false;
		}
	}};
	 */
  }
}