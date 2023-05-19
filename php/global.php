<!-- We make a page where we show the runners that are running, the time they have been running and the position they are in. The table is reloaded automatically, and the position of the runners is shown in real time -->
<DOCTYPE html>
<html>
<head>
    <title>Sant Jordi</title>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="style.css">
</head>

<body>
    <div id="corredors">
        <table>
            <tr>
                <th>Posició</th>
                <th>Corredor</th>
                <th>P.control</th>
                <th>Temps</th>
            </tr>
            <?php
            //use mysql pdo to connect to the database
            $servername = "localhost";
            $username = "dbuser";
            $password = "dbpassword";
            $dbname = "race";
            //create connection
            $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
            //set the PDO error mode to exception
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            //We grab each runners first checkpoint time and subtract it to the last checkpoint time MAX(checkpoint_time) - MIN(checkpoint_time)
            //We order the result by last checkpoint and min time
            //We have to group by uid to get it to work
            //We have to join the times to runners table to get the name
            $sql = "SELECT runners.name, runners.surnames, runners.uid, MAX(checkpoint_id) AS checkpoint, checkpoint_id, TIMEDIFF(MAX(checkpoint_time), MIN(checkpoint_time)) AS time FROM runners INNER JOIN times ON runners.uid = times.uid GROUP BY runners.uid ORDER BY MAX(checkpoint_id) DESC, time ASC";
            $stmt = $conn->prepare($sql);
            $stmt->execute();
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
            $posicio = 1;
            foreach ($result as $row) {
                echo "<tr>";
                echo "<td>" . $posicio . "</td>";
                echo "<td>" . $row['name'] . " " . $row['surnames'] . "</td>";
                echo "<td>" . $row['checkpoint'] . "</td>";
                echo "<td>" . $row['time'] . "</td>";
                echo "</tr>";
                $posicio++;
            }            
            ?>
        </table>
    </div>
    <script>
        setInterval(function() {
            location.reload();
        }, 1000);
    </script>
</body>
</html>









