<?php

use StartupDevs\Surety\Surety;

class SuretyTest extends PHPUnit_Framework_TestCase
{
    protected $surety;

    public function __construct()
    {
        $baseUri = null;
        $user= null;
        $pass= null;
        $this->surety = new Surety($baseUri, $user, $pass);
    }

    /**
     * @expectedException StartupDevs\Surety\SuretyException
     */
    public function testCheckFilePathException()
    {
        $path = '/home/';
        $this->surety->timestamp( $path );
    }

}
