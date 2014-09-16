<?php

namespace StartupDevs\Surety\Model;

class Surety
{
    public $data;

    public function __construct(array $data)
    {
        $this->data = $data;
        $this->fill();
    }

    protected function getUrl($key)
    {
        $result = $this->getFromData($key);

        return $result;
    }

    protected function getDecodeUrl($key)
    {
        $result = $this->getFromData($key);

        return $result;
    }

    protected function getAsn1Token($key)
    {
        $result = $this->getFromData($key);
        if($result){
            $result = str_replace('ASN1 Token: ', '', $result);
        }
        return $result;
    }

    protected function getTimestamp($key)
    {
        $result = $this->getFromData($key);
        if($result){
            $result = str_replace('Timestamp: ', '', $result);
        }
        return $result;
    }

    protected function getSerialNumber($key)
    {
        $result = $this->getFromData($key);
        if($result){
            $result = str_replace('Serial Number: ', '', $result);
        }
        return $result;
    }

    protected function getTsaName($key)
    {
        $result = $this->getFromData($key);
        if($result){
            $result = str_replace('TSA Name: ', '', $result);
        }
        return $result;
    }

    protected function getCoordinationZone($key)
    {
        $result = $this->getFromData($key);
        if($result){
            $result = str_replace('Coordination Zone: ', '', $result);
        }
        return $result;
    }

    protected function getSHA256($key)
    {
        $result = $this->getFromData($key);
        if($result){
            $result = str_replace('Hashed Data: ', '', $result);
        }
        return $result;
    }

    protected function getRIPEMD160($key)
    {
        $result = $this->getFromData($key);
        if($result){
            $result = str_replace('Hashed Data: ', '', $result);
        }
        return $result;
    }

    protected function getJson()
    {
        return json_encode($this->data);
    }

    private function getFromData($key)
    {
        $result = null;
        if(isset($this->data[$key])){
            $result = $this->data[$key];
        }
        return $result;
    }


}
