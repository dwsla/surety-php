<?php

namespace Dws\Surety\Model;

use \Dws\Surety\Model\Surety;
use \Dws\Surety\Repository\SuretyModelInterface;

class Renew extends Surety implements SuretyModelInterface
{
    // prevent magic numbers
    const KEY_URL = 1;
    const KEY_DECODE_URL = 0;

    public $url;
    public $decode_url;
    public $json;

    public function fill()
    {
        $this->url = $this->getUrl(self::KEY_URL);
        $this->decode_url = $this->getDecodeUrl(self::KEY_DECODE_URL);
        $this->json = $this->getJson();
    }
}
