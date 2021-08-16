class DevsGrammar(object):
	def __init__(self):
		self.tokens = {
			'AFTER_TOK': {'type': 'token', 'reg' : r'after', 'errortext': 'any'},
			'ANY_TOK': {'type': 'token', 'reg' : r'any', 'errortext': 'any'},
			'TRANSITION_TOK': { 'type': 'token', 'reg' : r'->', 'errortext': 'transition'},
			'OUT_TOK': {'type': 'token', 'reg' : r'out', 'errortext': 'out'},
			'CONNECTIONS_TOK': {'type': 'token', 'reg' : r'connections', 'errortext': 'connections'},
			'FROM': {'type': 'token', 'reg' : r'from', 'errortext': 'from'},
			'TO': {'type': 'token', 'reg' : r'to', 'errortext': 'to'},

			'LBRAC': {'type': 'token', 'reg' : r'{', 'errortext': '{'},
			'RBRAC': {'type': 'token', 'reg' : r'}', 'errortext': '}'},
			'LSQP': {'type': 'token', 'reg' : r'\[', 'errortext': '['},
			'RSQP': {'type': 'token', 'reg' : r'\]', 'errortext': ']'},

			'LPAR': {'type': 'token', 'reg' : r'\(', 'errortext': 'left parenthesis'},
			'RPAR': {'type': 'token', 'reg' : r'\)', 'errortext': 'right parenthesis'},


			'SUM_TOK': {'type': 'token', 'reg' : r'\+', 'errortext': '+'},
			'SUB_TOK': {'type': 'token', 'reg' : r'-', 'errortext': '-'},
			'MULT_TOK': {'type': 'token', 'reg' : r'\*', 'errortext': '*'},
			'DIV_TOK': {'type': 'token', 'reg' : r'/', 'errortext': '/'},

 			'DECIMAL': {'type': 'token', 'reg' : r'[+-]?(0|[1-9]\d*[lL]?)', 'errortext': 'decimal'},
 			'FLOAT': {'type': 'token', 'reg' : r'[+-]?((\d+\.\d*|\.\d+)([eE][-+]?\d+)?|\d+[eE][-+]?\d+)', 'errortext': 'float'},

 			'STRVALUE': {'type': 'token', 'reg' : r'u?r?("(?!"").*?(?<!\\)(\\\\)*?"|\'(?!\'\').*?(?<!\\)(\\\\)*?\')', 
						'errortext': 'string value'},
 			'LONG_STRVALUE': {'type': 'token', 'reg' : r'(?s)u?r?(""".*?(?<!\\)(\\\\)*?"""|\'\'\'.*?(?<!\\)(\\\\)*?\'\'\')', 
						'errortext': 'long string value'},

			'TRUE': {'type': 'token', 'reg' : r'True', 'errortext': 'True value'},
			'FALSE': {'type': 'token', 'reg' : r'False', 'errortext': 'False value'},

 			'NONE': {'type': 'token', 'reg' : r'None', 'errortext': 'None value'},
 			'NOTHING': {'type': 'token', 'reg' : r'nothing', 'errortext': 'nothing value'},

 			'EXT_TOK':  {'type': 'token', 'reg' : r'ext', 'errortext': 'ext'},
 			'IF_TOK':  {'type': 'token', 'reg' : r'if', 'errortext': 'if'},
 			'ELSE_TOK':  {'type': 'token', 'reg' : r'else', 'errortext': 'else'},
 			'RETURN_TOK':  {'type': 'token', 'reg' : r'return', 'errortext': 'return'},
 			'INITIAL_TOK':  {'type': 'token', 'reg' : r'initial', 'errortext': 'initial'},
 			'MODE_TOK':  {'type': 'token', 'reg' : r'mode', 'errortext': 'mode'},

 			'ATOMIC_TOK':  {'type': 'token', 'reg' : r'atomic', 'errortext': 'atomic'},
 			'COUPLED_TOK':  {'type': 'token', 'reg' : r'coupled', 'errortext': 'coupled'},

 			'OUTPORTS_TOK':  {'type': 'token', 'reg' : r'outports', 'errortext': 'outports'},
 			'INPORTS_TOK':  {'type': 'token', 'reg' : r'inports', 'errortext': 'inports'},
 			'COMPONENT_TOK': {'type': 'token', 'reg' : r'component', 'errortext': 'component'},
 			'FUNCTION_TOK': {'type': 'token', 'reg' : r'function', 'errortext': 'function'},
 			'DOT': {'type': 'token', 'reg' : r'\.', 'errortext': 'dot'},
			'NAME': {'type': 'token', 'reg' : r'[a-zA-Z_][a-zA-Z_0-9]*(?!r?"|r?\')', 'errortext': 'name token'},
 			'WHITESPACE': {'type': 'token', 'reg' : r'[ ]+', 'errortext': 'white space'},
			'NEWLINE': {'type': 'token', 'reg' : r'[ \t]*\n', 'errortext': 'newline'},
 			'COMMENTS': {'type': 'token', 'reg' : r'\#[^\n]*\n+', 'errortext': 'comments'},
			'COMMA': {'type': 'token', 'reg' : r',', 'errortext': 'comma'},
			'SEMICOLON': {'type': 'token', 'reg' : r';', 'errortext': 'semicolon'},
			'ASSIGN': {'type': 'token', 'reg' : r'=', 'errortext': 'assign'},
			'EQUALS': {'type': 'token', 'reg' : r'==', 'errortext': 'equals'},

			'COLON': {'type': 'token', 'reg' : r':', 'errortext': 'colon \':\' token'},

 			'TABSPACE': {'type': 'token', 'reg' : r'\t', 'errortext': 'tab'},
 			'WS4': {'type': 'token', 'reg' : r'    ', 'errortext': 'four spaces'}
		}
		self.rules = {
			'start': {'type': 'prod', 'body' : ['+', ['.', ['*','@ignore'],'@toplevel', ['*','@ignore']]]},

			'toplevel': {'type': 'prod', 'body' : ['|', '@component', '@function_def']},

 			'component': {'type': 'prod', 'body' : ['.', '$COMPONENT_TOK', ['+','$WHITESPACE'], '$NAME', 
													'$LPAR', ['?','@args'], '$RPAR', 
													['|',['+', '$NEWLINE'], 
														['.','$COLON',['+','$NEWLINE'],['+',['#indent','@component_body']]]
													],['*','$NEWLINE']
												],
						'errortext': 'component definition'},

			'component_body': {'type': 'prod', 'body' : ['|', '@function_def','@port_attribute', '@atomic', '@coupled', '@connections'], 
							'errortext': 'component body'},

			'function_def': {'type': 'prod', 'body' : ['.', '$NAME', 
													'$LPAR', ['?','@args'], '$RPAR', 
													'$COLON',['+','$NEWLINE'],['+',['#indent','@statement']],['*','$NEWLINE']
												],
						'errortext': 'function definition'},

			'statement': {'type': 'prod', 'body' : ['|', '@ifelse', '@return'], 
							'errortext': 'statement definition'},

			'inlinestatement': {'type': 'prod', 'body' : ['|', '@in_ifelse', '@in_return'], 
							'errortext': 'statement definition'},

			'return': {'type': 'prod', 'body' : ['.', '$RETURN_TOK',['?','$WHITESPACE'],'@expression',['+','$NEWLINE']], 'errortext': 'return definition'},
			'in_return': {'type': 'prod', 'body' : ['.', '$RETURN_TOK',['?','$WHITESPACE'],'@expression','$SEMICOLON',['?','$WHITESPACE']], 'errortext': 'return definition'},

			'ifelse': {'type': 'prod', 'body' : ['.', '$IF_TOK',['?','$WHITESPACE'],'@expression',['?','$WHITESPACE'],'$COLON',['*','$NEWLINE'],
													['+',['#indent','@statement']],
													['?',['#(0)indent','$ELSE_TOK','$COLON',['*','$NEWLINE'],['+',['#indent','@statement']]]]], 
													'errortext': 'if else definition'},

			'in_ifelse': {'type': 'prod', 'body' : ['.', '$IF_TOK',['?','$WHITESPACE'],'@expression',['?','$WHITESPACE'],'$COLON',['?','$WHITESPACE'],
													['+','@inlinestatement'], ['?',['.','$ELSE_TOK','$COLON',['?','$WHITESPACE'],['+','@inlinestatement']]]],
													'errortext': 'if else definition'},

			'connections': {'type': 'prod', 'body' : ['.', '$CONNECTIONS_TOK','$COLON','$NEWLINE',
													['+',['#indent','@connections_body']]], 'errortext': 'connections definition'},

			'connections_body': {'type': 'prod', 'body' : ['.', '$FROM', ['?','$WHITESPACE'], '@dotted_name', ['?','$WHITESPACE'], '$TO', ['?','$WHITESPACE'],'@dotted_name',
												['+','$NEWLINE']], 
								'errortext': 'connections definition'},

			'atomic': {'type': 'prod', 'body' : ['.', '$ATOMIC_TOK','$COLON',['+','$NEWLINE'],
													['+',['#indent','@atomic_body']]], 'errortext': 'atomic definition'},

			'atomic_body': {'type': 'prod', 'body' : ['|', '@initial','@mode'], 'errortext': 'atomic body'},

			'initial': {'type': 'prod', 'body' : ['.', '$INITIAL_TOK','$WHITESPACE', '@functioncall',
												['+','$NEWLINE']], 'errortext': 'initial definition'},

 			'pars': {'type': 'prod', 'body' : ['.', '@expression', ['*',['.','$COMMA',['?','$WHITESPACE'],'@expression']]],
						'errortext': 'parameters'},

			'mode': {'type': 'prod', 'body' : ['.', '$MODE_TOK','$WHITESPACE','@functioncall', '$COLON', 
												['+','$NEWLINE'],['+',['#indent', '@mode_body']]
												], 'errortext': 'mode definition'},

			'mode_body': {'type': 'prod', 'body' : ['|', '@transition','@out'], 
						'errortext': 'mode body'},

			'out': {'type': 'prod', 'body' : ['.', '$OUT_TOK','$WHITESPACE','@code', ['*','$NEWLINE']], 
				'errortext': 'output function'},

			'code': {'type': 'prod', 'body' : ['|', '@expression', ['.', '$LBRAC',['?','$WHITESPACE'],'@inlinestatement', ['?','$WHITESPACE'],'$RBRAC']], 
				'errortext': 'output function'},


			'transition': {'type': 'prod', 'body' : ['.', '@pre', '$WHITESPACE', '$TRANSITION_TOK','$WHITESPACE','@pos', ['+','$NEWLINE']], 
						'errortext': 'transition'},

			'pre': {'type': 'prod', 'body' : ['|', '@after', '$ANY_TOK','@external'], 
						'errortext': 'precondition'},

			'external': {'type': 'prod', 'body' : ['.', '$EXT_TOK', '$WHITESPACE','@code'], 
						'errortext': 'external'},

			'after': {'type': 'prod', 'body' : ['.', '$AFTER_TOK', '$WHITESPACE','@code'], 
						'errortext': 'after precondition'},

			'pos': {'type': 'prod', 'body' : ['|', '@functioncall', '$ANY_TOK'], 
						'errortext': 'poscondition'},

			'functioncall': {'type': 'prod', 'body' : ['.', '$NAME', '$LPAR', ['?','@pars'],'$RPAR'], 
						'errortext': 'mode call'},

			'coupled': {'type': 'prod', 'body' : ['.', '$COUPLED_TOK','$COLON',['+','$NEWLINE'],
													['+',['#indent','@assignment']]], 'errortext': 'coupled definition'},

			'assignment': {'type': 'prod', 'body' : ['.', '$NAME',['?','$WHITESPACE'],'$ASSIGN',['?','$WHITESPACE'],'@functioncall', ['+','$NEWLINE']], 
												'errortext': 'assignment definition'},

			'inport_attribute': {'type': 'prod', 'body' : ['.', '$INPORTS_TOK',
														'$WHITESPACE', '@name_list',
														['+','$NEWLINE']], 'errortext': 'inport attribute'},

			'outport_attribute': {'type': 'prod', 'body' : ['.', '$OUTPORTS_TOK',
														'$WHITESPACE', '@name_list',
														['+','$NEWLINE']], 'errortext': 'outport attribute'},

 			'name_list': {'type': 'prod', 'body' : ['.', '$NAME', ['*',['.','$COMMA',['?','$WHITESPACE'],'$NAME']]],
						'errortext': 'name list definition'},

			'port_attribute': {'type': 'prod', 'body' : ['|','@outport_attribute','@inport_attribute'],
														'errortext': 'port attribute'},

 			'args': {'type': 'prod', 'body' : ['.', '@argument', ['*',['.','$COMMA',['?','$WHITESPACE'],'@argument']]],
						'errortext': 'arguments definition'},

 			'argument': {'type': 'prod', 'body' : ['.', '$NAME', ['?',['.','$ASSIGN',['?','@ignore'],'@atomvalue']]],
						'errortext': 'argument definition'},

			'atomvalue': {'type': 'prod', 'body' : ['|', '@number', '@boolean', '@string', '$NONE', '$NOTHING'], 'errortext': 'atom value'},
			
			'expression': {'type': 'prod', 'body' : ['|', '@atomvalue', '@dotted_name', '@operation', '@functioncall', '@selection','@dict', '@vect'], 
						'errortext': 'expression'},

			'operation': {'type': 'prod', 'body' : ['.', '@expression', ['?','$WHITESPACE'], '@op', ['?','$WHITESPACE'], '@expression'], 
						'errortext': 'operation'},

			'op': {'type': 'prod', 'body' : ['|', '$EQUALS','$SUM_TOK', '$SUB_TOK', '$MULT_TOK', '$DIV_TOK'], 
						'errortext': 'op symbol'},

			'dict': {'type': 'prod', 'body' : ['.', '$LBRAC', ['?','@dict_elems'], '$RBRAC'], 
						'errortext': 'dictionary'},

			'dict_elems': {'type': 'prod', 'body' : ['.', '@dict_elem', ['*',['.', '$COMMA', ['?','@ignore'],'@dict_elem']]],
						'errortext': 'dictionary elements'},

			'dict_elem': {'type': 'prod', 'body' : ['.', '@expression', ['?','$WHITESPACE'], '$COLON', ['?','$WHITESPACE'], '@expression'], 
						'errortext': 'dictionary elements'},

			'selection': {'type': 'prod', 'body' : ['.', '@expression','$LSQP', '@expression', '$RSQP'], 
						'errortext': 'selection'},

			'vect': {'type': 'prod', 'body' : ['.', '$LSQP', ['?','@vect_elems'], '$RSQP'], 
						'errortext': 'vector'},

			'vect_elems': {'type': 'prod', 'body' : ['.', '@expression', ['*',[ '.', '$COMMA', ['?','@ignore'],'@expression']]],
						'errortext': 'vector elements'},

			'number': {'type': 'prod', 'body' : ['|', '$DECIMAL', '$FLOAT'], 'errortext': 'number'},

			'string': {'type': 'prod', 'body' : ['|', '$STRVALUE', '$LONG_STRVALUE'], 'errortext': 'string'},

			'boolean': {'type': 'prod', 'body' : ['|', '$TRUE', '$FALSE'], 'errortext': 'boolean value'},

 			'dotted_name': {'type': 'prod', 'body' : ['.', '$NAME', ['*', ['.','$DOT', '$NAME']]], 'errortext': 'dotted name'},

 			'indent': {'type': 'prod', 'body' : ['|', '$TABSPACE', '$WS4'], 'errortext': 'indentation'},
 			'ignore': {'type': 'prod', 'body' : ['|', '$WHITESPACE', '$COMMENTS'], 'errortext': 'ignore'}
		}