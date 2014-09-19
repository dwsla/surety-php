# simple.py - test and sample code for the Surety AbsoluteProof
# service REST SDK
#
# Usage:
# 
# python simple.py <command> <path> <baseUri> <account> <password>
#
# Where command can be timestamp, verify, renew, extend, renew
# or show; and path is the path to the file to be operated on.
#
# Copyright (c) 2012 Surety, LLC.
# 
# The following Sample Code is provided for your reference
# purposes only and may be used by you solely in connection 
# with your use of the Surety AbsoluteProof (TM) software
# product that you have licensed from Surety LLC.("Surety") and
# in accordance with, and subject to, the terms of the SDK
# License Agreement that accompanies this Sample Code.
# 
# Your rights to use and distribute the Sample Code are as
# described in the SDK License Agreement and shall remain in
# effect so long as you have a valid license for the 
# AbsoluteProof(tm) software, provided that (i) a copyright 
# notice in the in the form of "Copyright (c)1998-2006 Surety
# LLC. All Rights Reserved" appears in all copies, and (ii) both 
# the copyright notice and this permission notice appear in any
# supporting documentation.
# 
# This software is protected by copyright law and international
# treaties. Unauthorized reproduction or distribution of this
# software, or any portion of it, may result in severe civil and
# criminal penalties, and will be prosecuted to the maximum
# extent possible under the law.

from ap import *
import sys
import os
import base64


# Implementation Notes:
#
# - Tokens are handled internally as base64 encoded strings, but saved in
#   binary format for compatibility with AP Desktop and AP Viewer.
#
# - This sample assumes that tokens are named by placing an "snr" extension
#   on the corresponding data file name. For example, the token for file.ext 
#   would be file.ext.snr.
#
# - The classes in ap.py support batching, but the use of batching is not 
#   included in this sample to keep things simple.
#
# - The Debug flag can be set on the service using the setDebug() method. 
#   Setting debug to True causes the URL, request XML, response headers, 
#   and response XML to be written to standard output.



#
# Read in the token corresponding to the specified file. The service
# is required because we use the service to decode the token.  A TSAToken 
# object is returned.
#
def readToken(path, service):
  # build token path
  snrpath = path + ".snr"

  # read in binary token and encode to base64
  binary = open(snrpath, 'rb').read()
  token = base64.b64encode(binary)

  # decode the token using the service
  response = service.process(DecodeRequest([token]))

  # get the token object from the response and return it to the caller
  result = response.getTSAResults()[0]
  if result.getSuccess() == 'true':
    return result.getToken()
  else:
    print snrpath + ": decode failed, error code: " + result.getStatus() 
    return Nonereturn 


#
# Write out the TSAToken object for the specified file. 
#
def writeToken(path, token):
    snrfile = path + ".snr"
    f = open(snrfile, 'wb')
    f.write(base64.b64decode(token.getASN1Token()))
    f.close()


#
# Print out the contents of the token for the specified file. See readToken().
#
def printToken(path, service):
  print readToken(path, service)


#
# Timestamp the specified file.
#
def timestamp(path, service):
  
  # calculate imprint
  ci = CompoundImprint.generate(path, ['sha-256', 'ripemd160'])

  # request timestamp
  response = service.process(TimestampRequest([ci]))

  # process response
  result = response.getTSAResults()[0]
  if result.getSuccess() == 'true':
    writeToken(path, result.getToken()) 
    print result.getToken()
    print "timestamp succeeded"
  else:
    print "timestamp failed, error code: " + result.getStatus() 


#
# Verify the specified file.
#
def verify(path, service):
  # read the token
  token = readToken(path, service)

  # verify file hash
  imprint1 = CompoundImprint.generate(path, ['sha-256', 'ripemd160'])
  imprint2 = token.getCompoundImprint()
  if not imprint1.equals(imprint2):
    print path + ": file has been modified"
    return

  # validate token
  response = service.process(VerifyRequest([token]))

  # process response
  result = response.getTSAResults()[0]
  if result.getSuccess() == 'true':
    print result.getToken()
    print "verify succeeded"
  else:
    print "verify failed, error code: " + result.getStatus() 


#
# Extend the token for the specified file.
#
def extend(path, service):
  # read the token
  token = readToken(path, service)
  # extend token
  response = service.process(ExtendRequest([token]))

  # process response
  result = response.getTSAResults()[0]
  if result.getSuccess() == 'true':
    writeToken(path, result.getToken()) 
    print result.getToken()
    print "extend succeeded"
  else:
    print result
    print "extend failed, error code: " + result.getStatus() 


#
# Renew the token for the specified file.
#
def renew(path, service):
  # calculate imprint
  ci = CompoundImprint.generate(path, ['sha-256', 'ripemd160'])

  # read the token
  token = readToken(path, service)

  # extend token
  response = service.process(RenewRequest([{'compoundImprint': ci, 
    'token' : token}]))

  # process response
  result = response.getTSAResults()[0]
  if result.getSuccess() == 'true':
    writeToken(path, result.getToken()) 
    print "renew succeeded"
  else:
    print "renew failed, error code: " + result.getStatus() 


#
# Function to print a simple usage message
#
def usage():
  # argv[0] = command
  # argv[1] = filePath
  # argv[2] = baseUri
  # argv[3] = account
  # argv[4] = password
  print "Usage:" 
  print "  timestamp <path> <baseUri> <account> <password>"
  print "  verify <path> <baseUri> <account> <password>"
  print "  renew <path> <baseUri> <account> <password>"
  print "  extend <path> <baseUri> <account> <password>"
  print "  show <path> <baseUri> <account> <password>"


#
# Main program for this sample
#
def main(argv):
    if len(argv) < 5:
      usage()
      return
    # argv[0] = command
    # argv[1] = filePath
    # argv[2] = baseUri
    # argv[3] = account
    # argv[4] = password




    # Set up the TSA Service object (include trailing "/" on URI)
    baseURI = argv[2]
    # Uncomment the following line to use the production server
    # baseURI = "https://ws1.surety.com/ap_tx_api_v1.0/"
    account = argv[3]
    password = argv[4]
    service = TSAService(baseURI, account, password)

    # Set this to true to get debugging info
    service.setDebug(False)

    # Handle the requested command
    if argv[0] == 'show':
        printToken(argv[1], service)
    elif argv[0] == 'timestamp':
        timestamp(argv[1], service)
    elif argv[0] == 'verify':
        verify(argv[1], service)
    elif argv[0] == 'extend':
        extend(argv[1], service)
    elif argv[0] == 'renew':
        renew(argv[1], service)
    else:
        print "Unknown command: " + argv[0]
        usage()


if __name__ == "__main__":
     main(sys.argv[1:])
