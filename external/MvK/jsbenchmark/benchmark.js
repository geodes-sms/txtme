function loadTest(callback){
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'tests.js';

    script.onreadystatechange = callback;
    script.onload = callback;

    document.getElementsByTagName('head')[0].appendChild(script);
}

var begin;
var current_test;
var servername = "localhost";

var xhr = new XMLHttpRequest();

function next_ws_benchmark(ws){
    current_test = current_test + 1;
    if(current_test == tests.length){
        // Finished our tests
        diff = window.performance.now() - begin;
        document.getElementById("content_WS").innerHTML = "Time taken for WS = " + diff + "ms";
        document.getElementById("content_XML").innerHTML = "Running XMLHTTPRequest test, please wait...";
        ws.close();
        run_xml_benchmark();
    }
    else{
        ws.send(tests[current_test][0] + "/" + tests[current_test][1]);
    }
}

function next_xml_benchmark(){
    current_test = current_test + 1;
    if(current_test == tests.length){
        diff = window.performance.now() - begin;
        document.getElementById("content_XML").innerHTML = "Time taken for XMLHTTPRequests = " + diff + "ms";
    }
    else{
        if(tests[current_test][0] == "read"){
            xhr.open('GET', 'http://' + servername + ':8000/?func=' + tests[current_test][0] + '&args=' + tests[current_test][1], true)
            xhr.send(null);
        }
        else{
            xhr.open('POST', 'http://' + servername + ':8000', true);
            params = "func=" + tests[current_test][0] + "&args=" + tests[current_test][1]
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xhr.setRequestHeader("Content-length", params.length);
            xhr.send(params);
        }
    }
}   

function run_ws_benchmark(ws){
    current_test = -1;
    ws.onmessage = function(event){
        next_ws_benchmark(ws);
    }
    begin = window.performance.now();
    next_ws_benchmark(ws);
}

function run_xml_benchmark(){
    current_test = -1;
    xhr.onreadystatechange = function(){if(xhr.readyState == 4) {next_xml_benchmark()}}
    begin = window.performance.now();
    next_xml_benchmark();
}

function benchmark(){
    var ws = new WebSocket("ws://" + servername + ":8002/ws");

    ws.onopen = function(){
        run_ws_benchmark(ws);
    }
}

function init(){
    //loadTest(benchmark)
    loadTest(run_xml_benchmark)
}

window.onload = init
