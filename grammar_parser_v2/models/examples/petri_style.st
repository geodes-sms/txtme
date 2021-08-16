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
    .do  { color:rgb(51,102,255); font-weight:bold !important; }
    .re  { color:rgb(153,204,0); font-size:14pt; font-weight:normal;}
    .mi  { font-family:'Comic Sans MS'; font-size:12pt; color:rgb(153,0,255); font-weight:bold; font-style:italic; }
    .fa  { color:rgb(102,0,204); font-weight:bold; }
    .sol { color:rgb(0,0,255); font-weight:bold; }
}

stylemap{
    @Default default: def;//.the name doesnt matter
    @Error error :err; //the name doesnt matter
    @Keywords general: do; //the word @Keyword is needed because it needs to be saved elsewhere than the rules or Tokens
    @Keywords pn: re;
    //COMMENT: mi;
    //transition_decl: fa;
    //transition_decl.name: sol;
    //name: do; just here to test if name or transition_decl.name is going to get chosen
}