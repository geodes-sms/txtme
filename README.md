# TxtME
Generator of customizable textual domain-specific modeling editors


# SCCD Text Editor
*Daniel Riegelhaupt with thanks to: Bruno Barroca*

This is a statechart and class diagram based text editor whose purposes are: 
The creation and editing of software models through the use of domain specific textual languages 
and the creation of those languages.

This readme contains mostly information pertaining the web based editor itself.
For information on how to create domain specif languages please see the language manual pdf file.


# HOW TO START

From the project root directory:
1) in Linux:    ./runServer.sh [port]
   in windows:  runServer.bat [port]
   
Where port is an optional port number for the server. 
The default port is 8000.

IMPORTANT this project uses Python 2 (currently 2.7) not 3 so it the python command refers to python 3 this will not work


2) In the browser of your choice ( meaning Firefox, Chrome has too many issues) go to http://localhost:8000/SCCDTextEditor/editor.html.
If another port has been used when starting the server use that port instead of 8000

# USING THE EDITOR

1) Load the grammar first. Typing is disabled until a grammar has been loaded. 
The console will display a message when typing is an enabled (or simply wait one or two second after pressing the load grammar button)  

2) Usage of the editor

The editor contains basic text editing 
- overwrite (insert key), write  
- backspace , delete 
- enter
- arrow keys
- rearrange on line break and remove line break but no word wrap
- Mouse Click and select
- Save and load txt 
- Save and load svg 
- Export to rtf
- copy/cut/paste
- selection
- error check
- autocomplete

Not available yet:
- no scroll yet (it was a bit buggy and slowed things down immensely) but you can change the size of the editor in the html to make it as big as you want
- no tab key yet

Keyboard shortcuts:
- ctrl + a: select all
- ctrl + c: copy selection to editor clipboard
- ctrl + x: cut selection to editor clipboard
- ctrl + v: paste content of editor clipboard
- ctrl + s: save to svg
- ctrl + t: save to txt
- ctrl + m: save to rtf
- ctrl + l: load a file (svg or txt) 
- ctrl + q: exit
- ctrl + e: check error
- ctrl + space: autocomplete (esc to close or enter to select something, up and down arrow keys to select from the options or show them)

# KNOWN ISSUES
- Auto complete menu is created but not shown in Chrome (if you pressed ctrl + space , press esc to give back focus to the editor)
- Use monospace fonts in css !!!!!
- while any css can be injected in the style mapping only use mono-space fonts because otherwise this cause problems with the visual cursor position compared to actual text position
- the same applies with spaces and line breaks in chrome. if the text is big enough or there are multiple white spaces next to each other the cursor behaves weirdly (note that moving the cursor programmaticaly to a row col gets the desired result but the cursor itself might not been shown at the correct place)
=> in other words for the moment do not use with chrome

- exit: firefox doesn't allow the closing of pages by scripts. pressing ctrl+q will close the server and disable typing but not close the tab. (does work in chrome)
- exit2: i've noticed that closing the server the legal way will cause it to block the port longer than if ctrl+c is pressed in the console. i have no clue why i used the legal python way to close the server when ctrl+q is pressed

# EXTERNAL
The following external projects  are used by and included with this project: jQuery, jQuery UI, Mvk, SCCD compiler
They are property of their original authors.
They have been used according to license or with permission.
