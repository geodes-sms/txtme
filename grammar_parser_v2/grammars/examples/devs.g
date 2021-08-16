grammar{

  start: ( ignore* toplevel ignore* )+;  

  toplevel:  component | function_def ;

  component: COMPONENT_TOK WHITESPACE+ NAME LPAR args? RPAR (NEWLINE+ | COLON NEWLINE+ (indent component_body)#+ ) NEWLINE*
	@Msg 'component definition';

  component_body: function_def | port_attribute | atomic | coupled | connections 
	      @Msg 'component body';

  function_def: NAME LPAR args ? RPAR COLON NEWLINE+(indent statement)#+ NEWLINE*
	    @Msg 'function definition';

  statement: ifelse| return 
	  @Msg 'statement definition';

  inlinestatement: in_ifelse | in_return 
	      @Msg 'statement definition';

  return: RETURN_TOK WHITESPACE? expression NEWLINE+
      @Msg 'return definition';

  in_return: RETURN_TOK WHITESPACE? expression SEMICOLON WHITESPACE?  
	  @Msg 'return definition';

  ifelse: IF_TOK WHITESPACE? expression WHITESPACE? COLON NEWLINE* (indent statement)#+ (indent ELSE_TOK COLON NEWLINE* (indent statement)#+ )#[0]?
      @Msg 'if else definition';

  in_ifelse: IF_TOK WHITESPACE? expression WHITESPACE? COLON WHITESPACE? inlinestatement+ (ELSE_TOK COLON WHITESPACE? inlinestatement+)?
	  @Msg 'if else definition';

  connections: CONNECTIONS_TOK COLON NEWLINE (indent connections_body)#+
	    @Msg 'connections definition';

  connections_body: FROM WHITESPACE? dotted_name WHITESPACE? TO WHITESPACE? dotted_name NEWLINE+
		@Msg 'connections definition';

  atomic:  ATOMIC_TOK COLON NEWLINE+ (indent atomic_body)#+
      @Msg 'atomic definition';

  atomic_body: initial | mode
	    @Msg 'atomic body';

  initial: INITIAL_TOK WHITESPACE functioncall NEWLINE+ 
	@Msg 'initial definition';

  pars: expression (COMMA WHITESPACE? expression)*
    @Msg 'parameters';

  mode: MODE_TOK WHITESPACE functioncall COLON NEWLINE+ (indent mode_body)#+
    @Msg 'mode definition';

  mode_body: transition | out 
	  @Msg 'mode body';

  out: OUT_TOK WHITESPACE code NEWLINE* 
	  @Msg 'output function';

  code: expression | ( LBRAC WHITESPACE? inlinestatement WHITESPACE? RBRAC ) 
    @Msg 'output function';


  transition: pre WHITESPACE TRANSITION_TOK WHITESPACE pos NEWLINE+ 
	  @Msg 'transition';

  pre: after| ANY_TOK | external 
    @Msg 'precondition';

  external: EXT_TOK WHITESPACE code 
	@Msg 'external';

  after: AFTER_TOK WHITESPACE code 
      @Msg 'after precondition';

  pos: functioncall| ANY_TOK 
    @Msg 'poscondition';

  functioncall: NAME LPAR pars? RPAR 
	    @Msg 'mode call';

  coupled: COUPLED_TOK COLON NEWLINE+ (indent assignment)#+ 
	@Msg 'coupled definition';

  assignment: NAME WHITESPACE? ASSIGN WHITESPACE? functioncall NEWLINE+ 
	  @Msg 'assignment definition';

  inport_attribute: INPORTS_TOK WHITESPACE name_list NEWLINE+ 
		@Msg 'inport attribute';

  outport_attribute: OUTPORTS_TOK WHITESPACE name_list NEWLINE+
		  @Msg 'outport attribute';

  name_list:  NAME (COMMA WHITESPACE? NAME)*
	  @Msg 'name list definition';

  port_attribute: outport_attribute | inport_attribute
	      @Msg 'port attribute';

  args: argument ( COMMA WHITESPACE? argument)*
    @Msg 'arguments definition';

  argument: NAME (ASSIGN ignore? atomvalue)?
	@Msg 'argument definition';

  atomvalue:  number | boolean | string | NONE | NOTHING 
	  @Msg 'atom value';

  expression: atomvalue | dotted_name | operation | functioncall | selection | dict | vect 
	  @Msg 'expression';
  
  operation: expression WHITESPACE? op WHITESPACE? expression 
	  @Msg 'operation';

  op: EQUALS | SUM_TOK | SUB_TOK | MULT_TOK | DIV_TOK 
  @Msg 'op symbol';

  dict: LBRAC dict_elems? RBRAC 
    @Msg 'dictionary';

  dict_elems: dict_elem (COMMA ignore? dict_elem)* 
	  @Msg 'dictionary elements';

  dict_elem: expression WHITESPACE? COLON WHITESPACE? expression 
	  @Msg 'dictionary elements';

  selection: expression LSQP expression RSQP 
	  @Msg 'selection';

  vect: LSQP vect_elems? RSQP 
    @Msg 'vector';

  vect_elems: expression (COMMA ignore? expression)* 
	  @Msg 'vector elements';

  number:  DECIMAL | FLOAT
      @Msg 'number';

  string: STRVALUE | LONG_STRVALUE 
      @Msg 'string';

  boolean: TRUE | FALSE
      @Msg 'boolean value';

  dotted_name: NAME (DOT NAME)*
	    @Msg 'dotted name';

  indent: TABSPACE | WS4
      @Msg 'indentation';

  ignore: WHITESPACE | COMMENTS 
      @Msg 'ignore';


  tokens{
	  AFTER_TOK:  'after' @Msg 'any';
	  ANY_TOK:  'any' @Msg 'any';
	  TRANSITION_TOK: '->' @Msg 'transition';
	  OUT_TOK:  'out' @Msg 'out';
	  CONNECTIONS_TOK:  'connections' @Msg 'connections';
	  FROM:  'from' @Msg 'from';
	  TO:  'to' @Msg 'to';

	  LBRAC:  '{' @Msg '{';
	  RBRAC:  '}' @Msg '}';
	  LSQP:  '\[' @Msg '[';
	  RSQP:  '\]' @Msg ']';

	  LPAR:  '\(' @Msg 'left parenthesis';
	  RPAR:  '\)' @Msg 'right parenthesis';


	  SUM_TOK:  '\+' @Msg '+';
	  SUB_TOK:  '-' @Msg '-';
	  MULT_TOK:  '\*' @Msg '*';
	  DIV_TOK:  '/' @Msg '/';

	  DECIMAL:  '[+-]?(0|[1-9]\d*[lL]?)' @Msg 'decimal';
	  FLOAT:  '[+-]?((\d+\.\d*|\.\d+)([eE][-+]?\d+)?|\d+[eE][-+]?\d+)' @Msg 'float';

	  STRVALUE:  'u?r?("(?!"").*?(?<!\\)(\\\\)*?"|\'(?!\'\').*?(?<!\\)(\\\\)*?\')' 
				 @Msg 'string value';
	  LONG_STRVALUE:  '(?s)u?r?(""".*?(?<!\\)(\\\\)*?"""|\'\'\'.*?(?<!\\)(\\\\)*?\'\'\')'
				   @Msg 'long string value';

	  TRUE:  'True' @Msg 'True value';
	  FALSE:  'False' @Msg 'False value';

	  NONE:  'None' @Msg 'None value';
	  NOTHING:  'nothing' @Msg 'nothing value';

	  EXT_TOK:   'ext' @Msg 'ext';
	  IF_TOK:   'if' @Msg 'if';
	  ELSE_TOK:   'else' @Msg 'else';
	  RETURN_TOK:   'return' @Msg 'return';
	  INITIAL_TOK:   'initial' @Msg 'initial';
	  MODE_TOK:   'mode' @Msg 'mode';

	  ATOMIC_TOK:   'atomic' @Msg 'atomic';
	  COUPLED_TOK:   'coupled' @Msg 'coupled';

	  OUTPORTS_TOK:   'outports' @Msg 'outports';
	  INPORTS_TOK:   'inports' @Msg 'inports';
	  COMPONENT_TOK:  'component' @Msg 'component';
	  FUNCTION_TOK:  'function' @Msg 'function';
	  DOT:  '\.' @Msg 'dot';
	  NAME:  '[a-zA-Z_][a-zA-Z_0-9]*(?!r?"|r?\')' @Msg 'name token';
	  WHITESPACE:  '[ ]+' @Msg 'white space';
	  NEWLINE:  '[ \t]*\n' @Msg 'newline';
	  COMMENTS:  '\#[^\n]*\n+' @Msg 'comments';
	  COMMA:  ',' @Msg 'comma';
	  SEMICOLON:  ';' @Msg 'semicolon';
	  ASSIGN:  '=' @Msg 'assign';
	  EQUALS:  '==' @Msg 'equals';

	  COLON:  ':' @Msg 'colon ';

	  TABSPACE:  '\t' @Msg 'tab';
	  WS4:  '    ' @Msg 'four spaces';
  }
}

