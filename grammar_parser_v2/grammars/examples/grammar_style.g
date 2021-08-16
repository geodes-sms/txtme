/*
 a simple grammar that consits of 2 parts
 map a name to a string symbolyizing a style.
 map a doted name (a production rule or token) to said style
 note that they both have there own root and so can be parsed from different files.
*/
grammar{
    start : (styles | style_mapping)+;

    styles: STYLES LCBR style_def* RCBR;
    style_def: class_name  LCBR attr_def (SEMICOL attr_def)* SEMICOL? RCBR; //';' is not required at the end
    attr_def: attr_name COLON style IMPORTANT?;
    class_name: CSS_CLASS_NAME;
    attr_name: CSS_ATTR_NAME;
    style: STR;

    style_mapping: STYLE_MAP LCBR style_map* RCBR;
    style_map: type? path_name COLON style_name SEMICOL;
    type: KEYWORDS |DEFAULT |ERROR;
    style_name: IDENTIFIER;
    path_name: IDENTIFIER (DOT IDENTIFIER)* | STAR;


    tokens{
        CSS_CLASS_NAME: '[\.][a-zA-Z_][a-zA-Z_0-9]*' @Msg 'CSS class name'; //is the same as an indentifier but must start with a dot
        CSS_ATTR_NAME: '[:]?[a-zA-Z_\-:][a-zA-Z_0-9\-]*'  @Msg 'CSS attribute name'; //a css attr name can start with -, : or ::
        IDENTIFIER: '[a-zA-Z_][a-zA-Z_0-9\-]*' @Msg 'Identifier';

        STYLES: 'styles';
        STYLE_MAP: 'stylemap';
        KEYWORDS: '@Keywords';
        IMPORTANT: '!important';
        DEFAULT: '@Default';
        ERROR: '@Error';
        STAR : '\*';

        STR: '.[^;!]*' @Msg 'String content'; //any character excpt new line !(because of !important) or ;

        LCBR: '\{' @Msg '{';
        RCBR: '\}' @Msg '}';
        COLON: ':';
        SEMICOL: ';';
        DOT: '\.' @Msg '.';


        // Implicit declarations tokens are tokens that can be applied anywhere in the grammar and don't have to be explicitly declared
        NEWLINE: '(\r?\n[\t ]*)+' @Msg 'New Line' @Implicit;
        WS: '[\t \f]+' @Msg 'White space' @Implicit;
        LINE_CONT: '\\[\t \f]*\r?\n' @Implicit @Msg 'Line continuation';
        SINGLE_COMMENT: '//[^\n]*' @Implicit @Msg 'Single line comment';
        MULTI_COMMENT: '/\*(.|\n)*?\*/' @Implicit @Msg 'Multi line comment';
    }
}