<?php 
@session_start(); 
@set_time_limit(0); 
@error_reporting(0); 
function encode($D,$K){ 
    for($i=0;$i<strlen($D);$i++) { 
        $c = $K[$i+1&15]; 
        $D[$i] = $D[$i]^$c; 
    } 
    return $D; 
}

$key = '3c6e0b8a9c15224a';

$data = substr("", 16, -16);
// $data = "";

echo encode(base64_decode($data), $key);
echo "\n\n";
echo gzdecode(encode(base64_decode($data), $key));
?>