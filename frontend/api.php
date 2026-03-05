<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$envPath = __DIR__ . '/../backend/.env';

if (!file_exists($envPath)) {
    echo json_encode(["status" => "error", "message" => "Configuration error"]);
    exit;
}

$env = parse_ini_file($envPath);

try {
    $dsn = "mysql:host=" . ($env['DB_HOST'] ?? '127.0.0.1') . ";dbname=" . $env['DB_NAME'] . ";charset=utf8mb4";
    
    $pdo = new PDO($dsn, $env['DB_USER'], $env['DB_PASS']);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $pdo->query("SELECT id, created_at, fastest_fee, half_hour_fee, hour_fee, minimum_fee FROM btc_mempool ORDER BY id DESC LIMIT 1");
    $latestData = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($latestData) {
        echo json_encode([
            "status" => "success", 
            "data" => $latestData
        ]);
    } else {
        echo json_encode(["status" => "error", "message" => "No data found"]);
    }

} catch(PDOException $e) {


    echo json_encode([
        "status" => "error", 
        "message" => "Server error. Please try again later."
    ]);
}
?>