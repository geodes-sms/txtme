@echo off

:: set the path of the grammar parser and the MvK
:: to use a different version of MvK simply comment out the part about mvk_path_col and set your own
:: the end value must be an absolute path

:: change this number to the desired port.
set default_port=8000
set grammar_path_loc=grammar_parser_v2
set mvk_path_loc=external\MvK

set grammar_path=""
set mvk_path=""

IF NOT "%1"=="" (
 set default_port=%1
)

call:rel2abs %grammar_path_loc% grammar_path
call:rel2abs %mvk_path_loc% mvk_path

::echo after func call: %grammar_path%
::echo after func call: %mvk_path%


set PYTHONPATH=%grammar_path%;%mvk_path%
::echo PYTHONPATH has been set to: %PYTHONPATH%
:: start the python server 
echo Python server will now start. Please do not close this window.
:: START /B C:\Python27\python.exe server\HTTPServer.py %default_port% ::uncomment this and comment the line below if python starts python 3 instead of python 2
START python server\HTTPServer.py %default_port%

GOTO:EOF

:rel2Abs    
:: converts a given path from relative to absolute 
:: param 1 the path (a value) 
:: param 2 the variable to save the result at (a reference)                
SETLOCAL
::%~f1 means expands  parameter one into a full path.
set fullPath=%~f1
(ENDLOCAL
 set "%2=%fullPath%"
)
GOTO:EOF 
