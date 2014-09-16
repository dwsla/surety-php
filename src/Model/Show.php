<?php

namespace Dws\Surety\Model;

use \Dws\Surety\Model\Surety;
use \Dws\Surety\Model\PreviousToken;
use \Dws\Surety\Repository\SuretyModelInterface;

class Show extends Surety implements SuretyModelInterface
{
    // prevent magic numbers
    const KEY_DECODE_URL = 0;
    const KEY_ASN1_TOKEN = 1;
    const KEY_TIMESTAMP = 2;
    const KEY_SERIAL_NUMBER = 3;
    const KEY_TSA_NAME = 4;
    const KEY_COORDINATION_ZONE = 5;
    const KEY_SHA256 = 9;
    const KEY_RIPEMD160 = 12;

    public $url;
    public $asn1_token;
    public $timestamp;
    public $serial_number;
    public $tsa_name;
    public $coordination_zone;
    public $SHA256;
    public $RIPEMD160;
    public $json;

    public function fill()
    {
        $this->url = $this->getDecodeUrl(self::KEY_DECODE_URL);
        $this->asn1_token = $this->getAsn1Token(self::KEY_ASN1_TOKEN);
        $this->timestamp = $this->getTimestamp(self::KEY_TIMESTAMP);
        $this->serial_number = $this->getSerialNumber(self::KEY_SERIAL_NUMBER);
        $this->tsa_name = $this->getTsaName(self::KEY_TSA_NAME);
        $this->coordination_zone = $this->getCoordinationZone(self::KEY_COORDINATION_ZONE);
        $this->SHA256 = $this->getSHA256(self::KEY_SHA256);
        $this->RIPEMD160 = $this->getRIPEMD160(self::KEY_RIPEMD160);
        $this->json = $this->getJson();
    }

    public function getPreviousToken($level = null)
    {
        $previousToken = array();

        $keySize = 13;
        $counter = 0;
        foreach($this->data as $key => $data){

            if($data == 'Previous Token:'){
                $prevTokenData = array_slice($this->data, $key, $keySize);

                $model = new PreviousToken($this->data);
                $model->get($key);

                $previousToken[$counter] = $model;

                $counter++;
            }
        }

        if(!is_null($level) && isset($previousToken[$level])){
            return $previousToken[$level];
        }
        return $previousToken;
    }
}
