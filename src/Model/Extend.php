<?php

namespace StartupDevs\Surety\Model;

use \StartupDevs\Surety\Model\Surety;
use \StartupDevs\Surety\Repository\SuretyModelInterface;

class Extend extends Surety implements SuretyModelInterface
{
    public $json;

    public function fill()
    {
        //@todo: not implemented yet because I need a expired file to test.
        //getting: error code: extend failed, error code: UNAVAILABLE_VALUE

        $this->json = $this->getJson();
    }

}
