import http.client
import ssl
import base64
import string
import json

__author__ = "Louis Jia"
__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates"

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

  postpayload ='seedIp='+switchip + '&isFWSM=false&isV3=true&username='+device_username + '&password='+device_password+'&v3protocol=0&community=admin&maxHop=noop&enablePwd=&groupDbId=2&isDeepDiscovery=false&serverIpaddress='+ serverip + '&isSingleDeviceTask=true'

  print(postpayload)
  conn.request("POST", "/fm/fmrest/san/discoverLan", postpayload, headers)
  print(conn.getresponse().read().decode("utf-8"))
  return


# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "nbv12345", "172.28.164.160")
print(restToken)

# DCNM server ip, switch ip, device user name, device password, resetTotken
discoverLanSwitch("172.28.164.160", "172.22.31.106", "admin","cisco123",restToken)


