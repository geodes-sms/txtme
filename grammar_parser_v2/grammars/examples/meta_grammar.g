/*
  Daniel Riegelhaupt - October 2014
  A grammar that describes other grammars and even itself.

  It is partially based on Erez Shinan's PlyPlus grammar.
*/
grammar{
   
   /*------------------------------
    Production rules
  ------------------------------*/
  start: grammar? mapper?
   @Msg 'Top level start' ;
  
  grammar: GRAMMAR LCBR production_rule* RCBR
     @Msg 'Grammar definition' ;
  
  production_rule: rule_definition | token_collection
	     @Msg 'Top level production rule definition';

  rule_definition: rule_name COLON rule_right_hand_side message? SEMICOL
	     @Msg 'Production rule definition';

  rule_name: LOWER_CASE
       @Msg 'Rule name'; 

  rule_right_hand_side: token_name
		      | token_value
		      | rule_name
		      | LPAR rule_right_hand_side RPAR cardinality?
		      | rule_right_hand_side OR rule_right_hand_side
		      | (rule_right_hand_side rule_right_hand_side) //parentheses not needed just to test visitor
		      | rule_right_hand_side OPER
		   @Msg 'Production rule right hand side'
		      ;

  cardinality: CARD (LSBR MINUS? INT RSBR)?
        @Msg 'Cardinality';

  message: MESSAGE_MOD message_value 
      @Msg 'Error message';
  
  message_value: REGEXP
	   @Msg 'Error message value';
  
  token_collection: TOKENS LCBR  (token_sub_collection | token_definition)*  RCBR
	       @Msg 'Top level token definition';

  token_sub_collection: token_collection_category COLON collection_name LCBR token_definition* RCBR
                   @Msg 'Token collection definition';

  token_collection_category: KEYWORDS
		        @Msg 'Possible token collection categories'; //keep this in a rule in case we decide to add more kind of colelctions such as group that share the same modifier

  collection_name: LOWER_CASE
	      @Msg 'Token collection name';

  token_definition: token_name COLON token_value (modifier|message)* SEMICOL
	      @Msg 'Token definition';
  
  token_name: UPPER_CASE
	@Msg 'Token name';
  
  token_value: REGEXP
         @Msg 'Token value';

  modifier: IMPLICIT_MOD | COMMENT_MOD
      @Msg 'Possible modifiers';

      
  /*------------------------------
    Model mapping
  ------------------------------*/    
      
  mapper: MAPPER LCBR model_mapping_rule RCBR
    @Msg 'Top level model mapper definition';
  
  model_mapping_rule: prod_name ARROW MODEL concept_name LCBR mapping_rules* RCBR
                @Msg 'Model mapper definition';

  mapping_rules: attr_mapping_rule
	      |class_mapping_rule
	      |assoc_mapping_rule
	    @Msg 'Top level mapping rules';
	      
  //we can create one rule containg both using (ATTR|REF) but this allows for modifications later 	      
  attr_mapping_rule: prod_name ARROW ATTR concept_name SEMICOL
	        @Msg 'Attribute mapping rule';
  ref_mapping_rule: prod_name ARROW REF concept_name SEMICOL
	       @Msg 'Reference mapping rule';

  class_mapping_rule: prod_name ARROW CLASS concept_name LCBR attr_mapping_rule* RCBR
                 @Msg 'Class mapping rule';
  assoc_mapping_rule: prod_name ARROW ASSOC concept_name LCBR (attr_mapping_rule|ref_mapping_rule)* RCBR
                 @Msg 'Association mapping rule';

  prod_name: path
       @Msg 'Name of production rule being mapped'; //this must be a path
  concept_name: path
       @Msg 'Name of concept being mapped to'; //maybe make this an identifier but that is more restrictive

  path: IDENTIFIER (DOT IDENTIFIER)*
   @Msg 'Dotted name';           
              
  tokens{
    LOWER_CASE:  '[a-z_][a-z_0-9]*' @Msg 'Lower case characters';
    UPPER_CASE: '[A-Z_][A-Z_0-9]*' @Msg 'Upper case characters';
    REGEXP:  '\'(.|\n)*?[^\\]\'' @Msg 'Regular expression';
    INT: '[0-9]*' @Msg 'Integers';

    IMPLICIT_MOD: '(@Implicit|@Impl)' @Msg '@Implicit or @Impl';
    MESSAGE_MOD: '(@Message|@Msg)' @Msg '@Message or @Msg';
    COMMENT_MOD: '(@Comment|@Cmnt)' @Msg '@Comment or @Cmnt';
    
    //note that there is no need for the keyword part, it is optional and only used here as an example
    keywords:general{
      TOKENS: 'tokens';
      KEYWORDS: 'keywords';
      GRAMMAR: 'grammar';
      MAPPER: 'mapper';
    }

    MINUS: '-';
    OPER :'[?*+]' @Msg 'operator: ?, * or +';
    CARD: '#';
    OR : '\|' @Msg '|';
    LPAR : '\(' @Msg '(';
    RPAR : '\)' @Msg ')';
    SEMICOL: ';';
    COMMA: ',';
    LCBR: '\{' @Msg '{';
    RCBR: '\}' @Msg '}';
    COLON: ':';
    LSBR: '\[' @Msg '[';
    RSBR: '\]' @Msg ']';
    
    
    //mapper tokens
    IDENTIFIER: '[a-zA-Z_][a-zA-Z_0-9]*' @Msg 'Identifier'; //This might cause ambiguities with the parser with lower and uppercase
    DOT: '\.' @Msg '.';
    ARROW: '->';
    ASSOC: '@Assoc' @Msg 'Association mapper symbol';
    ATTR: '@Attr' @Msg 'Attribute mapper symbol';
    CLASS: '@Class' @Msg 'Class mapper symbol';
    MODEL: '@Model' @Msg 'Model mapper symbol';
    REF: '@Ref' @Msg 'Reference mapper symbol';

    // Implicit declarations tokens are tokens that can be applied anywhere in the grammar and don't have to be explicitly declared
    NEWLINE: '(\r?\n[\t ]*)+' @Msg 'New Line' @Implicit;
    WS: '[\t \f]+' @Msg 'White space' @Implicit;
    LINE_CONT: '\\[\t \f]*\r?\n' @Implicit @Msg 'Line continuation';
    SINGLE_COMMENT: '//[^\n]*' @Comment @Msg 'Single line comment';
    MULTI_COMMENT: '/\*(.|\n)*?\*/' @Comment @Msg 'Multi line comment';
  }
}