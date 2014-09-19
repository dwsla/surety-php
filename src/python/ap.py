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

import urllib2
import base64
import hashlib
from functools import partial
from xml.dom.minidom import *

NS="http://schema.surety.com/restapi/v1.0"


#
# This is an XML utility class used in the classes below
#
class XmlWriter:
 
  def __init__(self):
    self.doc = Document()
 
  def createNode(self, nodeName, parentNode = '', withAttribs = {}, text = ''):
    node = self.doc.createElement(nodeName)
    if parentNode == '':   # create a parent node
      createdNode = self.doc.appendChild(node)
    else:                  # create a child node
      createdNode = parentNode.appendChild(node)
 
    if withAttribs != {}:
      for key, value in withAttribs.items():
        self.setAttribute(createdNode, key, value)

    if text != '':  
      txt = self.doc.createTextNode(text)
      createdNode.appendChild(txt)
 
    return createdNode

  def addNode(self, parentNode, node):
    parentNode.appendChild(node)

  def createTextNode(self, parentNode, text):
    node = self.doc.createTextNode(text)
    createdNode = parentNode.appendChild(node)

    return createdNode
    
  def setAttribute(self, node, key, value):
    node.setAttribute(key, value)
 
  def getXML(self):
    return self.doc.toprettyxml(indent="  ", encoding="UTF-8")

  def printXML(self):
    print self.getXML()


#
# This class handles the processing of requests using the AbsoluteProof
# service.
#
class TSAService(object):
    def __init__(self, baseURI, account, password):
        self.baseURI = baseURI
        self.account = account 
        self.password = password
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, baseURI, account, password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        self.debug = True

    def setDebug(self, debug):
        self.debug = debug

    def process(self, tsaRequest):
        url = self.baseURI + tsaRequest.getOperation()
        request = urllib2.Request(url, tsaRequest.getXML())
        request.add_header("Content-type", "application/xml")
        
        if self.debug:
            print url
            print tsaRequest.getXML()
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            raise HTTPErrorResponse(e)
        xml = response.read()
        if self.debug:
            print response.info().headers
            print xml
        return TSAResponse(xml)


#
# This class is the parent class of all TSA Requests
#
class TSARequest(object):
    def __init__(self):
        self.operation = "undefined"
        self.debug = False

    def getXML(self):
        return ""

    def getOperation(self):
        return self.operation


#
# Class for the APXML timestamp request.
#
class TimestampRequest(TSARequest): 
    def __init__(self, compoundImprints, tags=None):
        super(TimestampRequest, self).__init__()
        self.compoundImprints = compoundImprints
        self.tags = tags
        self.operation = "timestamp"

    def getXML(self):
      doc = XmlWriter()
      timestampRequest = doc.createNode("a:timestamp-request", 
        withAttribs = {"xmlns:a": NS}) 

      for index, ci in enumerate(self.compoundImprints):
        try:
            attribs = {"a:tag": str(self.tags[index])}
        except:
            attribs = {}
        timestampRequestElement = doc.createNode(
          "a:timestamp-request-element", timestampRequest,
          withAttribs = attribs) 
        ci.createNode(doc, timestampRequestElement)

      return doc.getXML()


#
# Class for the APXML decode request. 
#
class DecodeRequest(TSARequest): 
    def __init__(self, tokens, tags=None):
        super(DecodeRequest, self).__init__()
        self.tokens = tokens
        self.tags = tags
        self.operation = "decode"

    def getXML(self):
      doc = XmlWriter()
      decodeRequest = doc.createNode("a:decode-request", 
        withAttribs = {"xmlns:a": NS}) 

      for index, token  in enumerate(self.tokens):
        try:
          attribs = {"a:tag": str(self.tags[index])}
        except:
          attribs = {}
        decodeRequestElement = doc.createNode(
          "a:decode-request-element", decodeRequest,
          withAttribs = attribs)

        doc.createNode("a:asn1-token", decodeRequestElement, 
          text = token)

      return doc.getXML()


