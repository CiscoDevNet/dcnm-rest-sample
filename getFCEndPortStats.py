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
  print(longstr)
  strArr=longstr.split("\"")
  return strArr[3]

def  getRrdID(serverip, switchid, interface, resttoken):
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
  
  swIfName=str(switchid)+ " " + str(interface);
  for x in decoded :
      if ( x['swIfName'] == swIfName) :
        return x['rrdFile']
  return -1

def  getFabricId(serverip, switchname, resttoken):
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
      if ( x['logicalName'] == switchname ) :
        #print(x['fid'])
        return x['fid']
  return -1

def  getInterfaceStats(serverip, fid, rrdid, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }


  conn.request("GET", "/fm/fmrest/statistics/pmChartData?rrdFile="+rrdid+"&fid="+str(fid)+ "&pmType=3&interval=1", 
    headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")
  items = json.loads(jsonstr)
  #print(items)
  print("rx")
  print(items['items'][0]) 
  print("tx")
  print(items['items'][1]) 
  print("millisec")
  print(items['xLabels']) 
  return 


#serverip
server="10.10.10.10"
# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "xxxxxxx", server)
print(restToken)

fid=getFabricId(server, "minishan", restToken)

# DCNM server ip, switch ip, resetTotken
rrdID=getRrdID(server, "minishan", "fc1/2", restToken)
print(rrdID)

#serverip fabric-id interface-id restToken
getInterfaceStats(server,fid, rrdID, restToken)



