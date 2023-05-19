<?php
// retrieve POST data
$request_body = file_get_contents('php://input');

// decode JSON data
$data = json_decode($request_body, true);

// we reasign the values to variables
$user = $data['user'];
$password = $data['password'];
$uid = intval($data['uid']);
$checkpoint_id = intval($data['checkpoint_id']);
$time = $data['time'];

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


// insert data into database
$sql = "INSERT INTO times (uid, checkpoint_id, checkpoint_time) VALUES (?, ?, ?)";
$stmt = $pdo->prepare($sql);
if ($stmt->execute([$uid, $checkpoint_id, $time])) {
    echo "Data inserted successfully";
} else {
    echo "Error inserting data: " . $stmt->errorInfo()[2];
}

$pdo = null;
?>
