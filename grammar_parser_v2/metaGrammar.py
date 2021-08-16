"""
Author: Daniel Riegelhaupt
Date: October 2014

The meta grammar needed by Bruno Barroca's parser to read other grammars.
Based on his data structure
"""

class MetaGrammar(object):

    def __init__(self):

        self.tokens = {
            #'<token name>' : { 'type': 'token', 'reg': '<token value>' 'errortext': '<human readable error text>'}
            #important note: for a single backslash character the reg must be r'[\\]' writting '\\' will not work
            #for the error text: the slash is also the escape for strings so '\\' must be written
            "LOWER_CASE":  { 'type': 'token', 'reg': r'[a-z_][a-z_0-9]*', 'errortext': 'Lower case characters'},
            "UPPER_CASE": { 'type': 'token', 'reg': r'[A-Z_][A-Z_0-9]*', 'errortext': 'Upper case characters'},
            "REGEXP":  { 'type': 'token', 'reg': r'\'(.|\n)*?[^\\]\'', 'errortext': 'Regular expression'},
            "INT":  { 'type': 'token', 'reg': r'[0-9]*', 'errortext': 'Integers'},

            "IMPLICIT_MOD": { 'type': 'token', 'reg': r'(@Implicit|@Impl)', 'errortext': '@Implicit or @Impl'},
            "MESSAGE_MOD": { 'type': 'token', 'reg': r'(@Message|@Msg)', 'errortext': '@Message or  @Msg'},
            "COMMENT_MOD": { 'type': 'token', 'reg': r'(@Comment|@Cmnt)', 'errortext': '@Comment or @Cmnt'},
            
            "TOKENS": { 'type': 'token', 'reg': r'tokens'  , 'errortext': 'tokens'},
            "KEYWORDS": { 'type': 'token', 'reg': r'keywords', 'errortext': 'keywords'},
            "GRAMMAR": { 'type': 'token', 'reg': r'grammar', 'errortext': 'grammar'},
            "MAPPER": { 'type': 'token', 'reg': r'mapper', 'errortext': 'mapper'},

            "OPER": { 'type': 'token', 'reg': r'[?*+]', 'errortext': 'operator: ?, * or +'},
            "CARD": { 'type': 'token', 'reg': r'#', 'errortext': '#'},
            "MINUS": { 'type': 'token', 'reg': r'-', 'errortext': '-'},
            "OR": { 'type': 'token', 'reg': r'\|', 'errortext': '|' },
            "LPAR": { 'type': 'token', 'reg': r'\(', 'errortext': '(' },
            "RPAR": { 'type': 'token', 'reg': r'\)', 'errortext': ')' },
            "SEMICOL": { 'type': 'token', 'reg': r';', 'errortext': ';' },
            "COMMA": { 'type': 'token', 'reg': r',', 'errortext': ',' },
            "LCBR": { 'type': 'token', 'reg': r'\{', 'errortext':  '{'},
            "RCBR": { 'type': 'token', 'reg': r'\}', 'errortext': '}' },
            "LSBR": { 'type': 'token', 'reg': r'\[', 'errortext':  '['},
            "RSBR": { 'type': 'token', 'reg': r'\]', 'errortext': ']' },
            "DOT": { 'type': 'token', 'reg': r'\.', 'errortext':  '.'},
            "COLON": { 'type': 'token', 'reg': r':', 'errortext': ':'},

            "IDENTIFIER": { 'type': 'token', 'reg': r'[a-zA-Z_][a-zA-Z_0-9]*', 'errortext': 'Identifier'},
            "ARROW": { 'type': 'token', 'reg': r'->', 'errortext': '->'},
            "ASSOC": { 'type': 'token', 'reg': r'@Assoc', 'errortext': 'Association mapper symbol'},
            "ATTR": { 'type': 'token', 'reg': r'@Attr', 'errortext': 'Attribute mapper symbol'},
            "CLASS": { 'type': 'token', 'reg': r'@Class', 'errortext': 'Class mapper symbol'},
            "MODEL": { 'type': 'token', 'reg': r'@Model', 'errortext': 'Model mapper symbol'},
            "REF": { 'type': 'token', 'reg': r'@Ref', 'errortext': 'Reference mapper symbol'},

            "NEWLINE": { 'type': 'token', 'reg': r'(\r?\n[\t ]*)+'  , 'errortext': 'New Line'},
            "WS": { 'type': 'token', 'reg': r'[\t \f]+'  , 'errortext': 'White space'},
            "LINE_CONT": { 'type': 'token', 'reg': r'\\[\t \f]*\r?\n', 'errortext': 'Line continuation'},
            "SINGLE_COMMENT": { 'type': 'token', 'reg': r'//[^\n]*', 'hidden': False, 'errortext': 'Single line comment'},
            "MULTI_COMMENT": { 'type': 'token', 'reg': r'/\*(.|\n)*?\*/', 'hidden': False, 'errortext': 'Multi line comment'}
        }

        self.rules = {
            'start':  {'type': 'prod', 'body':['.', ['?', '@grammar'], ['?', '@mapper' ]] , 'errortext': 'Top level start',
                       'interleave': ['?','@implicit'] },
            
            'grammar':  {'type': 'prod', 'body': ['.', '$GRAMMAR', '$LCBR', ['*', '@production_rule'], '$RCBR' ], 
                         'errortext': 'Grammar definition'},
            
            'production_rule':  {'type': 'prod', 'body': ['|', '@rule_definition',  '@token_collection' ], 
                                 'errortext': 'Top level production rule definition'},

            'rule_definition':  {'type': 'prod', 'body':
                                ['.', '@rule_name', '$COLON', '@rule_right_hand_side', ['?', '@message'],'$SEMICOL' ],
                                'errortext': 'Production rule definition'},

            'rule_name':  {'type': 'prod', 'body': ['.' , '$LOWER_CASE'], 'errortext': 'Rule name' },

            'rule_right_hand_side': { 'type': 'prod', 'body':  [ '|', '@token_name', '@token_value', '@rule_name',
                                                         ['.', '$LPAR',  '@rule_right_hand_side', '$RPAR',
                                                          ['?', '@cardinality']],
                                                         ['.', '@rule_right_hand_side', '$OR', '@rule_right_hand_side'],
                                                         ['.', '@rule_right_hand_side', '@rule_right_hand_side'],
                                                         ['.', '@rule_right_hand_side', '$OPER' ]],
                                    'errortext':  'Production rule right hand side'},


            'cardinality': { 'type': 'prod', 'body':  ['.', '$CARD', ['?', ['.','$LSBR', ['?', '$MINUS'], '$INT' ,'$RSBR']]],
                         'errortext': 'Cardinality'},

            'message': { 'type': 'prod', 'body':  ['.', '$MESSAGE_MOD', '@message_value'],
                         'errortext': 'Error message'},

            'message_value': { 'type': 'prod', 'body':  ['.','$REGEXP'], 'errortext': 'Error message value' },

            'token_collection': { 'type': 'prod', 'body': ['.', '$TOKENS', '$LCBR',
                                                           ['*',  [ '|', '@token_sub_collection', '@token_definition']],
                                                           '$RCBR' ],
                                'errortext': 'Top level token definition' },

            'token_sub_collection': { 'type': 'prod', 'body': [ '.', '@token_collection_category', '$COLON',
                                                      '@collection_name', '$LCBR',
                                                      ['*' ,'@token_definition'] ,'$RCBR'],
                                      'errortext': 'Token collection definition' },

            'token_collection_category': { 'type': 'prod', 'body': ['.', '$KEYWORDS'],
                                           'errortext':  'Token collection categories: keywords' },

            'collection_name': { 'type': 'prod', 'body': ['.', '$LOWER_CASE'] , 'errortext':  'Token collection name'},

            'token_definition': { 'type': 'prod', 'body': [ '.', '@token_name', '$COLON', '@token_value',
                                                            ['*',['|','@modifier','@message']], '$SEMICOL'],
                                  'errortext':  'Token definition' },

            'token_name': { 'type': 'prod', 'body': ['.', '$UPPER_CASE'] , 'errortext':  'Token name'},

            'token_value': { 'type': 'prod', 'body': ['.', '$REGEXP'] , 'errortext':  'Token value'},

            'modifier': { 'type': 'prod', 'body': ['|', '$IMPLICIT_MOD', '$COMMENT_MOD'], 'errortext':  'Possible modifiers'},

            'mapper': { 'type': 'prod', 'body': ['.', '$MAPPER','$LCBR', '@model_mapping_rule', '$RCBR'],
                        'errortext':  'Top level mapper definition'},


            'model_mapping_rule': { 'type': 'prod', 'body': ['.', '@prod_name', '$ARROW', '$MODEL', '@concept_name',
                                                             '$LCBR', ['*', '@mapping_rules'], '$RCBR' ],
                                    'errortext': 'Model mapper definition'},

            'mapping_rules': { 'type': 'prod', 'body': ['|', '@attr_mapping_rule', '@class_mapping_rule',
                                                        '@assoc_mapping_rule'],
                               'errortext': 'Top level mapping rules'},

            'attr_mapping_rule': { 'type': 'prod', 'body': ['.', '@prod_name', '$ARROW', '$ATTR', '@concept_name',
                                                            '$SEMICOL'],
                                   'errortext': 'Attribute mapping rule'},

            'ref_mapping_rule': { 'type': 'prod', 'body': ['.', '@prod_name', '$ARROW', '$REF', '@concept_name',
                                                           '$SEMICOL'],
                                  'errortext': 'Reference mapping rule'},

            'class_mapping_rule': { 'type': 'prod', 'body': ['.', '@prod_name', '$ARROW', '$CLASS', '@concept_name',
                                                             '$LCBR', ['*', '@attr_mapping_rule'], '$RCBR'],
                                    'errortext': 'Class mapping rule'},

            'assoc_mapping_rule': { 'type': 'prod', 'body':['.', '@prod_name', '$ARROW', '$ASSOC', '@concept_name',
                                                            '$LCBR',
                                                            ['*',['|', '@attr_mapping_rule','@ref_mapping_rule']],
                                                            '$RCBR' ],
                                    'errortext': 'Association mapping rule'},

            'prod_name': { 'type': 'prod', 'body': ['.', '@path'], 'errortext': 'Name of production rule being mapped'},

            'concept_name': { 'type': 'prod', 'body': ['.', '@path'], 'errortext': 'Name of concept being mapped to'},

            'path': { 'type': 'prod', 'body': ['.', '$IDENTIFIER', ['*', ['.', '$DOT', '$IDENTIFIER']]],
                      'errortext': 'Dotted name'},

            'implicit': {'type': 'prod', 'body':['*', ['|', '$NEWLINE', '$WS', '$LINE_CONT', '$SINGLE_COMMENT',
                                                       '$MULTI_COMMENT']],
                         'errortext': 'Implicit'}
        }
