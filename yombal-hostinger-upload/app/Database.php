<?php
declare(strict_types=1);

final class Database
{
    private static ?PDO $pdo = null;

    public static function pdo(): PDO
    {
        if (self::$pdo === null) {
            $host = env('DB_HOST', 'localhost');
            $port = env('DB_PORT', '3306');
            $name = env('DB_NAME', 'yombal');
            $user = env('DB_USER', 'root');
            $pass = env('DB_PASS', '');
            $dsn = "mysql:host={$host};port={$port};dbname={$name};charset=utf8mb4";
            self::$pdo = new PDO($dsn, $user, $pass, [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
            ]);
        }
        return self::$pdo;
    }

    public static function query(string $sql, array $params = []): PDOStatement
    {
        $st = self::pdo()->prepare($sql);
        $st->execute($params);
        return $st;
    }

    public static function fetch(string $sql, array $params = []): ?array
    {
        $row = self::query($sql, $params)->fetch();
        return $row === false ? null : $row;
    }

    public static function fetchAll(string $sql, array $params = []): array
    {
        return self::query($sql, $params)->fetchAll();
    }

    public static function insert(string $table, array $data): int
    {
        $cols = array_keys($data);
        $fields = implode(', ', array_map(fn ($c) => "`$c`", $cols));
        $placeholders = implode(', ', array_map(fn ($c) => ':' . $c, $cols));
        self::query("INSERT INTO `{$table}` ({$fields}) VALUES ({$placeholders})", $data);
        return (int) self::pdo()->lastInsertId();
    }

    public static function update(string $table, array $data, string $where, array $whereParams = []): void
    {
        $sets = [];
        foreach (array_keys($data) as $c) {
            $sets[] = "`$c` = :$c";
        }
        self::query(
            "UPDATE `{$table}` SET " . implode(', ', $sets) . " WHERE {$where}",
            array_merge($data, $whereParams)
        );
    }
}
