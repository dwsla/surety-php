<?php

namespace Dws\Surety\Model;

use \Dws\Surety\Model\Surety;
use \Dws\Surety\Repository\SuretyModelInterface;

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
