import http.client
import ssl
import base64
import string
import json

__author__ = "Louis Jia"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates"

def getRestToken(username, password, serverip):
  ssl._create_default_https_context = ssl._create_unverified_context

  ##replace server ip address here
  conn = http.client.HTTPSConnection(serverip)

  payload = "{\"expirationTime\" : 10000000000}\n"

  ## replace user name and password here
  authenStr="%s:%s" % (username, password)

  base64string = base64.encodestring(bytes(authenStr, 'utf-8'))
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
  print(data)
  longstr=data.decode("utf-8")
  strArr=longstr.split("\"")
  return strArr[3]


def  discoverLanSwitch(serverip, switchip, device_username, device_password, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }

# v3protocol mapping
# 0 - MD5
# 1 - SHA
# 2 - MD5_DES
# 3 - MD5_AES
# 4 - SHA_DES
# 5 - SHA_AES

  postpayload = 'seed='+switchip+ '&isV3=true&username='+device_username + '&password='+device_password
  postpayload = postpayload+'&v3protocol=0&community=admin&globalEnableNpvDiscovery=true&fmserver='+serverip

  print(postpayload)
  conn.request("POST", "/fm/fmrest/san/discoverFabricWithServer", postpayload, headers)
  print(conn.getresponse().read().decode("utf-8"))
  return


# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "xxxxxxxxxx", "10.10.10.10")
print(restToken)

# DCNM server ip, switch ip, device snmp user name, device snmp password, resetTotken
# This sample uses MD5
discoverLanSwitch("10.10.10.102", "10.10.10.10.", "admin","yyyyyyyyyyy",restToken)


