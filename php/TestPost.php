<?php
// retrieve raw HTTP request body
$request_body = file_get_contents('php://input');

// decode JSON data
$data = json_decode($request_body, true);

// check if croqueta parameter is set in the data array
if (isset($data['croqueta'])) {
    $pass = "pernil";
    $pass2 = $data['croqueta'];
    //If password is correct, returns "Its OK" to python request
    if($pass == $pass2){
        echo "Its OK";
    }
    //If password is incorrect, returns "No OK" to python request
    else{
        echo "No OK";
    }
} else {
    // croqueta parameter is missing from data array
    echo "Error: croqueta parameter is missing";
}
