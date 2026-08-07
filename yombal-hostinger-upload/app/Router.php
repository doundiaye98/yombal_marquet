<?php
declare(strict_types=1);

final class Router
{
    /** @var list<array{methods: string[], pattern: string, handler: callable}> */
    private array $routes = [];

    public function get(string $pattern, callable $handler): void
    {
        $this->add(['GET'], $pattern, $handler);
    }

    public function post(string $pattern, callable $handler): void
    {
        $this->add(['POST'], $pattern, $handler);
    }

    public function any(string $pattern, callable $handler): void
    {
        $this->add(['GET', 'POST'], $pattern, $handler);
    }

    private function add(array $methods, string $pattern, callable $handler): void
    {
        $this->routes[] = [
            'methods' => $methods,
            'pattern' => $pattern,
            'handler' => $handler,
        ];
    }

    public function dispatch(string $method, string $uri): void
    {
        $path = parse_url($uri, PHP_URL_PATH) ?: '/';
        $path = rawurldecode($path);

        // Racine projet : /yombal_marquet/index.php → /
        $scriptName = str_replace('\\', '/', (string) ($_SERVER['SCRIPT_NAME'] ?? ''));
        $scriptDir = rtrim(dirname($scriptName), '/');
        if ($scriptDir && $scriptDir !== '/' && str_starts_with($path, $scriptDir)) {
            $path = substr($path, strlen($scriptDir)) ?: '/';
        }

        // /index.php, /index.php/… → route applicative
        if ($path === '/index.php' || $path === 'index.php') {
            $path = '/';
        } elseif (str_starts_with($path, '/index.php/')) {
            $path = substr($path, strlen('/index.php')) ?: '/';
        }

        if ($path === '' || $path === false) {
            $path = '/';
        }

        // /ecosysteme/ → /ecosysteme (évite 404 sur slash final)
        if ($path !== '/' && str_ends_with($path, '/')) {
            $path = rtrim($path, '/') ?: '/';
        }

        foreach ($this->routes as $route) {
            if (!in_array($method, $route['methods'], true)) {
                continue;
            }
            $regex = '@^' . preg_replace('@\{([a-zA-Z_][a-zA-Z0-9_]*)\}@', '(?P<$1>[^/]+)', $route['pattern']) . '$@';
            if (!preg_match($regex, $path, $m)) {
                continue;
            }
            $params = array_filter($m, 'is_string', ARRAY_FILTER_USE_KEY);
            ($route['handler'])(...array_values($params));
            return;
        }

        http_response_code(404);
        view('errors/404', ['ep' => '404', 'page_title' => 'Page introuvable']);
    }
}
