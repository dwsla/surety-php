<?php

namespace Dws\Surety;

class SuretyPython extends Surety
{
    public function timestamp($path)
    {
        $data = $this->runPython('timestamp', $path);

        return new Model\Timestamp($data);
    }

    public function verify($path)
    {
        $data = $this->runPython('verify', $path);

        return new Model\Verify($data);
    }

    public function renew($path)
    {
        $data = $this->runPython('renew', $path);

        return new Model\Renew($data);
    }

    public function extend($path)
    {
        $data = $this->runPython('extend', $path);

        return new Model\Extend($data);
    }

    public function show($path)
    {
        $data = $this->runPython('show', $path);

        return new Model\Show($data);
    }

    protected function runPython($command, $path)
    {
        $this->checkFilePath($path);

        $simplePy = __DIR__ . '/python/simple.py';

        exec("/usr/bin/python {$simplePy} {$command} {$path} {$this->getCredentialsString()}", $output, $return);
        if ($return) {
            throw new SuretyException("Error executing command - error code: {$return}");
        }
        // responses have on the last element a success or a failed.
        $response = end($output);
        if(strpos($response, 'failed') !== false){
            throw new SuretyException("Error executing command - error code: {$response}");
        }
        return $output;
    }

    protected function getCredentialsString()
    {
        return "{$this->baseUri} {$this->user} {$this->pass}";
    }
}
