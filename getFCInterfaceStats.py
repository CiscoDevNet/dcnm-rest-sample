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
  print(data)
  longstr=data.decode("utf-8")
  strArr=longstr.split("\"")
  return strArr[3]

def  getSwitchId(serverip, switchip, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }


  conn.request("GET", "/fm/fmrest/inventory/switches/?name=foo1&navId=-1", headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")
  decoded = json.loads(jsonstr)
  
  for x in decoded :
      if ( x['ipAddress'] == switchip ) :
        print(x['switchDbID'])
        return x['switchDbID']
  return -1

def  getSwitchIntfId(serverip, switchid, interface, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }


  conn.request("GET", "/fm/fmrest/inventory/getInterfacesBySwitch/?switchDbID="+str(switchid)+"&network=SAN", headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")
  decoded = json.loads(jsonstr)
  
  for x in decoded :
      if ( x['ifName'] == interface ) :
        return x['endPortId']
  return -1

def  getInterfaceStats(serverip, interface, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }


  conn.request("GET", "/fm/fmrest/statistics/pmInterfaceChartData?interfaceDbId="+str(interface) + "&fid=10&interval=1&navId=-1", headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")

  decoded = json.loads(jsonstr)
  items=decoded['chartDO']
  print("rx")
  print(items['items'][0]) 
  print("tx")
  print(items['items'][1]) 
  print("millisec")
  print(items['xLabels']) 
  return 


#serverip
server="172.10.10.10"
# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "xxxxxxxx", server)
print(restToken)

# DCNM server ip, switch ip, resetTotken
switchid=getSwitchId(server, "172.25.174.139",restToken)
print(switchid)

intfid= getSwitchIntfId(server, switchid, "fc1/16", restToken)
print(intfid)

getInterfaceStats(server,intfid, restToken)



