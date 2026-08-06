<?php
declare(strict_types=1);

final class Mailer
{
    public static function send(string $to, string $subject, string $body): bool
    {
        $server = env('MAIL_SERVER');
        if (!$server || env('MAIL_SUPPRESS_SEND') === 'true') {
            error_log("[mail] To: {$to} | {$subject}\n{$body}");
            return true;
        }
        $from = env('MAIL_DEFAULT_SENDER', env('CONTACT_EMAIL', 'noreply@yombalmarket.com'));
        $headers = [
            'From: ' . $from,
            'Reply-To: ' . $from,
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=UTF-8',
        ];
        return @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers));
    }
}
