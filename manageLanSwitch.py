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


def  changeSwitchManagement(serverip, switchip, state, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }


  conn.request("GET", "/fm/fmrest/san/getEthSwitchAllWithTaskInfo/?navId=-1", headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")
  decoded = json.loads(jsonstr)
  
  for x in decoded :
      if ( x['seedSwIP'] == switchip ) :
        print(x['csSeedDbId']+":"+x['lanId'] +":"+x['groupDbId'])
        postpayload = 'lanKeys='+x['lanId']+'&newName=&seedIps='+switchip+'&cdpSeedKeys='+x['csSeedDbId']+'&cdpTaskTypes=LAN-IpList&cdpSeedDbIds='+x['csSeedDbId']+'&manageStatus=' +state+'&maxHops=undefined&groupDbIds=2&serverIpaddress='+serverip
        print(postpayload)
        conn.request("POST", "/fm/fmrest/san/setCdpSeed", postpayload, headers)
        print(conn.getresponse().read().decode("utf-8"))
  return


# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "nbv_12345", "172.22.241.185")
print(restToken)

# DCNM server ip, switch ip, management state( toggle between managed and unmanaged )
changeSwitchManagement("172.22.241.185", "18.1.24.201", "managed", restToken)


