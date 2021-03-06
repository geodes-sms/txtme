"""
Author: Daniel Riegelhaupt
Date: december  2014

Auto generated by creating the StyleGrammar( subclass of BaseGrammar) class using the grammarCompilerVisitor and calling
classToSt() on it
"""
class StyleGrammar(object):
	def __init__(self):
		self.rules = {
			'styles': {'body': ['.', '$STYLES', '$LCBR', ['*', '@style_def'], '$RCBR'], 'type': 'prod', 'errortext': 'styles'},
			'path_name': {'body': ['|', ['.', '$IDENTIFIER', ['*', ['.', '$DOT', '$IDENTIFIER']]], '$STAR'], 'type': 'prod', 'errortext': 'path_name'},
			'style': {'body': ['.', '$STR'], 'type': 'prod', 'errortext': 'style'},
			'attr_def': {'body': ['.', '@attr_name', '$COLON', '@style', ['?', '$IMPORTANT']], 'type': 'prod', 'errortext': 'attr_def'},
			'class_name': {'body': ['.', '$CSS_CLASS_NAME'], 'type': 'prod', 'errortext': 'class_name'},
			'attr_name': {'body': ['.', '$CSS_ATTR_NAME'], 'type': 'prod', 'errortext': 'attr_name'},
			'style_mapping': {'body': ['.', '$STYLE_MAP', '$LCBR', ['*', '@style_map'], '$RCBR'], 'type': 'prod', 'errortext': 'style_mapping'},
			'style_def': {'body': ['.', '@class_name', '$LCBR', '@attr_def', ['*', ['.', '$SEMICOL', '@attr_def']], ['?', '$SEMICOL'], '$RCBR'], 'type': 'prod', 'errortext': 'style_def'},
			'start': {'body': ['+', ['|', '@styles', '@style_mapping']], 'interleave': ['?', '@implicit'], 'type': 'prod', 'errortext': 'start'},
			'style_name': {'body': ['.', '$IDENTIFIER'], 'type': 'prod', 'errortext': 'style_name'},
			'type': {'body': ['|', '$KEYWORDS', '$DEFAULT', '$ERROR'], 'type': 'prod', 'errortext': 'type'},
			'implicit': {'body': ['*', ['|', '$NEWLINE', '$WS', '$LINE_CONT', '$SINGLE_COMMENT', '$MULTI_COMMENT']], 'type': 'prod', 'errortext': "Automatically generated 'Implict' rule"},
			'style_map': {'body': ['.', ['?', '@type'], '@path_name', '$COLON', '@style_name', '$SEMICOL'], 'type': 'prod', 'errortext': 'style_map'}
		}

		self.tokens = {
			'CSS_ATTR_NAME': { 'type': 'token', 'reg': r'[:]?[a-zA-Z_\-:][a-zA-Z_0-9\-]*', 'errortext': 'CSS attribute name'},
			'STYLES': { 'type': 'token', 'reg': r'styles', 'errortext': 'styles'},
			'NEWLINE': { 'type': 'token', 'reg': r'(\r?\n[\t ]*)+', 'errortext': 'New Line'},
			'CSS_CLASS_NAME': { 'type': 'token', 'reg': r'[\.][a-zA-Z_][a-zA-Z_0-9]*', 'errortext': 'CSS class name'},
			'RCBR': { 'type': 'token', 'reg': r'\}', 'errortext': '}'},
			'DEFAULT': { 'type': 'token', 'reg': r'@Default', 'errortext': '@Default'},
			'MULTI_COMMENT': { 'type': 'token', 'reg': r'/\*(.|\n)*?\*/', 'errortext': 'Multi line comment'},
			'WS': { 'type': 'token', 'reg': r'[\t \f]+', 'errortext': 'White space'},
			'SEMICOL': { 'type': 'token', 'reg': r';', 'errortext': ';'},
			'LCBR': { 'type': 'token', 'reg': r'\{', 'errortext': '{'},
			'LINE_CONT': { 'type': 'token', 'reg': r'\\[\t \f]*\r?\n', 'errortext': 'Line continuation'},
			'STYLE_MAP': { 'type': 'token', 'reg': r'stylemap', 'errortext': 'stylemap'},
			'IMPORTANT': { 'type': 'token', 'reg': r'!important', 'errortext': '!important'},
			'COLON': { 'type': 'token', 'reg': r':', 'errortext': ':'},
			'SINGLE_COMMENT': { 'type': 'token', 'reg': r'//[^\n]*', 'errortext': 'Single line comment'},
			'STR': { 'type': 'token', 'reg': r'.[^;!]*', 'errortext': 'String content'},
			'ERROR': { 'type': 'token', 'reg': r'@Error', 'errortext': '@Error'},
			'KEYWORDS': { 'type': 'token', 'reg': r'@Keywords', 'errortext': '@Keywords'},
			'STAR': { 'type': 'token', 'reg': r'\*', 'errortext': '\*'},
			'IDENTIFIER': { 'type': 'token', 'reg': r'[a-zA-Z_][a-zA-Z_0-9\-]*', 'errortext': 'Identifier'},
			'DOT': { 'type': 'token', 'reg': r'\.', 'errortext': '.'}
		}