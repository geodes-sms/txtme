#!/bin/bash
python ../external/dawg-sccd/python_sccd_compiler/sccdc.py -o editor-behaviour.js -l javascript editor-behaviour.xml
read -n1 -r -p "Press any key to continue..." key