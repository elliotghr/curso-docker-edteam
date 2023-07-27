<?php

echo '<h1>Hola mundo! Cómo están? </h1>';


$conexion = new PDO('mysql:host=db;dbname=xampp', 'root', 'hello1234');

$res = $conexion->exec('SELECT "HOLA A TODOS"');

echo $res;
