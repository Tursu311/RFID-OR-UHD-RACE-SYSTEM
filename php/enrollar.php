<?php
// retrieve POST data
$request_body = file_get_contents('php://input');

// decode JSON data
$data = json_decode($request_body, true);

// we reasign the values to variables
$user = $data['user'];
$password = $data['password'];
$uid = intval($data['uid']);
$name = $data['name'];
$surnames = $data['surnames'];

//vardump all
var_dump($user);
var_dump($password);
var_dump($uid);
var_dump($name);
var_dump($surnames);
// connect to MySQL database using PDO
$dsn = "mysql:host=localhost;dbname=race";
$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
];
try {
        $pdo = new PDO($dsn, $user, $password, $options);
    } catch (PDOException $e) {
        die("Connection failed: " . $e->getMessage());
    }


// prepare SQL statement
$sql = "INSERT INTO `runners` (`uid`, `name`, `surnames`) VALUES (?, ?, ?)";
$stmt = $pdo->prepare($sql);

// execute SQL statement
if ($stmt->execute([$uid, $name, $surnames])) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $pdo->error;
}

$pdo = null;
?>
