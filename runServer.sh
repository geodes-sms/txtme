#!/bin/sh

#change this number to the desired port.
default_port=8000

#if the number of argumnnts >= 1 use the given argument as port
if [ $# -ge 1 ] 
then
    default_port=$1
fi


mvk_path=$(readlink -f external/MvK)
grammar_path=$(readlink -f grammar_parser_v2)

#echo $mvk_path
#echo $grammar_path

export PYTHONPATH=$PYTHONPATH:$mvk_path:$grammar_path
echo $PYTHONPATH

python server/HTTPServer.py $default_port #& & = runs in the background , needed because otherwise the firefox command is not executed while the server is on