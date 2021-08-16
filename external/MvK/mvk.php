<?php
$error_message = "{'type': 'MvKReadLog', 'value': {'keys': [{'type': 'StringValue', 'value': 'status_message'}, {'type': 'StringValue', 'value': 'status_code'}], 'values': [{'type': 'StringValue', 'value': 'Connection problem'}, {'type': 'IntegerValue', 'value': 800}]}}";
$server_id = $_GET["server_id"];
$client_id = $_GET["client_id"];
$my_port = 8000 + ((int) $server_id);
$url = "http://localhost:$my_port/";
if (empty($_POST))
{
        // Assume it is a GET request
        $func = urlencode(preg_replace('/\s+/','', $_GET["func"]));
        $args = urlencode(preg_replace('/\s+/','', $_GET["args"]));
        $url = "$url?func=$func&args=$args&client_id=$client_id";
        $response = file_get_contents($url);
        if (empty($response)){
                // Connection was probably lost or something
                echo "$error_message";
        }
        else{
                echo "$response";
        }
}
else{
        // Assume it is a POST request
        $func = $_POST["func"];
        $args = $_POST["args"];
        $reqbody = "func=$func&args=$args&client_id=$client_id";
        $options = array(
                'http' => array(
                        'header' => "Content-type: application/x-www-form-urlencoded\r\n",
                        'method' => 'POST',
                        'content' => $reqbody,
                ),
        );
        $context = stream_context_create($options);
        $response = file_get_contents($url, false, $context);
        if (empty($response)){
                echo "$error_message";
        }
        else{
                echo "$response";
        }
}
?>
