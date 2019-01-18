import http.client
import ssl
import base64
import string
import json

__author__ = "Louis Jia"
__copyright__ = "Copyright (C) 2018 Cisco System"

#sample code to use REST API /fm/fmrest/storageorchestration/createZones 
#
#
# createZones REST API does the following:
# validates init and target pwwn are in same fabric and same vsan
# gets enforced zone set, otherwise creates new zone set named CONNECT-ZONE-SET
# zone names are prefixed with “CONNECT-“ followed by initiator WWN (ie: CONNECT-20:00:e8:65:49:d6:ef:cd) 
# where zone contains single initiator & multiple targets
# run activate zoneset, commit and "copy r s" CLI

def getRestToken(username, password, serverip):
  ssl._create_default_https_context = ssl._create_unverified_context

  ##replace server ip address here
  conn = http.client.HTTPSConnection(serverip)

  payload = "{\"expirationTime\" : 100000000000}\n"

  ## replace user name and password here
  authenStr="%s:%s" % (username, password)

  base64string = base64.encodebytes(bytes(authenStr, 'utf-8'))
  tmpstr= "Basic %s" % base64string
  authorizationStr = tmpstr.replace("b\'","").replace("\\n\'","");
  print(authorizationStr);

  headers = {
      'content-type': "application/json",
      'authorization': authorizationStr,
      'cache-control': "no-cache"
      }

  conn.request("POST", "/rest/logon", payload, headers)

  res = conn.getresponse()
  data = res.read()
  longstr=data.decode("utf-8")
  strArr=longstr.split("\"")
  return strArr[3]

def zone(initWwn, targetWwn,  serverip, restToken):
  ssl._create_default_https_context = ssl._create_unverified_context
  headers = {
    'dcnm-token': restToken,
    'content-type': "application/json"
    }

  ##replace server ip address here
  conn = http.client.HTTPSConnection(serverip)

  payload = "{  \"zones\": [ {   \"initiatorWwn\": \""+initWwn+"\"  , \"targetWwns\": [   \""+targetWwn +"\" ]  }   ] } "
  print(payload)

  conn.request("POST", "/fm/fmrest/storageorchestration/createZones", payload, headers)

  res = conn.getresponse()
  data = res.read()
  longstr=data.decode("utf-8")
  print(longstr)
  return longstr


#serverip
server="10.10.10.10"
# DCNM username, password, DCNM server ip address
restToken=getRestToken("xxxxxx", "xxxxxxxxx", server)
print(restToken)


#initiator wwn, target wwn, restToken
zone("21:01:00:e0:8b:39:ea:58",  "21:00:00:e0:8b:19:af:58",server,restToken)



