import http.client
import ssl
import base64
import string
import json

__author__ = "Louis Jia"
__copyright__ = "Copyright (C) 2018 Cisco System"

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
  longstr=data.decode("utf-8")
  strArr=longstr.split("\"")
  return strArr[3]


def  getAllInterfaceStats(serverip, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }


  conn.request("GET", "/fm/fmrest/statistics/endportStat?interval=Day&endDeviceType=All&navId=-1", headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")
  decoded = json.loads(jsonstr)
  
  for x in decoded :
      print("  fabric"+":"+ x['fabric'] +":"+"entity"+":"+ x['entityName'] +":"+"swIfName"+":"+ x['swIfName'] +":")  
      print("     maxRxStr"+":"+ x['maxRxStr'] +":"+"maxTxStr"+":"+ x['maxTxStr'] +":"+"speedStr"+":"+ x['speedStr'] +":")
      print("     avgRxStr"+":"+ x['avgRxStr'] +":"+"avgTxStr"+":"+ x['avgTxStr'] +":"+"errorStr"+":"+ x['errorStr'] +":")

  return 


#serverip
server="10.157.34.138"
# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "xxxxxxxxxx", server)
print(restToken)



#serverip fabric-id interface-id restToken
getAllInterfaceStats(server, restToken)



