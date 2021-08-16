/* INSERT NEW GRAMMARS HERE
	
you can add a new DSL grammar here:

by writing the grammar name (will appear in the menu)
followed by the locations of the four important parts
the following locations must be provided:

*concretesyntax: is the concrete syntax grammar.
*metamap: is the part responsible for mapping the concrete syntax to the metamodel
*styles: the styles used for higlighting
         they consist of a name (free to chose) that will appear in the menu and two parts: 
             styledef: the css style defintions
             stylemap: mapps the concretesytax to a styledef 

note that all parts van be in the same file but even so all four parts must be declared.
leaving stylemap and stledef empty (there must at least me an empty string). will result in the use of the defaults style
*/
var GRAMMARS = //DO NOT CHANGE THIS NAME ! 
	{	  
		"Petrinet" 		:{ 	"concretesyntax": "grammar_parser_v2/grammars/examples/petrinet.g",
							"metamap": "grammar_parser_v2/grammars/examples/petrinet.g",
							"styles" :  { 
											"default" : { 
															"styledef": "grammar_parser_v2/models/examples/petri_style.st" , 
															"stylemap": "grammar_parser_v2/models/examples/petri_style.st" 
														},
											"generic":  { 
															"styledef": "" ,  //will use default style 
															"stylemap": "" 
														}
										} //end petrinet styles
						}, //end petrinet
		"MetaGrammar" 	:{ 	"concretesyntax": "grammar_parser_v2/grammars/examples/meta_grammar.g",
							"metamap": "",
							"styles" :  { 
											"default" : { 
															"styledef": "grammar_parser_v2/models/examples/meta_grammar.st" , 
															"stylemap": "grammar_parser_v2/models/examples/meta_grammar.st" 
														},
											"generic":  { 
															"styledef": "" , //will use default style 
															"stylemap": "" 
														}
										} //end metagrammar styles
							} //end meta grammar
					
	}//end of list 
