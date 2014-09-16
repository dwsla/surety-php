<?php

namespace StartupDevs\Surety;

use StartupDevs\Surety\SuretyInterface;
use StartupDevs\Surety\SuretyException;
use DOMDocument;

class Surety implements SuretyInterface
{
    const XML_NS = "http://schema.surety.com/restapi/v1.0";

    protected $baseUri;
    protected $user;
    protected $pass;

    private $allowedHashs = array(
        'SHA-1', //	No longer secure, should not be used
        'MD5', // No longer secure, should not be used
        'SHA-256', // Current preferred algorithm
        'SHA-384',
        'SHA-512',
        'RIPEMD160', // Current preferred algorithm
        'WHIRLPOOL',
    );

    public function __construct($baseUri, $user, $pass)
    {
        $this->baseUri = $baseUri;
        $this->user = $user;
        $this->pass = $pass;
    }

    public function timestamp($path)
    {
        // @todo: Make php work properly
        trigger_error("Please use SuretyPython timestamp method", E_USER_NOTICE);
        $operation = 'timestamp';

        $this->checkFilePath($path);
        $file = $this->getFile($path);

        $hashes = array(
            'SHA-256' => base64_encode(hash_file('sha256', $file)),
            'RIPEMD160' => base64_encode(hash_file('ripemd160', $file)),
        );
        $xml = $this->createTimestampXML($hashes);

        $response = $this->makeRequest($operation, $xml->saveXML());
        $response = $this->processResponse($response);

        return $response;
    }


    private function createTimestampXML(array $hashes)
    {
        // create the xml
        $xml = new DOMDocument('1.0', 'UTF-8');
        $xml->preserveWhiteSpace = false;
        $xml->formatOutput = true;

        // create the node a:timestamp-request
        $elemTimestampRequest = $xml->createElement("a:timestamp-request");
        $elemTimestampRequest->setAttribute('xmlns:a', self::XML_NS);

        // create the nodea:timestamp-request-element
        $elemTimestampRequestElement = $xml->createElement('a:timestamp-request-element');

        // create the node a:compound-imprint
        $elemCompountImprint = $xml->createElement('a:compound-imprint');

        foreach($hashes as $algorithm => $hash){

            if(!in_array($algorithm, $this->allowedHashs)){
                continue;
            }

            // create the node a:imprint
            $elemImprint = $xml->createElement('a:imprint');
            // create the node a:hash-algorithm
            $elemHashAlgorithm = $xml->createElement('a:hash-algorithm', $algorithm);
            // create the node a:hashed-data
            $elemHashedData = $xml->createElement('a:hashed-data', $hash);

            $elemImprint->appendChild($elemHashAlgorithm);
            $elemImprint->appendChild($elemHashedData);
            $elemCompountImprint->appendChild($elemImprint);
        }

        $elemTimestampRequestElement->appendChild($elemCompountImprint);
        $elemTimestampRequest->appendChild($elemTimestampRequestElement);

        $xml->appendChild($elemTimestampRequest);

        return $xml;
    }

    protected function makeRequest($operation, $xml)
    {
        $url =  rtrim($this->baseUri, '/') . '/' . ltrim($operation, '/');
        $username = $this->user;
        $password = $this->pass;

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt($ch, CURLOPT_USERPWD, "$username:$password");
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $xml);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
           'Content-type: application/xml',
           'Content-length: ' . strlen($xml)
        ));

        $output = curl_exec($ch);

        if($output === false){
            $error = curl_error($ch);
            $errorNo = curl_errno($ch);
            throw new SuretyException($error, $errorNo);
        }
        curl_close($ch);
        return $output;
    }

    protected function processResponse($response)
    {
        $xml = simplexml_load_string($response);

        $status = current($xml->children('a', true)->httpstatus);
        $message = current($xml->children('a', true)->message);
        $description = current($xml->children('a', true)->description);

        // If a response is returned with an error status code (400-499 or 500-599), the server,
        // the response body will usually contain an error document, but in some cases the
        // response may contain a different error document (such as an HTML document.)
        // An application should not rely on the exact contents of an error document,
        // only the status code; the error document contents should only be used for debugging.
        if($status >= '400' && $status <= '599'){
            $error = sprintf('status: %s - %s', $status, $message);
            throw new SuretyException($error);
        }

        print_r($xml);
        die(__FILE__.__LINE__);
    }

    protected function checkFilePath($path)
    {
        if(!file_exists($path) || !is_file($path) || is_readable($path)){
            // for security purposes don't display "the path" just the variable $path
            if(!file_exists($path)){
                throw new SuretyException('$path file doesn\'t exist.');
            }
            if(!is_file($path)){
                throw new SuretyException('$path file is not a file.');
            }
            if(!is_readable($path)){
                throw new SuretyException('$path file is not a readable.');
            }
        }
        return true;
    }

    protected function getFile($path)
    {
        $filename = $path;
        $handle = fopen($filename, "r");
        $contents = fread($handle, filesize($filename));
        fclose($handle);

        return $contents;
    }

}
