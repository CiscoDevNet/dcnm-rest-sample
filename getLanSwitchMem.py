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

def  getSwitchMem(serverip, switchname, resttoken):
  ssl._create_default_https_context = ssl._create_unverified_context
 
  conn = http.client.HTTPSConnection(serverip)

  headers = {
    'dcnm-token': resttoken,
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }


  conn.request("GET", "/fm/fmrest/statistics/memoryStatES?interval=Day&navId=-1", headers=headers)

  res = conn.getresponse()
  data = res.read()
  jsonstr=data.decode("utf-8")
  decoded = json.loads(jsonstr)
  
  for x in decoded :
      if ( x['entityName'] == switchname ) :
        print('switchname:'+ switchname + ' avg mem:' + x['avgTxStr'] + ' min mem:' +x['minTxStr']+ ' max mem:' +x['maxTxStr'])

        getCPUDataURL='/fm/fmrest/statistics/pmChartData?rrdFile='+x['rrdFile']+'&pmType=15&fid='+str(x['fid'])+'&interval=1&navId=-1'
        conn.request("GET", getCPUDataURL, headers=headers)
        cpures=conn.getresponse()
        cpudata=cpures.read()
        print('Details:')
        print(cpudata.decode("utf-8"))
  return


# DCNM username, password, DCNM server ip address
restToken=getRestToken("admin", "Dcnm_123", "172.22.31.146")
print(restToken)

# DCNM server ip, device name, resetTotken
getSwitchMem("172.22.31.146", "leaf-91",restToken)