#
# Class for the APXML verify request. 
#
class VerifyRequest(TSARequest): 
    def __init__(self, tokens, tags=None):
        super(VerifyRequest, self).__init__()
        self.tokens = tokens
        self.tags = tags
        self.operation = "verify"

    def getXML(self):
      doc = XmlWriter()
      verifyRequest = doc.createNode("a:verify-request", 
        withAttribs = {"xmlns:a": NS}) 

      for index, token in enumerate(self.tokens):
        try:
            attribs = {"a:tag": str(self.tags[index])}
        except:
            attribs = {}
        verifyRequestElement = doc.createNode(
          "a:verify-request-element", verifyRequest,
          withAttribs = attribs)

        doc.addNode(verifyRequestElement, token.getNode())
        return doc.getXML()


#
# Class for the APXML extend request.
#
class ExtendRequest(TSARequest): 
    def __init__(self, tokens, tags=None):
        super(ExtendRequest, self).__init__()
        self.tokens = tokens
        self.tags = tags
        self.operation = "extend"

    def getXML(self):
      doc = XmlWriter()
      extendRequest = doc.createNode("a:extend-request", 
        withAttribs = {"xmlns:a": NS}) 

      for index, token in enumerate(self.tokens):
        try:
            attribs = {"a:tag": str(self.tags[index])}
        except:
            attribs = {}
        extendRequestElement = doc.createNode(
          "a:extend-request-element", extendRequest,
          withAttribs = attribs)

        doc.addNode(extendRequestElement, token.getNode())

      return doc.getXML()


#
# Class for the APXML renew request.
#
#
# Constructed with a list of renewal information, where each item is a
# dictionary containing a 'compoundImprint' and a 'token' object
#
class RenewRequest(TSARequest): 
    def __init__(self, renewalInfos, tags=None):
        super(RenewRequest, self).__init__()
        self.renewalInfos = renewalInfos
        self.tags = tags
        self.operation = "renew"

    def getXML(self):
      doc = XmlWriter()
      renewRequest = doc.createNode("a:renew-request", 
        withAttribs = {"xmlns:a": NS}) 

      for index, renewalInfo in enumerate(self.renewalInfos):
        try:
            attribs = {"a:tag": str(self.tags[index])}
        except:
            attribs = {}
        renewRequestElement = doc.createNode(
          "a:renew-request-element", renewRequest,
          withAttribs = attribs)

        renewalInfo['compoundImprint'].createNode(doc, renewRequestElement)

        doc.addNode(renewRequestElement, renewalInfo['token'].getNode())

      return doc.getXML()

#
# Class for the APXML Error reqponse. 
#
# This is a subclass of Exception so it can be thrown when an error is 
# encountered.
#
class HTTPErrorResponse(Exception):
    def __init__(self, e):
        self.xmlstring = e.read()
        self.code = e.code
        try:
            self.dom = xml.dom.minidom.parseString(self.xmlstring)
        except:
            self.httpstatus = self.code
            self.description = ""
            self.message = self.xmlstring
            return
 
        elements = self.dom.getElementsByTagNameNS(NS, "error");
        for child in elements[0].childNodes:
            if child.localName=='httpstatus':
                self.httpstatus = child.childNodes[0].nodeValue
            elif child.localName=='message':
                self.message = child.childNodes[0].nodeValue
            elif child.localName=='description':
                self.description = child.childNodes[0].nodeValue

    def __str__(self):
        print self.xmlstring
        result = "[httpstatus: " + self.httpstatus + "; "
        result = result + "message: " + self.message + "; "
        result = result + "description: " + self.description + "]"
        return result


#
# Class for the APXML TSA Response message.
#
class TSAResponse(object):
    def __init__(self, xmlstring):
        self.dom = xml.dom.minidom.parseString(xmlstring)
        elements = self.dom.getElementsByTagNameNS(NS, "timestamp-authority-response-element");
        self.results = []
        for result in elements:
            self.results.append(TSAResult(result))

    def getTSAResults(self):
        return self.results

    def __str__(self):
        out = ""
        for index, result in enumerate(self.results):
            out = out + "TSA Result " + str(index) + "\n" + str(result)

        return out


