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


def  getFabricKeyByName(serverip, fabricname, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }



  conn.request("GET",  "/fm/fmrest/san/getFabricWithSnmpCredentail_fromDB/?navId=-1", headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")
  decoded = json.loads(jsonstr)
  
  for x in decoded :
    if  ( x['fabricName'] == fabricname ) :
    	return (x['fabrickey'])
  return

def  deleteSanFabric(serverip, fabrickey, fabricName, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }

  postpayload = 'fids='+fabrickey+'&fnames=' + fabricName+'&fmserver=-'


  print(postpayload)
  conn.request("POST", "/fm/fmrest/san/deleteFabricsWithServer", postpayload, headers)
  print(conn.getresponse().read().decode("utf-8"))
  return

# DCNM username, password, DCNM server ip address
serverIp="10.157.34.133"

restToken=getRestToken("admin", "nbv_12345", serverIp)
print(restToken)

print("***********************getFabricKeyByName*********************************")
fabricName="Fabric_v-83"
fabricKey=getFabricKeyByName(serverIp, fabricName, restToken)
print(fabricKey)

deleteSanFabric(serverIp, fabricKey,fabricName, restToken)
