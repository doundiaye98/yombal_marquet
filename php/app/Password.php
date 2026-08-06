<?php
declare(strict_types=1);

/**
 * Compatible password_hash PHP + hashes Werkzeug (Flask) pbkdf2:sha256.
 * Format Werkzeug: pbkdf2:sha256:iterations$salt$hash_base64
 */
final class Password
{
    public static function hash(string $password): string
    {
        return password_hash($password, PASSWORD_DEFAULT);
    }

    public static function verify(string $password, string $stored): bool
    {
        $stored = trim($stored);
        if ($stored === '') {
            return false;
        }
        if (str_starts_with($stored, '$2y$') || str_starts_with($stored, '$argon2') || str_starts_with($stored, '$2a$')) {
            return password_verify($password, $stored);
        }
        if (str_starts_with($stored, 'pbkdf2:')) {
            return self::verifyWerkzeugPbkdf2($password, $stored);
        }
        if (str_starts_with($stored, 'scrypt:')) {
            // scrypt Werkzeug — non supporté en PHP natif ; demander reset
            return false;
        }
        return false;
    }

    private static function verifyWerkzeugPbkdf2(string $password, string $stored): bool
    {
        // pbkdf2:sha256:600000$salt$hash
        $parts = explode('$', $stored, 3);
        if (count($parts) !== 3) {
            return false;
        }
        [$method, $salt, $hashB64] = $parts;
        $methodParts = explode(':', $method);
        if (count($methodParts) < 2 || $methodParts[0] !== 'pbkdf2') {
            return false;
        }
        $algo = $methodParts[1] ?? 'sha256';
        $iterations = isset($methodParts[2]) ? (int) $methodParts[2] : 600000;
        $dklen = 32;
        if ($algo === 'sha256') {
            $algoPhp = 'sha256';
        } elseif ($algo === 'sha512') {
            $algoPhp = 'sha512';
            $dklen = 64;
        } else {
            return false;
        }
        $calc = hash_pbkdf2($algoPhp, $password, $salt, $iterations, $dklen, true);
        $expected = base64_decode($hashB64, true);
        if ($expected === false) {
            // parfois hex
            $expected = hex2bin($hashB64);
        }
        if ($expected === false) {
            return false;
        }
        return hash_equals($expected, $calc);
    }
}
