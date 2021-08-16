styles{
    .def { font-family:'Nimbus Mono L';
           font-size:12pt;
           color:rgb(0,0,0);
           font-weight: normal;
           font-style: normal;
           text-decoration: none;
         }

    .err {
           text-decoration:  underline;
           text-decoration-style: wavy;
           text-decoration-color: red; //will not work, not supported except by mozilla
           -moz-text-decoration-style: wavy;
           -moz-text-decoration-color: red; //will not work: because svg tspan are used instead html span.
           color :red; //because underline color is not supported the whole text is colored red
         }
    .highlight {
           font-family:'Nimbus Mono L';
           font-size:12pt;
           color:rgb(0,0,255);
           font-weight: bold;
           font-style: normal;
           text-decoration: none;
    }

    .purple {
            color:rgb(102,0,204);
    }

    .blue{
        color:rgb(60,160,160);
    }
}

stylemap{
    @Default default: def;//.the name doesnt matter
    @Error error :err; //the name doesnt matter
    @Keywords *: highlight; //the word @Keyword is needed because it needs to be saved elsewhere than the rules or Tokens
    rule_name: purple;
    token_name: blue;
}