#
# Class for the TSA Result element of the APXML TSA Response message.
#
class TSAResult(object):
    def __init__(self, node):
        self.token = None
        self.tag = node.getAttributeNS(NS, 'tag')
        for child in node.childNodes:
            if child.localName=='status':
                self.status = child.childNodes[0].nodeValue
            elif child.localName=='success':
                self.success = child.childNodes[0].nodeValue
            elif child.localName=='timestamp-token':
                self.token = TSAToken(child)

    def getTag(self):
        return self.tag

    def getStatus(self):
        return self.status

    def getSuccess(self):
        return self.success

    def getToken(self):
        return self.token

    def __str__(self):
        result = "Tag: " + self.getTag() + "\n"
        result = result + "Timestamp Token: \n" + str(self.getToken())
        result = result + "Success: " + self.getSuccess() + "\n"
        result = result + "Status: " + self.getStatus() + "\n"
        return result


#
# Class for the TSA Token element that is included multiple APXML 
# request and response messages.
#
class TSAToken(object):
    def __init__(self, node):
        self.node = node
        self.ASN1Token = ""
        self.timestamp = ""
        self.serialNumber = ""
        self.TSAName = ""
        self.coordinationZone = ""
        self.compoundImprint = None
        self.previousToken = None
        self.publicationInfo = None
        for child in node.childNodes:
            if child.localName=='asn1-token':
                self.ASN1Token = child.childNodes[0].nodeValue
            elif child.localName=='timestamp':
                self.timestamp = child.childNodes[0].nodeValue
            elif child.localName=='serial-number':
                self.serialNumber = child.childNodes[0].nodeValue
            elif child.localName=='timestamp-authority-name':
                self.TSAName = child.childNodes[0].nodeValue
            elif child.localName=='coordination-zone':
                self.coordinationZone = child.childNodes[0].nodeValue
            elif child.localName=='compound-imprint':
                self.compoundImprint = CompoundImprint.fromXML(child)
            elif child.localName=='previous-token':
                self.previousToken = TSAToken(child)
            elif child.localName=='publication-info':
                self.publicationInfo = PublicationInfo(child)

    def getASN1Token(self):
        return self.ASN1Token

    def getTimestamp(self):
        return self.timestamp

    def getSerialNumber(self):
        return self.serialNumber

    def getTSAName(self):
        return self.TSAName

    def getCoordinationZone(self):
        return self.coordinationZone

    def getCompoundImprint(self):
        return self.compoundImprint

    def getNode(self):
        return self.node

    def __str__(self):
        result = "ASN1 Token: " + self.ASN1Token + "\n"
        result = result + "Timestamp: " + self.timestamp + "\n"
        result = result + "Serial Number: " + self.serialNumber + "\n"
        result = result + "TSA Name: " + self.TSAName + "\n"
        result = result + "Coordination Zone: " + self.coordinationZone + "\n"
        result = result + "Compound Imprint: \n" + str(self.compoundImprint)
        if self.publicationInfo is not None:
            result = result + "Publication Information: \n" + str(self.publicationInfo) + "\n"
        if self.previousToken is not None:
            result = result + "[\nPrevious Token: \n" + str(self.previousToken) + "]\n"

        return result
  

class PublicationInfo(object):
    def __init__(self, node):
        self.publicationId = ""
        self.publicationDate = ""
        self.publishedValue = ""
        for child in node.childNodes:
            if child.localName=='publication':
                self.publicationId = child.getAttribute('id')
                self.publicationDate = child.getAttribute('date')
            elif child.localName=='published-value':
                self.publishedValue = child.childNodes[0].nodeValue

    def getPublicationId(self):
        return self.publicationId

    def getPublicationDate(self):
        return self.publicationDate

    def getPublicationValue(self):
        return self.publicationValue

    def __str__(self):
        result = "Publication Id: " + self.publicationId + "\n"
        result = result + "Publication Date: " + self.publicationDate + "\n"
        result = result + "Published Value: " + self.publishedValue 
        return result


