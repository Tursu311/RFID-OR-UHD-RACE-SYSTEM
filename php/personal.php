
<DOCTYPE html>
<html>
<head>
    <title>Sant Jordi</title>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="style.css">
</head>

<body>
    <div id="corredors">
        <h1>Total temps</h1>
    <?php
    //TODO Change identification to something more usable by the user
    if (isset($_POST['uid'])) {
        echo "<table>";
        echo "<tr>";
        echo "<th>Posicio</th>";
        echo "<th>Corredor</th>";
        echo "<th>P.control</th>";
        echo "<th>Temps</th>";
        echo "</tr>";
        //use mysql pdo to connect to the database
        $servername = "localhost";
        $username = "dbuser";
        $password = "dbpassword";
        $dbname = "race";
        //create connection
        $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
        //set the PDO error mode to exception
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        $uid = $_POST['uid'];
        // Get runner time
        $sql = "SELECT runners.name, runners.surname, runners.uid, MAX(checkpoint_id) AS checkpoint, checkpoint_id, MAX(checkpoint_time) - MIN(checkpoint_time) AS time FROM runners INNER JOIN times ON runners.uid = times.uid WHERE runners.uid = '$uid' GROUP BY runners.uid ORDER BY MAX(checkpoint_id) DESC, time ASC";
        $stmt = $conn->prepare($sql);
        $stmt->execute();
        $corredor = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        // Get runner position in the leaderboard
        $sql = "SELECT runners.name, runners.surname, runners.uid, MAX(checkpoint_id) AS checkpoint, checkpoint_id, MAX(checkpoint_time) - MIN(checkpoint_time) AS time FROM runners INNER JOIN times ON runners.uid = times.uid GROUP BY runners.uid ORDER BY MAX(checkpoint_id) DESC, time ASC";
        $stmt = $conn->prepare($sql);
        $stmt->execute();
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
        $posicio = 1;
        foreach ($result as $row) {
            if ($row['uid'] == $uid) {
                break;
            }
            $posicio++;
        }

        // We show the runner time and position
        foreach ($corredor as $row) {
            echo "<tr>";
            echo "<td>" . $posicio . "</td>";
            echo "<td>" . $row['name'] . " " . $row['surname'] . "</td>";
            echo "<td>" . $row['checkpoint'] . "</td>";
            echo "<td>" . $row['time'] . "s"  .  "</td>";
            echo "</tr>";
        }
        echo "</table>";
        echo "</div>";
        echo "<div id='temps'>";
        echo "<h2>Temps entre checkpoints</h2>";
        echo "<table>";
        echo "<tr>";
        echo "<th>Corredor</th>";
        echo "<th>P.control</th>";
        echo "<th>Temps</th>";
        echo "</tr>";
        // We show the runner times between checkpoints
        for ($i = 1; $i <= 10; $i++) {
            $sql = "SELECT runners.name, runners.surname, runners.uid, checkpoint_id, TIMEDIFF(checkpoint_time, (SELECT checkpoint_time FROM times WHERE checkpoint_id = $i - 1 AND runners.uid = times.uid)) AS checkpoint_time FROM runners INNER JOIN times ON runners.uid = times.uid WHERE runners.uid = '$uid' AND checkpoint_id = $i";
            $stmt = $conn->prepare($sql);
            $stmt->execute();
            $temps = $stmt->fetchAll(PDO::FETCH_ASSOC);
            //We dont want the first time
            if ($i == 1) {
                continue;
            } else {
                foreach ($temps as $row) {
                    echo "<tr>";
                    echo "<td>" . $row['name'] . " " . $row['surname'] . "</td>";
                    echo "<td>" . $row['checkpoint_id'] . "</td>";
                    echo "<td>" . $row['checkpoint_time'] . "</td>";
                    echo "</tr>";
                    }
                }
            }
        echo "</table>";
        echo "</div>";
    } else {
        echo "<p>Introdueix el teu uid</p>";
    }
    ?>
        </table>
    </div>
</body>
</html>
    