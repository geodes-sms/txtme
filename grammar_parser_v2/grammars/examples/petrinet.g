//Petri Net written in Meta Grammar
//author Daniel Riegelhaupt

grammar{
    start: PETRINET name (place_decl | transition_decl | arc_decl)* END;

    place_decl: PLACE name place_def? SEMICOL;
    place_def: LCBR (tokens_def (COMMA capacity_def)? | capacity_def (COMMA tokens_def)? ) RCBR;

    capacity_def: CAPACITY COLON integer;
    tokens_def: TOKENS COLON integer;

    transition_decl: TRANSITION name SEMICOL;

    arc_decl: ARC name weight_def? COLON FROM source TO destination SEMICOL;

    weight_def: LCBR WEIGHT COLON integer RCBR;

    name: IDENTIFIER;
    source: IDENTIFIER;
    destination: IDENTIFIER;
    integer: DIGIT+;

    tokens{
        // TOKENS (written in CAPS)
        IDENTIFIER: '[a-zA-Z_][a-zA-Z_0-9]*' @Msg 'Identifier';

        keywords:pn{
            PETRINET: 'Petrinet';
            PLACE: 'Place';
            TRANSITION: 'Transition';
            ARC: 'Arc';
            WEIGHT: 'weight';
            CAPACITY: 'capacity';
            TOKENS: 'tokens';
        }

        keywords:general{
            END: 'end';
            FROM: 'from';
            TO: 'to';
        }

        COLON: ':';
        LPAR: '\(' @Msg '(';
        RPAR: '\)' @Msg ')';
        COMMA: ',';
        SEMICOL: ';';
        LCBR: '\{' @Msg '{';
        RCBR: '\}' @Msg '}';

        DIGIT: '[0-9]' @Msg 'Digit';

        NEWLINE: '(\r?\n[\t ]*)+' @Impl @Msg 'New Line';
        LINE_CONT: '\\[\t \f]*\r?\n' @Impl @Msg 'Line Continuation';
        WS: '[\t \f]+' @Impl @Msg 'White Space';
        COMMENT: '//[^\n]*' @Cmnt @Msg 'Comment';
    }
}

mapper{
  
  start -> @Model MyFormalisms.PetriNet{
    start.name -> @Attr name;

    place_decl -> @Class Place {
      place_decl.name -> @Attr name;
      tokens_def.integer -> @Attr token;
      capacity_def.integer -> @Attr capacity;
    }

    transition_decl -> @Class Transition {
      transition_decl.name -> @Attr name;
    }

    arc_decl -> @Assoc InArc{
      arc_decl.name -> @Attr name;
      weight_def.integer -> @Attr weight;
      arc_decl.source -> @Ref from_port;
      arc_decl.destination -> @Ref to_port;
    }
  }

}