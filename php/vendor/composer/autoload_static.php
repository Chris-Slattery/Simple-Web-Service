<?php

// autoload_static.php @generated by Composer

namespace Composer\Autoload;

class ComposerStaticInit0dba6a15c7bc5949182ddf924154de5c
{
    public static $prefixLengthsPsr4 = array (
        'P' => 
        array (
            'PhpAmqpLib\\' => 11,
        ),
    );

    public static $prefixDirsPsr4 = array (
        'PhpAmqpLib\\' => 
        array (
            0 => __DIR__ . '/..' . '/php-amqplib/php-amqplib/PhpAmqpLib',
        ),
    );

    public static function getInitializer(ClassLoader $loader)
    {
        return \Closure::bind(function () use ($loader) {
            $loader->prefixLengthsPsr4 = ComposerStaticInit0dba6a15c7bc5949182ddf924154de5c::$prefixLengthsPsr4;
            $loader->prefixDirsPsr4 = ComposerStaticInit0dba6a15c7bc5949182ddf924154de5c::$prefixDirsPsr4;

        }, null, ClassLoader::class);
    }
}
