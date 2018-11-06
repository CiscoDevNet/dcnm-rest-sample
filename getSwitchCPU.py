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

def  getSwitchCPU(serverip, switchname, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }


  conn.request("GET", "/fm/fmrest/statistics/cpuStatES?interval=Day&navId=-1", headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")
  decoded = json.loads(jsonstr)
  
  for x in decoded :
      if ( x['entityName'] == switchname ) :
        print(x['rrdFile'])
        print(x['fid'])
        getCPUDataURL='/fm/fmrest/statistics/pmChartData?rrdFile='+x['rrdFile']+'&pmType=5&fid='+str(x['fid'])+'&interval=1&navId=-1'
        conn.request("GET", getCPUDataURL, headers=headers)
        cpures=conn.getresponse()
        cpudata=cpures.read()
        print(cpudata.decode("utf-8"))
  return


# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "xxxxx", "10.157.35.59")
print(restToken)

# DCNM server ip, switch name, resetTotken
getSwitchCPU("10.157.35.59", "sw172-22-47-20",restToken)


