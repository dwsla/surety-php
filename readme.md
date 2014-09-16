# Surety PHP

The Surety PHP is a library to interact with the Surety API using php.
This library is using Python to make the calls on the API. (python is required to run this library)

## Usage

```php
<?php

require_once 'vendor/autoload.php';

use Dws\Surety\SuretyPython as Surety;
use Dws\Surety\SuretyException as SuretyException;

try{

	$result = null;

	$accounts = array(
		'test' => array(
			'baseURI' => "x",
			'account' => "x",
			'password' => "x",
		),
		'prod' => array(
			'baseURI' => "y",
			'account' => "y",
			'password' => "y",
		)
	);

	extract($accounts['test']);
	
	$surety = new Surety($baseURI, $account, $password);

	// call the method you need.

}catch(SuretyException $e){
	die($e->getMessage());
}
```

## Available Methods

### Timestamp

```php
<?php
	
	$file = '/path/to/file.extension';

	$surety = new Surety($baseURI, $account, $password);

	$timestamp = $surety->timestamp($file);

	// it will return a Dws\Surety\Model\Timestamp 
	// or throw an Dws\Surety\SuretyException

	// the Dws\Surety\Model\Timestamp has the following properties
	echo $timestamp->url; # the url string 
    echo $timestamp->asn1_token; # the asn1_token string 
    echo $timestamp->timestamp; # the timestamp string 
    echo $timestamp->serial_number; # the serial_number string 
    echo $timestamp->tsa_name; # the tsa_name string 
    echo $timestamp->coordination_zone; # the coordination_zone string 
    echo $timestamp->SHA256; # the SHA256 string 
    echo $timestamp->RIPEMD160; # the RIPEMD160 string 
    echo $timestamp->json; # the json string with the full response 

```


### Verify

```php
<?php
	
	$file = '/path/to/file.extension';

	$surety = new Surety($baseURI, $account, $password);

	$verify = $surety->verify($file);

	// it will return a Dws\Surety\Model\Verify 
	// or throw an Dws\Surety\SuretyException

	// the Dws\Surety\Model\Verify has the following properties
	echo $verify->url; # the url string 
    echo $verify->decode_url; # the decode_url string 
    echo $verify->asn1_token; # the asn1_token string 
    echo $verify->timestamp; # the timestamp string 
    echo $verify->serial_number; # the serial_number string 
    echo $verify->tsa_name; # the tsa_name string 
    echo $verify->coordination_zone; # the coordination_zone string 
    echo $verify->SHA256; # the SHA256 string 
    echo $verify->RIPEMD160; # the RIPEMD160 string 
    echo $verify->json; # the json string with the full response 

```
### Renew

```php
<?php
	
	$file = '/path/to/file.extension';

	$surety = new Surety($baseURI, $account, $password);

	$renew = $surety->renew($file);

	// it will return a Dws\Surety\Model\Renew 
	// or throw an Dws\Surety\SuretyException

	// the Dws\Surety\Model\Renew has the following properties
	echo $renew->url; # the url string 
    echo $renew->decode_url; # the decode_url string 
    echo $renew->json; # the json string with the full response 

```
### Extend

```php
<?php
	
	#not implemented yet.

```

### Show

```php
<?php
	
	$file = '/path/to/file.extension';

	$surety = new Surety($baseURI, $account, $password);

	$show = $surety->show($file);

	// it will return a Dws\Surety\Model\Show 
	// or throw an Dws\Surety\SuretyException

	// the Dws\Surety\Model\Show has the following properties
	echo $show->url; # the url string 
    echo $show->asn1_token; # the asn1_token string 
    echo $show->timestamp; # the timestamp string 
    echo $show->serial_number; # the serial_number string 
    echo $show->tsa_name; # the tsa_name string 
    echo $show->coordination_zone; # the coordination_zone string 
    echo $show->SHA256; # the SHA256 string 
    echo $show->RIPEMD160; # the RIPEMD160 string 
    echo $show->json; # the json string with the full response 

    // the Dws\Surety\Model\Show also have the getPreviousToken method
    // each key of the previous token array contains a 
    // Dws\Surety\Model\PreviousToken

    $show->getPreviousToken(); # the array with all previous token

    // you can also get a specifc previous token by passing the "level"
    $level = 0;
    $previousToken = $show->getPreviousToken( $level );

    // the Dws\Surety\Model\PreviousToken has the following properties
	echo $previousToken->asn1_token; # the asn1_token string 
    echo $previousToken->timestamp; # the timestamp string 
    echo $previousToken->serial_number; # the serial_number string 
    echo $previousToken->tsa_name; # the tsa_name string 
    echo $previousToken->coordination_zone; # the coordination_zone string 
    echo $previousToken->SHA256; # the SHA256 string 
    echo $previousToken->RIPEMD160; # the RIPEMD160 string 
```