class CompoundImprint(object):
    def __init__(self, imprints):
        self.imprints = imprints

    @classmethod
    def fromXML(cls, node):
        imprints = []
        for child in node.childNodes:
            if child.localName=='imprint':
                imprints.append(Imprint.fromXML(child))
        return cls(imprints)

    @classmethod
    def generate(cls, filename, algs):
        imprints = []
        for alg in algs:
            imprints.append(Imprint.generate(filename, alg))
        return cls(imprints)

    def getImprints(self):
        return self.imprints

    def equals(self, other):
        match = True
        for index, imprint in enumerate(self.imprints):
            match = match and imprint.equals(other.getImprints()[index])
        return match 

    def createNode(self, doc, parent):
        compoundImprint = doc.createNode("a:compound-imprint", parent)
        for item in self.imprints:
          imprint = doc.createNode("a:imprint", compoundImprint)
          doc.createNode("a:hash-algorithm", imprint, text = item.getHashAlgorithm())
          doc.createNode('a:hashed-data', imprint, text = item.getHashedData())
           
 
    def __str__(self):
        result = ""
        for index, imprint in enumerate(self.imprints):
            result = result + "Imprint " + str(index) + "\n" + str(imprint)

        return result


class Imprint(object):
    def __init__(self, hashAlgorithm, hashedData):
        self.hashAlgorithm = hashAlgorithm
        self.hashedData = hashedData
   
    @classmethod
    def fromXML(cls, node):
        hashAlgorithm = ""
        hashedData = ""
        for child in node.childNodes:
            if child.localName=='hash-algorithm':
                hashAlgorithm = child.childNodes[0].nodeValue
            elif child.localName=='hashed-data':
                hashedData = child.childNodes[0].nodeValue
        return cls(hashAlgorithm, hashedData)

    @classmethod
    def generate(cls, filename, alg):
        fcn = HashFunction(alg)
        hashAlgorithm = fcn.getAlgName()
        hashedData = fcn.computeHash(filename)
        return cls(hashAlgorithm, hashedData)

    def getHashAlgorithm(self):
        return self.hashAlgorithm

    def getHashedData(self):
        return self.hashedData

    def equals(self, other):
        return self.hashedData == other.hashedData and \
         HashFunction.compareNames(self.hashAlgorithm, other.hashAlgorithm)

    def __str__(self):
        result =  "Hash Algorithm: " + self.getHashAlgorithm() + "\n"
        result = result + "Hashed Data: " + self.getHashedData() + "\n"

        return result

#
# Hash Function class supports the creation of specific hash function 
# objects by supplying the name of that desired hash function. Supports both
# standard naming of hash functions (which is used by AbsoluteProof) and 
# names used by the Python hashlib library.
#
class HashFunction(object):
    def __init__(self, algName):
        self.stdAlgMap = {
            "SHA-1" : "SHA-1",
            "SHA1" : "SHA-1",
            "MD5" : "MD5",
            "SHA-256" : "SHA-256", 
            "SHA256" : "SHA-256", 
            "SHA-384" : "SHA-384",
            "SHA384" : "SHA-384",
            "SHA-512" : "SHA512",
            "SHA512" : "SHA512",
            "RIPEMD160" : "RIPEMD160" }
        self.hashlibAlgMap = {
            "SHA-1" : "SHA1",
            "SHA1" : "SHA1",
            "MD5" : "MD5",
            "SHA-256" : "SHA256", 
            "SHA256" : "SHA256", 
            "SHA-384" : "SHA384",
            "SHA384" : "SHA384",
            "SHA-512" : "SHA512",
            "SHA512" : "SHA512",
            "RIPEMD160" : "RIPEMD160" }
        self.stdAlgName = self.stdAlgMap[algName.upper()]
        self.hashlibAlgName = self.hashlibAlgMap[algName.upper()]


    @staticmethod
    def compareNames(algName1, algName2):
        name1 = HashFunction(algName1).getAlgName()
        name2 = HashFunction(algName2).getAlgName()
        return name1 == name2

    def getAlgName(self):
        return self.stdAlgName
 
    def computeHash(self, filename):
        with open(filename, mode='rb') as f:
            d = hashlib.new(self.hashlibAlgName)
            for buf in iter(partial(f.read, 128), b''):
                d.update(buf)
        return base64.b64encode(d.digest())
