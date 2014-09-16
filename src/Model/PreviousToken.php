<?php

namespace Dws\Surety\Model;

use \Dws\Surety\Model\Show;

class PreviousToken extends Show
{
    public function get($key)
    {
        $this->asn1_token = $this->getAsn1Token($key + parent::KEY_ASN1_TOKEN);
        $this->timestamp = $this->getTimestamp($key + parent::KEY_TIMESTAMP);
        $this->serial_number = $this->getSerialNumber($key + parent::KEY_SERIAL_NUMBER);
        $this->tsa_name = $this->getTsaName($key + parent::KEY_TSA_NAME);
        $this->coordination_zone = $this->getCoordinationZone($key + parent::KEY_COORDINATION_ZONE);
        $this->SHA256 = $this->getSHA256($key + parent::KEY_SHA256);
        $this->RIPEMD160 = $this->getRIPEMD160($key + parent::KEY_RIPEMD160);

        unset($this->url);
        unset($this->json);
        unset($this->data);
    }
}
